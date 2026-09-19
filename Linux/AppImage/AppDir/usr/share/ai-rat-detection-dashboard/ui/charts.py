"""
AI-RAT-Detection-Dashboard - Telemetry Charts Component
Interactive Plotly charts styled to match all 8 theme palettes with Nerd Font icons.
"""

import streamlit as st
import plotly.graph_objects as go
from typing import List, Dict, Any
from ui.icons import get_icon
from ui.icons import icon_html
from ui.themes.manager import get_plotly_theme_config


def _base_chart_layout(title: str = "", y_title: str = "%", y_range=None, theme: str = "cyber_dark") -> dict:
    """Standardized cybersecurity layout for Plotly charts adapting to all 8 theme palettes."""
    cfg = get_plotly_theme_config(theme)

    top_margin = 35 if title else 10
    layout = dict(
        height=185,
        margin=dict(l=35, r=15, t=top_margin, b=25),
        paper_bgcolor=cfg["bg_color"],
        plot_bgcolor=cfg["bg_color"],
        font=dict(family="JetBrains Mono, monospace", size=10, color=cfg["text_color"]),
        xaxis=dict(
            showgrid=True,
            gridcolor=cfg["grid_color"],
            linecolor=cfg["border_color"],
            tickfont=dict(size=9, color=cfg["text_color"]),
            tickangle=0,
            nticks=6,
            fixedrange=True,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=cfg["grid_color"],
            linecolor=cfg["border_color"],
            tickfont=dict(size=9, color=cfg["text_color"]),
            ticksuffix=y_title if y_title != "KB/s" else "",
            fixedrange=True,
        ),
        showlegend=False,
    )
    if title:
        layout["title"] = dict(
            text=f"<b style='color:{cfg['title_color']}; font-size:13px;'>{title}</b>",
            x=0.02,
            y=0.95,
        )
    if y_range:
        layout["yaxis"]["range"] = y_range
    return layout


def render_history_charts(recent_metrics: List[Dict[str, Any]], theme: str = "cyber_dark"):
    """Renders the 4 history telemetry charts side by side in 4 columns."""
    col1, col2, col3, col4 = st.columns(4)

    active_theme = st.session_state.get("theme", theme)
    cfg = get_plotly_theme_config(active_theme)

    timestamps = []
    for m in recent_metrics:
        ts = str(m.get("timestamp", ""))
        if len(ts) >= 16 and " " in ts:
            timestamps.append(ts.split(" ")[1][:5])
        elif len(ts) >= 8:
            timestamps.append(ts[-8:-3] if ":" in ts[-8:-3] else ts[-5:])
        else:
            timestamps.append(ts or "00:00")
    if not timestamps:
        timestamps = ["00:00"]

    cpu_vals = [m.get("cpu_percent", 0.0) for m in recent_metrics] or [0.0]
    ram_vals = [m.get("memory_percent", 0.0) for m in recent_metrics] or [0.0]
    disk_vals = [m.get("disk_percent", 0.0) for m in recent_metrics] or [0.0]

    # Calculate delta for network rate (KB/s)
    sent_kb = []
    recv_kb = []
    for i in range(len(recent_metrics)):
        if i == 0:
            sent_kb.append(0.0)
            recv_kb.append(0.0)
        else:
            diff_sent = max(0, recent_metrics[i].get("bytes_sent", 0) - recent_metrics[i-1].get("bytes_sent", 0))
            diff_recv = max(0, recent_metrics[i].get("bytes_recv", 0) - recent_metrics[i-1].get("bytes_recv", 0))
            sent_kb.append(round(diff_sent / 1024.0, 1))
            recv_kb.append(round(diff_recv / 1024.0, 1))

    # 1. CPU History
    with col1:
        st.markdown(
            f"""
            <div class="chart-card-header">
                {icon_html('chart_line', extra_styles=f'color:{cfg["accent_blue"]}; font-size:0.92rem;')} CPU Usage History
            </div>
            """,
            unsafe_allow_html=True,
        )
        fig_cpu = go.Figure()
        cpu_color = cfg["accent_blue"]
        fig_cpu.add_trace(go.Scatter(
            x=timestamps,
            y=cpu_vals,
            mode="lines",
            line=dict(color=cpu_color, width=2, shape="spline"),
            fill="tozeroy",
            fillcolor=f"rgba{tuple(list(int(cpu_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + [0.14])}",
        ))
        fig_cpu.update_layout(_base_chart_layout("", "%", [0, 105], theme=active_theme))
        st.plotly_chart(fig_cpu, use_container_width=True, config={"displayModeBar": False})

    # 2. RAM History
    with col2:
        st.markdown(
            f"""
            <div class="chart-card-header">
                {icon_html('chart_bar', extra_styles=f'color:{cfg["accent_purple"]}; font-size:0.92rem;')} RAM Usage History
            </div>
            """,
            unsafe_allow_html=True,
        )
        fig_ram = go.Figure()
        ram_color = cfg["accent_purple"]
        fig_ram.add_trace(go.Scatter(
            x=timestamps,
            y=ram_vals,
            mode="lines",
            line=dict(color=ram_color, width=2, shape="spline"),
            fill="tozeroy",
            fillcolor=f"rgba{tuple(list(int(ram_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + [0.14])}",
        ))
        fig_ram.update_layout(_base_chart_layout("", "%", [0, 105], theme=active_theme))
        st.plotly_chart(fig_ram, use_container_width=True, config={"displayModeBar": False})

    # 3. Disk History
    with col3:
        st.markdown(
            f"""
            <div class="chart-card-header">
                {icon_html('disk', extra_styles=f'color:{cfg["accent_yellow"]}; font-size:0.92rem;')} Disk Usage History
            </div>
            """,
            unsafe_allow_html=True,
        )
        fig_disk = go.Figure()
        disk_color = cfg["accent_yellow"]
        fig_disk.add_trace(go.Scatter(
            x=timestamps,
            y=disk_vals,
            mode="lines",
            line=dict(color=disk_color, width=2, shape="spline"),
            fill="tozeroy",
            fillcolor=f"rgba{tuple(list(int(disk_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + [0.14])}",
        ))
        fig_disk.update_layout(_base_chart_layout("", "%", [0, 105], theme=active_theme))
        st.plotly_chart(fig_disk, use_container_width=True, config={"displayModeBar": False})

    # 4. Network History
    with col4:
        st.markdown(
            f"""
            <div class="chart-card-header">
                {icon_html('network', extra_styles=f'color:{cfg["accent_blue"]}; font-size:0.92rem;')} Network Usage (KB/s)
            </div>
            """,
            unsafe_allow_html=True,
        )
        fig_net = go.Figure()
        net_sent_color = cfg["accent"]
        net_recv_color = cfg["accent_blue"]
        fig_net.add_trace(go.Scatter(
            x=timestamps,
            y=sent_kb,
            name="Sent (KB/s)",
            mode="lines",
            line=dict(color=net_sent_color, width=1.8, shape="spline"),
        ))
        fig_net.add_trace(go.Scatter(
            x=timestamps,
            y=recv_kb,
            name="Recv (KB/s)",
            mode="lines",
            line=dict(color=net_recv_color, width=1.8, shape="spline"),
        ))
        layout_net = _base_chart_layout("", " KB/s", theme=active_theme)
        layout_net["showlegend"] = True
        layout_net["legend"] = dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=8, color=cfg["text_color"]),
        )
        fig_net.update_layout(layout_net)
        st.plotly_chart(fig_net, use_container_width=True, config={"displayModeBar": False})
