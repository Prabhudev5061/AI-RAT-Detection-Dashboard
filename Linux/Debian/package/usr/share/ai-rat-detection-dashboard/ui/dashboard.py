"""
AI-RAT-Detection-Dashboard - Dashboard & Subpage Views
Implements each navigation page with rich, interactive, real-time cyber security components
utilizing centralized Nerd Font icons and modular themes.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, List

from config.config import APP_TITLE, APP_SUBTITLE, APP_VERSION, load_settings, save_settings
from database.database import db
from ui.icons import get_icon, icon_html
from ui.themes.manager import (
    get_theme,
    get_theme_names_list,
    get_key_from_display_name,
    normalize_theme_key,
)
from ui.cards import render_metric_cards
from ui.charts import render_history_charts
from ui.tables import (
    render_top_processes_card,
    render_startup_programs_card,
    render_parent_child_card,
    render_active_connections_card,
    render_suspicious_ports_card,
    render_security_status_card,
    render_ai_prediction_card,
    render_event_timeline_card,
    render_ai_recommendations_card,
)
from services.report_service import report_service
from utils.formatting import get_severity_badge_html, get_risk_badge_html


def render_dashboard_header(last_updated: str, refresh_interval: int):
    """Renders the top title banner and status pills matching the reference image."""
    shield_glyph = icon_html("shield", extra_classes="dashboard-header-shield-icon", extra_styles="font-size:1.35rem;")
    clock_glyph = icon_html("clock", extra_classes="accent-blue", extra_styles="font-size:0.85rem;")
    dot_glyph = icon_html("dot", extra_styles="color:var(--badge-safe-text); font-size:0.65rem;")
    st.markdown(
        f"""
        <div class="dashboard-header-container">
            <div class="dashboard-header-banner">
                <div class="dashboard-header-title-box">
                    <span class="dashboard-header-shield">{shield_glyph}</span>
                    <span class="dashboard-header-title">{APP_TITLE}</span>
                </div>
                <div class="dashboard-header-status-box">
                    <div class="dashboard-pill-updated">
                        {clock_glyph} Last Updated: <b class="dashboard-pill-time">{last_updated}</b>
                    </div>
                    <div class="dashboard-pill-active">
                        {dot_glyph} AI Engine Active | {refresh_interval}s
                    </div>
                </div>
            </div>
            <div class="dashboard-header-subtitle">
                {APP_SUBTITLE}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard_view(data: Dict[str, Any], recent_metrics: List[Dict[str, Any]], refresh_interval: int):
    """Renders the primary SOC overview dashboard matching reference image."""
    metrics = data.get("metrics", {})
    render_dashboard_header(metrics.get("timestamp", ""), refresh_interval)

    # Historical data series for sparklines and charts
    cpu_history = [m.get("cpu_percent", 0.0) for m in recent_metrics]
    ram_history = [m.get("memory_percent", 0.0) for m in recent_metrics]
    disk_history = [m.get("disk_percent", 0.0) for m in recent_metrics]
    proc_history = [m.get("process_count", 0) for m in recent_metrics]

    # Row 1: Top 4 Metric Cards with Sparklines
    render_metric_cards(metrics, cpu_history, ram_history, disk_history, proc_history)

    # Row 2: 4 Telemetry History Charts
    render_history_charts(recent_metrics)

    # Row 3: 3 Middle Panels (Top Processes, Startup Programs, Parent-Child)
    col1, col2, col3 = st.columns(3)
    with col1:
        render_top_processes_card(data.get("top_processes", []))
    with col2:
        render_startup_programs_card(data.get("startup_items", []))
    with col3:
        render_parent_child_card(data.get("parent_child", []))

    # Row 4: 3 Network & Sensor Panels (Active Conns, Suspicious Ports, Security Status)
    col4, col5, col6 = st.columns(3)
    with col4:
        render_active_connections_card(data.get("connections", []))
    with col5:
        render_suspicious_ports_card(data.get("suspicious_ports", []))
    with col6:
        render_security_status_card(data.get("security_status", {}))

    # Row 5: 3 Bottom Panels (AI Prediction, Event Timeline, Recommendations)
    col7, col8, col9 = st.columns(3)
    with col7:
        render_ai_prediction_card(data.get("evaluation", {}))
    with col8:
        recent_events = db.get_recent_events(limit=5)
        render_event_timeline_card(recent_events)
    with col9:
        render_ai_recommendations_card(data.get("evaluation", {}).get("recommendations", []))


