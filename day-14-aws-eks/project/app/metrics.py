"""CPU and memory used by this container.

In Kubernetes the numbers come from the container's cgroup, so they match the
resource limits set in k8s/deployment.yaml. Outside a container we fall back to
the process's own usage.
"""

import os
import threading
import time
from pathlib import Path

_lock = threading.Lock()
_last = None          # (monotonic time, cpu seconds) from the previous sample
_last_percent = 0.0


def _read(path):
    return Path(path).read_text().strip()


def _cgroup_v2():
    memory = int(_read("/sys/fs/cgroup/memory.current"))
    raw_limit = _read("/sys/fs/cgroup/memory.max")
    limit = None if raw_limit == "max" else int(raw_limit)

    cpu_seconds = 0.0
    for line in _read("/sys/fs/cgroup/cpu.stat").splitlines():
        if line.startswith("usage_usec"):
            cpu_seconds = int(line.split()[1]) / 1_000_000

    quota = _read("/sys/fs/cgroup/cpu.max").split()
    cores = (os.cpu_count() or 1) if quota[0] == "max" else int(quota[0]) / int(quota[1])
    return memory, limit, cpu_seconds, cores, "cgroup"


def _process():
    rss = 0
    try:
        for line in _read("/proc/self/status").splitlines():
            if line.startswith("VmRSS"):
                rss = int(line.split()[1]) * 1024
    except OSError:
        pass
    times = os.times()
    return rss, None, times.user + times.system, os.cpu_count() or 1, "process"


def _machine_memory():
    try:
        for line in _read("/proc/meminfo").splitlines():
            if line.startswith("MemTotal"):
                return int(line.split()[1]) * 1024
    except OSError:
        pass
    return None


def container_metrics():
    global _last, _last_percent

    try:
        memory, limit, cpu_seconds, cores, source = _cgroup_v2()
    except (OSError, ValueError, IndexError, ZeroDivisionError):
        memory, limit, cpu_seconds, cores, source = _process()

    limit = limit or _machine_memory()
    now = time.monotonic()

    with _lock:
        if _last is not None and now - _last[0] >= 0.5:
            wall = now - _last[0]
            used = max(0.0, cpu_seconds - _last[1])
            _last_percent = min(100.0, used / wall / cores * 100)
            _last = (now, cpu_seconds)
        elif _last is None:
            _last = (now, cpu_seconds)
        percent = _last_percent

    return {
        "source": source,
        "cpu_percent": round(percent, 1),
        "cpu_cores": round(cores, 2),
        "memory_bytes": memory,
        "memory_limit_bytes": limit,
        "memory_percent": round(memory / limit * 100, 1) if limit else None,
    }
