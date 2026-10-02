"""A tiny, read-only Kubernetes API client that uses only the standard library.

Inside a pod, Kubernetes mounts a service account token and CA certificate.
We use them to ask the API server for nodes, pods, deployments and events.
"""

import json
import os
import ssl
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SA_DIR = Path("/var/run/secrets/kubernetes.io/serviceaccount")
CACHE_SECONDS = 3


class NotInCluster(RuntimeError):
    """Raised when the app is not running inside a Kubernetes pod."""


_cache = {}
_ssl_context = None


def in_cluster():
    return bool(os.getenv("KUBERNETES_SERVICE_HOST")) and (SA_DIR / "token").exists()


def _context():
    global _ssl_context
    if _ssl_context is None:
        _ssl_context = ssl.create_default_context(cafile=str(SA_DIR / "ca.crt"))
    return _ssl_context


def get(path):
    """GET a path from the API server. Results are cached for a few seconds."""
    if not in_cluster():
        raise NotInCluster("not running inside a Kubernetes cluster")

    now = time.monotonic()
    hit = _cache.get(path)
    if hit and now - hit[0] < CACHE_SECONDS:
        return hit[1]

    host = os.environ["KUBERNETES_SERVICE_HOST"]
    port = os.getenv("KUBERNETES_SERVICE_PORT", "443")
    if ":" in host:  # IPv6
        host = f"[{host}]"

    # The token is rotated by Kubernetes, so read it fresh each time.
    token = (SA_DIR / "token").read_text().strip()
    request = urllib.request.Request(
        f"https://{host}:{port}{path}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=4, context=_context()) as response:
        data = json.load(response)

    _cache[path] = (now, data)
    return data


# ---------- Normalisers: turn raw API objects into small, flat dicts ----------

def _age(timestamp):
    if not timestamp:
        return None
    then = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    return max(0, int((datetime.now(timezone.utc) - then).total_seconds()))


def _pod_status(pod):
    if pod["metadata"].get("deletionTimestamp"):
        return "Terminating"
    status = pod.get("status", {})
    statuses = status.get("initContainerStatuses", []) + status.get("containerStatuses", [])
    for container in statuses:
        waiting = container.get("state", {}).get("waiting")
        if waiting and waiting.get("reason"):
            return waiting["reason"]  # e.g. CrashLoopBackOff, ImagePullBackOff
    return status.get("phase", "Unknown")


def _pod(item):
    meta, spec, status = item["metadata"], item.get("spec", {}), item.get("status", {})
    containers = status.get("containerStatuses", [])
    ready = sum(1 for c in containers if c.get("ready"))
    return {
        "name": meta["name"],
        "status": _pod_status(item),
        "ready": f"{ready}/{len(spec.get('containers', []))}",
        "restarts": sum(c.get("restartCount", 0) for c in containers),
        "node": spec.get("nodeName") or "unscheduled",
        "ip": status.get("podIP") or "-",
        "age_seconds": _age(meta.get("creationTimestamp")),
    }


def _node(item):
    labels = item["metadata"].get("labels", {})
    conditions = {c["type"]: c["status"] for c in item.get("status", {}).get("conditions", [])}
    return {
        "name": item["metadata"]["name"],
        "ready": conditions.get("Ready") == "True",
        "instance_type": labels.get("node.kubernetes.io/instance-type", "unknown"),
        "zone": labels.get("topology.kubernetes.io/zone", "unknown"),
    }


def _deployment(item):
    return {
        "name": item["metadata"]["name"],
        "ready": item.get("status", {}).get("readyReplicas") or 0,
        "desired": item.get("spec", {}).get("replicas") or 0,
    }


def _event(item):
    stamp = (
        item.get("lastTimestamp")
        or item.get("eventTime")
        or item["metadata"].get("creationTimestamp")
    )
    target = item.get("involvedObject", {})
    return {
        "type": item.get("type", "Normal"),
        "reason": item.get("reason", ""),
        "message": item.get("message", ""),
        "object": f"{target.get('kind', '')}/{target.get('name', '')}",
        "age_seconds": _age(stamp),
        "count": item.get("count") or 1,
    }


def summarize(topology, pods, deployments, services):
    """Numbers for the summary band at the top of the dashboard."""
    return {
        "nodes": sum(1 for n in topology if not n.get("virtual")),
        "nodes_ready": sum(1 for n in topology if n["ready"] and not n.get("virtual")),
        "pods": len(pods),
        "pods_running": sum(1 for p in pods if p["status"] == "Running"),
        "deployments": len(deployments),
        "replicas_ready": sum(d["ready"] for d in deployments),
        "replicas_desired": sum(d["desired"] for d in deployments),
        "services": services,
    }


def collect(namespace):
    """Read everything the dashboard needs from the cluster."""
    version = get("/version").get("gitVersion", "unknown")
    node_items = get("/api/v1/nodes")["items"]
    pods = sorted(
        (_pod(p) for p in get(f"/api/v1/namespaces/{namespace}/pods")["items"]),
        key=lambda p: p["name"],
    )
    deployments = [
        _deployment(d) for d in get(f"/apis/apps/v1/namespaces/{namespace}/deployments")["items"]
    ]
    services = len(get(f"/api/v1/namespaces/{namespace}/services")["items"])
    events = sorted(
        (_event(e) for e in get(f"/api/v1/namespaces/{namespace}/events")["items"]),
        key=lambda e: e["age_seconds"] if e["age_seconds"] is not None else 10**9,
    )[:25]

    by_node = {}
    for pod in pods:
        by_node.setdefault(pod["node"], []).append(pod)

    topology = [{**_node(n), "pods": by_node.pop(n["metadata"]["name"], [])} for n in node_items]
    for name, group in by_node.items():  # pods on nodes we could not list, or not yet scheduled
        topology.append(
            {"name": name, "ready": False, "virtual": True, "instance_type": "", "zone": "", "pods": group}
        )

    region = os.getenv("AWS_REGION", "unknown")
    if node_items:
        region = node_items[0]["metadata"].get("labels", {}).get("topology.kubernetes.io/region", region)

    return {
        "version": version,
        "region": region,
        "nodes": topology,
        "pods": pods,
        "deployments": deployments,
        "events": events,
        "counts": summarize(topology, pods, deployments, services),
    }
