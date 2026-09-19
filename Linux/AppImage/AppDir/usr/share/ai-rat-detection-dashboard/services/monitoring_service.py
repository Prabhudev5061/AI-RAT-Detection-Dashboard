"""
AI-RAT-Detection-Dashboard - Monitoring Service
Unified background and on-demand coordinator for all data collectors and analyzers.
Features a decoupled background worker thread with tiered sampling intervals
to minimize CPU usage, prevent UI blocking, and ensure instantaneous UI response.
"""

import time
import threading
import logging
from typing import Dict, Any, Optional

from database.database import db
from monitoring.system_monitor import system_monitor
from monitoring.process_monitor import process_monitor
from monitoring.network_monitor import network_monitor
from monitoring.startup_monitor import startup_monitor
from monitoring.behavior_monitor import behavior_monitor
from detection.risk_engine import risk_engine
from services.alert_service import alert_service

logger = logging.getLogger("MonitoringService")


class MonitoringService:
    """Coordinates telemetry harvesting, evaluation, persistence, and state caching."""

    def __init__(self):
        self._lock = threading.Lock()
        self._latest_snapshot: Optional[Dict[str, Any]] = None
        self._worker_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

        # Sampling intervals (seconds)
        self.metrics_interval: float = 3.0      # CPU, RAM, Disk, Network IO
        self.process_interval: float = 10.0     # Processes, sockets, risk evaluation
        self.deep_scan_interval: float = 60.0   # Registry startup, defensive sensors
        self.prune_interval: float = 300.0      # DB cleanup

        # Cached telemetry partitions
        self._cached_metrics: Dict[str, Any] = {}
        self._cached_processes = []
        self._cached_top_processes = []
        self._cached_parent_child = []
        self._cached_startup_items = []
        self._cached_connections = []
        self._cached_suspicious_ports = []
        self._cached_security_status: Dict[str, Any] = {}
        self._cached_evaluation: Dict[str, Any] = {}

        # Register clean shutdown on process termination
        import atexit
        atexit.register(self.stop)

    def start(self):
        """Starts the decoupled background collector worker thread if not already active."""
        with self._lock:
            if self._worker_thread is not None and self._worker_thread.is_alive():
                return
            self._stop_event.clear()
            self._worker_thread = threading.Thread(
                target=self._worker_loop,
                name="TelemetryCollectorThread",
                daemon=True,
            )
            self._worker_thread.start()

    def stop(self, timeout: float = 2.0):
        """Signals background worker to stop and waits for completion."""
        self._stop_event.set()
        with self._lock:
            if self._worker_thread and self._worker_thread.is_alive():
                self._worker_thread.join(timeout=timeout)
            self._worker_thread = None

    def _full_collect_sync(self) -> Dict[str, Any]:
        """Performs a full synchronous telemetry collection and risk evaluation."""
        metrics = system_monitor.get_system_metrics()
        try:
            db.insert_system_metric(
                cpu_percent=metrics["cpu_percent"],
                memory_percent=metrics["memory_percent"],
                disk_percent=metrics["disk_percent"],
                process_count=metrics["total_processes"],
                bytes_sent=metrics["bytes_sent"],
                bytes_recv=metrics["bytes_recv"],
                timestamp=metrics["timestamp"],
            )
        except Exception as e:
            logger.debug(f"Metric insertion notice: {e}")

        processes = process_monitor.get_all_processes()
        top_processes = process_monitor.get_top_cpu_processes(limit=5, processes=processes)
        parent_child = process_monitor.get_parent_child_relationships(limit=15, processes=processes)
        startup_items = startup_monitor.get_startup_programs()
        connections = network_monitor.get_active_connections(limit=50)
        suspicious_ports = network_monitor.get_suspicious_port_connections()
        security_status = behavior_monitor.get_security_status(processes=processes)

        parent_map = {p["pid"]: p["name"] for p in processes}
        evaluation = risk_engine.evaluate_system(
            processes=processes,
            connections=connections,
            startup_items=startup_items,
            parent_child_map=parent_map,
        )

        try:
            alert_service.process_threat_evaluation(evaluation)
        except Exception as e:
            logger.debug(f"Alert service notice: {e}")

        snapshot = {
            "metrics": metrics,
            "processes": processes,
            "top_processes": top_processes,
            "parent_child": parent_child,
            "startup_items": startup_items,
            "connections": connections,
            "suspicious_ports": suspicious_ports,
            "security_status": security_status,
            "evaluation": evaluation,
        }

        with self._lock:
            self._cached_metrics = metrics
            self._cached_processes = processes
            self._cached_top_processes = top_processes
            self._cached_parent_child = parent_child
            self._cached_startup_items = startup_items
            self._cached_connections = connections
            self._cached_suspicious_ports = suspicious_ports
            self._cached_security_status = security_status
            self._cached_evaluation = evaluation
            self._latest_snapshot = dict(snapshot)

        return snapshot

    def _worker_loop(self):
        """Background worker executing tiered telemetry collection to prevent high CPU."""
        last_metric_time = 0.0
        last_process_time = 0.0
        last_deep_time = 0.0
        last_prune_time = time.time()

        # Immediate initial collect on startup
        try:
            self._full_collect_sync()
            now = time.time()
            last_metric_time = now
            last_process_time = now
            last_deep_time = now
        except Exception as e:
            logger.error(f"Initial worker collection failed: {e}")

        while not self._stop_event.is_set():
            try:
                now = time.time()

                # Tier 1: High-frequency metrics (CPU, RAM, Disk, Network IO)
                if now - last_metric_time >= self.metrics_interval:
                    m = system_monitor.get_system_metrics()
                    try:
                        db.insert_system_metric(
                            cpu_percent=m["cpu_percent"],
                            memory_percent=m["memory_percent"],
                            disk_percent=m["disk_percent"],
                            process_count=m["total_processes"],
                            bytes_sent=m["bytes_sent"],
                            bytes_recv=m["bytes_recv"],
                            timestamp=m["timestamp"],
                        )
                    except Exception:
                        pass
                    with self._lock:
                        self._cached_metrics = m
                    last_metric_time = now

                # Tier 2: Low-frequency deep scan (Startup items & Security status)
                if now - last_deep_time >= self.deep_scan_interval:
                    items = startup_monitor.get_startup_programs()
                    sec = behavior_monitor.get_security_status(processes=self._cached_processes)
                    with self._lock:
                        self._cached_startup_items = items
                        self._cached_security_status = sec
                    last_deep_time = now

                # Tier 3: Medium-frequency (Processes, sockets, risk evaluation)
                if now - last_process_time >= self.process_interval:
                    procs = process_monitor.get_all_processes()
                    top_procs = process_monitor.get_top_cpu_processes(limit=5, processes=procs)
                    pc = process_monitor.get_parent_child_relationships(limit=15, processes=procs)
                    conns = network_monitor.get_active_connections(limit=50)
                    susp = network_monitor.get_suspicious_port_connections()

                    parent_map = {p["pid"]: p["name"] for p in procs}
                    eval_res = risk_engine.evaluate_system(
                        processes=procs,
                        connections=conns,
                        startup_items=self._cached_startup_items,
                        parent_child_map=parent_map,
                    )
                    try:
                        alert_service.process_threat_evaluation(eval_res)
                    except Exception:
                        pass

                    with self._lock:
                        self._cached_processes = procs
                        self._cached_top_processes = top_procs
                        self._cached_parent_child = pc
                        self._cached_connections = conns
                        self._cached_suspicious_ports = susp
                        self._cached_evaluation = eval_res
                    last_process_time = now

                # Tier 4: Database Maintenance
                if now - last_prune_time >= self.prune_interval:
                    try:
                        db.prune_old_data()
                    except Exception:
                        pass
                    last_prune_time = now

                # Compose snapshot in lock
                with self._lock:
                    self._latest_snapshot = {
                        "metrics": self._cached_metrics,
                        "processes": self._cached_processes,
                        "top_processes": self._cached_top_processes,
                        "parent_child": self._cached_parent_child,
                        "startup_items": self._cached_startup_items,
                        "connections": self._cached_connections,
                        "suspicious_ports": self._cached_suspicious_ports,
                        "security_status": self._cached_security_status,
                        "evaluation": self._cached_evaluation,
                    }

            except Exception as e:
                logger.error(f"Error in background telemetry collector loop: {e}")

            # Wait briefly without hogging CPU
            self._stop_event.wait(timeout=0.5)

    def collect_and_evaluate(self, force: bool = False) -> Dict[str, Any]:
        """
        Retrieves the latest telemetry snapshot.
        If force=False, returns the instantaneous cached state from the background collector.
        If force=True, forces an immediate synchronous refresh.
        """
        if force:
            return self._full_collect_sync()

        # Ensure background worker is active
        if self._worker_thread is None or not self._worker_thread.is_alive():
            self.start()

        with self._lock:
            if self._latest_snapshot is not None:
                return dict(self._latest_snapshot)

        # If no snapshot yet, perform initial collection
        return self._full_collect_sync()

    def get_latest_data(self) -> Dict[str, Any]:
        """Convenience alias for retrieving cached snapshot."""
        return self.collect_and_evaluate(force=False)


# Singleton instance
monitoring_service = MonitoringService()
