"""
AI-RAT-Detection-Dashboard - Dashboard & Subpage Views
Implements each navigation page with rich, interactive, real-time cyber security components.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, List

from config.config import APP_TITLE, APP_SUBTITLE, APP_VERSION, load_settings, save_settings
from database.database import db
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
    col_title, col_status = st.columns([3, 2])
    with col_title:
        st.markdown(
            f"""
            <div style="margin-bottom: 1.2rem;">
                <h2 style="margin:0; font-size:1.65rem; font-weight:800; color:#f8fafc; letter-spacing:-0.5px;">
                    {APP_TITLE}
                </h2>
                <div style="font-size:0.82rem; color:#94a3b8; margin-top:2px;">
                    {APP_SUBTITLE}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_status:
        st.markdown(
            f"""
            <div style="display:flex; justify-content:flex-end; align-items:center; gap:12px; margin-top:6px;">
                <div style="
                    background:#111827; border:1px solid #1f293d; border-radius:8px;
                    padding:6px 12px; font-size:0.75rem; color:#94a3b8; font-family:'JetBrains Mono', monospace;
                ">
                    ðŸ•’ Last Updated: <b style="color:#cbd5e1;">{last_updated}</b>
                </div>
                <div style="
                    background:rgba(52, 211, 153, 0.12); border:1px solid rgba(52, 211, 153, 0.3);
                    border-radius:8px; padding:6px 12px; font-size:0.75rem; color:#34d399; font-weight:600;
                ">
                    ðŸŸ¢ AI Engine Active | {refresh_interval}s
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
    st.markdown("### âš¡ Live System & Resource Telemetry")
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
    drive_label = metrics.get("drive_label", "System Drive")

    with col1:
        st.markdown(
            f"""
            <div class="cyber-card">
                <div class="card-title">ðŸ’¾ RAM Memory Allocation</div>
                <div style="margin-top:10px; font-family:'JetBrains Mono', monospace; font-size:0.85rem;">
                    <div>Used: <b>{metrics.get('memory_used', 0) / (1024**3):.2f} GB</b></div>
                    <div>Total: <b>{metrics.get('memory_total', 0) / (1024**3):.2f} GB</b></div>
                    <div>Percentage: <b>{metrics.get('memory_percent', 0)}%</b></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="cyber-card">
                <div class="card-title">ðŸ—„ï¸ Primary Storage Allocation</div>
                <div style="margin-top:10px; font-family:'JetBrains Mono', monospace; font-size:0.85rem;">
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
        st.markdown(
            f"""
            <div class="cyber-card">
                <div class="card-title">ðŸŽ® GPU Graphics Telemetry</div>
                <div style="margin-top:10px; font-family:'JetBrains Mono', monospace; font-size:0.85rem;">
                    {gpu_status_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_process_analysis_view(data: Dict[str, Any]):
    """Detailed process inventory and forensic analysis view."""
    st.markdown("### ðŸ” Process Behavioral Analysis")
    st.markdown("Audits running executables, identifies anomalous execution paths, and evaluates risk.")

    processes = data.get("processes", [])
    flagged = data.get("evaluation", {}).get("flagged_processes", [])

    if flagged:
        st.warning(f"âš ï¸ {len(flagged)} process(es) flagged with elevated risk indicators.")
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
    st.markdown("### ðŸŒ Network Socket & Connection Auditing")
    st.markdown("Surfaces all active TCP and UDP sockets with correlated process identifiers.")

    conns = data.get("connections", [])
    suspicious = data.get("suspicious_ports", [])

    if suspicious:
        st.error(f"ðŸš¨ {len(suspicious)} connection(s) associated with known suspicious/RAT ports!")
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
    st.markdown("### ðŸ› ï¸ Defensive Security Tools & Diagnostic Audit")
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
    st.markdown("### ðŸ“œ Security Audit & Event Logs")
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
    st.markdown("### ðŸ“Š Forensic Reports & Data Exports")
    st.markdown("Export comprehensive telemetry dumps and formatted executive PDF reports.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="cyber-card">
                <div class="card-title">ðŸ“„ Executive PDF Security Report</div>
                <div class="card-subtitle">Formatted PDF report with threat scoring, process lists, and audit findings.</div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Generate Executive PDF Report", key="btn_gen_pdf"):
            with st.spinner("Compiling PDF report..."):
                pdf_path = report_service.generate_pdf_report(data)
                with open(pdf_path, "rb") as f:
                    pdf_bytes = f.read()
                st.session_state["last_generated_pdf"] = {
                    "name": pdf_path.name,
                    "bytes": pdf_bytes,
                }
                st.success(f"Report compiled successfully: {pdf_path.name}")

        if "last_generated_pdf" in st.session_state:
            st.download_button(
                label=f"â¬‡ï¸ Download {st.session_state['last_generated_pdf']['name']}",
                data=st.session_state["last_generated_pdf"]["bytes"],
                file_name=st.session_state["last_generated_pdf"]["name"],
                mime="application/pdf",
                key="download_pdf_btn",
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(
            """
            <div class="cyber-card">
                <div class="card-title">ðŸ“ Raw Data CSV Exports</div>
                <div class="card-subtitle">Export telemetry and event log tables in standard CSV format.</div>
            """,
            unsafe_allow_html=True,
        )
        csv_metrics = report_service.generate_csv_metrics()
        st.download_button(
            label="â¬‡ï¸ Export Metrics History (CSV)",
            data=csv_metrics,
            file_name="system_metrics_export.csv",
            mime="text/csv",
            key="btn_dl_csv_metrics",
        )

        csv_events = report_service.generate_csv_events()
        st.download_button(
            label="â¬‡ï¸ Export Event Logs (CSV)",
            data=csv_events,
            file_name="security_events_export.csv",
            mime="text/csv",
            key="btn_dl_csv_events",
        )
        st.markdown("</div>", unsafe_allow_html=True)


def render_settings_view():
    """Application configuration and maintenance settings."""
    st.markdown("### âš™ï¸ Application Settings & Configuration")
    st.markdown("Tune refresh parameters, visual themes, detection thresholds, and database maintenance.")

    current_cfg = load_settings()
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="cyber-card">
                <div class="card-title">ðŸŽ¨ Appearance & Interface</div>
            """,
            unsafe_allow_html=True,
        )
        theme_options = ["Dark", "Light", "System"]
        current_theme = st.session_state.get("theme", current_cfg.get("theme", "dark")).capitalize()
        theme_idx = theme_options.index(current_theme) if current_theme in theme_options else 0

        selected_theme = st.selectbox(
            "Display Theme Mode",
            options=theme_options,
            index=theme_idx,
            key="settings_theme_select",
            help="Choose between Dark Cybersecurity SOC, Light Professional, or System default",
        )

        st.markdown("<br><div class='card-title'>â±ï¸ Monitoring Parameters</div>", unsafe_allow_html=True)
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
            "Enable Windows Registry Startup Auditing",
            value=current_cfg.get("enable_startup", True),
            key="settings_enable_startup",
        )

        if st.button("ðŸ’¾ Save Preferences", key="btn_save_settings"):
            new_theme = selected_theme.lower()
            st.session_state["theme"] = new_theme
            st.session_state["setting_refresh_interval"] = selected_interval
            st.session_state["setting_enable_net"] = enable_net
            st.session_state["setting_enable_startup"] = enable_startup
            save_settings({
                "theme": new_theme,
                "refresh_interval": selected_interval,
                "auto_refresh_enabled": st.session_state.get("setting_auto_refresh_enabled", True),
                "enable_net": enable_net,
                "enable_startup": enable_startup,
            })
            st.success("âœ… Preferences saved successfully! Theme and parameters updated.")
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(
            """
            <div class="cyber-card">
                <div class="card-title">ðŸ—„ï¸ Database & Storage Maintenance</div>
            """,
            unsafe_allow_html=True,
        )
        st.write(f"SQLite Database File: `{db.db_path}`")
        st.write(f"Application Version: `v{APP_VERSION}`")
        st.write("JetBrains Mono Font: `Embedded Offline (Base64)`")

        if st.button("ðŸ§¹ Prune Historical Database Records", key="btn_prune_db"):
            db.prune_old_data(max_records=500)
            st.success("Database pruned to latest 500 records.")
        st.markdown("</div>", unsafe_allow_html=True)

    from platforms import platform_adapter
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="cyber-card">
            <div class="card-title">â„¹ï¸ About AI RAT Detection Dashboard</div>
            <div style="margin-top: 10px; font-size: 0.85rem; line-height: 1.6;">
                <div><b>Application:</b> AI RAT Detection Dashboard</div>
                <div><b>Version:</b> v{APP_VERSION} (Production Release)</div>
                <div><b>Active Platform:</b> {platform_adapter.platform_name.capitalize()} Platform Adapter</div>
                <div><b>Architecture:</b> Unified Master Core with Decoupled Background Telemetry</div>
                <div><b>Font Family:</b> JetBrains Mono (100% Offline Embedded Base64)</div>
                <div><b>Theme Modes:</b> Dark (SOC Operations), Light (Professional Day), System Default</div>
                <div style="margin-top: 8px; color: var(--text-muted); font-size: 0.78rem;">
                    Engineered for cross-platform defensive cyber security telemetry, anomaly detection, and RAT behavioral forensics.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

