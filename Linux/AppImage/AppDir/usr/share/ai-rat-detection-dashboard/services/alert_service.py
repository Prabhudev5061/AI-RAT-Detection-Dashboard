"""
AI-RAT-Detection-Dashboard - Alert Service
State-based alert generation with cooldowns to prevent notification floods.
"""

import time
from typing import Dict, Any, List, Optional
from database.database import db
from services.logging_service import log_event


class AlertService:
    """Manages active alert states, deduplication, and alert cooldowns."""

    def __init__(self, cooldown_seconds: int = 60):
        self.cooldown_seconds = cooldown_seconds
        # Mapping: alert_key -> timestamp of last fired alert
        self._last_alerted: Dict[str, float] = {}

    def process_threat_evaluation(self, evaluation: Dict[str, Any]):
        """
        Takes the output of RiskEngine.evaluate_system and generates
        alerts for high-risk findings if cooldown has expired.
        """
        now = time.time()
        score = evaluation.get("risk_score", 0)
        level = evaluation.get("threat_level", "LOW")

        # 1. Process alerts
        for proc in evaluation.get("flagged_processes", []):
            pid = proc.get("pid")
            name = proc.get("name")
            p_score = proc.get("risk_score", 0)
            p_level = proc.get("risk_level", "LOW")

            if p_score >= 25:
                for rule_hit in proc.get("rule_hits", []):
                    alert_key = f"proc_{pid}_{rule_hit}"
                    last_time = self._last_alerted.get(alert_key, 0)
                    if now - last_time > self.cooldown_seconds:
                        self._last_alerted[alert_key] = now
                        desc = f"{name} (PID: {pid}) triggered {rule_hit}. Reasons: {'; '.join(proc.get('reasons', []))}"
                        db.insert_alert(
                            rule_name=rule_hit,
                            description=desc,
                            severity=p_level,
                            risk_score=p_score,
                            pid=pid,
                            process_name=name,
                        )
                        log_event(
                            event_type="THREAT_ALERT",
                            description=desc,
                            severity=p_level,
                            source="ProcessAnalyzer",
                            pid=pid,
                        )

        # 2. Network alerts
        for conn in evaluation.get("flagged_connections", []):
            port = conn.get("port")
            proc = conn.get("process")
            pid = conn.get("pid")
            alert_key = f"net_{pid}_{port}"
            last_time = self._last_alerted.get(alert_key, 0)
            if now - last_time > self.cooldown_seconds:
                self._last_alerted[alert_key] = now
                desc = f"Connection to suspicious port {port} ({conn.get('description')}) by {proc} (PID: {pid})"
                db.insert_alert(
                    rule_name="Known RAT / Backdoor Port Usage",
                    description=desc,
                    severity=conn.get("risk_level", "HIGH"),
                    risk_score=70,
                    pid=pid,
                    process_name=proc,
                )
                log_event(
                    event_type="NETWORK_ALERT",
                    description=desc,
                    severity=conn.get("risk_level", "HIGH"),
                    source="NetworkAnalyzer",
                    pid=pid,
                    port=port,
                )

        # Clean old cooldown entries periodically
        if len(self._last_alerted) > 1000:
            self._last_alerted = {
                k: v for k, v in self._last_alerted.items() if now - v < self.cooldown_seconds * 2
            }


# Singleton instance
alert_service = AlertService()
