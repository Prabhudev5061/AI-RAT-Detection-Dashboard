"""
AI-RAT-Detection-Dashboard - Formatting Module
Color maps, badges, and status HTML generators.
"""

from typing import Tuple


def get_risk_color(level: str) -> str:
    """Return hex color corresponding to risk level."""
    lvl = str(level).upper()
    if lvl == "CRITICAL":
        return "#ef4444"  # Red
    elif lvl == "HIGH":
        return "#f97316"  # Orange
    elif lvl == "MEDIUM":
        return "#eab308"  # Yellow
    else:
        return "#10b981"  # Emerald Green


def get_severity_badge_html(severity: str) -> str:
    """Generate HTML badge for event severity."""
    sev = str(severity).upper()
    color = "#3b82f6"  # Info - Blue
    bg = "rgba(59, 130, 246, 0.15)"
    border = "rgba(59, 130, 246, 0.3)"

    if sev in ("HIGH", "CRITICAL"):
        color = "#ef4444"
        bg = "rgba(239, 68, 68, 0.15)"
        border = "rgba(239, 68, 68, 0.3)"
    elif sev == "WARNING":
        color = "#f59e0b"
        bg = "rgba(245, 158, 11, 0.15)"
        border = "rgba(245, 158, 11, 0.3)"

    return (
        f'<span style="background-color: {bg}; color: {color}; border: 1px solid {border}; '
        f'padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; '
        f'display: inline-block;">{sev}</span>'
    )


def get_risk_badge_html(level: str, score: int) -> str:
    """Generate HTML badge for process/threat risk."""
    color = get_risk_color(level)
    bg = f"{color}22"
    return (
        f'<span style="background-color: {bg}; color: {color}; border: 1px solid {color}55; '
        f'padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 700;">'
        f'{level} ({score})</span>'
    )
