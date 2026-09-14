"""
AI-RAT-Detection-Dashboard - Network Analyzer
Identifies suspicious communication channels, RAT listeners, and burst connections.
"""

from collections import Counter
from typing import List, Dict, Any
from config.config import SUSPICIOUS_PORTS
from detection.rules import RULES


class NetworkAnalyzer:
    """Evaluates network telemetry against threat rules and connection anomalies."""

    def analyze_connections(self, connections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Scans a batch of active connections for suspicious ports and burst patterns.
        """
        flagged_conns = []
        rule_hits = []
        overall_net_score = 0

        # Count outbound connections per PID
        outbound_counts = Counter()
        for c in connections:
            if c.get("remote_ip") and c.get("status") == "ESTABLISHED":
                outbound_counts[c.get("pid")] += 1

        # Check for multiple outbound burst rule
        for pid, count in outbound_counts.items():
            if count >= 10:
                rule = RULES["MULTIPLE_OUTBOUND"]
                overall_net_score += rule["weight"]
                rule_hits.append(f"{rule['name']} (PID {pid}: {count} sockets)")

        # Port checks
        for c in connections:
            l_port = c.get("local_port", 0)
            r_port = c.get("remote_port", 0)
            flagged_port = None

            if l_port in SUSPICIOUS_PORTS:
                flagged_port = l_port
            elif r_port in SUSPICIOUS_PORTS:
                flagged_port = r_port

            if flagged_port:
                desc, risk = SUSPICIOUS_PORTS[flagged_port]
                weight = RULES["SUSPICIOUS_PORT"]["weight"]
                overall_net_score += weight
                rule_hits.append(f"Suspicious port {flagged_port} ({desc}) on {c.get('process_name')}")

                flagged_conns.append({
                    "port": flagged_port,
                    "process": c.get("process_name", "Unknown"),
                    "pid": c.get("pid"),
                    "local_address": c.get("local_address"),
                    "remote_address": c.get("remote_address"),
                    "status": c.get("status"),
                    "description": desc,
                    "risk_level": risk,
                })

        final_score = min(100, overall_net_score)

        return {
            "network_risk_score": final_score,
            "flagged_connections": flagged_conns,
            "rule_hits": list(set(rule_hits)),
        }


# Singleton instance
network_analyzer = NetworkAnalyzer()
