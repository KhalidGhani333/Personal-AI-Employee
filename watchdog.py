#!/usr/bin/env python3
"""
System Health Watchdog - Monitor and Restart Services
Monitors all AI Employee services and restarts if stopped
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
import time
import psutil

# Configuration
VAULT = Path("AI_Employee_Vault")
HEALTH_LOG = VAULT / "Logs" / "system_health.md"
HEALTH_JSON = VAULT / "Logs" / "system_health.json"
LOGS_DIR = Path("logs")

# Ensure directories exist
HEALTH_LOG.parent.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Services to monitor (PM2 names)
SERVICES = [
    "orchestrator",
    "gmail-watcher",
    "whatsapp-watcher",
    "linkedin-watcher",
    "reply-generator",
    "reply-sender",
    "ralph-wiggum"
]

# Critical services (must be running)
CRITICAL_SERVICES = ["orchestrator"]

# Health thresholds
MAX_LOG_SIZE_MB = 50
MAX_DISK_USAGE_PERCENT = 90
MIN_FREE_DISK_GB = 5


class HealthStatus:
    """Health status tracker"""

    def __init__(self):
        self.timestamp = datetime.now()
        self.services = {}
        self.system = {}
        self.vault = {}
        self.issues = []
        self.critical_issues = []

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "services": self.services,
            "system": self.system,
            "vault": self.vault,
            "issues": self.issues,
            "critical_issues": self.critical_issues
        }


def check_pm2_installed():
    """Check if PM2 is installed"""
    try:
        subprocess.run(["pm2", "--version"],
                      capture_output=True,
                      check=True,
                      timeout=5)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False


def get_pm2_status():
    """Get PM2 process status"""
    try:
        result = subprocess.run(
            ["pm2", "jlist"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError,
            FileNotFoundError, subprocess.TimeoutExpired):
        return []


def check_service_status(service_name, pm2_list):
    """Check if a service is running"""
    for proc in pm2_list:
        if proc.get("name") == service_name:
            status = proc.get("pm2_env", {}).get("status", "stopped")
            return {
                "running": status == "online",
                "status": status,
                "uptime": proc.get("pm2_env", {}).get("pm_uptime", 0),
                "restarts": proc.get("pm2_env", {}).get("restart_time", 0),
                "memory": proc.get("monit", {}).get("memory", 0),
                "cpu": proc.get("monit", {}).get("cpu", 0)
            }
    return {
        "running": False,
        "status": "not_found",
        "uptime": 0,
        "restarts": 0,
        "memory": 0,
        "cpu": 0
    }


def restart_service(service_name):
    """Restart a PM2 service"""
    try:
        result = subprocess.run(
            ["pm2", "restart", service_name],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False


def check_system_resources():
    """Check system resources"""
    try:
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)

        # Memory usage
        memory = psutil.virtual_memory()

        # Disk usage
        disk = psutil.disk_usage('.')

        return {
            "cpu_percent": cpu_percent,
            "memory_total_gb": round(memory.total / (1024**3), 2),
            "memory_used_gb": round(memory.used / (1024**3), 2),
            "memory_percent": memory.percent,
            "disk_total_gb": round(disk.total / (1024**3), 2),
            "disk_used_gb": round(disk.used / (1024**3), 2),
            "disk_free_gb": round(disk.free / (1024**3), 2),
            "disk_percent": disk.percent
        }
    except Exception as e:
        return {"error": str(e)}


def check_vault_status():
    """Check vault folder status"""
    try:
        vault_status = {}

        # Count files in each folder
        folders = [
            "Needs_Action/email",
            "Needs_Action/social",
            "Pending_Approval/email",
            "Pending_Approval/social",
            "Approved",
            "Done"
        ]

        for folder in folders:
            folder_path = VAULT / folder
            if folder_path.exists():
                file_count = len(list(folder_path.glob("*.md")))
                vault_status[folder.replace("/", "_")] = file_count
            else:
                vault_status[folder.replace("/", "_")] = 0

        # Check log sizes
        log_sizes = {}
        if LOGS_DIR.exists():
            for log_file in LOGS_DIR.glob("*.log"):
                size_mb = log_file.stat().st_size / (1024 * 1024)
                log_sizes[log_file.name] = round(size_mb, 2)

        vault_status["log_sizes_mb"] = log_sizes

        return vault_status
    except Exception as e:
        return {"error": str(e)}


def check_health():
    """Perform complete health check"""
    status = HealthStatus()

    # Check if PM2 is available
    pm2_available = check_pm2_installed()
    status.system["pm2_available"] = pm2_available

    if not pm2_available:
        status.critical_issues.append("PM2 not installed or not in PATH")
        return status

    # Get PM2 status
    pm2_list = get_pm2_status()

    # Check each service
    for service in SERVICES:
        service_status = check_service_status(service, pm2_list)
        status.services[service] = service_status

        if not service_status["running"]:
            issue = f"{service} is {service_status['status']}"
            if service in CRITICAL_SERVICES:
                status.critical_issues.append(issue)
            else:
                status.issues.append(issue)

    # Check system resources
    system_resources = check_system_resources()
    status.system.update(system_resources)

    # Check for resource issues
    if "disk_percent" in system_resources:
        if system_resources["disk_percent"] > MAX_DISK_USAGE_PERCENT:
            status.critical_issues.append(
                f"Disk usage critical: {system_resources['disk_percent']}%"
            )
        elif system_resources["disk_free_gb"] < MIN_FREE_DISK_GB:
            status.issues.append(
                f"Low disk space: {system_resources['disk_free_gb']} GB free"
            )

    if "memory_percent" in system_resources:
        if system_resources["memory_percent"] > 90:
            status.issues.append(
                f"High memory usage: {system_resources['memory_percent']}%"
            )

    # Check vault status
    vault_status = check_vault_status()
    status.vault = vault_status

    # Check log file sizes
    if "log_sizes_mb" in vault_status:
        for log_name, size_mb in vault_status["log_sizes_mb"].items():
            if size_mb > MAX_LOG_SIZE_MB:
                status.issues.append(
                    f"Large log file: {log_name} ({size_mb} MB)"
                )

    return status


def restart_stopped_services(status):
    """Restart any stopped services"""
    restarted = []
    failed = []

    for service, service_status in status.services.items():
        if not service_status["running"]:
            print(f"🔄 Restarting {service}...")
            if restart_service(service):
                restarted.append(service)
                print(f"✅ Restarted {service}")
            else:
                failed.append(service)
                print(f"❌ Failed to restart {service}")

    return restarted, failed


def write_health_log(status, restarted, failed):
    """Write health status to markdown log"""

    # Prepare markdown content
    content = f"""# System Health Status