def render_live_monitor_view(data: Dict[str, Any], recent_metrics: List[Dict[str, Any]]):
    """Detailed high-frequency hardware and system live monitoring view."""
    bolt_glyph = get_icon("bolt")
    st.markdown(f"### {bolt_glyph} Live System & Resource Telemetry")
    st.markdown("Real-time streaming telemetry with bandwidth throughput and resource allocation.")

    metrics = data.get("metrics", {})
    user_info = metrics.get("user_info", {})

    c1, c2, c3 = st.columns(3)
    c1.metric("Current User", user_info.get("username", "Unknown"))
    c2.metric("Host Machine", user_info.get("machine_name", "LocalHost"))
    c3.metric("Privilege Status", "Administrator" if user_info.get("is_admin") else "Standard User")

    st.markdown("---")
    render_history_charts(recent_metrics)

    st.markdown("#### Hardware Resource Breakdown")
    col1, col2, col3 = st.columns(3)
    gpu = metrics.get("gpu", {})

    with col1:
        ram_icon = icon_html("memory", extra_classes="accent-purple")
        st.markdown(
            f"""
            <div class="cyber-card">
                <div class="card-title">{ram_icon} RAM Memory Allocation</div>
                <div style="margin-top:10px; font-family:'JetBrainsMono Nerd Font', 'JetBrains Mono', monospace; font-size:0.85rem;">
                    <div>Used: <b>{metrics.get('memory_used', 0) / (1024**3):.2f} GB</b></div>
                    <div>Total: <b>{metrics.get('memory_total', 0) / (1024**3):.2f} GB</b></div>
                    <div>Percentage: <b>{metrics.get('memory_percent', 0)}%</b></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        disk_icon = icon_html("disk", extra_classes="accent-yellow")
        st.markdown(
            f"""
            <div class="cyber-card">
                <div class="card-title">{disk_icon} Primary Storage Allocation</div>
                <div style="margin-top:10px; font-family:'JetBrainsMono Nerd Font', 'JetBrains Mono', monospace; font-size:0.85rem;">
                    <div>Used: <b>{metrics.get('disk_used', 0) / (1024**3):.2f} GB</b></div>
                    <div>Total: <b>{metrics.get('disk_total', 0) / (1024**3):.2f} GB</b></div>
                    <div>Percentage: <b>{metrics.get('disk_percent', 0)}%</b></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        gpu_avail = gpu.get("available", False)
        gpu_name = gpu.get("name", "Integrated Display Adapter")
        gpu_util = gpu.get("utilization_percent", 0.0)
        gpu_driver = gpu.get("driver_version", "N/A")
        gpu_mem_used = gpu.get("memory_used_mb", 0.0)
        gpu_mem_total = gpu.get("memory_total_mb", 0.0)

        gpu_status_html = (
            f"<div>Model: <b>{gpu_name}</b></div>"
            f"<div>Load: <b>{gpu_util}%</b></div>"
            f"<div>VRAM: <b>{gpu_mem_used:.0f} / {gpu_mem_total:.0f} MB</b></div>"
            f"<div>Driver: <b>{gpu_driver}</b></div>"
            if gpu_avail
            else f"<div>Model: <b>{gpu_name}</b></div><div>Status: <b>Standard / Integrated Graphics</b></div><div>Driver: <b>System Default</b></div>"
        )
        gpu_icon = icon_html("gpu", extra_classes="accent-blue")
        st.markdown(
            f"""
            <div class="cyber-card">
                <div class="card-title">{gpu_icon} GPU Graphics Telemetry</div>
                <div style="margin-top:10px; font-family:'JetBrainsMono Nerd Font', 'JetBrains Mono', monospace; font-size:0.85rem;">
                    {gpu_status_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_process_analysis_view(data: Dict[str, Any]):
    """Detailed process inventory and forensic analysis view."""
    search_glyph = get_icon("search")
    st.markdown(f"### {search_glyph} Process Behavioral Analysis")
    st.markdown("Audits running executables, identifies anomalous execution paths, and evaluates risk.")

    processes = data.get("processes", [])
    flagged = data.get("evaluation", {}).get("flagged_processes", [])

    if flagged:
        warn_glyph = get_icon("warning")
        st.warning(f"{warn_glyph} {len(flagged)} process(es) flagged with elevated risk indicators.")
        flagged_df = pd.DataFrame(flagged)[["pid", "name", "risk_score", "risk_level", "reasons"]]
        st.dataframe(flagged_df, use_container_width=True)

    st.markdown("#### Active Processes Directory")
    search_term = st.text_input("Filter by Process Name or PID", "", placeholder="e.g. chrome, python, 1234")

    filtered = processes
    if search_term:
        term = search_term.lower()
        filtered = [
            p for p in processes
            if term in p.get("name", "").lower() or term in str(p.get("pid", ""))
        ]

    df = pd.DataFrame(filtered)
    if not df.empty:
        df_display = df[["pid", "name", "cpu_percent", "memory_percent", "status", "exe_path"]]
        st.dataframe(df_display, use_container_width=True, height=450)
    else:
        st.info("No matching processes found.")


def render_network_monitor_view(data: Dict[str, Any]):
    """Deep network socket auditing view."""
    net_glyph = get_icon("network")
    st.markdown(f"### {net_glyph} Network Socket & Connection Auditing")
    st.markdown("Surfaces all active TCP and UDP sockets with correlated process identifiers.")

    conns = data.get("connections", [])
    suspicious = data.get("suspicious_ports", [])

    if suspicious:
        alert_glyph = get_icon("warning")
        st.error(f"{alert_glyph} {len(suspicious)} connection(s) associated with known suspicious/RAT ports!")
        st.dataframe(pd.DataFrame(suspicious), use_container_width=True)

    st.markdown("#### Active Sockets Table")
    state_filter = st.selectbox("Filter by Socket State", ["ALL", "ESTABLISHED", "LISTEN", "TIME_WAIT", "CLOSE_WAIT"])

    filtered_conns = conns
    if state_filter != "ALL":
        filtered_conns = [c for c in conns if c.get("status") == state_filter]

    if filtered_conns:
        df_conns = pd.DataFrame(filtered_conns)[
            ["pid", "process_name", "protocol", "local_address", "remote_address", "status"]
        ]
        st.dataframe(df_conns, use_container_width=True, height=450)
    else:
        st.info("No connections match the selected filter.")


def render_security_tools_view(data: Dict[str, Any]):
    """Defensive security tools and diagnostic audits."""
    shield_glyph = get_icon("shield")
    st.markdown(f"### {shield_glyph} Defensive Security Tools & Diagnostic Audit")
    st.markdown("Specialized inspection tools for host hardening, registry startup, and privilege validation.")

    t1, t2, t3 = st.tabs(["Startup Programs Audit", "Sensor Privacy Telemetry", "Host Diagnostics"])

    with t1:
        st.markdown("#### Autostart & Registry Run Entries")
        startup_items = data.get("startup_items", [])
        if startup_items:
            st.dataframe(pd.DataFrame(startup_items), use_container_width=True)
        else:
            st.info("No autostart applications detected.")

    with t2:
        st.markdown("#### Hardware Access Auditing")
        sec_status = data.get("security_status", {})
        render_security_status_card(sec_status)

    with t3:
        st.markdown("#### System Integrity Diagnostics")
        metrics = data.get("metrics", {})
        user_info = metrics.get("user_info", {})
        st.json({
            "Host Name": user_info.get("machine_name"),
            "Current User": user_info.get("username"),
            "Elevation Level": "Admin" if user_info.get("is_admin") else "Standard",
            "Total Active PIDs": metrics.get("total_processes"),
            "Database Records": len(db.get_recent_metrics(100)),
        })


def render_event_logs_view(data: Dict[str, Any]):
    """Historical security events and audit log view."""
    history_glyph = get_icon("history")
    st.markdown(f"### {history_glyph} Security Audit & Event Logs")
    st.markdown("Chronological forensic event log stored in local SQLite database.")

    col1, col2 = st.columns([2, 1])
    with col1:
        sev_filter = st.selectbox("Filter Severity", ["ALL", "INFO", "WARNING", "HIGH", "CRITICAL"])
    with col2:
        log_limit = st.slider("Max Events", 10, 200, 50)

    filter_sev = None if sev_filter == "ALL" else sev_filter
    events = db.get_recent_events(limit=log_limit, min_severity=filter_sev)

    if events:
        df_events = pd.DataFrame(events)[["timestamp", "severity", "event_type", "description", "source", "pid", "ip", "port"]]
        st.dataframe(df_events, use_container_width=True, height=500)
    else:
        st.info("No security events match the current filter.")


def render_reports_view(data: Dict[str, Any]):
    """Export and reporting center for CSV and PDF reports."""
    report_glyph = get_icon("report")
    st.markdown(f"### {report_glyph} Forensic Reports & Data Exports")
    st.markdown("Export comprehensive telemetry dumps and formatted executive PDF reports.")

    col1, col2 = st.columns(2)

    with col1:
        pdf_icon = icon_html("file", extra_classes="accent-blue")
        st.markdown(
            f"""
            <div class="cyber-card">
                <div class="card-title">{pdf_icon} Executive PDF Security Report</div>
                <div class="card-subtitle">Formatted PDF report with threat scoring, process lists, and audit findings.</div>
            """,
            unsafe_allow_html=True,
        )
        dl_glyph = get_icon("download")
        if st.button(f"{get_icon('file')} Generate Executive PDF Report", key="btn_gen_pdf"):
            with st.spinner("Compiling PDF report..."):
                pdf_path = report_service.generate_pdf_report(data)
                with open(pdf_path, "rb") as f:
                    pdf_bytes = f.read()
                st.session_state["last_generated_pdf"] = {
                    "name": pdf_path.name,
                    "bytes": pdf_bytes,
                }
                st.success(f"{get_icon('success')} Report compiled successfully: {pdf_path.name}")

        if "last_generated_pdf" in st.session_state:
            st.download_button(
                label=f"{dl_glyph} Download {st.session_state['last_generated_pdf']['name']}",
                data=st.session_state["last_generated_pdf"]["bytes"],
                file_name=st.session_state["last_generated_pdf"]["name"],
                mime="application/pdf",
                key="download_pdf_btn",
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        folder_icon = icon_html("folder", extra_classes="accent-purple")
        st.markdown(
            f"""
            <div class="cyber-card">
                <div class="card-title">{folder_icon} Raw Data CSV Exports</div>
                <div class="card-subtitle">Export telemetry and event log tables in standard CSV format.</div>
            """,
            unsafe_allow_html=True,
        )
        csv_metrics = report_service.generate_csv_metrics()
        st.download_button(
            label=f"{dl_glyph} Export Metrics History (CSV)",
            data=csv_metrics,
            file_name="system_metrics_export.csv",
            mime="text/csv",
            key="btn_dl_csv_metrics",
        )

        csv_events = report_service.generate_csv_events()
        st.download_button(
            label=f"{dl_glyph} Export Event Logs (CSV)",
            data=csv_events,
            file_name="security_events_export.csv",
            mime="text/csv",
            key="btn_dl_csv_events",
        )
        st.markdown("</div>", unsafe_allow_html=True)


def render_settings_view():
    """Application configuration and maintenance settings."""
    settings_glyph = get_icon("settings")
    st.markdown(f"### {settings_glyph} Application Settings & Configuration")
    st.markdown("Tune refresh parameters, visual themes, detection thresholds, and database maintenance.")

    current_cfg = load_settings()
    col1, col2 = st.columns(2)

    with col1:
        palette_icon = icon_html("palette", extra_classes="accent-blue")
        st.markdown(
            f"""
            <div class="cyber-card">
                <div class="card-title">{palette_icon} Appearance & Interface</div>
            """,
            unsafe_allow_html=True,
        )
        theme_names = get_theme_names_list()
        current_theme_key = normalize_theme_key(st.session_state.get("theme", current_cfg.get("theme", "cyber_dark")))
        current_display = get_theme(current_theme_key).name
        theme_idx = theme_names.index(current_display) if current_display in theme_names else 0

        selected_display_theme = st.selectbox(
            "Display Theme Mode",
            options=theme_names,
            index=theme_idx,
            key="settings_theme_select",
            help="Choose between Dark themes (Catppuccin, Dracula, Nord, Cyber) and Light themes (White Slur, Gruvbox, Windows XP, Classic)",
        )

        clock_icon = icon_html("clock", extra_classes="accent-yellow")
        st.markdown(f"<br><div class='card-title'>{clock_icon} Monitoring Parameters</div>", unsafe_allow_html=True)
        current_interval = int(st.session_state.get("setting_refresh_interval", current_cfg.get("refresh_interval", 5)))
        intervals = [3, 5, 10, 15, 30]
        interval_idx = intervals.index(current_interval) if current_interval in intervals else 1

        selected_interval = st.selectbox(
            "Auto Refresh Interval (Seconds)",
            options=intervals,
            index=interval_idx,
            key="settings_interval_select",
        )
        enable_net = st.checkbox(
            "Enable Background Network Socket Correlator",
            value=current_cfg.get("enable_net", True),
            key="settings_enable_net",
        )
        enable_startup = st.checkbox(
            "Enable Startup Registry & File Auditing",
            value=current_cfg.get("enable_startup", True),
            key="settings_enable_startup",
        )

        save_glyph = get_icon("save")
        if st.button(f"{save_glyph} Save Preferences", key="btn_save_settings"):
            new_theme_key = get_key_from_display_name(selected_display_theme)
            st.session_state["theme"] = new_theme_key
            st.session_state["setting_refresh_interval"] = selected_interval
            st.session_state["setting_enable_net"] = enable_net
            st.session_state["setting_enable_startup"] = enable_startup
            save_settings({
                "theme": new_theme_key,
                "refresh_interval": selected_interval,
                "auto_refresh_enabled": st.session_state.get("setting_auto_refresh_enabled", True),
                "enable_net": enable_net,
                "enable_startup": enable_startup,
            })
            success_glyph = get_icon("success")
            st.success(f"{success_glyph} Preferences saved successfully! Theme and parameters updated.")
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        db_icon = icon_html("database", extra_classes="accent-purple")
        st.markdown(
            f"""
            <div class="cyber-card">
                <div class="card-title">{db_icon} Database & Storage Maintenance</div>
            """,
            unsafe_allow_html=True,
        )
        st.write(f"SQLite Database File: `{db.db_path}`")
        st.write(f"Application Version: `v{APP_VERSION}`")
        st.write("JetBrains Mono Nerd Font: `Bundled Offline (Base64)`")

        broom_glyph = get_icon("broom")
        if st.button(f"{broom_glyph} Prune Historical Database Records", key="btn_prune_db"):
            db.prune_old_data(max_records=500)
            st.success(f"{get_icon('success')} Database pruned to latest 500 records.")
        st.markdown("</div>", unsafe_allow_html=True)

    from platforms import platform_adapter
    info_icon = icon_html("info", extra_classes="accent-blue")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="cyber-card">
            <div class="card-title">{info_icon} About AI RAT Detection Dashboard</div>
            <div style="margin-top: 10px; font-size: 0.85rem; line-height: 1.6;">
                <div><b>Application:</b> AI RAT Detection Dashboard</div>
                <div><b>Version:</b> v{APP_VERSION} (Production Release)</div>
                <div><b>Active Platform:</b> {platform_adapter.platform_name.capitalize()} Platform Adapter</div>
                <div><b>Architecture:</b> Unified Master Core with Decoupled Background Telemetry</div>
                <div><b>Typography:</b> JetBrains Mono Nerd Font (100% Offline Embedded Base64)</div>
                <div><b>Theme Modes:</b> 8 Complete Palettes (Dark: Catppuccin, Dracula, Nord, Cyber | Light: White Slur, Gruvbox, Windows XP, Classic)</div>
                <div style="margin-top: 8px; color: var(--text-muted); font-size: 0.78rem;">
                    Engineered for cross-platform defensive cyber security telemetry, anomaly detection, and RAT behavioral forensics.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
