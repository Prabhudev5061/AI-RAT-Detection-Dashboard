"""
AI RAT Detection Dashboard - Linux Platform Adapter
Implements Linux-specific telemetry, XDG autostart inspection, sysfs GPU metrics, and rootless sensors.
"""

import os
import sys
import getpass
import socket
import time
import shutil
import subprocess
from typing import Dict, Any, List
from pathlib import Path

from platforms.base import BasePlatformAdapter


class LinuxPlatformAdapter(BasePlatformAdapter):
    """Linux hardware and OS telemetry implementation supporting Debian, Ubuntu, Fedora, and Arch."""

    def __init__(self):
        self._gpu_cache: Dict[str, Any] = {
            "available": False,
            "name": "Integrated / Not Detected",
            "utilization_percent": 0.0,
            "memory_total_mb": 0.0,
            "memory_used_mb": 0.0,
            "driver_version": "N/A",
        }
        self._last_gpu_check = 0.0
        self._gpu_check_interval = 10.0
        self._nvidia_smi_path = shutil.which("nvidia-smi")

    @property
    def platform_name(self) -> str:
        return "linux"

    def is_admin(self) -> bool:
        """Check for root privileges."""
        try:
            return os.geteuid() == 0
        except Exception:
            return False

    def get_user_info(self) -> Dict[str, Any]:
        """Obtains Linux username, hostname, and sudo/root status."""
        try:
            username = getpass.getuser()
        except Exception:
            username = os.environ.get("USER", "unknown")

        hostname = socket.gethostname()
        admin = self.is_admin()

        return {
            "username": username,
            "machine_name": hostname,
            "domain": hostname,
            "is_admin": admin,
            "display": f"{hostname}\\{username}" + (" (Root)" if admin else " (Standard User)"),
        }

    def get_primary_drive(self) -> str:
        return "/"

    def get_autostart_entries(self) -> List[Dict[str, Any]]:
        """Scans standard Linux XDG autostart locations."""
        entries = []
        home = os.path.expanduser("~")
        search_dirs = [
            os.path.join(home, ".config", "autostart"),
            "/etc/xdg/autostart",
            "/etc/init.d",
        ]

        for sdir in search_dirs:
            p = Path(sdir)
            if not p.exists():
                continue

            try:
                for f in p.glob("*"):
                    if f.is_file():
                        if f.suffix == ".desktop":
                            # Parse desktop file
                            name = f.stem
                            exec_cmd = ""
                            try:
                                with open(f, "r", encoding="utf-8", errors="ignore") as df:
                                    for line in df:
                                        if line.startswith("Name="):
                                            name = line.strip().split("=", 1)[1]
                                        elif line.startswith("Exec="):
                                            exec_cmd = line.strip().split("=", 1)[1]
                            except Exception:
                                pass

                            entries.append({
                                "name": name,
                                "command": exec_cmd or str(f),
                                "location": sdir,
                                "type": "XDG Desktop",
                                "suspicious": False,
                            })
                        elif sdir == "/etc/init.d":
                            entries.append({
                                "name": f.name,
                                "command": str(f),
                                "location": "/etc/init.d",
                                "type": "Init Script",
                                "suspicious": False,
                            })
            except Exception:
                continue

        return entries

    def get_gpu_metrics(self) -> Dict[str, Any]:
        """Harvests Linux GPU metrics (NVIDIA / AMD / Intel) via sysfs and nvidia-smi with 10s caching."""
        now = time.time()
        if now - self._last_gpu_check < self._gpu_check_interval:
            return self._gpu_cache

        self._last_gpu_check = now

        # 1. Check NVIDIA via nvidia-smi
        if self._nvidia_smi_path:
            try:
                cmd = [
                    self._nvidia_smi_path,
                    "--query-gpu=name,utilization.gpu,memory.total,memory.used,driver_version",
                    "--format=csv,noheader,nounits",
                ]
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
                if res.returncode == 0 and res.stdout.strip():
                    parts = [p.strip() for p in res.stdout.strip().split(",")]
                    if len(parts) >= 5:
                        self._gpu_cache = {
                            "available": True,
                            "name": parts[0],
                            "utilization_percent": float(parts[1]) if parts[1].replace(".", "").isdigit() else 0.0,
                            "memory_total_mb": float(parts[2]) if parts[2].replace(".", "").isdigit() else 0.0,
                            "memory_used_mb": float(parts[3]) if parts[3].replace(".", "").isdigit() else 0.0,
                            "driver_version": parts[4],
                        }
                        return self._gpu_cache
            except Exception:
                pass

        # 2. Check AMD / Intel via /sys/class/drm
        drm_path = Path("/sys/class/drm")
        if drm_path.exists():
            try:
                for card in drm_path.glob("card[0-9]"):
                    busy_file = card / "device" / "gpu_busy_percent"
                    if busy_file.exists():
                        try:
                            val = float(busy_file.read_text().strip())
                            self._gpu_cache = {
                                "available": True,
                                "name": "AMD/Intel DRM Graphics Adapter",
                                "utilization_percent": val,
                                "memory_total_mb": 0.0,
                                "memory_used_mb": 0.0,
                                "driver_version": "Mesa/DRM",
                            }
                            return self._gpu_cache
                        except Exception:
                            pass
            except Exception:
                pass

        # 3. Fallback
        self._gpu_cache = {
            "available": False,
            "name": "Integrated / Standard Display Adapter",
            "utilization_percent": 0.0,
            "memory_total_mb": 0.0,
            "memory_used_mb": 0.0,
            "driver_version": "N/A",
        }
        return self._gpu_cache

    def get_security_sensors(self) -> Dict[str, Any]:
        """Checks webcam device nodes without requiring root."""
        webcam_active = False
        webcam_app = "None"
        mic_active = False
        mic_app = "None"

        # Check for open video devices
        v4l = Path("/sys/class/video4linux")
        if v4l.exists():
            try:
                cams = list(v4l.glob("video*"))
                if cams:
                    webcam_app = f"{len(cams)} Camera Device(s) Present"
            except Exception:
                pass

        return {
            "webcam_active": webcam_active,
            "webcam_app": webcam_app,
            "mic_active": mic_active,
            "mic_app": mic_app,
        }

