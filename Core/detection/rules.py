"""
AI-RAT-Detection-Dashboard - Detection Rules
Formal definitions for behavioral heuristics, risk weights, and severity classifications.
"""

from typing import Dict, Any, List

RULES = {
    "SUSPICIOUS_PATH": {
        "id": "RULE_001",
        "name": "Executable in Suspicious Path",
        "weight": 30,
        "severity": "HIGH",
        "description": "Process executable is located in a high-risk directory (e.g. Temp, AppData, Public).",
    },
    "SUSPICIOUS_PORT": {
        "id": "RULE_002",
        "name": "Known RAT / Backdoor Port Usage",
        "weight": 35,
        "severity": "HIGH",
        "description": "Process communicates or listens on a port associated with Metasploit, RATs, or reverse shells.",
    },
    "ANOMALOUS_SPAWN": {
        "id": "RULE_003",
        "name": "Suspicious Parent-Child Process Chain",
        "weight": 40,
        "severity": "CRITICAL",
        "description": "A shell or scripting interpreter was spawned by an unexpected parent (e.g. Word, Excel, svchost).",
    },
    "RESOURCE_SPIKE": {
        "id": "RULE_004",
        "name": "Abnormal Process Resource Consumption",
        "weight": 15,
        "severity": "MEDIUM",
        "description": "Process is consuming abnormally high CPU or RAM (> 80%).",
    },
    "MULTIPLE_OUTBOUND": {
        "id": "RULE_005",
        "name": "High Outbound Connection Burst",
        "weight": 25,
        "severity": "MEDIUM",
        "description": "Single process holds an unusually high number of active external network connections.",
    },
    "PERSISTENCE_STARTUP": {
        "id": "RULE_006",
        "name": "Suspicious Startup Persistence",
        "weight": 35,
        "severity": "HIGH",
        "description": "Auto-start entry points to an executable in temporary or user-writable locations.",
    },
    "REMOTE_ACCESS_ACTIVE": {
        "id": "RULE_007",
        "name": "Active Remote Access Software",
        "weight": 20,
        "severity": "MEDIUM",
        "description": "A known remote administration or screen sharing tool is currently running.",
    },
}
