"""
AI-RAT-Detection-Dashboard - Sidebar Navigation Component
Renders sidebar navigation, brand logo, operational status, and global controls
utilizing centralized Nerd Font icons and modular themes.
"""

import streamlit as st
from config.config import APP_VERSION, load_settings, save_settings
from utils.permissions import is_admin
from ui.icons import get_icon, icon_html
from ui.themes.manager import (
    get_theme,
    get_theme_names_list,
    get_key_from_display_name,
    normalize_theme_key,
)

# Icon mapping for main navigation menu
NAV_ICONS = {
    "Dashboard": "dashboard",
    "Live Monitor": "pulse",
    "Process Analysis": "process",
    "Network Monitor": "network",
    "Security Tools": "shield",
    "Event Logs": "history",
    "Reports": "report",
    "Settings": "settings",
}


def render_sidebar() -> str:
    """Renders the modular SOC sidebar and returns the selected navigation view."""
    with st.sidebar:
        # 1. Branding Header
        shield_icon = icon_html("shield", extra_styles="font-size: 1.35rem; color: #ffffff;")
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:1.5rem; padding: 0 4px;">
                <div style="
                    background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
                    width: 40px; height: 40px; border-radius: 9px;
                    display: flex; align-items: center; justify-content: center;
                    box-shadow: 0 0 14px rgba(56, 189, 248, 0.35);
                ">
                    {shield_icon}
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

        # 2. Admin Privilege Badge
        admin_mode = is_admin()
        if admin_mode:
            badge_icon = icon_html("admin", extra_styles="font-size:0.85rem;")
            badge_text = f"{badge_icon} Elevated (Admin)"
            badge_color = "var(--accent-green)"
        else:
            badge_icon = icon_html("warning", extra_styles="font-size:0.85rem;")
            badge_text = f"{badge_icon} Standard User"
            badge_color = "var(--accent-yellow)"

        st.markdown(
            f"""
            <div style="
                background: var(--card-bg); border: 1px solid var(--card-border);
                border-radius: 6px; padding: 6px 10px; margin-bottom: 1.2rem;
                font-size: 0.75rem; color: {badge_color}; font-weight: 600;
                display: flex; justify-content: space-between; align-items: center;
            ">
                <span style="color:var(--text-secondary);">Privilege Mode</span>
                <span style="display:flex; align-items:center; gap:5px;">{badge_text}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 3. Navigation Menu with Nerd Font Icons
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

        def format_nav_item(item: str) -> str:
            icon_key = NAV_ICONS.get(item, "circle")
            glyph = get_icon(icon_key)
            return f"{glyph}  {item}"

        query_page = st.query_params.get("page")
        if query_page:
            clean_qp = query_page.lower().replace("_", " ").strip()
            for opt in menu_options:
                if opt.lower().strip() == clean_qp:
                    if st.session_state.get("main_nav_radio") != opt:
                        st.session_state["main_nav_radio"] = opt
                    break

        selected_page = st.radio(
            "Navigation",
            options=menu_options,
            format_func=format_nav_item,
            label_visibility="collapsed",
            key="main_nav_radio",
        )

        st.markdown("<hr style='border-color: var(--sidebar-border); margin: 1rem 0 0.8rem 0;'>", unsafe_allow_html=True)

        # 4. Advanced Grouped Theme Selector
        theme_names = get_theme_names_list()
        current_theme_key = normalize_theme_key(st.session_state.get("theme", "cyber_dark"))
        current_theme_tokens = get_theme(current_theme_key)
        current_display_name = current_theme_tokens.name

        theme_idx = theme_names.index(current_display_name) if current_display_name in theme_names else 0

        def on_theme_change():
            chosen_name = st.session_state.get("ui_theme_selector", "Cyber Dark")
            new_key = get_key_from_display_name(chosen_name)
            st.session_state["theme"] = new_key
            cfg = load_settings()
            cfg["theme"] = new_key
            save_settings(cfg)

        palette_icon = icon_html("palette", extra_styles="color:var(--accent-blue); font-size:0.95rem; margin-right:6px;")
        st.markdown(
            f"""
            <div style="font-size:0.82rem; font-weight:600; color:var(--text-secondary); margin-bottom:4px; display:flex; align-items:center;">
                {palette_icon} UI Theme
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.selectbox(
            "UI Theme",
            options=theme_names,
            index=theme_idx,
            key="ui_theme_selector",
            on_change=on_theme_change,
            label_visibility="collapsed",
            help="Switch between Dark (Catppuccin, Dracula, Nord, Cyber) and Light (White Slur, Gruvbox, Windows XP, Classic) themes",
        )

        # 5. Live Feed Toggle
        bolt_glyph = get_icon("bolt")
        st.toggle(f"{bolt_glyph} Live Auto-Refresh", key="setting_auto_refresh_enabled", help="Toggle background telemetry updates")

        st.markdown("<hr style='border-color: var(--sidebar-border); margin: 0.8rem 0 1rem 0;'>", unsafe_allow_html=True)

        # 6. Bottom System Status Indicator
        status_dot = icon_html("dot", extra_styles="color:var(--accent-green); font-size:0.65rem;")
        st.markdown(
            f"""
            <div style="padding: 0 4px;">
                <div style="display:flex; align-items:center; gap:8px; font-size:0.82rem; color:var(--accent-green); font-weight:600;">
                    {status_dot} AI Protection Active
                </div>
                <div style="font-size:0.72rem; color:var(--text-muted); margin-top:4px;">
                    Engine: Rule-Based Behavioral v{APP_VERSION}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return selected_page
