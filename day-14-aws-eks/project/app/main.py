import logging
import os
import platform
import socket
import time
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from . import demo, k8s, metrics

APP_VERSION = os.getenv("APP_VERSION", "1.1.0")
BASE_DIR = Path(__file__).resolve().parent
STARTED = time.time()

log = logging.getLogger("eks-demo")
app = FastAPI(title="Helm: EKS Control Room", version=APP_VERSION)

requests_served = 0

try:
    LOCAL_IP = socket.gethostbyname(socket.gethostname())
except OSError:
    LOCAL_IP = "127.0.0.1"


@app.middleware("http")
async def count_requests(request: Request, call_next):
    """Count every request except health probes, and never cache API answers."""
    global requests_served
    if request.url.path != "/healthz":
        requests_served += 1
    response = await call_next(request)
    if request.url.path.startswith("/api"):
        response.headers["Cache-Control"] = "no-store"
    return response


def identity():
    """Who is answering? In Kubernetes these values come from the Downward API
    (see the env section of k8s/deployment.yaml)."""
    return {
        "pod": os.getenv("POD_NAME") or socket.gethostname(),
        "namespace": os.getenv("POD_NAMESPACE", "default"),
        "node": os.getenv("NODE_NAME", "local machine"),
        "pod_ip": os.getenv("POD_IP") or LOCAL_IP,
        "uptime_seconds": int(time.time() - STARTED),
        "requests_served": requests_served,
        "version": APP_VERSION,
        "python": platform.python_version(),
    }


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/api/whoami")
def whoami():
    return identity()


@app.get("/api/dashboard")
def dashboard():
    me = identity()
    mode, reason = "cluster", None

    try:
        data = k8s.collect(me["namespace"])
    except k8s.NotInCluster:
        data, mode = demo.collect(me), "demo"
        reason = "This app is not running inside a Kubernetes cluster, so the page shows sample data."
    except Exception as exc:  # RBAC missing, API timeout, and so on
        log.exception("Could not read the cluster API")
        data, mode = demo.collect(me), "demo"
        reason = f"The cluster API could not be read ({type(exc).__name__}), so the page shows sample data."

    return {
        "mode": mode,
        "reason": reason,
        "me": me,
        "cluster": {
            "name": os.getenv("CLUSTER_NAME", "eks-demo"),
            "region": data["region"],
            "version": data["version"],
            "environment": os.getenv("ENVIRONMENT", "Development"),
        },
        "counts": data["counts"],
        "topology": data["nodes"],
        "pods": data["pods"],
        "deployments": data["deployments"],
        "events": data["events"],
        "metrics": metrics.container_metrics(),
        "server_time": datetime.now(timezone.utc).isoformat(),
    }


app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/")
def home():
    return FileResponse(BASE_DIR / "static" / "index.html")
