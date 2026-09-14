"""
AI-RAT-Detection-Dashboard - UI Stylesheet & Theme System
Provides complete Dark Mode, Light Mode, and System Theme modes.
Bundles and embeds JetBrains Mono font locally as Base64 for 100% offline,
production-ready desktop execution with zero external network dependencies.
"""

import base64
import logging
from pathlib import Path
from config.config import ASSETS_DIR

logger = logging.getLogger("UIStyles")

# Global font cache to avoid re-reading disk
_FONT_FACE_CSS = ""


def _load_embedded_fonts() -> str:
    """Encodes local JetBrains Mono TTF files into @font-face base64 CSS."""
    global _FONT_FACE_CSS
    if _FONT_FACE_CSS:
        return _FONT_FACE_CSS

    css_parts = []
    fonts_dir = ASSETS_DIR / "fonts"
    reg_path = fonts_dir / "JetBrainsMono-Regular.ttf"
    bold_path = fonts_dir / "JetBrainsMono-Bold.ttf"

    try:
        if reg_path.exists():
            b64_reg = base64.b64encode(reg_path.read_bytes()).decode("ascii")
            css_parts.append(
                f"""
                @font-face {{
                    font-family: 'JetBrains Mono';
                    src: url('data:font/ttf;charset=utf-8;base64,{b64_reg}') format('truetype');
                    font-weight: 400;
                    font-style: normal;
                    font-display: swap;
                }}
                """
            )
        if bold_path.exists():
            b64_bold = base64.b64encode(bold_path.read_bytes()).decode("ascii")
            css_parts.append(
                f"""
                @font-face {{
                    font-family: 'JetBrains Mono';
                    src: url('data:font/ttf;charset=utf-8;base64,{b64_bold}') format('truetype');
                    font-weight: 700;
                    font-style: normal;
                    font-display: swap;
                }}
                """
            )
    except Exception as e:
        logger.warning(f"Could not load local font files: {e}")

    # Fallback to system monospace if font loading encounters an issue
    if not css_parts:
        css_parts.append(
            """
            @font-face {
                font-family: 'JetBrains Mono';
                src: local('JetBrains Mono'), local('Courier New'), monospace;
            }
            """
        )

    _FONT_FACE_CSS = "\n".join(css_parts)
    return _FONT_FACE_CSS


# Palette definitions
DARK_VARS = """
    --app-bg: #0b0f19;
    --app-text: #f8fafc;
    --sidebar-bg: #0c1222;
    --sidebar-border: #1e293b;
    --card-bg: #111827;
    --card-border: #1f293d;
    --card-hover: #334155;
    --card-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    --text-primary: #f8fafc;
    --text-secondary: #cbd5e1;
    --text-muted: #64748b;
    --table-header-bg: #131d31;
    --table-header-text: #94a3b8;
    --table-border: #1a2333;
    --table-row-hover: #162035;
    --badge-safe-bg: rgba(52, 211, 153, 0.12);
    --badge-safe-border: rgba(52, 211, 153, 0.3);
    --badge-safe-text: #34d399;
    --badge-risk-bg: rgba(248, 113, 113, 0.12);
    --badge-risk-border: rgba(248, 113, 113, 0.3);
    --badge-risk-text: #f87171;
    --badge-warn-bg: rgba(250, 204, 21, 0.12);
    --badge-warn-border: rgba(250, 204, 21, 0.3);
    --badge-warn-text: #facc15;
    --input-bg: #1e293b;
    --input-border: #334155;
    --input-text: #f8fafc;
    --accent-blue: #38bdf8;
    --accent-purple: #c084fc;
    --accent-yellow: #facc15;
    --accent-green: #34d399;
    --accent-red: #f87171;
    --sec-border: #1e293b;
"""

LIGHT_VARS = """
    --app-bg: #f8fafc;
    --app-text: #0f172a;
    --sidebar-bg: #f1f5f9;
    --sidebar-border: #e2e8f0;
    --card-bg: #ffffff;
    --card-border: #e2e8f0;
    --card-hover: #cbd5e1;
    --card-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    --text-primary: #0f172a;
    --text-secondary: #334155;
    --text-muted: #64748b;
    --table-header-bg: #f1f5f9;
    --table-header-text: #475569;
    --table-border: #e2e8f0;
    --table-row-hover: #f8fafc;
    --badge-safe-bg: rgba(22, 163, 74, 0.12);
    --badge-safe-border: rgba(22, 163, 74, 0.35);
    --badge-safe-text: #15803d;
    --badge-risk-bg: rgba(220, 38, 38, 0.12);
    --badge-risk-border: rgba(220, 38, 38, 0.35);
    --badge-risk-text: #b91c1c;
    --badge-warn-bg: rgba(217, 119, 6, 0.12);
    --badge-warn-border: rgba(217, 119, 6, 0.35);
    --badge-warn-text: #b45309;
    --input-bg: #ffffff;
    --input-border: #cbd5e1;
    --input-text: #0f172a;
    --accent-blue: #0284c7;
    --accent-purple: #7c3aed;
    --accent-yellow: #d97706;
    --accent-green: #16a34a;
    --accent-red: #dc2626;
    --sec-border: #e2e8f0;
"""


