import psutil
import json
import os
from datetime import datetime


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory.percent


def get_disk_usage():
    disk = psutil.disk_usage("/")
    return disk.percent


def get_top_processes():
    processes = []

    for proc in psutil.process_iter(["name", "cpu_percent"]):
        try:
            info = proc.info

            if info["name"] is None:
                continue

            if info["cpu_percent"] is None:
                continue

            processes.append(info)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    processes = sorted(processes, key=lambda x: x["cpu_percent"], reverse=True)

    return processes[:5]


def generate_report():
    report = {
        "timestamp": datetime.now().isoformat(),
        "cpu_usage_percent": get_cpu_usage(),
        "memory_usage_percent": get_memory_usage(),
        "disk_usage_percent": get_disk_usage(),
        "top_processes": get_top_processes(),
    }

    return report


def save_report(report, folder="reports"):
    os.makedirs(folder, exist_ok=True)

    filename = f"system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(folder, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    return filepath