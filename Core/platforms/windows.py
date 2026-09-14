"""
AI RAT Detection Dashboard - Windows Platform Adapter
Implements Windows-specific telemetry, registry inspection, GPU querying, and security sensors.
"""

import os
import sys
import ctypes
import getpass
import time
import shutil
import subprocess
from typing import Dict, Any, List
from pathlib import Path

from platforms.base import BasePlatformAdapter


class WindowsPlatformAdapter(BasePlatformAdapter):
    """Windows-specific hardware and OS telemetry implementation."""

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
        self._gpu_check_interval = 10.0  # 10s caching to avoid high CPU
        self._nvidia_smi_path = shutil.which("nvidia-smi") or (
            r"C:\Windows\System32\nvidia-smi.exe"
            if os.path.exists(r"C:\Windows\System32\nvidia-smi.exe")
            else None
        )
        self._has_checked_smi = False

    @property
    def platform_name(self) -> str:
        return "windows"

    def is_admin(self) -> bool:
        """Check if current process has Administrator privileges on Windows."""
        try:
            return bool(ctypes.windll.shell32.IsUserAnAdmin() != 0)
        except Exception:
            return False

    def get_user_info(self) -> Dict[str, Any]:
        """Obtains Windows user, domain, computer name, and elevation status."""
        try:
            username = getpass.getuser()
        except Exception:
            username = os.environ.get("USERNAME", "Unknown")

        machine = os.environ.get("COMPUTERNAME", "LocalHost")
        domain = os.environ.get("USERDOMAIN", machine)
        admin = self.is_admin()

        return {
            "username": username,
            "machine_name": machine,
            "domain": domain,
            "is_admin": admin,
            "display": f"{domain}\\{username}" + (" (Administrator)" if admin else " (Standard User)"),
        }

    def get_primary_drive(self) -> str:
        """Returns primary system drive."""
        sys_drive = os.environ.get("SystemDrive", "C:")
        return f"{sys_drive}\\"

    def get_autostart_entries(self) -> List[Dict[str, Any]]:
        """Queries Windows Registry Run and RunOnce keys plus Startup folders."""
        entries = []
        try:
            import winreg

            locations = [
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", "HKCU\\Run"),
                (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", "HKLM\\Run"),
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\RunOnce", "HKCU\\RunOnce"),
                (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\RunOnce", "HKLM\\RunOnce"),
            ]

            for hkey, subkey, loc_name in locations:
                try:
                    with winreg.OpenKey(hkey, subkey, 0, winreg.KEY_READ) as key:
                        count = winreg.QueryInfoKey(key)[1]
                        for i in range(count):
                            try:
                                name, val, _ = winreg.EnumValue(key, i)
                                entries.append({
                                    "name": name,
                                    "command": str(val),
                                    "location": loc_name,
                                    "type": "Registry",
                                    "suspicious": False,
                                })
                            except Exception:
                                pass
                except Exception:
                    pass
        except ImportError:
            pass

        # Check Startup folder
        startup_paths = [
            os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"),
            os.path.expandvars(r"%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs\Startup"),
        ]
        for sp in startup_paths:
            p = Path(sp)
            if p.exists():
                for f in p.glob("*"):
                    if f.is_file() and not f.name.startswith("desktop.ini"):
                        entries.append({
                            "name": f.name,
                            "command": str(f.resolve()),
                            "location": "Startup Folder",
                            "type": "File",
                            "suspicious": False,
                        })

        return entries

    def get_gpu_metrics(self) -> Dict[str, Any]:
        """Harvests GPU metrics with caching to minimize CPU consumption."""
        now = time.time()
        if now - self._last_gpu_check < self._gpu_check_interval:
            return self._gpu_cache

        self._last_gpu_check = now

        if self._nvidia_smi_path:
            try:
                cmd = [
                    self._nvidia_smi_path,
                    "--query-gpu=name,utilization.gpu,memory.total,memory.used,driver_version",
                    "--format=csv,noheader,nounits",
                ]
                res = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=2,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                )
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

        # Fallback: integrated / standard GPU
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
        """Audits active microphone and webcam hardware sensors on Windows."""
        webcam_active = False
        mic_active = False
        webcam_app = "None"
        mic_app = "None"

        try:
            import winreg

            base_keys = [
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam"),
                (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam"),
            ]
            for root, base_key in base_keys:
                try:
                    with winreg.OpenKey(root, base_key, 0, winreg.KEY_READ) as key:
                        count = winreg.QueryInfoKey(key)[0]
                        for i in range(count):
                            subkey_name = winreg.EnumKey(key, i)
                            if subkey_name == "NonPackaged":
                                with winreg.OpenKey(key, subkey_name, 0, winreg.KEY_READ) as np_key:
                                    np_count = winreg.QueryInfoKey(np_key)[0]
                                    for j in range(np_count):
                                        app_key_name = winreg.EnumKey(np_key, j)
                                        with winreg.OpenKey(np_key, app_key_name, 0, winreg.KEY_READ) as app_k:
                                            try:
                                                stop_val, _ = winreg.QueryValueEx(app_k, "LastUsedTimeStop")
                                                start_val, _ = winreg.QueryValueEx(app_k, "LastUsedTimeStart")
                                                if start_val > stop_val:
                                                    webcam_active = True
                                                    webcam_app = app_key_name.split("#")[-1]
                                                    break
                                            except Exception:
                                                pass
                except Exception:
                    pass

            mic_keys = [
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone"),
                (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone"),
            ]
            for root, base_key in mic_keys:
                try:
                    with winreg.OpenKey(root, base_key, 0, winreg.KEY_READ) as key:
                        count = winreg.QueryInfoKey(key)[0]
                        for i in range(count):
                            subkey_name = winreg.EnumKey(key, i)
                            if subkey_name == "NonPackaged":
                                with winreg.OpenKey(key, subkey_name, 0, winreg.KEY_READ) as np_key:
                                    np_count = winreg.QueryInfoKey(np_key)[0]
                                    for j in range(np_count):
                                        app_key_name = winreg.EnumKey(np_key, j)
                                        with winreg.OpenKey(np_key, app_key_name, 0, winreg.KEY_READ) as app_k:
                                            try:
                                                stop_val, _ = winreg.QueryValueEx(app_k, "LastUsedTimeStop")
                                                start_val, _ = winreg.QueryValueEx(app_k, "LastUsedTimeStart")
                                                if start_val > stop_val:
                                                    mic_active = True
                                                    mic_app = app_key_name.split("#")[-1]
                                                    break
                                            except Exception:
                                                pass
                except Exception:
                    pass
        except Exception:
            pass

        return {
            "webcam_active": webcam_active,
            "webcam_app": webcam_app,
            "mic_active": mic_active,
            "mic_app": mic_app,
        }