def get_theme_css(theme: str = "dark") -> str:
    """
    Generates complete injected CSS stylesheet with embedded JetBrains Mono font
    and CSS variable tokens for the specified theme ('dark', 'light', or 'system').
    """
    fonts_css = _load_embedded_fonts()
    normalized_theme = theme.lower().strip() if theme else "dark"

    if normalized_theme == "light":
        root_css = f":root {{\n{LIGHT_VARS}\n}}"
    elif normalized_theme == "system":
        root_css = f"""
        :root {{
            {DARK_VARS}
        }}
        @media (prefers-color-scheme: light) {{
            :root {{
                {LIGHT_VARS}
            }}
        }}
        """
    else:  # default to dark
        root_css = f":root {{\n{DARK_VARS}\n}}"

    return f"""
    <style>
    /* 1. Bundled Local Fonts */
    {fonts_css}

    /* 2. Theme Variables */
    {root_css}

    /* 3. Global App Styling */
    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }}

    .stApp {{
        background-color: var(--app-bg) !important;
        color: var(--app-text) !important;
    }}

    /* Tighten top container padding and allow responsive full-width layout */
    .block-container {{
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }}

    h1, h2, h3, h4, h5, h6 {{
        color: var(--text-primary) !important;
    }}

    /* Sidebar styling */
    section[data-testid="stSidebar"] {{
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid var(--sidebar-border) !important;
    }}

    section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"] {{
        padding-top: 1.2rem;
    }}

    /* Custom Card Container */
    .cyber-card {{
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 14px;
        box-shadow: var(--card-shadow);
        position: relative;
        overflow: hidden;
        transition: border-color 0.2s ease;
    }}

    .cyber-card:hover {{
        border-color: var(--card-hover);
    }}

    .card-title-row {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 8px;
    }}

    .card-title {{
        font-size: 0.92rem;
        font-weight: 600;
        color: var(--text-secondary);
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .card-subtitle {{
        font-size: 0.72rem;
        color: var(--text-muted);
        margin-top: -4px;
        margin-bottom: 10px;
    }}

    .metric-big-val {{
        font-size: 1.9rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
        color: var(--text-primary);
    }}

    /* Accent Colors */
    .accent-blue {{ color: var(--accent-blue) !important; }}
    .accent-purple {{ color: var(--accent-purple) !important; }}
    .accent-yellow {{ color: var(--accent-yellow) !important; }}
    .accent-green {{ color: var(--accent-green) !important; }}
    .accent-red {{ color: var(--accent-red) !important; }}

    /* Status Badges */
    .badge-safe {{
        background-color: var(--badge-safe-bg) !important;
        color: var(--badge-safe-text) !important;
        border: 1px solid var(--badge-safe-border) !important;
        padding: 3px 9px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }}

    .badge-risk {{
        background-color: var(--badge-risk-bg) !important;
        color: var(--badge-risk-text) !important;
        border: 1px solid var(--badge-risk-border) !important;
        padding: 3px 9px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }}

    .badge-warn {{
        background-color: var(--badge-warn-bg) !important;
        color: var(--badge-warn-text) !important;
        border: 1px solid var(--badge-warn-border) !important;
        padding: 3px 9px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }}

    /* Modern Cyber Table */
    .cyber-table {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 0.8rem;
        color: var(--text-secondary);
        table-layout: fixed;
    }}

    .cyber-table th {{
        background-color: var(--table-header-bg);
        color: var(--table-header-text);
        text-align: left;
        padding: 8px 10px;
        font-weight: 600;
        font-size: 0.75rem;
        border-bottom: 1px solid var(--table-border);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}

    .cyber-table td {{
        padding: 7px 10px;
        border-bottom: 1px solid var(--table-border);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.76rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}

    .cyber-table tr:hover td {{
        background-color: var(--table-row-hover);
    }}

    /* Security Item Row */
    .sec-item-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 4px;
        border-bottom: 1px solid var(--sec-border);
    }}

    .sec-item-row:last-child {{
        border-bottom: none;
    }}

    .sec-item-label {{
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 0.85rem;
        color: var(--text-primary);
    }}

    /* Recommendation Item */
    .rec-item {{
        display: flex;
        align-items: flex-start;
        gap: 10px;
        font-size: 0.82rem;
        color: var(--text-secondary);
        margin-bottom: 8px;
        line-height: 1.35;
    }}

    /* Streamlit Input / Widget Theming */
    div[data-testid="stMetricValue"] {{
        font-family: 'JetBrains Mono', monospace;
        color: var(--text-primary) !important;
    }}

    /* Buttons & Inputs Theming */
    div[data-testid="stButton"] > button {{
        background-color: var(--input-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--input-border) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }}

    div[data-testid="stButton"] > button:hover {{
        border-color: var(--accent-blue) !important;
        color: var(--accent-blue) !important;
    }}

    /* Selectbox Theming */
    div[data-baseweb="select"] > div {{
        background-color: var(--input-bg) !important;
        color: var(--text-primary) !important;
        border-color: var(--input-border) !important;
    }}

    div[data-baseweb="select"] * {{
        color: var(--text-primary) !important;
    }}

    /* Hide Streamlit default hamburger menu & footer */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
    """


# Backward-compatible constant
DARK_THEME_CSS = get_theme_css("dark")
