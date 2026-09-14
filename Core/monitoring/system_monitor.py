"""
AI RAT Detection Dashboard - System Monitor
Collects real-time CPU, RAM, Disk, GPU, process metrics, and host user context.
"""

from pathlib import Path
import psutil
import datetime
from typing import Dict, Any

from platforms import platform_adapter


class SystemMonitor:
    """Collects system-level hardware, GPU, and operating system telemetry."""

    def __init__(self):
        # Primer call for CPU percent
        try:
            psutil.cpu_percent(interval=None)
        except Exception:
            pass

    def get_system_metrics(self) -> Dict[str, Any]:
        """
        Gathers current CPU, RAM, Disk, GPU, process counts, and network totals.
        Returns a dictionary with robust cross-platform fallbacks.
        """
        # CPU
        try:
            cpu_percent = psutil.cpu_percent(interval=None)
        except Exception:
            cpu_percent = 0.0

        # Memory
        try:
            mem = psutil.virtual_memory()
            memory_percent = mem.percent
            memory_used = mem.used
            memory_total = mem.total
        except Exception:
            memory_percent = 0.0
            memory_used = 0
            memory_total = 0

        # Disk
        try:
            drive = platform_adapter.get_primary_drive()
            try:
                disk = psutil.disk_usage(drive)
            except Exception:
                disk = psutil.disk_usage(Path.cwd().anchor or "/")
            disk_percent = disk.percent
            disk_used = disk.used
            disk_total = disk.total
        except Exception:
            disk_percent = 0.0
            disk_used = 0
            disk_total = 0

        # GPU metrics (cross-platform, cached to prevent CPU overhead)
        try:
            gpu_metrics = platform_adapter.get_gpu_metrics()
        except Exception:
            gpu_metrics = {
                "available": False,
                "name": "Integrated / Not Detected",
                "utilization_percent": 0.0,
                "memory_total_mb": 0.0,
                "memory_used_mb": 0.0,
                "driver_version": "N/A",
            }

        # Processes count
        try:
            total_processes = len(psutil.pids())
        except Exception:
            total_processes = 0

        # Network I/O
        try:
            net_io = psutil.net_io_counters()
            bytes_sent = net_io.bytes_sent
            bytes_recv = net_io.bytes_recv
        except Exception:
            bytes_sent = 0
            bytes_recv = 0

        # User and Host context
        try:
            user_info = platform_adapter.get_user_info()
        except Exception:
            user_info = {
                "username": "Unknown",
                "machine_name": "LocalHost",
                "domain": "LocalHost",
                "is_admin": False,
                "display": "Standard User",
            }

        return {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cpu_percent": round(cpu_percent, 1),
            "memory_percent": round(memory_percent, 1),
            "memory_used": memory_used,
            "memory_total": memory_total,
            "disk_percent": round(disk_percent, 1),
            "disk_used": disk_used,
            "disk_total": disk_total,
            "gpu": gpu_metrics,
            "total_processes": total_processes,
            "bytes_sent": bytes_sent,
            "bytes_recv": bytes_recv,
            "user_info": user_info,
        }


# Singleton instance
system_monitor = SystemMonitor()

