"""
AI-RAT-Detection-Dashboard - Process Monitor
Collects running processes, parent-child hierarchies, and resource allocations.
"""

import psutil
import datetime
from typing import List, Dict, Any, Optional


class ProcessMonitor:
    """Monitors running processes and inspects execution hierarchies."""

    def get_all_processes(self) -> List[Dict[str, Any]]:
        """
        Enumerate all active processes defensively.
        Handles AccessDenied, NoSuchProcess, ZombieProcess gracefully.
        """
        processes = []
        for proc in psutil.process_iter(
            ["pid", "name", "cpu_percent", "memory_percent", "exe", "ppid", "create_time", "status"]
        ):
            try:
                info = proc.info
                pid = info.get("pid")
                name = info.get("name") or "Unknown"
                cpu = info.get("cpu_percent") or 0.0
                mem = info.get("memory_percent") or 0.0
                exe = info.get("exe") or "[Access Denied]"
                ppid = info.get("ppid") or 0
                status = info.get("status") or "running"

                try:
                    ctime = datetime.datetime.fromtimestamp(info["create_time"]).strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    ctime = "N/A"

                processes.append({
                    "pid": pid,
                    "name": name,
                    "cpu_percent": round(float(cpu), 1),
                    "memory_percent": round(float(mem), 2),
                    "exe_path": exe,
                    "parent_pid": ppid,
                    "create_time": ctime,
                    "status": status,
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
            except Exception:
                continue

        return processes

    def get_top_cpu_processes(
        self,
        limit: int = 5,
        processes: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """Returns the most CPU-intensive active processes without redundant iteration."""
        procs = list(processes) if processes is not None else self.get_all_processes()
        procs.sort(key=lambda x: x.get("cpu_percent", 0.0), reverse=True)
        return procs[:limit]

    def get_parent_child_relationships(
        self,
        limit: int = 15,
        processes: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Builds parent-child execution pairings without redundant process scans.
        """
        procs = processes if processes is not None else self.get_all_processes()
        pid_map = {p["pid"]: p["name"] for p in procs}

        relationships = []
        for p in procs:
            ppid = p.get("parent_pid")
            if ppid and ppid in pid_map:
                parent_name = pid_map[ppid]
                relationships.append({
                    "parent_name": parent_name,
                    "parent_pid": ppid,
                    "child_name": p["name"],
                    "child_pid": p["pid"],
                    "child_exe": p["exe_path"],
                })

        return relationships[:limit]


# Singleton instance
process_monitor = ProcessMonitor()
