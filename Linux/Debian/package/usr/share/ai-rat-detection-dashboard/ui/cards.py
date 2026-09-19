"""
AI-RAT-Detection-Dashboard - Top Metric Cards Component
Renders the 4 primary telemetry summary cards with integrated Plotly sparklines
and centralized Nerd Font icons adhering to the active theme tokens.
"""

import streamlit as st
import plotly.graph_objects as go
from typing import List
from ui.icons import icon_html
from ui.themes.manager import get_theme


def create_sparkline(data_points: List[float], color: str) -> go.Figure:
    """Generates a sleek, minimal sparkline figure for card visualization."""
    fig = go.Figure()
    if not data_points:
        data_points = [0.0]

    # Fill area under sparkline with translucent gradient
    # Safe hex-to-rgba converter
    clean_hex = color.lstrip("#")
    try:
        if len(clean_hex) == 6:
            r, g, b = tuple(int(clean_hex[i:i+2], 16) for i in (0, 2, 4))
            fill_color = f"rgba({r}, {g}, {b}, 0.18)"
        else:
            fill_color = "rgba(56, 189, 248, 0.18)"
    except Exception:
        fill_color = "rgba(56, 189, 248, 0.18)"

    fig.add_trace(go.Scatter(
        y=data_points,
        mode="lines",
        line=dict(color=color, width=2.2, shape="spline"),
        fill="tozeroy",
        fillcolor=fill_color,
        hoverinfo="skip",
    ))

    fig.update_layout(
        height=45,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False, fixedrange=True),
        yaxis=dict(visible=False, fixedrange=True),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def render_metric_cards(
    metrics: dict,
    cpu_history: List[float],
    ram_history: List[float],
    disk_history: List[float],
    proc_history: List[float],
):
    """Renders the four top summary cards: CPU, RAM, Disk, Total Processes."""
    col1, col2, col3, col4 = st.columns(4)
    active_theme = st.session_state.get("theme", "cyber_dark")
    tokens = get_theme(active_theme)

    c_blue = tokens.accent_blue
    c_purple = tokens.accent_purple
    c_yellow = tokens.accent_yellow
    c_green = tokens.accent_green

    # 1. CPU Usage
    with col1:
        cpu_val = metrics.get("cpu_percent", 0.0)
        cpu_icon = icon_html("cpu", extra_classes="accent-blue", extra_styles="font-size:1.1rem;")
        st.markdown(
            f"""
            <div class="cyber-card" style="margin-bottom: 0px;">
                <div class="card-title-row">
                    <span class="card-title">{cpu_icon} CPU Usage</span>
                </div>
                <div class="metric-big-val accent-blue">{cpu_val}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        fig_cpu = create_sparkline(cpu_history[-15:], c_blue)
        st.plotly_chart(fig_cpu, use_container_width=True, config={"displayModeBar": False})

    # 2. RAM Usage
    with col2:
        ram_val = metrics.get("memory_percent", 0.0)
        ram_icon = icon_html("memory", extra_classes="accent-purple", extra_styles="font-size:1.1rem;")
        st.markdown(
            f"""
            <div class="cyber-card" style="margin-bottom: 0px;">
                <div class="card-title-row">
                    <span class="card-title">{ram_icon} RAM Usage</span>
                </div>
                <div class="metric-big-val accent-purple">{ram_val}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        fig_ram = create_sparkline(ram_history[-15:], c_purple)
        st.plotly_chart(fig_ram, use_container_width=True, config={"displayModeBar": False})

    # 3. Disk Usage
    with col3:
        disk_val = metrics.get("disk_percent", 0.0)
        disk_icon = icon_html("disk", extra_classes="accent-yellow", extra_styles="font-size:1.1rem;")
        st.markdown(
            f"""
            <div class="cyber-card" style="margin-bottom: 0px;">
                <div class="card-title-row">
                    <span class="card-title">{disk_icon} Disk Usage</span>
                </div>
                <div class="metric-big-val accent-yellow">{disk_val}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        fig_disk = create_sparkline(disk_history[-15:], c_yellow)
        st.plotly_chart(fig_disk, use_container_width=True, config={"displayModeBar": False})

    # 4. Total Processes
    with col4:
        proc_val = metrics.get("total_processes", 0)
        proc_icon = icon_html("process", extra_classes="accent-green", extra_styles="font-size:1.1rem;")
        st.markdown(
            f"""
            <div class="cyber-card" style="margin-bottom: 0px;">
                <div class="card-title-row">
                    <span class="card-title">{proc_icon} Total Processes</span>
                </div>
                <div class="metric-big-val accent-green">{proc_val}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        fig_proc = create_sparkline(proc_history[-15:], c_green)
        st.plotly_chart(fig_proc, use_container_width=True, config={"displayModeBar": False})
