"""
AI-RAT-Detection-Dashboard - Process Analyzer
Evaluates process metadata against behavioral heuristics and calculates forensic risk.
"""

from typing import Dict, Any, List, Tuple
from config.config import SUSPICIOUS_PATHS, SUSPICIOUS_SPAWNS, KNOWN_REMOTE_TOOLS
from detection.rules import RULES


class ProcessAnalyzer:
    """Performs deep heuristic and behavioral analysis on individual processes."""

    def analyze_process(
        self,
        process: Dict[str, Any],
        parent_name: str = "",
    ) -> Dict[str, Any]:
        """
        Analyzes a process dictionary and computes risk score and detailed reasons.
        """
        score = 0
        reasons = []
        rule_hits = []

        name = process.get("name", "").lower()
        exe = process.get("exe_path", "")
        cpu = process.get("cpu_percent", 0.0)
        mem = process.get("memory_percent", 0.0)

        # 1. Suspicious Path Check
        if exe and exe != "[Access Denied]":
            for sp in SUSPICIOUS_PATHS:
                if sp.lower() in exe.lower():
                    rule = RULES["SUSPICIOUS_PATH"]
                    score += rule["weight"]
                    reasons.append(f"Executable running from high-risk directory: {sp}")
                    rule_hits.append(rule["name"])
                    break

        # 2. Resource Spike Check
        if cpu > 80.0 or mem > 80.0:
            rule = RULES["RESOURCE_SPIKE"]
            score += rule["weight"]
            reasons.append(f"Abnormally high resource utilization (CPU: {cpu}%, RAM: {mem}%)")
            rule_hits.append(rule["name"])

        # 3. Suspicious Parent-Child Spawn Check
        if parent_name:
            p_clean = parent_name.lower()
            if p_clean in SUSPICIOUS_SPAWNS:
                bad_children = SUSPICIOUS_SPAWNS[p_clean]
                if any(child.lower() in name for child in bad_children):
                    rule = RULES["ANOMALOUS_SPAWN"]
                    score += rule["weight"]
                    reasons.append(f"Suspicious spawn: {name} launched by {parent_name}")
                    rule_hits.append(rule["name"])

        # 4. Known Remote Tool Check
        if any(rt.lower() in name for rt in KNOWN_REMOTE_TOOLS):
            rule = RULES["REMOTE_ACCESS_ACTIVE"]
            score += rule["weight"]
            reasons.append(f"Remote administration software detected: {name}")
            rule_hits.append(rule["name"])

        # Cap score at 100
        final_score = min(100, max(0, score))
        risk_level = self.classify_risk_score(final_score)

        return {
            "pid": process.get("pid"),
            "name": process.get("name"),
            "cpu_percent": cpu,
            "memory_percent": mem,
            "exe_path": exe,
            "risk_score": final_score,
            "risk_level": risk_level,
            "reasons": reasons,
            "rule_hits": rule_hits,
        }

    @staticmethod
    def classify_risk_score(score: int) -> str:
        """Classify numerical risk score into standard risk tier."""
        if score >= 75:
            return "CRITICAL"
        elif score >= 50:
            return "HIGH"
        elif score >= 25:
            return "MEDIUM"
        else:
            return "LOW"


# Singleton instance
process_analyzer = ProcessAnalyzer()
