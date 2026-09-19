"""
AI-RAT-Detection-Dashboard - Theme Manager
Registers themes, handles key normalizations, generates CSS variables,
and provides theme metadata for Plotly charts and UI selectors.
"""

from typing import Dict, List, Optional, Tuple
from ui.themes.tokens import ThemeTokens
from ui.themes.dark_themes import CATPPUCCIN_DARK, DRACULA_DARK, NORD_DARK, CYBER_DARK
from ui.themes.light_themes import WHITE_SLUR, GRUVBOX_LIGHT, WINDOWS_XP, CLASSIC_LIGHT

# All registered theme definitions
THEMES: Dict[str, ThemeTokens] = {
    "catppuccin_dark": CATPPUCCIN_DARK,
    "dracula_dark": DRACULA_DARK,
    "nord_dark": NORD_DARK,
    "cyber_dark": CYBER_DARK,
    "white_slur": WHITE_SLUR,
    "gruvbox_light": GRUVBOX_LIGHT,
    "windows_xp": WINDOWS_XP,
    "classic_light": CLASSIC_LIGHT,
}

# Aliases for backward compatibility and case-insensitive resolution
THEME_ALIASES: Dict[str, str] = {
    "dark": "cyber_dark",
    "cyber": "cyber_dark",
    "cyber dark": "cyber_dark",
    "catppuccin": "catppuccin_dark",
    "catppuccin dark": "catppuccin_dark",
    "dracula": "dracula_dark",
    "dracula dark": "dracula_dark",
    "nord": "nord_dark",
    "nord dark": "nord_dark",
    "light": "classic_light",
    "classic light": "classic_light",
    "white slur": "white_slur",
    "whiteslur": "white_slur",
    "gruvbox": "gruvbox_light",
    "gruvbox light": "gruvbox_light",
    "xp": "windows_xp",
    "windows xp": "windows_xp",
    "windows xp light": "windows_xp",
    "windows_xp_light": "windows_xp",
    "system": "cyber_dark",
}


def normalize_theme_key(key: str) -> str:
    """Normalizes any theme string, alias, or display name to a canonical theme key."""
    if not key:
        return "cyber_dark"
    clean = str(key).lower().strip().replace("-", "_")
    # Check aliases
    if clean in THEME_ALIASES:
        return THEME_ALIASES[clean]
    # Check if exact key
    if clean in THEMES:
        return clean
    # Check if clean with spaces
    clean_spaces = str(key).lower().strip()
    if clean_spaces in THEME_ALIASES:
        return THEME_ALIASES[clean_spaces]
    return "cyber_dark"


def get_theme(key: str) -> ThemeTokens:
    """Retrieves ThemeTokens for the specified key with fallback to Cyber Dark."""
    norm_key = normalize_theme_key(key)
    return THEMES.get(norm_key, CYBER_DARK)


def get_grouped_themes() -> Dict[str, List[ThemeTokens]]:
    """Returns all themes grouped by 'Dark' and 'Light'."""
    grouped: Dict[str, List[ThemeTokens]] = {"Dark": [], "Light": []}
    for theme in THEMES.values():
        if theme.group in grouped:
            grouped[theme.group].append(theme)
    return grouped


def get_theme_names_list() -> List[str]:
    """Returns a flat list of display names for selectboxes."""
    # Dark group first, then Light group
    names = []
    for t in [CATPPUCCIN_DARK, DRACULA_DARK, NORD_DARK, CYBER_DARK]:
        names.append(t.name)
    for t in [WHITE_SLUR, GRUVBOX_LIGHT, WINDOWS_XP, CLASSIC_LIGHT]:
        names.append(t.name)
    return names


def get_key_from_display_name(display_name: str) -> str:
    """Finds canonical key from display name."""
    for key, theme in THEMES.items():
        if theme.name.lower() == display_name.lower().strip():
            return key
    return normalize_theme_key(display_name)


