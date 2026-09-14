"""
AI RAT Detection & System Network Monitoring Dashboard
Main Streamlit Application Entrypoint.
"""

import streamlit as st
from config.config import APP_TITLE, DEFAULT_REFRESH_INTERVAL, load_settings
from database.database import db
from services.monitoring_service import monitoring_service
from ui.styles import get_theme_css
from ui.sidebar import render_sidebar
from ui.dashboard import (
    render_dashboard_view,
    render_live_monitor_view,
    render_process_analysis_view,
    render_network_monitor_view,
    render_security_tools_view,
    render_event_logs_view,
    render_reports_view,
    render_settings_view,
)

# 1. Page Configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Load Persisted Settings & Inject Custom CSS
if "settings_loaded" not in st.session_state:
    saved_cfg = load_settings()
    st.session_state["theme"] = saved_cfg.get("theme", "dark")
    st.session_state["refresh_interval"] = saved_cfg.get("refresh_interval", DEFAULT_REFRESH_INTERVAL)
    st.session_state["setting_auto_refresh_enabled"] = saved_cfg.get("auto_refresh_enabled", True)
    st.session_state["settings_loaded"] = True
    monitoring_service.start()

active_theme = st.session_state.get("theme", "dark")
st.markdown(get_theme_css(active_theme), unsafe_allow_html=True)

# 3. Render Navigation Sidebar
selected_page = render_sidebar()

refresh_sec = st.session_state.get("setting_refresh_interval", st.session_state.get("refresh_interval", DEFAULT_REFRESH_INTERVAL))
auto_refresh_active = st.session_state.get("setting_auto_refresh_enabled", True)

# 4. Main View Routing
@st.fragment(run_every=5)
def live_telemetry_fragment(page: str):
    """Fragment-based live updates for Dashboard and Live Monitor."""
    data = monitoring_service.collect_and_evaluate()
    recent_metrics = db.get_recent_metrics(limit=50)

    if page == "Dashboard":
        render_dashboard_view(data, recent_metrics, refresh_sec)
    elif page == "Live Monitor":
        render_live_monitor_view(data, recent_metrics)


def static_view_container(page: str):
    """Direct rendering for interactive pages to prevent auto-refresh from interrupting inputs."""
    data = monitoring_service.collect_and_evaluate()

    if page == "Process Analysis":
        render_process_analysis_view(data)
    elif page == "Network Monitor":
        render_network_monitor_view(data)
    elif page == "Security Tools":
        render_security_tools_view(data)
    elif page == "Event Logs":
        render_event_logs_view(data)
    elif page == "Reports":
        render_reports_view(data)
    elif page == "Settings":
        render_settings_view()


if selected_page in ("Dashboard", "Live Monitor"):
    if auto_refresh_active:
        live_telemetry_fragment(selected_page)
    else:
        data = monitoring_service.collect_and_evaluate()
        recent_metrics = db.get_recent_metrics(limit=50)
        if selected_page == "Dashboard":
            render_dashboard_view(data, recent_metrics, refresh_sec)
        else:
            render_live_monitor_view(data, recent_metrics)
else:
    static_view_container(selected_page)
