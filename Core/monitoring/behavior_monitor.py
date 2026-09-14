"""
AI RAT Detection Dashboard - Defensive Behavior & Security Status Monitor
Monitors host security sensors: Camera, Microphone, Screen Recording, and Remote Access.
Cross-platform support across Windows and Linux.
"""

from typing import Dict, Any, Tuple
from config.config import KNOWN_REMOTE_TOOLS
from monitoring.process_monitor import process_monitor
from platforms import platform_adapter


class BehaviorMonitor:
    """Provides defensive host sensor evaluations with transparent visibility notes."""

    def get_security_status(self) -> Dict[str, Dict[str, Any]]:
        """
        Evaluates active security states across Windows and Linux.
        Returns status and visibility indicators without fake claims.
        """
        camera_status, camera_note = self._check_camera_active()
        mic_status, mic_note = self._check_microphone_active()
        screen_status, screen_note = self._check_screen_recording_active()
        remote_status, remote_note = self._check_remote_access_active()

        return {
            "camera": {
                "label": "Camera Detection",
                "status": camera_status,
                "note": camera_note,
                "is_active": camera_status != "No suspicious activity",
            },
            "microphone": {
                "label": "Microphone Detection",
                "status": mic_status,
                "note": mic_note,
                "is_active": mic_status != "No suspicious activity",
            },
            "screen": {
                "label": "Screen Recording Detection",
                "status": screen_status,
                "note": screen_note,
                "is_active": screen_status != "No suspicious activity",
            },
            "remote": {
                "label": "Remote Access Detection",
                "status": remote_status,
                "note": remote_note,
                "is_active": remote_status != "No suspicious activity",
            },
        }

    def _check_camera_active(self) -> Tuple[str, str]:
        """Check active webcam usage via the platform adapter."""
        try:
            sensors = platform_adapter.get_security_sensors()
            if sensors.get("webcam_active"):
                app = sensors.get("webcam_app", "Unknown")
                return f"Active ({app})", "Camera stream engaged"
            elif sensors.get("webcam_app") and sensors.get("webcam_app") != "None":
                return "Device Present", str(sensors.get("webcam_app"))
            return "No suspicious activity", "No active camera handle"
        except Exception:
            return "Monitoring limited", "Camera sensor query restricted"

    def _check_microphone_active(self) -> Tuple[str, str]:
        """Check active microphone usage via the platform adapter."""
        try:
            sensors = platform_adapter.get_security_sensors()
            if sensors.get("mic_active"):
                app = sensors.get("mic_app", "Unknown")
                return f"Active ({app})", "Microphone audio session engaged"
            return "No suspicious activity", "No active audio input session"
        except Exception:
            return "Monitoring limited", "Audio sensor query restricted"

    def _check_screen_recording_active(self) -> Tuple[str, str]:
        """Check for known screen recording software processes."""
        known_recorders = {
            "obs64.exe", "obs32.exe", "obs", "camtasia.exe", "bandicam.exe",
            "screenrec.exe", "sharex.exe", "simplescreenrecorder", "kazam", "recordmydesktop"
        }
        try:
            procs = process_monitor.get_all_processes()
            detected = [p["name"] for p in procs if p["name"].lower() in known_recorders]
            if detected:
                return f"Active ({', '.join(detected)})", "Screen recorder active"
            return "No suspicious activity", "No active screen recorder detected"
        except Exception:
            return "Monitoring limited", "Process inspection restricted"

    def _check_remote_access_active(self) -> Tuple[str, str]:
        """Check for active remote access software processes."""
        try:
            procs = process_monitor.get_all_processes()
            detected = []
            for p in procs:
                p_lower = p["name"].lower()
                for tool in KNOWN_REMOTE_TOOLS:
                    if tool in p_lower and p["name"] not in detected:
                        detected.append(p["name"])
            if detected:
                return f"Active ({', '.join(detected[:3])})", "Remote access software active"
            return "No suspicious activity", "No active remote access tools detected"
        except Exception:
            return "Monitoring limited", "Process inspection restricted"


# Singleton instance
behavior_monitor = BehaviorMonitor()

