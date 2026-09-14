"""
Unit tests for SQLite Database Layer
"""

import pytest
from pathlib import Path
from database.database import DatabaseManager


@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_monitoring.db"
    return DatabaseManager(db_path=db_file)


def test_db_initialization(temp_db):
    assert temp_db.db_path.exists()
    with temp_db.get_connection() as conn:
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row["name"] for row in cursor.fetchall()]
        assert "system_metrics" in tables
        assert "events" in tables
        assert "alerts" in tables
        assert "process_snapshots" in tables
        assert "network_snapshots" in tables


def test_insert_and_get_metrics(temp_db):
    temp_db.insert_system_metric(15.5, 55.0, 70.0, 200, 1000, 2000)
    temp_db.insert_system_metric(20.0, 56.0, 70.0, 201, 1500, 2500)

    recent = temp_db.get_recent_metrics(limit=10)
    assert len(recent) == 2
    assert recent[0]["cpu_percent"] == 15.5
    assert recent[1]["cpu_percent"] == 20.0


def test_insert_and_get_events(temp_db):
    temp_db.insert_event("LOGIN", "User logged in", "INFO", "Auth")
    temp_db.insert_event("RAT_DETECTED", "High threat on port 4444", "CRITICAL", "Detection", pid=1234, port=4444)

    events = temp_db.get_recent_events(limit=10)
    assert len(events) == 2

    critical_events = temp_db.get_recent_events(limit=10, min_severity="CRITICAL")
    assert len(critical_events) == 1
    assert critical_events[0]["event_type"] == "RAT_DETECTED"
    assert critical_events[0]["pid"] == 1234


def test_insert_and_get_alerts(temp_db):
    temp_db.insert_alert("Suspicious Port", "Listening on port 4444", "HIGH", 75, pid=999, process_name="evil.exe")
    alerts = temp_db.get_recent_alerts(limit=10)
    assert len(alerts) == 1
    assert alerts[0]["rule_name"] == "Suspicious Port"
    assert alerts[0]["risk_score"] == 75


def test_prune_old_data(temp_db):
    for i in range(20):
        temp_db.insert_system_metric(float(i), 50.0, 60.0, 100, 10, 20)

    assert len(temp_db.get_recent_metrics(limit=50)) == 20
    temp_db.prune_old_data(max_records=5)
    assert len(temp_db.get_recent_metrics(limit=50)) == 5
