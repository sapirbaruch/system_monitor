import psutil
import json
import os
from datetime import datetime


def get_cpu_usage():
    # Return current CPU usage percentage
    return psutil.cpu_percent(interval=1)


def get_memory_usage():
    memory = psutil.virtual_memory()
    # Return memory usage percentage
    return memory.percent


def get_disk_usage():
    # Get disk usage statistics for the root partition
    disk = psutil.disk_usage("/")
   
    return disk.percent


def get_top_processes():
    # List to store process information
    processes = []

    for proc in psutil.process_iter(["name", "cpu_percent"]):
        try:
            info = proc.info

            # Skip processes without a valid name
            if info["name"] is None:
                continue

            # Skip processes without CPU data
            if info["cpu_percent"] is None:
                continue

            # Add process info to the list
            processes.append(info)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    processes = sorted(processes, key=lambda x: x["cpu_percent"], reverse=True)

    # Return top 5 processes consuming CPU
    return processes[:5]


def generate_report():
    # Build a dictionary containing system metrics
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

    # Generate a unique filename based on the current timestamp
    filename = f"system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    filepath = os.path.join(folder, filename)

    # Write the report dictionary to a JSON file
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    return filepath