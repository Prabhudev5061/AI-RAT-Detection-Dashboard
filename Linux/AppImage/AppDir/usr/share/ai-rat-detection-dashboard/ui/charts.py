"""
AI-RAT-Detection-Dashboard - Telemetry Charts Component
Interactive Plotly charts styled to match dark SOC cybersecurity visual reference.
"""

import streamlit as st
import plotly.graph_objects as go
from typing import List, Dict, Any


def _base_chart_layout(title: str, y_title: str = "%", y_range=None, theme: str = "dark") -> dict:
    """Standardized cybersecurity layout for Plotly charts adapting to Dark and Light themes."""
    is_light = theme == "light"
    bg_color = "#ffffff" if is_light else "#111827"
    grid_color = "#f1f5f9" if is_light else "#1f293d"
    border_color = "#e2e8f0" if is_light else "#1f293d"
    title_color = "#0f172a" if is_light else "#cbd5e1"
    text_color = "#64748b"

    layout = dict(
        title=dict(
            text=f"<b style='color:{title_color}; font-size:13px;'>{title}</b>",
            x=0.02,
            y=0.95,
        ),
        height=190,
        margin=dict(l=35, r=15, t=35, b=25),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        font=dict(family="JetBrains Mono, monospace", size=10, color=text_color),
        xaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            linecolor=border_color,
            tickfont=dict(size=9, color=text_color),
            fixedrange=True,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            linecolor=border_color,
            tickfont=dict(size=9, color=text_color),
            ticksuffix=y_title if y_title != "KB/s" else "",
            fixedrange=True,
        ),
        showlegend=False,
    )
    if y_range:
        layout["yaxis"]["range"] = y_range
    return layout


def render_history_charts(recent_metrics: List[Dict[str, Any]], theme: str = "dark"):
    """Renders the 4 history telemetry charts side by side in 4 columns."""
    col1, col2, col3, col4 = st.columns(4)

    active_theme = st.session_state.get("theme", theme)

    timestamps = [m.get("timestamp", "")[-8:] for m in recent_metrics] or ["00:00:00"]
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
        fig_cpu = go.Figure()
        fig_cpu.add_trace(go.Scatter(
            x=timestamps,
            y=cpu_vals,
            mode="lines",
            line=dict(color="#38bdf8" if active_theme != "light" else "#0284c7", width=2, shape="spline"),
            fill="tozeroy",
            fillcolor="rgba(56, 189, 248, 0.12)" if active_theme != "light" else "rgba(2, 132, 199, 0.12)",
        ))
        fig_cpu.update_layout(_base_chart_layout("📈 CPU Usage History", "%", [0, 105], theme=active_theme))
        st.plotly_chart(fig_cpu, use_container_width=True, config={"displayModeBar": False})

    # 2. RAM History
    with col2:
        fig_ram = go.Figure()
        fig_ram.add_trace(go.Scatter(
            x=timestamps,
            y=ram_vals,
            mode="lines",
            line=dict(color="#c084fc" if active_theme != "light" else "#7c3aed", width=2, shape="spline"),
            fill="tozeroy",
            fillcolor="rgba(192, 132, 252, 0.12)" if active_theme != "light" else "rgba(124, 58, 237, 0.12)",
        ))
        fig_ram.update_layout(_base_chart_layout("📊 RAM Usage History", "%", [0, 105], theme=active_theme))
        st.plotly_chart(fig_ram, use_container_width=True, config={"displayModeBar": False})

    # 3. Disk History
    with col3:
        fig_disk = go.Figure()
        fig_disk.add_trace(go.Scatter(
            x=timestamps,
            y=disk_vals,
            mode="lines",
            line=dict(color="#facc15" if active_theme != "light" else "#d97706", width=2, shape="spline"),
            fill="tozeroy",
            fillcolor="rgba(250, 204, 21, 0.12)" if active_theme != "light" else "rgba(217, 119, 6, 0.12)",
        ))
        fig_disk.update_layout(_base_chart_layout("🗄️ Disk Usage History", "%", [0, 105], theme=active_theme))
        st.plotly_chart(fig_disk, use_container_width=True, config={"displayModeBar": False})

    # 4. Network History
    with col4:
        fig_net = go.Figure()
        fig_net.add_trace(go.Scatter(
            x=timestamps,
            y=sent_kb,
            name="Bytes Sent",
            mode="lines",
            line=dict(color="#06b6d4" if active_theme != "light" else "#0891b2", width=1.8, shape="spline"),
        ))
        fig_net.add_trace(go.Scatter(
            x=timestamps,
            y=recv_kb,
            name="Bytes Recv",
            mode="lines",
            line=dict(color="#3b82f6" if active_theme != "light" else "#2563eb", width=1.8, shape="spline"),
        ))
        layout_net = _base_chart_layout("🌐 Network Usage (KB/s)", " KB/s", theme=active_theme)
        layout_net["showlegend"] = True
        layout_net["legend"] = dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=8, color="#64748b"),
        )
        fig_net.update_layout(layout_net)
        st.plotly_chart(fig_net, use_container_width=True, config={"displayModeBar": False})
