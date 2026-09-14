"""
AI RAT Detection Dashboard - Startup Program Monitor
Audits system autostart configurations, registry persistence, and desktop autostart directories.
"""

from typing import List, Dict, Any
from platforms import platform_adapter


class StartupMonitor:
    """Detects programs configured to launch automatically on boot across Windows and Linux."""

    def get_startup_programs(self) -> List[Dict[str, Any]]:
        """Harvests persistent autostart entries via the active platform adapter."""
        try:
            return platform_adapter.get_autostart_entries()
        except Exception:
            return []


# Singleton instance
startup_monitor = StartupMonitor()

