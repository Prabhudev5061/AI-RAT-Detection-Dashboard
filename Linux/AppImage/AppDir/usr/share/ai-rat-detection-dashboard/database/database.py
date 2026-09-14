"""
AI-RAT-Detection-Dashboard - Database Manager
Thread-safe SQLite connection handling, schema initialization, and querying.
"""

import sqlite3
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from config.config import DATABASE_PATH, DB_RETENTION_MAX_RECORDS


class DatabaseManager:
    """Manages SQLite storage for system metrics, events, alerts, and snapshots."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = Path(db_path) if db_path else DATABASE_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        """Returns a connection configured with WAL mode and row factory."""
        conn = sqlite3.connect(str(self.db_path), timeout=10.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        return conn

    def init_db(self):
        """Initializes tables and indexes using schema.sql."""
        schema_path = Path(__file__).resolve().parent / "schema.sql"
        if schema_path.exists():
            with open(schema_path, "r", encoding="utf-8") as f:
                schema_sql = f.read()
            with self.get_connection() as conn:
                conn.executescript(schema_sql)

    # ------------------ Metrics Operations ------------------

    def insert_system_metric(
        self,
        cpu_percent: float,
        memory_percent: float,
        disk_percent: float,
        process_count: int,
        bytes_sent: int,
        bytes_recv: int,
        timestamp: Optional[str] = None,
    ) -> int:
        ts = timestamp or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO system_metrics (timestamp, cpu_percent, memory_percent, disk_percent, process_count, bytes_sent, bytes_recv)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (ts, float(cpu_percent), float(memory_percent), float(disk_percent), int(process_count), int(bytes_sent), int(bytes_recv)),
            )
            return cursor.lastrowid

    def get_recent_metrics(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT * FROM system_metrics
                ORDER BY id DESC LIMIT ?
                """,
                (limit,),
            )
            rows = cursor.fetchall()
            # Return ascending order for time-series visualization
            return [dict(r) for r in reversed(rows)]

    # ------------------ Events Operations ------------------

    def insert_event(
        self,
        event_type: str,
        description: str,
        severity: str,
        source: str = "System",
        pid: Optional[int] = None,
        ip: Optional[str] = None,
        port: Optional[int] = None,
        timestamp: Optional[str] = None,
    ) -> int:
        ts = timestamp or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO events (timestamp, event_type, description, severity, source, pid, ip, port)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (ts, event_type, description, severity.upper(), source, pid, ip, port),
            )
            return cursor.lastrowid

    def get_recent_events(self, limit: int = 50, min_severity: Optional[str] = None) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            if min_severity:
                cursor = conn.execute(
                    """
                    SELECT * FROM events
                    WHERE severity = ?
                    ORDER BY id DESC LIMIT ?
                    """,
                    (min_severity.upper(), limit),
                )
            else:
                cursor = conn.execute(
                    """
                    SELECT * FROM events
                    ORDER BY id DESC LIMIT ?
                    """,
                    (limit,),
                )
            return [dict(r) for r in cursor.fetchall()]

    # ------------------ Alerts Operations ------------------

    def insert_alert(
        self,
        rule_name: str,
        description: str,
        severity: str,
        risk_score: int,
        pid: Optional[int] = None,
        process_name: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> int:
        ts = timestamp or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO alerts (timestamp, rule_name, description, severity, risk_score, pid, process_name, resolved)
                VALUES (?, ?, ?, ?, ?, ?, ?, 0)
                """,
                (ts, rule_name, description, severity.upper(), int(risk_score), pid, process_name),
            )
            return cursor.lastrowid

    def get_recent_alerts(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT * FROM alerts
                ORDER BY id DESC LIMIT ?
                """,
                (limit,),
            )
            return [dict(r) for r in cursor.fetchall()]

    # ------------------ Snapshots Operations ------------------

    def insert_process_snapshots(self, snapshots: List[Dict[str, Any]]):
        if not snapshots:
            return
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rows = [
            (
                ts,
                s.get("pid", 0),
                s.get("name", "unknown"),
                float(s.get("cpu_percent", 0.0)),
                float(s.get("memory_percent", 0.0)),
                s.get("exe_path", ""),
                s.get("parent_pid"),
                int(s.get("risk_score", 0)),
                s.get("risk_level", "LOW"),
            )
            for s in snapshots
        ]
        with self.get_connection() as conn:
            conn.executemany(
                """
                INSERT INTO process_snapshots (timestamp, pid, name, cpu_percent, memory_percent, exe_path, parent_pid, risk_score, risk_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )

    def insert_network_snapshots(self, snapshots: List[Dict[str, Any]]):
        if not snapshots:
            return
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rows = [
            (
                ts,
                s.get("pid"),
                s.get("process_name", "unknown"),
                s.get("protocol", "TCP"),
                s.get("local_addr", ""),
                s.get("local_port"),
                s.get("remote_addr", ""),
                s.get("remote_port"),
                s.get("status", "NONE"),
            )
            for s in snapshots
        ]
        with self.get_connection() as conn:
            conn.executemany(
                """
                INSERT INTO network_snapshots (timestamp, pid, process_name, protocol, local_addr, local_port, remote_addr, remote_port, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )

    # ------------------ Retention / Maintenance ------------------

    def prune_old_data(self, max_records: int = DB_RETENTION_MAX_RECORDS):
        """Keep historical tables within bounded row count."""
        with self.get_connection() as conn:
            conn.execute(
                """
                DELETE FROM system_metrics
                WHERE id NOT IN (
                    SELECT id FROM system_metrics ORDER BY id DESC LIMIT ?
                )
                """,
                (max_records,),
            )
            conn.execute(
                """
                DELETE FROM events
                WHERE id NOT IN (
                    SELECT id FROM events ORDER BY id DESC LIMIT ?
                )
                """,
                (max_records,),
            )
            conn.execute(
                """
                DELETE FROM alerts
                WHERE id NOT IN (
                    SELECT id FROM alerts ORDER BY id DESC LIMIT ?
                )
                """,
                (max_records,),
            )


# Default singleton instance
db = DatabaseManager()
