"""Sample data, used when the app runs outside a cluster (for example `docker run` on a laptop).

It has the same shape as the real data from k8s.collect(), and the dashboard
clearly labels it as sample data.
"""

from .k8s import summarize

NODE_A = "ip-10-0-1-45.ec2.internal"
NODE_B = "ip-10-0-2-112.ec2.internal"


def _pod(name, node, ip, age):
    return {
        "name": name,
        "status": "Running",
        "ready": "1/1",
        "restarts": 0,
        "node": node,
        "ip": ip,
        "age_seconds": age,
    }


def collect(me):
    pods = sorted(
        [
            _pod(me["pod"], NODE_A, me["pod_ip"], me["uptime_seconds"]),
            _pod("eks-demo-6d8f7c9b5-r8wmn", NODE_B, "10.0.2.112", 9840),
            _pod("eks-demo-6d8f7c9b5-t4hzc", NODE_A, "10.0.1.67", 9840),
        ],
        key=lambda p: p["name"],
    )

    nodes = [
        {"name": NODE_A, "ready": True, "instance_type": "t3.small", "zone": "us-east-1a"},
        {"name": NODE_B, "ready": True, "instance_type": "t3.small", "zone": "us-east-1b"},
    ]
    topology = [{**n, "pods": [p for p in pods if p["node"] == n["name"]]} for n in nodes]
    deployments = [{"name": "eks-demo", "ready": 3, "desired": 3}]

    events = [
        {"type": "Normal", "reason": "Started", "message": "Started container eks-demo",
         "object": "Pod/eks-demo-6d8f7c9b5-t4hzc", "age_seconds": 120, "count": 1},
        {"type": "Normal", "reason": "Pulled", "message": "Container image already present on machine",
         "object": "Pod/eks-demo-6d8f7c9b5-t4hzc", "age_seconds": 125, "count": 1},
        {"type": "Normal", "reason": "Scheduled", "message": "Successfully assigned eks-demo to a node",
         "object": "Pod/eks-demo-6d8f7c9b5-t4hzc", "age_seconds": 130, "count": 1},
        {"type": "Normal", "reason": "ScalingReplicaSet", "message": "Scaled up replica set eks-demo-6d8f7c9b5 to 3",
         "object": "Deployment/eks-demo", "age_seconds": 135, "count": 1},
        {"type": "Normal", "reason": "EnsuredLoadBalancer", "message": "Ensured load balancer",
         "object": "Service/eks-demo", "age_seconds": 600, "count": 1},
    ]

    return {
        "version": "v1.30 (sample)",
        "region": "us-east-1",
        "nodes": topology,
        "pods": pods,
        "deployments": deployments,
        "events": events,
        "counts": summarize(topology, pods, deployments, 1),
    }
