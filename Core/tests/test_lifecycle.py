"""
Unit tests for Telemetry Lifecycle, Threading, and Clean Shutdown.
Validates thread creation, idempotent start/stop, snapshot caching, and robust error fallbacks.
"""

import time
import pytest
from services.monitoring_service import MonitoringService
from monitoring.system_monitor import SystemMonitor


def test_telemetry_service_lifecycle():
    """Verify monitoring service starts, collects, caches, and cleanly shuts down."""
    service = MonitoringService()
    assert service._worker_thread is None

    # Start worker
    service.start()
    assert service._worker_thread is not None
    assert service._worker_thread.is_alive()

    # Idempotent start (calling again shouldn't spawn a new thread)
    first_thread = service._worker_thread
    service.start()
    assert service._worker_thread is first_thread

    # Wait briefly for initial snapshot
    time.sleep(0.5)
    data = service.get_latest_data()
    assert isinstance(data, dict)
    assert "metrics" in data
    assert "processes" in data
    assert "evaluation" in data

    # Clean shutdown
    service.stop(timeout=2.0)
    assert service._worker_thread is None

    # Can restart cleanly after stop
    service.start()
    assert service._worker_thread is not None
    assert service._worker_thread.is_alive()
    service.stop(timeout=2.0)


def test_system_monitor_robustness():
    """Verify system monitor returns complete dictionary with graceful fallbacks."""
    monitor = SystemMonitor()
    metrics = monitor.get_system_metrics()

    assert "cpu_percent" in metrics
    assert "memory_percent" in metrics
    assert "disk_percent" in metrics
    assert "gpu" in metrics
    assert "total_processes" in metrics
    assert "bytes_sent" in metrics
    assert "bytes_recv" in metrics
    assert "user_info" in metrics

    # Value ranges
    assert 0.0 <= metrics["cpu_percent"] <= 100.0
    assert 0.0 <= metrics["memory_percent"] <= 100.0
    assert 0.0 <= metrics["disk_percent"] <= 100.0
    assert isinstance(metrics["gpu"], dict)