def get_plotly_theme_config(theme_key: str) -> dict:
    """
    Returns standardized Plotly layout styling matching the active theme palette.
    """
    tokens = get_theme(theme_key)
    return {
        "bg_color": tokens.chart_bg,
        "grid_color": tokens.chart_grid,
        "border_color": tokens.chart_border,
        "title_color": tokens.chart_title,
        "text_color": tokens.chart_text,
        "font_family": "JetBrainsMono Nerd Font, JetBrains Mono, monospace",
        "accent_blue": tokens.accent_blue,
        "accent_purple": tokens.accent_purple,
        "accent_yellow": tokens.accent_yellow,
        "accent_green": tokens.accent_green,
        "accent_red": tokens.accent_red,
        "accent": tokens.accent,
        "is_dark": tokens.is_dark,
    }


def generate_theme_css(theme_key: str, fonts_css: str = "") -> str:
    """
    Generates the complete CSS stylesheet for the specified theme,
    including CSS variables, font-face rules, cards, tables, and Streamlit component theming.
    """
    tokens = get_theme(theme_key)
    css_vars = tokens.to_css_variables()
    transparency = tokens.transparency_css
    custom_overrides = tokens.custom_css

    card_extra = f"{transparency}" if transparency else ""

    return f"""
    <style>
    /* 1. Bundled Local Fonts */
    {fonts_css}

    /* 2. Theme Tokens */
    :root {{
    {css_vars}
    }}

    /* 3. Global App Styling */
    html, body, [class*="css"] {{
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', 'Segoe UI', system-ui, -apple-system, sans-serif !important;
    }}

    /* Nerd Font Icon Typography Class */
    .nf-icon {{
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', monospace !important;
        display: inline-block;
        vertical-align: middle;
        line-height: 1;
        font-style: normal;
    }}

    .stApp {{
        background-color: var(--app-bg) !important;
        color: var(--app-text) !important;
    }}

    /* Container padding & responsive layout */
    .block-container {{
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }}

    h1, h2, h3, h4, h5, h6 {{
        color: var(--text-primary) !important;
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', sans-serif !important;
    }}

    /* Sidebar styling */
    section[data-testid="stSidebar"] {{
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid var(--sidebar-border) !important;
        color: var(--text-primary) !important;
    }}

    section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"] {{
        padding-top: 1.2rem;
    }}

    /* Universal safeguard: Suppress raw Material Symbol ligature text fallback across the app */
    [data-testid="stIconMaterial"] {{
        font-size: 0 !important;
        line-height: 0 !important;
        color: transparent !important;
        user-select: none !important;
    }}

    /* Sidebar Collapse & Expand Controls: Replace Material ligature text with embedded Nerd Font icon glyphs */
    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="stSidebarCollapsedControl"] button,
    [data-testid="stExpandSidebarButton"] {{
        background-color: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 6px !important;
        box-shadow: none !important;
        cursor: pointer !important;
        color: var(--text-secondary) !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 2rem !important;
        height: 2rem !important;
        min-width: 32px !important;
        min-height: 32px !important;
        pointer-events: auto !important;
        visibility: visible !important;
        opacity: 1 !important;
        transition: background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, color 0.15s ease-in-out, transform 0.15s ease-in-out, box-shadow 0.15s ease-in-out !important;
        outline: none !important;
        position: relative !important;
    }}

    /* Collapsed state expand button: styled badge inheriting active theme */
    [data-testid="stExpandSidebarButton"],
    [data-testid="stSidebarCollapsedControl"] button {{
        background-color: var(--surface) !important;
        border: 1px solid var(--sidebar-border) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
        margin-top: 6px !important;
        margin-left: 6px !important;
    }}

    [data-testid="stSidebarCollapseButton"] button:hover,
    button[data-testid="stBaseButton-headerNoPadding"]:hover {{
        background-color: var(--surface-alt) !important;
        border-color: var(--card-border) !important;
        color: var(--accent-blue) !important;
        transform: scale(1.05) !important;
    }}

    [data-testid="stExpandSidebarButton"]:hover,
    [data-testid="stSidebarCollapsedControl"] button:hover {{
        background-color: var(--surface-alt) !important;
        border-color: var(--accent-blue) !important;
        color: var(--accent-blue) !important;
        transform: scale(1.05) !important;
    }}

    [data-testid="stSidebarCollapseButton"] button:active,
    [data-testid="stExpandSidebarButton"]:active,
    [data-testid="stSidebarCollapsedControl"] button:active {{
        transform: scale(0.95) !important;
    }}

    [data-testid="stSidebarCollapseButton"] button:focus-visible,
    [data-testid="stExpandSidebarButton"]:focus-visible,
    [data-testid="stSidebarCollapsedControl"] button:focus-visible {{
        outline: 2px solid var(--accent-blue) !important;
        outline-offset: 2px !important;
    }}

    /* Keep collapse container visible in sidebar header */
    [data-testid="stSidebarCollapseButton"] {{
        visibility: visible !important;
        opacity: 1 !important;
        display: block !important;
    }}

    /* Icon containers inside buttons */
    [data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"],
    [data-testid="stSidebarCollapsedControl"] [data-testid="stIconMaterial"],
    [data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"] {{
        font-size: 0 !important;
        line-height: 0 !important;
        color: transparent !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 1.5rem !important;
        height: 1.5rem !important;
        position: relative !important;
        user-select: none !important;
    }}

    /* Collapse icon glyph: \f100 (double angle left <<) */
    [data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"]::before {{
        content: "\\f100" !important; /* nf-fa-angle_double_left */
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', monospace !important;
        font-size: 1.15rem !important;
        line-height: 1 !important;
        color: var(--text-secondary) !important;
        display: inline-block !important;
        transition: color 0.15s ease-in-out, transform 0.15s ease-in-out !important;
    }}

    [data-testid="stSidebarCollapseButton"]:hover [data-testid="stIconMaterial"]::before,
    button[data-testid="stBaseButton-headerNoPadding"]:hover [data-testid="stIconMaterial"]::before {{
        color: var(--accent-blue) !important;
        transform: scale(1.1) !important;
    }}

    /* Expand icon glyph: \f101 (double angle right >>) */
    [data-testid="stSidebarCollapsedControl"] [data-testid="stIconMaterial"]::before,
    [data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"]::before {{
        content: "\\f101" !important; /* nf-fa-angle_double_right */
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', monospace !important;
        font-size: 1.15rem !important;
        line-height: 1 !important;
        color: var(--text-secondary) !important;
        display: inline-block !important;
        transition: color 0.15s ease-in-out, transform 0.15s ease-in-out !important;
    }}

    [data-testid="stSidebarCollapsedControl"]:hover [data-testid="stIconMaterial"]::before,
    [data-testid="stExpandSidebarButton"]:hover [data-testid="stIconMaterial"]::before {{
        color: var(--accent-blue) !important;
        transform: scale(1.1) !important;
    }}

    /* Clean CSS tooltips on hover */
    [data-testid="stSidebarCollapseButton"] button::after {{
        content: "Collapse sidebar";
        position: absolute;
        top: 115%;
        right: 0;
        background-color: var(--card-bg);
        color: var(--text-primary);
        border: 1px solid var(--card-border);
        padding: 3px 8px;
        font-size: 0.72rem;
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', monospace;
        border-radius: 4px;
        white-space: nowrap;
        z-index: 999999;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        pointer-events: none;
        opacity: 0;
        transform: translateY(-4px);
        transition: opacity 0.15s ease, transform 0.15s ease;
    }}

    [data-testid="stSidebarCollapseButton"] button:hover::after {{
        opacity: 1;
        transform: translateY(0);
    }}

    [data-testid="stExpandSidebarButton"]::after,
    [data-testid="stSidebarCollapsedControl"] button::after {{
        content: "Expand sidebar";
        position: absolute;
        top: 50%;
        left: calc(100% + 8px);
        transform: translateY(-50%) translateX(-4px);
        background-color: var(--card-bg);
        color: var(--text-primary);
        border: 1px solid var(--card-border);
        padding: 3px 8px;
        font-size: 0.72rem;
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', monospace;
        border-radius: 4px;
        white-space: nowrap;
        z-index: 999999;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.15s ease, transform 0.15s ease;
    }}

    [data-testid="stExpandSidebarButton"]:hover::after,
    [data-testid="stSidebarCollapsedControl"] button:hover::after {{
        opacity: 1;
        transform: translateY(-50%) translateX(0);
    }}

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4 {{
        color: var(--text-primary) !important;
    }}

    section[data-testid="stSidebar"] p {{
        color: var(--text-secondary) !important;
    }}

    section[data-testid="stSidebar"] hr {{
        border-color: var(--sidebar-border) !important;
    }}

    /* Sidebar Navigation Menu (stRadio) Overrides */
    div[data-testid="stRadio"] {{
        width: 100% !important;
    }}

    div[data-testid="stRadio"] > div[role="radiogroup"] {{
        gap: 3px !important;
    }}

    /* Hide the top widget label so only the navigation options appear */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-testid="stWidgetLabel"] {{
        display: none !important;
    }}

    /* Sidebar Navigation Item Labels */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-testid="stRadioOption"],
    div[data-testid="stRadio"] label[data-testid="stRadioOption"] {{
        background-color: transparent !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        margin-bottom: 2px !important;
        cursor: pointer !important;
        transition: all 0.15s ease-in-out !important;
        width: 100% !important;
        border: 1px solid transparent !important;
        display: flex !important;
        align-items: center !important;
    }}

    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-testid="stRadioOption"]:hover,
    div[data-testid="stRadio"] label[data-testid="stRadioOption"]:hover {{
        background-color: var(--surface-alt) !important;
        border-color: var(--card-border) !important;
    }}

    /* Force text inside radio items to take the theme colors */
    div[data-testid="stRadio"] label[data-testid="stRadioOption"] p,
    div[data-testid="stRadio"] label[data-testid="stRadioOption"] div,
    div[data-testid="stRadio"] label[data-testid="stRadioOption"] span {{
        color: var(--text-secondary) !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', sans-serif !important;
    }}

    div[data-testid="stRadio"] label[data-testid="stRadioOption"]:hover p,
    div[data-testid="stRadio"] label[data-testid="stRadioOption"]:hover div,
    div[data-testid="stRadio"] label[data-testid="stRadioOption"]:hover span {{
        color: var(--text-primary) !important;
    }}

    /* Active / Selected Item */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-testid="stRadioOption"][data-selected="true"],
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-testid="stRadioOption"]:has(input:checked),
    div[data-testid="stRadio"] label[data-testid="stRadioOption"]:has(input:checked) {{
        background-color: var(--surface-alt) !important;
        border: 1px solid var(--card-border) !important;
        border-left: 3px solid var(--accent-blue) !important;
    }}

    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-testid="stRadioOption"][data-selected="true"] p,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-testid="stRadioOption"]:has(input:checked) p,
    div[data-testid="stRadio"] label[data-testid="stRadioOption"]:has(input:checked) p {{
        color: var(--accent-blue) !important;
        font-weight: 700 !important;
    }}

    /* Clean SOC Button Layout: Hide the default radio circle in sidebar without hiding text */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-testid="stRadioOption"] div:has(+ div[data-testid="stMarkdownContainer"]) {{
        display: none !important;
    }}

    /* Buttons & Download Buttons Typography and Styling */
    div[data-testid="stButton"] button,
    div[data-testid="stButton"] button *,
    div[data-testid="stDownloadButton"] button,
    div[data-testid="stDownloadButton"] button *,
    div[data-baseweb="tab"] *,
    div[data-testid="stAlert"] * {{
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', monospace !important;
    }}

    div[data-testid="stButton"] > button,
    div[data-testid="stDownloadButton"] > button {{
        background-color: var(--surface-alt) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out !important;
    }}

    div[data-testid="stButton"] > button:hover,
    div[data-testid="stDownloadButton"] > button:hover {{
        background-color: var(--card-hover) !important;
        border-color: var(--accent-blue) !important;
        color: var(--accent-blue) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
    }}

    /* Dashboard Top Header Banner Container */
    .dashboard-header-container {{
        margin-bottom: 1.2rem;
    }}

    .dashboard-header-banner {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
    }}

    .dashboard-header-title-box {{
        display: flex;
        align-items: center;
    }}

    .dashboard-header-shield {{
        display: none;
    }}

    .dashboard-header-title {{
        margin: 0;
        font-size: 1.65rem;
        font-weight: 800;
        color: var(--text-primary);
        letter-spacing: -0.5px;
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', sans-serif;
    }}

    .dashboard-header-status-box {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}

    .dashboard-pill-updated {{
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 0.75rem;
        color: var(--text-secondary);
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', monospace;
        display: flex;
        align-items: center;
        gap: 6px;
    }}

    .dashboard-pill-time {{
        color: var(--text-primary);
    }}

    .dashboard-pill-active {{
        background: var(--badge-safe-bg);
        border: 1px solid var(--badge-safe-border);
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 0.75rem;
        color: var(--badge-safe-text);
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
    }}

    .dashboard-header-subtitle {{
        font-size: 0.82rem;
        color: var(--text-muted);
        margin-top: 2px;
    }}

    .chart-card-header {{
        font-size: 0.84rem;
        font-weight: 600;
        color: var(--text-secondary);
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 6px;
    }}

    /* Modular Cyber Card Container */
    .cyber-card {{
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 14px;
        box-shadow: var(--card-shadow);
        position: relative;
        overflow: hidden;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
        {card_extra}
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
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', monospace;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
        color: var(--text-primary);
    }}

    /* Accent Classes */
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
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }}

    .badge-risk {{
        background-color: var(--badge-risk-bg) !important;
        color: var(--badge-risk-text) !important;
        border: 1px solid var(--badge-risk-border) !important;
        padding: 3px 9px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }}

    .badge-warn {{
        background-color: var(--badge-warn-bg) !important;
        color: var(--badge-warn-text) !important;
        border: 1px solid var(--badge-warn-border) !important;
        padding: 3px 9px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }}

    /* Cyber Table */
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
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', monospace;
        font-size: 0.76rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        color: var(--text-secondary);
    }}

    .cyber-table tr:hover td {{
        background-color: var(--table-row-hover);
    }}

    /* Security Item Rows */
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

    /* Recommendation Items */
    .rec-item {{
        display: flex;
        align-items: flex-start;
        gap: 10px;
        font-size: 0.82rem;
        color: var(--text-secondary);
        margin-bottom: 8px;
        line-height: 1.35;
    }}

    /* Streamlit Widgets Theming */
    div[data-testid="stMetricValue"] {{
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', monospace;
        color: var(--text-primary) !important;
    }}

    div[data-testid="stMetricLabel"] p {{
        color: var(--text-muted) !important;
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', sans-serif !important;
    }}

    /* Widget Labels */
    div[data-testid="stWidgetLabel"] label,
    div[data-testid="stWidgetLabel"] p,
    div[data-testid="stWidgetLabel"] span {{
        color: var(--text-secondary) !important;
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', sans-serif !important;
        font-size: 0.84rem !important;
        font-weight: 600 !important;
    }}

    /* Toggle Widget Styling */
    div[data-testid="stToggle"] label {{
        color: var(--text-primary) !important;
    }}

    div[data-testid="stToggle"] label p,
    div[data-testid="stToggle"] label span,
    div[data-testid="stToggle"] label div {{
        color: var(--text-secondary) !important;
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }}

    div[data-testid="stToggle"]:hover label p {{
        color: var(--text-primary) !important;
    }}

    div[data-testid="stButton"] > button {{
        background-color: var(--btn-bg) !important;
        color: var(--btn-text) !important;
        border: 1px solid var(--btn-border) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', sans-serif !important;
        transition: all 0.2s ease !important;
    }}

    div[data-testid="stButton"] > button:hover {{
        border-color: var(--accent-blue) !important;
        color: var(--accent-blue) !important;
    }}

    /* Download Buttons */
    div[data-testid="stDownloadButton"] > button {{
        background-color: var(--btn-bg) !important;
        color: var(--btn-text) !important;
        border: 1px solid var(--btn-border) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', sans-serif !important;
    }}

    div[data-testid="stDownloadButton"] > button:hover {{
        border-color: var(--accent-blue) !important;
        color: var(--accent-blue) !important;
    }}

    /* Selectbox / Input Theming */
    div[data-baseweb="select"] > div {{
        background-color: var(--input-bg) !important;
        color: var(--input-text) !important;
        border-color: var(--input-border) !important;
        border-radius: 8px !important;
    }}

    div[data-baseweb="select"] * {{
        color: var(--input-text) !important;
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', sans-serif !important;
    }}

    /* Dropdown Popover Menus & Options */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[role="listbox"] {{
        background-color: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 8px !important;
        box-shadow: var(--card-shadow) !important;
    }}

    li[role="option"] {{
        color: var(--text-primary) !important;
        background-color: transparent !important;
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', sans-serif !important;
        font-size: 0.85rem !important;
        padding: 8px 12px !important;
    }}

    li[role="option"]:hover,
    li[role="option"][aria-selected="true"] {{
        background-color: var(--surface-alt) !important;
        color: var(--accent-blue) !important;
    }}

    li[role="option"] * {{
        color: inherit !important;
    }}

    div[data-baseweb="input"] > div {{
        background-color: var(--input-bg) !important;
        color: var(--input-text) !important;
        border-color: var(--input-border) !important;
        border-radius: 8px !important;
    }}

    div[data-baseweb="input"] input {{
        color: var(--input-text) !important;
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', monospace !important;
    }}

    /* Alerts & Callouts */
    div[data-testid="stAlert"] {{
        background-color: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        color: var(--text-primary) !important;
        border-radius: 8px !important;
    }}

    /* Suppress default Streamlit SVG icons to avoid duplicate icons */
    div[data-testid="stAlert"] [data-testid="stAlertIcon"] {{
        display: none !important;
    }}

    div[data-testid="stAlert"] p,
    div[data-testid="stAlert"] span,
    div[data-testid="stAlert"] div {{
        color: var(--text-primary) !important;
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', sans-serif !important;
    }}

    /* Tabs */
    button[data-baseweb="tab"] {{
        color: var(--text-muted) !important;
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', sans-serif !important;
    }}

    button[data-baseweb="tab"][aria-selected="true"] {{
        color: var(--accent-blue) !important;
        border-bottom-color: var(--accent-blue) !important;
    }}

    /* Expanders */
    div[data-testid="stExpander"] {{
        background-color: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 8px !important;
    }}

    div[data-testid="stExpander"] summary {{
        color: var(--text-primary) !important;
        font-family: 'JetBrainsMono Nerd Font', 'JetBrains Mono', sans-serif !important;
    }}

    div[data-testid="stExpander"] summary:hover {{
        color: var(--accent-blue) !important;
    }}

    /* Markdown Text & Captions */
    .stMarkdown p {{
        color: var(--text-secondary);
    }}

    .stCaption p, [data-testid="stCaptionContainer"] p {{
        color: var(--text-muted) !important;
    }}

    /* Dataframe table theming */
    div[data-testid="stDataFrame"] {{
        border: 1px solid var(--card-border);
        border-radius: 8px;
    }}

    /* Chrome cleanup: Keep header functional for expand controls while suppressing default chrome */
    #MainMenu {{visibility: hidden; display: none !important;}}
    footer {{visibility: hidden; display: none !important;}}
    [data-testid="stMainMenu"] {{display: none !important; visibility: hidden !important;}}
    [data-testid="stAppDeployButton"] {{display: none !important; visibility: hidden !important;}}
    [data-testid="stDecoration"] {{display: none !important; height: 0px !important;}}
    [data-testid="stStatusWidget"] {{display: none !important; visibility: hidden !important;}}

    header[data-testid="stHeader"] {{
        display: flex !important;
        background: transparent !important;
        color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        height: 3.2rem !important;
        pointer-events: none !important;
        z-index: 999990 !important;
    }}

    /* Suppress 0-height iframes completely so they take zero layout space */
    iframe[height="0"],
    div:has(> iframe[height="0"]) {{
        display: none !important;
        height: 0px !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    {custom_overrides}
    </style>
    """
