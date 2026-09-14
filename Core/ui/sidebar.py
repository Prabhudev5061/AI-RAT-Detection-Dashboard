"""
AI-RAT-Detection-Dashboard - Sidebar Navigation Component
Renders sidebar navigation, brand logo, operational status, and global controls.
"""

import streamlit as st
from config.config import APP_VERSION, load_settings, save_settings
from utils.permissions import is_admin


def render_sidebar() -> str:
    """Renders the dark SOC sidebar and returns the selected navigation view."""
    with st.sidebar:
        # Branding Header
        st.markdown(
            """
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:1.5rem; padding: 0 4px;">
                <div style="
                    background: linear-gradient(135deg, #0284c7, #38bdf8);
                    width: 38px; height: 38px; border-radius: 8px;
                    display: flex; align-items: center; justify-content: center;
                    box-shadow: 0 0 14px rgba(56, 189, 248, 0.4);
                    font-size: 1.2rem;
                ">
                    🛡️
                </div>
                <div>
                    <div style="font-weight:700; font-size:1.02rem; color:var(--text-primary); letter-spacing: -0.3px;">
                        AI RAT Detection Dashboard
                    </div>
                    <div style="font-size:0.68rem; color:var(--text-muted);">
                        Real-Time Cyber Security Monitoring
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Admin Badge
        admin_mode = is_admin()
        badge_text = "🛡️ Elevated (Admin)" if admin_mode else "⚠️ Standard User"
        badge_color = "var(--accent-green)" if admin_mode else "var(--accent-yellow)"
        st.markdown(
            f"""
            <div style="
                background: var(--card-bg); border: 1px solid var(--card-border);
                border-radius: 6px; padding: 6px 10px; margin-bottom: 1.2rem;
                font-size: 0.75rem; color: {badge_color}; font-weight: 600;
                display: flex; justify-content: space-between; align-items: center;
            ">
                <span style="color:var(--text-secondary);">Privilege Mode</span>
                <span>{badge_text}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Navigation Menu
        menu_options = [
            "Dashboard",
            "Live Monitor",
            "Process Analysis",
            "Network Monitor",
            "Security Tools",
            "Event Logs",
            "Reports",
            "Settings",
        ]

        selected_page = st.radio(
            "Navigation",
            options=menu_options,
            label_visibility="collapsed",
            key="main_nav_radio",
        )

        st.markdown("<hr style='border-color: var(--sidebar-border); margin: 1rem 0 0.8rem 0;'>", unsafe_allow_html=True)

        # Theme Selector
        theme_options = ["Dark", "Light", "System"]
        current_theme = st.session_state.get("theme", "dark").capitalize()
        theme_idx = theme_options.index(current_theme) if current_theme in theme_options else 0

        def on_theme_change():
            new_val = st.session_state.get("ui_theme_selector", "Dark").lower()
            st.session_state["theme"] = new_val
            cfg = load_settings()
            cfg["theme"] = new_val
            save_settings(cfg)

        st.selectbox(
            "🎨 UI Theme",
            options=theme_options,
            index=theme_idx,
            key="ui_theme_selector",
            on_change=on_theme_change,
            help="Switch between Dark, Light, or System default theme",
        )

        # Live Feed Toggle
        st.toggle("⚡ Live Auto-Refresh", key="setting_auto_refresh_enabled", help="Toggle background telemetry updates")

        st.markdown("<hr style='border-color: var(--sidebar-border); margin: 0.8rem 0 1rem 0;'>", unsafe_allow_html=True)

        # Bottom System Status
        st.markdown(
            f"""
            <div style="padding: 0 4px;">
                <div style="display:flex; align-items:center; gap:8px; font-size:0.82rem; color:#34d399; font-weight:600;">
                    <span style="font-size:0.6rem;">🟢</span> AI Protection Active
                </div>
                <div style="font-size:0.72rem; color:#64748b; margin-top:4px;">
                    Engine: Rule-Based Behavioral v{APP_VERSION}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return selected_page
