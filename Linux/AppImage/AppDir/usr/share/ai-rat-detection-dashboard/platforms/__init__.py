"""
AI RAT Detection Dashboard - Platform Abstraction Package
Exposes uniform platform adapter regardless of whether running on Windows or Linux.
"""

import sys
from platforms.base import BasePlatformAdapter


def get_platform_adapter() -> BasePlatformAdapter:
    """Factory function returning the active OS platform adapter."""
    if sys.platform == "win32":
        from platforms.windows import WindowsPlatformAdapter
        return WindowsPlatformAdapter()
    elif sys.platform.startswith("linux"):
        from platforms.linux import LinuxPlatformAdapter
        return LinuxPlatformAdapter()
    else:
        from platforms.linux import LinuxPlatformAdapter
        return LinuxPlatformAdapter()


platform_adapter = get_platform_adapter()
