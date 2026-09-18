"""
AI-RAT-Detection-Dashboard - Tables & Modular Panels Component
Renders the grid panels matching the layout of the visual reference,
utilizing centralized Nerd Font icons and theme CSS variables.
"""

import streamlit as st
from typing import List, Dict, Any
from ui.icons import get_icon, icon_html
from utils.formatting import get_severity_badge_html, get_risk_badge_html, get_risk_color


def render_top_processes_card(top_processes: List[Dict[str, Any]]):
    """Renders the Top Active Processes table card."""
    rows_html = ""
    for p in top_processes[:5]:
        pname = p.get("name", "unknown")
        pid = p.get("pid", 0)
        cpu = p.get("cpu_percent", 0.0)
        mem = p.get("memory_percent", 0.0)
        rows_html += f"<tr><td class='accent-blue' style='font-weight:600;'>{pname}</td><td>{pid}</td><td>{cpu}%</td><td>{mem}%</td></tr>"

    proc_icon = icon_html("process", extra_classes="accent-blue")
    html = (
        "<div class='cyber-card' style='min-height: 250px;'>"
        f"<div class='card-title'>{proc_icon} Top Active Processes</div>"
        "<div class='card-subtitle'>Real-time list of the most CPU-intensive processes</div>"
        "<table class='cyber-table'>"
        "<thead><tr><th style='width:38%;'>Process</th><th style='width:20%;'>PID</th><th style='width:21%;'>CPU (%)</th><th style='width:21%;'>Memory (%)</th></tr></thead>"
        f"<tbody>{rows_html}</tbody>"
        "</table>"
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def render_startup_programs_card(startup_items: List[Dict[str, Any]]):
    """Renders the Startup Programs table card."""
    rows_html = ""
    display_items = startup_items[:5] if startup_items else [{"name": "No startup programs found", "location": "N/A"}]
    for item in display_items:
        name = item.get("name", "")[:28]
        loc = item.get("location", "")
        rows_html += f"<tr><td class='accent-purple' style='font-weight:500;'>{name}</td><td style='color:var(--text-muted); font-size:0.7rem;'>{loc}</td></tr>"

    startup_icon = icon_html("startup", extra_classes="accent-purple")
    html = (
        "<div class='cyber-card' style='min-height: 250px;'>"
        f"<div class='card-title'>{startup_icon} Startup Programs</div>"
        "<div class='card-subtitle'>Applications configured to launch automatically when system starts</div>"
        "<table class='cyber-table'>"
        "<thead><tr><th style='width:45%;'>Startup Program</th><th style='width:55%;'>Location</th></tr></thead>"
        f"<tbody>{rows_html}</tbody>"
        "</table>"
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def render_parent_child_card(relationships: List[Dict[str, Any]]):
    """Renders the Parent-Child Process Relationship table card."""
    rows_html = ""
    display_rels = relationships[:5] if relationships else [{"parent_name": "explorer.exe", "child_name": "System", "child_pid": 0}]
    for r in display_rels:
        p_name = r.get("parent_name", "unknown")
        c_name = r.get("child_name", "unknown")
        c_pid = r.get("child_pid", 0)
        rows_html += f"<tr><td style='color:var(--text-muted);'>{p_name}</td><td class='accent-yellow' style='font-weight:500;'>{c_name}</td><td>{c_pid}</td></tr>"

    users_icon = icon_html("parent_child", extra_classes="accent-yellow")
    html = (
        "<div class='cyber-card' style='min-height: 250px;'>"
        f"<div class='card-title'>{users_icon} Parent-Child Process Relationship</div>"
        "<div class='card-subtitle'>Shows which processes launched other processes</div>"
        "<table class='cyber-table'>"
        "<thead><tr><th style='width:40%;'>Parent Process</th><th style='width:40%;'>Child Process</th><th style='width:20%;'>PID</th></tr></thead>"
        f"<tbody>{rows_html}</tbody>"
        "</table>"
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def render_active_connections_card(connections: List[Dict[str, Any]]):
    """Renders the Active Network Connections table card."""
    rows_html = ""
    display_conns = connections[:5] if connections else [{"local_address": "0.0.0.0:0", "remote_address": "0.0.0.0:0", "status": "NONE"}]
    for c in display_conns:
        laddr = c.get("local_address", "")
        raddr = c.get("remote_address", "")
        status = c.get("status", "")
        status_color = "var(--accent-green)" if status == "ESTABLISHED" else "var(--text-muted)"
        rows_html += f"<tr><td>{laddr}</td><td>{raddr}</td><td style='color:{status_color}; font-weight:600;'>{status}</td></tr>"

    net_icon = icon_html("network", extra_classes="accent-blue")
    html = (
        "<div class='cyber-card' style='min-height: 250px;'>"
        f"<div class='card-title'>{net_icon} Active Network Connections</div>"
        "<div class='card-subtitle'>Current inbound and outbound network connections</div>"
        "<table class='cyber-table'>"
        "<thead><tr><th style='width:40%;'>Local Address</th><th style='width:40%;'>Remote Address</th><th style='width:20%;'>Status</th></tr></thead>"
        f"<tbody>{rows_html}</tbody>"
        "</table>"
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def render_suspicious_ports_card(suspicious_ports: List[Dict[str, Any]]):
    """Renders the Suspicious Port Detection table card."""
    if suspicious_ports:
        rows_html = ""
        for sp in suspicious_ports[:5]:
            port = sp.get("port")
            proc = sp.get("process")
            risk = sp.get("risk_level", "HIGH")
            color = get_risk_color(risk)
            rows_html += f"<tr><td class='accent-red' style='font-weight:700;'>{port}</td><td>{proc}</td><td><span style='color:{color}; font-weight:600;'>{risk}</span></td></tr>"
    else:
        check_icon = icon_html("check", extra_styles="color:var(--accent-green); margin-right:4px;")
        rows_html = f"<tr><td colspan='3' style='text-align:center; color:var(--accent-green); padding: 18px 0;'>{check_icon} No active sockets bound to known high-risk RAT ports</td></tr>"

    warn_icon = icon_html("warning", extra_classes="accent-red")
    html = (
        "<div class='cyber-card' style='min-height: 250px;'>"
        f"<div class='card-title'>{warn_icon} Suspicious Port Detection</div>"
        "<div class='card-subtitle'>Identifies commonly abused ports for RAT communication</div>"
        "<table class='cyber-table'>"
        "<thead><tr><th style='width:25%;'>Port</th><th style='width:45%;'>Process</th><th style='width:30%;'>Risk Level</th></tr></thead>"
        f"<tbody>{rows_html}</tbody>"
        "</table>"
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def render_security_status_card(security_status: Dict[str, Any]):
    """Renders the Security Status sensor indicators."""
    items = [
        (f"{icon_html('camera', extra_classes='accent-blue')} Camera Detection", security_status.get("camera", {})),
        (f"{icon_html('microphone', extra_classes='accent-purple')} Microphone Detection", security_status.get("microphone", {})),
        (f"{icon_html('screen', extra_classes='accent-yellow')} Screen Recording Detection", security_status.get("screen", {})),
        (f"{icon_html('remote', extra_classes='accent-red')} Remote Access Detection", security_status.get("remote", {})),
    ]

    rows_html = ""
    for label, info in items:
        status_text = info.get("status", "No suspicious activity")
        is_active = info.get("is_active", False)
        badge_cls = "badge-risk" if is_active else "badge-safe"
        icon_badge = icon_html("warning" if is_active else "check", extra_styles="font-size:0.75rem;")
        rows_html += (
            "<div class='sec-item-row'>"
            f"<span class='sec-item-label'>{label}</span>"
            f"<span class='{badge_cls}'>{icon_badge} {status_text}</span>"
            "</div>"
        )

    shield_icon = icon_html("shield", extra_classes="accent-green")
    html = (
        "<div class='cyber-card' style='min-height: 250px;'>"
        f"<div class='card-title'>{shield_icon} Security Status</div>"
        "<div class='card-subtitle'>Defensive sensor telemetry and access indicators</div>"
        f"{rows_html}"
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def render_ai_prediction_card(evaluation: Dict[str, Any]):
    """Renders the AI / Behavioral Risk Prediction card with circular gauge badge."""
    score = evaluation.get("risk_score", 8)
    headline = evaluation.get("headline", "System is Safe")
    detail = evaluation.get("status_detail", "No RAT activity detected")
    is_safe = evaluation.get("is_safe", True)

    score_color = get_risk_color(evaluation.get("threat_level", "LOW"))
    status_icon = icon_html("shield_check" if is_safe else "warning", extra_styles=f"font-size: 2.2rem; color: {'var(--accent-green)' if is_safe else 'var(--accent-red)'};")
    headline_color = "var(--accent-green)" if is_safe else "var(--accent-red)"
    brain_icon = icon_html("brain", extra_classes="accent-purple")

    html = (
        "<div class='cyber-card' style='min-height: 185px;'>"
        f"<div class='card-title'>{brain_icon} AI Prediction & Risk Analysis</div>"
        "<div class='card-subtitle'>Rule-based behavioral threat inference engine</div>"
        "<div style='display: flex; justify-content: space-between; align-items: center; margin-top: 15px;'>"
        "<div style='display: flex; align-items: center; gap: 14px;'>"
        f"<div>{status_icon}</div>"
        "<div>"
        f"<div style='font-size: 1.15rem; font-weight: 700; color: {headline_color};'>{headline}</div>"
        f"<div style='font-size: 0.78rem; color: var(--text-muted); margin-top: 2px;'>{detail}</div>"
        "</div>"
        "</div>"
        "<div style='text-align: center;'>"
        "<div style='font-size: 0.72rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase;'>Risk Score</div>"
        f"<div style='width: 65px; height: 65px; border-radius: 50%; border: 3px solid {score_color}; display: flex; align-items: center; justify-content: center; font-family: \"JetBrainsMono Nerd Font\", \"JetBrains Mono\", monospace; font-size: 1.25rem; font-weight: 700; color: {score_color}; margin-top: 4px; box-shadow: 0 0 12px {score_color}33;'>{score}%</div>"
        "</div>"
        "</div>"
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def render_event_timeline_card(recent_events: List[Dict[str, Any]]):
    """Renders the Event Timeline table card."""
    rows_html = ""
    display_events = recent_events[:5] if recent_events else [
        {"timestamp": "Just now", "description": "System monitoring cycle normal", "severity": "INFO"}
    ]
    for ev in display_events:
        ts = ev.get("timestamp", "")[-8:]
        desc = ev.get("description", "")[:35]
        sev = ev.get("severity", "INFO")
        badge = get_severity_badge_html(sev)
        rows_html += f"<tr><td style='color:var(--text-muted); font-size:0.72rem;'>{ts}</td><td style='color:var(--text-primary);'>{desc}</td><td>{badge}</td></tr>"

    time_icon = icon_html("time", extra_classes="accent-blue")
    html = (
        "<div class='cyber-card' style='min-height: 185px;'>"
        f"<div class='card-title'>{time_icon} Event Timeline</div>"
        "<div class='card-subtitle'>Recent security events and alerts</div>"
        "<table class='cyber-table'>"
        "<thead><tr><th style='width:25%;'>Time</th><th style='width:50%;'>Event</th><th style='width:25%;'>Severity</th></tr></thead>"
        f"<tbody>{rows_html}</tbody>"
        "</table>"
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def render_ai_recommendations_card(recommendations: List[str]):
    """Renders the AI & Defensive Recommendations card."""
    recs = recommendations if recommendations else [
        "Keep your system updated with latest patches",
        "Avoid unknown email attachments and links",
        "Monitor startup programs regularly",
        "Use a firewall for added network protection",
        "Perform periodic full system antimalware scans",
    ]
    items_html = ""
    check_glyph = icon_html("check", extra_styles="color: var(--accent-green); font-weight: bold; margin-right: 6px;")
    for r in recs[:5]:
        items_html += (
            "<div class='rec-item'>"
            f"{check_glyph}"
            f"<span>{r}</span>"
            "</div>"
        )

    lightbulb_icon = icon_html("lightbulb", extra_classes="accent-yellow")
    html = (
        "<div class='cyber-card' style='min-height: 185px;'>"
        f"<div class='card-title'>{lightbulb_icon} AI Recommendations</div>"
        "<div class='card-subtitle'>Contextual defensive hardening actions</div>"
        f"<div style='margin-top: 10px;'>{items_html}</div>"
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)