**Last Updated:** {status.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

---

## 🎯 Overall Status

"""

    # Overall status
    if status.critical_issues:
        content += "**Status:** 🔴 CRITICAL\n\n"
        content += "### Critical Issues\n"
        for issue in status.critical_issues:
            content += f"- ❌ {issue}\n"
        content += "\n"
    elif status.issues:
        content += "**Status:** 🟡 WARNING\n\n"
    else:
        content += "**Status:** 🟢 HEALTHY\n\n"

    # Issues
    if status.issues:
        content += "### Issues\n"
        for issue in status.issues:
            content += f"- ⚠️  {issue}\n"
        content += "\n"

    # Restart actions
    if restarted:
        content += "### Actions Taken\n"
        for service in restarted:
            content += f"- 🔄 Restarted: {service}\n"
        content += "\n"

    if failed:
        content += "### Failed Actions\n"
        for service in failed:
            content += f"- ❌ Failed to restart: {service}\n"
        content += "\n"

    # Services status
    content += "---\n\n## 📊 Services Status\n\n"
    content += "| Service | Status | Uptime | Restarts | Memory | CPU |\n"
    content += "|---------|--------|--------|----------|--------|-----|\n"

    for service, service_status in status.services.items():
        status_icon = "🟢" if service_status["running"] else "🔴"
        uptime_hours = service_status["uptime"] / 3600 if service_status["uptime"] > 0 else 0
        memory_mb = service_status["memory"] / (1024 * 1024) if service_status["memory"] > 0 else 0

        content += f"| {service} | {status_icon} {service_status['status']} | "
        content += f"{uptime_hours:.1f}h | {service_status['restarts']} | "
        content += f"{memory_mb:.0f} MB | {service_status['cpu']:.1f}% |\n"

    # System resources
    content += "\n---\n\n## 💻 System Resources\n\n"

    if "cpu_percent" in status.system:
        content += f"**CPU Usage:** {status.system['cpu_percent']:.1f}%\n\n"

    if "memory_percent" in status.system:
        content += f"**Memory:** {status.system['memory_used_gb']:.1f} GB / "
        content += f"{status.system['memory_total_gb']:.1f} GB "
        content += f"({status.system['memory_percent']:.1f}%)\n\n"

    if "disk_percent" in status.system:
        content += f"**Disk:** {status.system['disk_used_gb']:.1f} GB / "
        content += f"{status.system['disk_total_gb']:.1f} GB "
        content += f"({status.system['disk_percent']:.1f}%) - "
        content += f"{status.system['disk_free_gb']:.1f} GB free\n\n"

    # Vault status
    content += "---\n\n## 📁 Vault Status\n\n"
    content += "| Folder | Files |\n"
    content += "|--------|-------|\n"

    for folder, count in status.vault.items():
        if folder != "log_sizes_mb":
            content += f"| {folder.replace('_', '/')} | {count} |\n"

    # Log sizes
    if "log_sizes_mb" in status.vault:
        content += "\n### Log File Sizes\n\n"
        for log_name, size_mb in status.vault["log_sizes_mb"].items():
            icon = "⚠️ " if size_mb > MAX_LOG_SIZE_MB else ""
            content += f"- {icon}{log_name}: {size_mb} MB\n"

    content += "\n---\n\n"
    content += "*Generated by System Health Watchdog*\n"

    # Write to file
    with open(HEALTH_LOG, 'w', encoding='utf-8') as f:
        f.write(content)

    # Also write JSON for programmatic access
    with open(HEALTH_JSON, 'w', encoding='utf-8') as f:
        json.dump(status.to_dict(), f, indent=2)


def main():
    """Main watchdog function"""
    print("🐕 System Health Watchdog")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")

    # Perform health check
    print("🔍 Checking system health...")
    status = check_health()

    # Report status
    if status.critical_issues:
        print("🔴 CRITICAL ISSUES DETECTED:")
        for issue in status.critical_issues:
            print(f"   ❌ {issue}")
        print("")

    if status.issues:
        print("🟡 WARNINGS:")
        for issue in status.issues:
            print(f"   ⚠️  {issue}")
        print("")

    # Restart stopped services
    restarted, failed = restart_stopped_services(status)

    # Write health log
    print("📝 Writing health log...")
    write_health_log(status, restarted, failed)
    print(f"✅ Health log written to: {HEALTH_LOG}")

    # Summary
    print("")
    print("📊 Summary:")
    running = sum(1 for s in status.services.values() if s["running"])
    total = len(status.services)
    print(f"   Services: {running}/{total} running")

    if restarted:
        print(f"   Restarted: {len(restarted)} service(s)")

    if failed:
        print(f"   Failed: {len(failed)} service(s)")

    if status.critical_issues:
        print("   Status: 🔴 CRITICAL")
        return 2  # Critical exit code
    elif status.issues or failed:
        print("   Status: 🟡 WARNING")
        return 1  # Warning exit code
    else:
        print("   Status: 🟢 HEALTHY")
        return 0  # Success exit code


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
