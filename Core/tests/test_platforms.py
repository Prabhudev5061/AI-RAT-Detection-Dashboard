"""
Unit tests for the cross-platform platform abstraction layer.
Validates Windows, Linux, and Base platform adapters.
"""

import pytest
from platforms import get_platform_adapter, platform_adapter
from platforms.base import BasePlatformAdapter
from platforms.windows import WindowsPlatformAdapter
from platforms.linux import LinuxPlatformAdapter


def test_platform_adapter_instance():
    """Verify active platform adapter is an instance of BasePlatformAdapter."""
    adapter = get_platform_adapter()
    assert isinstance(adapter, BasePlatformAdapter)
    assert adapter.platform_name in ("windows", "linux", "generic")


def test_user_info_structure():
    """Verify get_user_info returns standard schema."""
    info = platform_adapter.get_user_info()
    assert isinstance(info, dict)
    assert "username" in info
    assert "machine_name" in info
    assert "domain" in info
    assert "is_admin" in info
    assert "display" in info
    assert isinstance(info["is_admin"], bool)


def test_primary_drive():
    """Verify primary drive returns a valid non-empty root indicator."""
    drive = platform_adapter.get_primary_drive()
    assert isinstance(drive, str)
    assert len(drive) > 0


def test_gpu_metrics_schema():
    """Verify GPU metrics dictionary structure."""
    gpu = platform_adapter.get_gpu_metrics()
    assert isinstance(gpu, dict)
    assert "available" in gpu
    assert "name" in gpu
    assert "utilization_percent" in gpu
    assert "memory_total_mb" in gpu
    assert "memory_used_mb" in gpu
    assert "driver_version" in gpu
    assert isinstance(gpu["available"], bool)
    assert isinstance(gpu["utilization_percent"], (int, float))


def test_security_sensors_schema():
    """Verify security sensor evaluation structure."""
    sensors = platform_adapter.get_security_sensors()
    assert isinstance(sensors, dict)
    assert "webcam_active" in sensors
    assert "webcam_app" in sensors
    assert "mic_active" in sensors
    assert "mic_app" in sensors
    assert isinstance(sensors["webcam_active"], bool)
    assert isinstance(sensors["mic_active"], bool)


def test_autostart_entries_schema():
    """Verify autostart entries structure."""
    entries = platform_adapter.get_autostart_entries()
    assert isinstance(entries, list)
    for e in entries:
        assert "name" in e
        assert "command" in e
        assert "location" in e
        assert "type" in e


def test_linux_adapter_cross_platform_safety():
    """Verify Linux platform adapter can be instantiated and queried without crashing."""
    linux_adapter = LinuxPlatformAdapter()
    assert linux_adapter.platform_name == "linux"
    assert linux_adapter.get_primary_drive() == "/"
    
    # Should not crash even when executed on non-Linux
    user_info = linux_adapter.get_user_info()
    assert "username" in user_info
    assert isinstance(user_info["is_admin"], bool)

    gpu = linux_adapter.get_gpu_metrics()
    assert "available" in gpu

    sensors = linux_adapter.get_security_sensors()
    assert "webcam_active" in sensors

    autostart = linux_adapter.get_autostart_entries()
    assert isinstance(autostart, list)
