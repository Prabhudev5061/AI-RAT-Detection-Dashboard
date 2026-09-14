"""
AI RAT Detection Dashboard - Permissions Utilities
Handles Administrator/root privilege detection and logged-in user identification.
Cross-platform support via platform_adapter.
"""

from typing import Dict, Any
from platforms import platform_adapter


def is_admin() -> bool:
    """Check if current process has Administrator/root privileges."""
    try:
        return platform_adapter.is_admin()
    except Exception:
        return False


def get_system_user_info() -> Dict[str, Any]:
    """Retrieve logged-in username, machine/domain, and elevation status."""
    try:
        return platform_adapter.get_user_info()
    except Exception:
        return {
            "username": "Unknown",
            "machine_name": "LocalHost",
            "domain": "LocalHost",
            "is_admin": False,
            "display": "Standard User",
        }

