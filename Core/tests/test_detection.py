"""
Unit tests for Detection Rules and Risk Engine
"""

import pytest
from detection.rules import RULES
from detection.process_analyzer import ProcessAnalyzer
from detection.network_analyzer import NetworkAnalyzer
from detection.risk_engine import RiskEngine


def test_clean_process_analysis():
    analyzer = ProcessAnalyzer()
    proc = {
        "pid": 100,
        "name": "notepad.exe",
        "cpu_percent": 1.0,
        "memory_percent": 0.5,
        "exe_path": r"C:\Windows\System32\notepad.exe",
    }
    result = analyzer.analyze_process(proc, parent_name="explorer.exe")
    assert result["risk_score"] == 0
    assert result["risk_level"] == "LOW"
    assert len(result["reasons"]) == 0


def test_suspicious_path_detection():
    analyzer = ProcessAnalyzer()
    proc = {
        "pid": 200,
        "name": "updater.exe",
        "cpu_percent": 5.0,
        "memory_percent": 2.0,
        "exe_path": r"C:\Users\Alice\AppData\Local\Temp\updater.exe",
    }
    result = analyzer.analyze_process(proc, parent_name="explorer.exe")
    assert result["risk_score"] >= 30
    assert any("Temp" in r for r in result["reasons"])


def test_suspicious_parent_child_spawn():
    analyzer = ProcessAnalyzer()
    proc = {
        "pid": 300,
        "name": "powershell.exe",
        "cpu_percent": 2.0,
        "memory_percent": 1.5,
        "exe_path": r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
    }
    result = analyzer.analyze_process(proc, parent_name="winword.exe")
    assert result["risk_score"] >= 40
    assert any("spawn" in r.lower() for r in result["reasons"])


def test_network_suspicious_ports():
    net_analyzer = NetworkAnalyzer()
    connections = [
        {
            "pid": 500,
            "process_name": "nc.exe",
            "local_port": 4444,
            "remote_port": 0,
            "local_address": "0.0.0.0:4444",
            "remote_address": "0.0.0.0:0",
            "status": "LISTEN",
        },
        {
            "pid": 600,
            "process_name": "chrome.exe",
            "local_port": 54321,
            "remote_port": 443,
            "local_address": "192.168.1.10:54321",
            "remote_address": "142.250.190.46:443",
            "status": "ESTABLISHED",
        },
    ]
    res = net_analyzer.analyze_connections(connections)
    assert res["network_risk_score"] > 0
    assert len(res["flagged_connections"]) == 1
    assert res["flagged_connections"][0]["port"] == 4444


def test_risk_engine_evaluation():
    engine = RiskEngine()
    procs = [
        {
            "pid": 100,
            "name": "clean.exe",
            "cpu_percent": 2.0,
            "memory_percent": 1.0,
            "exe_path": r"C:\Program Files\App\clean.exe",
            "parent_pid": 10,
        }
    ]
    conns = []
    startup = []
    eval_res = engine.evaluate_system(procs, conns, startup)
    assert "risk_score" in eval_res
    assert "threat_level" in eval_res
    assert eval_res["threat_level"] in ("LOW", "MEDIUM", "HIGH", "CRITICAL")
    assert len(eval_res["recommendations"]) > 0


def test_risk_engine_prediction_interface():
    engine = RiskEngine()
    pred = engine.predict({"composite_risk": 85})
    assert pred["predicted_risk_score"] == 85
    assert pred["predicted_level"] == "CRITICAL"
