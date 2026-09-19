"""
AI RAT Detection Dashboard - Base Platform Adapter
Abstract interface defining platform-specific hardware and OS telemetry collection.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BasePlatformAdapter(ABC):
    """Abstract platform adapter ensuring cross-platform support across Windows and Linux."""

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Returns the OS identifier: 'windows', 'linux', or 'generic'."""
        pass

    @abstractmethod
    def is_admin(self) -> bool:
        """Check if current process has elevated (root/Administrator) privileges."""
        pass

    @abstractmethod
    def get_user_info(self) -> Dict[str, Any]:
        """Obtain logged-in username, hostname, domain, and elevation status."""
        pass

    @abstractmethod
    def get_autostart_entries(self) -> List[Dict[str, Any]]:
        """Harvest startup / persistent launch entries."""
        pass

    @abstractmethod
    def get_gpu_metrics(self) -> Dict[str, Any]:
        """Harvest GPU utilization, memory, and model without excessive polling."""
        pass

    @abstractmethod
    def get_security_sensors(self) -> Dict[str, Any]:
        """Audit active camera, microphone, or surveillance peripherals."""
        pass

    @abstractmethod
    def get_primary_drive(self) -> str:
        """Returns the root drive identifier for primary disk usage metrics."""
        pass
