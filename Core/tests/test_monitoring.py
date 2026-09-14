"""
Unit tests for Monitoring Subsystems
"""

import pytest
from monitoring.system_monitor import SystemMonitor
from monitoring.process_monitor import ProcessMonitor
from monitoring.startup_monitor import StartupMonitor
from monitoring.network_monitor import NetworkMonitor
from monitoring.behavior_monitor import BehaviorMonitor


def test_system_monitor_metrics():
    sys_mon = SystemMonitor()
    metrics = sys_mon.get_system_metrics()
    assert "cpu_percent" in metrics
    assert "memory_percent" in metrics
    assert "disk_percent" in metrics
    assert "total_processes" in metrics
    assert metrics["total_processes"] >= 0
    assert "user_info" in metrics
    assert "username" in metrics["user_info"]


def test_process_monitor_lists():
    proc_mon = ProcessMonitor()
    procs = proc_mon.get_all_processes()
    assert isinstance(procs, list)
    assert len(procs) > 0

    first = procs[0]
    assert "pid" in first
    assert "name" in first
    assert "cpu_percent" in first
    assert "memory_percent" in first


def test_process_monitor_top_cpu():
    proc_mon = ProcessMonitor()
    top = proc_mon.get_top_cpu_processes(limit=3)
    assert len(top) <= 3
    if len(top) >= 2:
        assert top[0]["cpu_percent"] >= top[1]["cpu_percent"]


def test_startup_monitor():
    start_mon = StartupMonitor()
    items = start_mon.get_startup_programs()
    assert isinstance(items, list)
    # Check that any returned items have valid structure
    for it in items:
        assert "name" in it
        assert "location" in it


def test_network_monitor():
    net_mon = NetworkMonitor()
    conns = net_mon.get_active_connections(limit=10)
    assert isinstance(conns, list)
    for c in conns:
        assert "pid" in c
        assert "protocol" in c
        assert "local_address" in c


def test_behavior_monitor():
    beh_mon = BehaviorMonitor()
    status = beh_mon.get_security_status()
    assert "camera" in status
    assert "microphone" in status
    assert "screen" in status
    assert "remote" in status
    for key, val in status.items():
        assert "label" in val
        assert "status" in val


def test_monitoring_service_caching_and_snapshot():
    from services.monitoring_service import MonitoringService
    svc = MonitoringService()
    # Force first snapshot
    data = svc.collect_and_evaluate(force=True)
    assert "metrics" in data
    assert "processes" in data
    assert "evaluation" in data
    # Second call should return cached data instantly
    data2 = svc.collect_and_evaluate(force=False)
    assert data2["metrics"]["timestamp"] == data["metrics"]["timestamp"]
    svc.stop()

