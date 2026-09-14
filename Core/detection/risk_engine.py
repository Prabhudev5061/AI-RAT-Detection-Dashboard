"""
AI-RAT-Detection-Dashboard - Risk Engine
Aggregates telemetry from process, network, and startup subsystems to compute
an explainable host threat score (0-100) and actionable security recommendations.
"""

from typing import List, Dict, Any, Optional
from detection.rules import RULES
from detection.process_analyzer import process_analyzer
from detection.network_analyzer import network_analyzer
from config.config import SUSPICIOUS_PATHS, RISK_LEVEL_LOW, RISK_LEVEL_MEDIUM, RISK_LEVEL_HIGH, RISK_LEVEL_CRITICAL


class RiskEngine:
    """
    Transparent rule-based behavioral risk engine.
    Calculates unified host threat level with explainable audit trails.
    """

    def __init__(self):
        self.version = "1.0.0 (Rule-Based Behavioral)"

    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Modular prediction interface for current rule engine and future ML model drop-in.
        """
        score = int(features.get("composite_risk", 0))
        level = process_analyzer.classify_risk_score(score)
        return {
            "model_version": self.version,
            "predicted_risk_score": score,
            "predicted_level": level,
        }

    def evaluate_system(
        self,
        processes: List[Dict[str, Any]],
        connections: List[Dict[str, Any]],
        startup_items: List[Dict[str, Any]],
        parent_child_map: Optional[Dict[int, str]] = None,
    ) -> Dict[str, Any]:
        """
        Evaluates full host posture across all behavioral vectors.
        """
        parent_map = parent_child_map or {}
        flagged_processes = []
        all_reasons = []

        # 1. Evaluate Processes
        proc_scores = []
        for p in processes:
            parent_name = parent_map.get(p.get("parent_pid", 0), "")
            res = process_analyzer.analyze_process(p, parent_name=parent_name)
            if res["risk_score"] > 0:
                flagged_processes.append(res)
                all_reasons.extend(res["reasons"])
                proc_scores.append(res["risk_score"])

        highest_proc_score = max(proc_scores) if proc_scores else 0

        # 2. Evaluate Network Connections
        net_res = network_analyzer.analyze_connections(connections)
        net_score = net_res["network_risk_score"]
        if net_res["rule_hits"]:
            all_reasons.extend(net_res["rule_hits"])

        # 3. Evaluate Startup Persistence
        startup_score = 0
        for item in startup_items:
            cmd = item.get("command", "").lower()
            for sp in SUSPICIOUS_PATHS:
                if sp.lower() in cmd:
                    startup_score += RULES["PERSISTENCE_STARTUP"]["weight"]
                    all_reasons.append(f"Suspicious startup persistence: {item.get('name')} in {sp}")
                    break

        # 4. Aggregate Composite Host Risk Score (Bounded 0 - 100)
        # Weighted formula: max process risk + network risk contribution + startup risk contribution
        composite_raw = highest_proc_score * 0.5 + net_score * 0.3 + startup_score * 0.2
        # Minimum baseline risk (clean system idle baseline ~ 5-10% normal variance)
        composite_score = int(min(100, max(5 if not all_reasons else 15, composite_raw)))

        threat_level = process_analyzer.classify_risk_score(composite_score)
        is_safe = composite_score < 50

        # Sort flagged processes by risk descending
        flagged_processes.sort(key=lambda x: x["risk_score"], reverse=True)

        # Generate Actionable Security Recommendations
        recommendations = self._generate_recommendations(composite_score, threat_level, all_reasons)

        headline = "System is Safe" if is_safe else "Potentially Suspicious Activity Detected"
        status_detail = "No RAT activity detected" if is_safe else f"Identified {len(all_reasons)} behavioral risk signals"

        return {
            "risk_score": composite_score,
            "threat_level": threat_level,
            "is_safe": is_safe,
            "headline": headline,
            "status_detail": status_detail,
            "reasons": list(dict.fromkeys(all_reasons)),  # Deduplicate preserving order
            "flagged_processes": flagged_processes[:10],
            "flagged_connections": net_res["flagged_connections"][:10],
            "recommendations": recommendations,
        }

    def _generate_recommendations(
        self,
        risk_score: int,
        threat_level: str,
        reasons: List[str],
    ) -> List[str]:
        """Produce context-aware defensive recommendations."""
        recs = [
            "Keep your operating system and security patches updated",
            "Avoid opening unknown email attachments or suspicious links",
            "Monitor startup programs regularly for unauthorized changes",
            "Ensure the Windows Defender Firewall is active on all profiles",
            "Perform periodic full-system antimalware scans",
        ]

        if any("port" in r.lower() for r in reasons):
            recs.insert(0, "Close unauthorized listening ports and verify firewall outbound rules")
        if any("startup" in r.lower() for r in reasons):
            recs.insert(0, "Audit Registry Run keys and remove unauthorized auto-start entries")
        if threat_level in (RISK_LEVEL_HIGH, RISK_LEVEL_CRITICAL):
            recs.insert(0, "Isolate the host from the local network and inspect flagged PIDs")

        return recs[:5]


# Singleton instance
risk_engine = RiskEngine()
