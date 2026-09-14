"""
AI-RAT-Detection-Dashboard - Network Monitor
Collects active network sockets, correlates PIDs, and audits open ports.
"""

import socket
import psutil
from typing import List, Dict, Any, Tuple
from config.config import SUSPICIOUS_PORTS


class NetworkMonitor:
    """Monitors TCP and UDP network connections and maps active communication channels."""

    def __init__(self):
        self._proc_cache: Dict[int, str] = {}

    def _get_process_name(self, pid: int) -> str:
        if not pid:
            return "System / Idle"
        if pid in self._proc_cache:
            return self._proc_cache[pid]
        try:
            name = psutil.Process(pid).name()
            # Bound cache size
            if len(self._proc_cache) > 1000:
                self._proc_cache.clear()
            self._proc_cache[pid] = name
            return name
        except Exception:
            return "Unknown"

    def get_active_connections(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Retrieves active network connections correlated with PIDs and process names.
        """
        connections = []
        try:
            # Query connections defensively (inet = IPv4 + IPv6, TCP and UDP)
            net_conns = psutil.net_connections(kind="inet")
        except (psutil.AccessDenied, PermissionError):
            # Non-admin users on Windows may get access denied on global net_connections
            return []
        except Exception:
            return []

        for conn in net_conns:
            try:
                protocol = "TCP" if conn.type == socket.SOCK_STREAM else "UDP"
                laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "0.0.0.0:0"
                local_port = conn.laddr.port if conn.laddr else 0
                raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "0.0.0.0:0"
                remote_ip = conn.raddr.ip if conn.raddr else ""
                remote_port = conn.raddr.port if conn.raddr else 0
                status = conn.status or ("LISTEN" if not conn.raddr else "ESTABLISHED")
                pid = conn.pid or 0
                pname = self._get_process_name(pid)

                connections.append({
                    "pid": pid,
                    "process_name": pname,
                    "protocol": protocol,
                    "local_address": laddr,
                    "local_port": local_port,
                    "remote_address": raddr,
                    "remote_ip": remote_ip,
                    "remote_port": remote_port,
                    "status": status,
                })
            except Exception:
                continue

        # Sort so that ESTABLISHED / active connections come first
        connections.sort(key=lambda x: (x["status"] != "ESTABLISHED", x["pid"] == 0))
        return connections[:limit]

    def get_suspicious_port_connections(self) -> List[Dict[str, Any]]:
        """
        Finds active connections that bind or connect to known suspicious / RAT ports.
        """
        active = self.get_active_connections(limit=200)
        flagged = []

        for conn in active:
            l_port = conn["local_port"]
            r_port = conn["remote_port"]

            matched_port = None
            if l_port in SUSPICIOUS_PORTS:
                matched_port = l_port
            elif r_port in SUSPICIOUS_PORTS:
                matched_port = r_port

            if matched_port:
                description, risk_level = SUSPICIOUS_PORTS[matched_port]
                flagged.append({
                    "port": matched_port,
                    "process": conn["process_name"],
                    "pid": conn["pid"],
                    "risk_level": risk_level,
                    "description": description,
                    "local_address": conn["local_address"],
                    "remote_address": conn["remote_address"],
                    "status": conn["status"],
                })

        return flagged


# Singleton instance
network_monitor = NetworkMonitor()
