from monitor import generate_report, save_report


def print_report(report):
    print("System Health Report")
    print("-" * 30)
    print(f"Timestamp: {report['timestamp']}")
    print(f"CPU Usage: {report['cpu_usage_percent']}%")
    print(f"Memory Usage: {report['memory_usage_percent']}%")
    print(f"Disk Usage: {report['disk_usage_percent']}%")
    print("\nTop Processes:")

    for proc in report["top_processes"]:
        print(f"{proc['name']} - {proc['cpu_percent']}%")


def main():
    report = generate_report()
    print_report(report)

    filepath = save_report(report)
    print(f"\nReport saved to: {filepath}")


if __name__ == "__main__":
    main()