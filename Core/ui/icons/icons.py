"""
AI-RAT-Detection-Dashboard - Centralized Nerd Font Icon Mapping System
Exports icon constants and rendering utilities for 100% offline UI typography.
"""

from typing import Dict

# Centralized Nerd Font glyph dictionary (Unicode Private Use Area codepoints)
ICONS: Dict[str, str] = {
    # Security & Protection
    "shield": "\uf132",            # nf-fa-shield
    "shield_check": "\uf2f7",      # nf-fa-shield_check
    "security": "\uf132",          # alias to shield
    "lock": "\uf023",              # nf-fa-lock
    "key": "\uf084",               # nf-fa-key
    "admin": "\uf084",             # admin privilege key

    # Dashboard & Navigation
    "dashboard": "\uf0e4",         # nf-fa-tachometer / dashboard
    "desktop": "\uf108",           # nf-fa-desktop
    "computer": "\uf108",          # alias to desktop
    "terminal": "\uf120",          # nf-fa-terminal
    "home": "\uf015",              # nf-fa-home

    # Hardware & Telemetry
    "cpu": "\uf2db",               # nf-fa-microchip
    "processor": "\uf2db",         # alias to cpu
    "memory": "\uf07a2",           # nf-md-memory
    "ram": "\uf07a2",              # alias to memory
    "disk": "\uf0a0",              # nf-fa-hdd_o
    "storage": "\uf0a0",           # alias to disk
    "gpu": "\uf11b",               # nf-fa-gamepad / display
    "gamepad": "\uf11b",           # alias to gpu
    "activity": "\uf21e",          # nf-fa-heartbeat
    "pulse": "\uf21e",             # alias to activity
    "telemetry": "\uf0e7",         # alias to bolt
    "bolt": "\uf0e7",              # nf-fa-bolt
    "lightning": "\uf0e7",         # alias to bolt

    # Process & Scheduling
    "process": "\uf085",           # nf-fa-cogs
    "processes": "\uf085",         # alias to process
    "gear": "\uf013",              # nf-fa-cog
    "settings": "\uf013",          # alias to gear
    "rocket": "\uf135",            # nf-fa-rocket (startup)
    "startup": "\uf135",           # alias to rocket
    "users": "\uf0c0",             # nf-fa-users (parent-child)
    "parent_child": "\uf0c0",      # alias to users

    # Network & Sockets
    "network": "\uf0ac",           # nf-fa-globe
    "globe": "\uf0ac",             # alias to network
    "connections": "\uf0ac",       # alias to network
    "ports": "\uf071",             # warning/port audit
    "plug": "\uf1e6",              # nf-fa-plug
    "remote": "\uf1e6",            # alias to plug

    # Alerts, Status & Badges
    "warning": "\uf071",           # nf-fa-exclamation_triangle
    "alert": "\uf071",             # alias to warning
    "danger": "\uf071",            # alias to warning
    "siren": "\uf071",             # alias to warning
    "success": "\uf058",           # nf-fa-check_circle
    "check": "\uf00c",             # nf-fa-check
    "check_circle": "\uf058",      # alias to success
    "error": "\uf057",             # nf-fa-times_circle
    "times_circle": "\uf057",      # alias to error
    "close": "\uf057",             # alias to error
    "info": "\uf05a",              # nf-fa-info_circle
    "info_circle": "\uf05a",       # alias to info
    "dot": "\uf111",               # nf-fa-circle (status dot)
    "circle": "\uf111",            # alias to dot
    "dot_circle": "\uf192",        # nf-fa-dot_circle_o

    # Sensors & Devices
    "camera": "\uf030",            # nf-fa-camera
    "microphone": "\uf130",        # nf-fa-microphone
    "screen": "\uf108",            # nf-fa-desktop (screen capture)

    # Intelligence & AI
    "brain": "\ueba4",             # nf-cod-brain
    "ai": "\ueba4",                # alias to brain
    "lightbulb": "\uf0eb",         # nf-fa-lightbulb_o
    "recommendation": "\uf0eb",    # alias to lightbulb

    # Search, Database & Data
    "search": "\uf002",            # nf-fa-search
    "database": "\uf1c0",          # nf-fa-database
    "report": "\uf15c",            # nf-fa-file_text_o
    "file": "\uf15c",              # alias to report
    "folder": "\uf07b",            # nf-fa-folder
    "download": "\uf019",          # nf-fa-download
    "save": "\uf0c7",              # nf-fa-save
    "trash": "\uf1f8",             # nf-fa-trash
    "broom": "\uf1f8",             # alias to trash/prune
    "palette": "\uf1fc",           # nf-fa-paint_brush
    "theme": "\uf1fc",             # alias to palette

    # Time & History
    "clock": "\uf017",             # nf-fa-clock_o
    "time": "\uf017",              # alias to clock
    "history": "\uf1da",           # nf-fa-history

    # Media & Charts
    "chart_line": "\uf201",        # nf-fa-line_chart
    "chart_bar": "\uf080",         # nf-fa-bar_chart
    "play": "\uf04b",              # nf-fa-play
    "stop": "\uf04d",              # nf-fa-stop
    "refresh": "\uf021",           # nf-fa-refresh
}


def get_icon(name: str, fallback: str = "") -> str:
    """
    Retrieve a Nerd Font icon glyph by name with optional fallback.
    Returns the mapped glyph string or the fallback if not found.
    """
    key = name.lower().strip()
    return ICONS.get(key, fallback or key)


def icon_html(name: str, extra_classes: str = "", extra_styles: str = "") -> str:
    """
    Renders an accessible, inline HTML span containing the Nerd Font glyph.
    Ensures correct font family and layout styling.
    """
    glyph = get_icon(name)
    style = f"font-family:'JetBrainsMono Nerd Font', 'JetBrains Mono', monospace; display:inline-block; vertical-align:middle; line-height:1; {extra_styles}".strip()
    cls = f"nf-icon {extra_classes}".strip()
    return f'<span class="{cls}" style="{style}" aria-hidden="true">{glyph}</span>'


def icon_with_label(name: str, label: str, extra_classes: str = "", extra_styles: str = "") -> str:
    """
    Renders an icon paired with a readable text label.
    Supports Section 11 Accessibility rules: [icon] Label.
    """
    return f"{icon_html(name, extra_classes=extra_classes, extra_styles=extra_styles)} {label}"
