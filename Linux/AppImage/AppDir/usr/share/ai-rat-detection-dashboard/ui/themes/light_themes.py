"""
AI-RAT-Detection-Dashboard - Light Themes Collection
Implements White Slur, Gruvbox Light, Windows XP Light, and the original Classic Light
with enhanced high-contrast text, legible navigation, and refined surface definitions.
"""

from ui.themes.tokens import ThemeTokens

# 1. White Slur (Clean translucent glass design with high contrast dark typography)
WHITE_SLUR = ThemeTokens(
    key="white_slur",
    name="White Slur",
    group="Light",
    is_dark=False,
    background="#f8fafc",
    surface="#ffffff",
    surface_alt="#f1f5f9",
    card="rgba(255, 255, 255, 0.88)",
    card_border="rgba(203, 213, 225, 0.8)",
    card_hover="#e2e8f0",
    card_shadow="0 4px 20px rgba(0, 0, 0, 0.06)",
    text="#0f172a",
    text_secondary="#1e293b",
    text_muted="#475569",
    accent="#0284c7",
    accent_secondary="#7c3aed",
    accent_blue="#0284c7",
    accent_purple="#7c3aed",
    accent_yellow="#b45309",
    accent_green="#15803d",
    accent_red="#b91c1c",
    success="#15803d",
    warning="#b45309",
    error="#b91c1c",
    info="#0284c7",
    button_bg="#ffffff",
    button_hover="#f1f5f9",
    button_text="#0f172a",
    button_border="#cbd5e1",
    input_bg="#ffffff",
    input_border="#cbd5e1",
    input_text="#0f172a",
    table_header_bg="#f1f5f9",
    table_header_text="#1e293b",
    table_border="#e2e8f0",
    table_row_hover="#f8fafc",
    badge_safe_bg="rgba(21, 128, 61, 0.12)",
    badge_safe_border="rgba(21, 128, 61, 0.35)",
    badge_safe_text="#15803d",
    badge_risk_bg="rgba(185, 28, 28, 0.12)",
    badge_risk_border="rgba(185, 28, 28, 0.35)",
    badge_risk_text="#b91c1c",
    badge_warn_bg="rgba(180, 83, 9, 0.12)",
    badge_warn_border="rgba(180, 83, 9, 0.35)",
    badge_warn_text="#b45309",
    chart_bg="#ffffff",
    chart_grid="#f1f5f9",
    chart_border="#e2e8f0",
    chart_title="#0f172a",
    chart_text="#475569",
    sec_border="#e2e8f0",
    transparency_css="backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);",
)

# 2. Gruvbox Light (Warm, high-contrast retro day palette)
GRUVBOX_LIGHT = ThemeTokens(
    key="gruvbox_light",
    name="Gruvbox Light",
    group="Light",
    is_dark=False,
    background="#fbf1c7",
    surface="#f2e5bc",
    surface_alt="#ebdbb2",
    card="#f2e5bc",
    card_border="#d5c4a1",
    card_hover="#ebdbb2",
    card_shadow="0 3px 12px rgba(60, 56, 54, 0.1)",
    text="#282828",
    text_secondary="#3c3836",
    text_muted="#504945",
    accent="#076678",
    accent_secondary="#8f3f71",
    accent_blue="#076678",
    accent_purple="#8f3f71",
    accent_yellow="#b57614",
    accent_green="#79740e",
    accent_red="#af3a03",
    success="#79740e",
    warning="#b57614",
    error="#af3a03",
    info="#076678",
    button_bg="#ebdbb2",
    button_hover="#d5c4a1",
    button_text="#282828",
    button_border="#bdae93",
    input_bg="#fbf1c7",
    input_border="#bdae93",
    input_text="#282828",
    table_header_bg="#ebdbb2",
    table_header_text="#282828",
    table_border="#d5c4a1",
    table_row_hover="#ebdbb2",
    badge_safe_bg="rgba(121, 116, 14, 0.16)",
    badge_safe_border="rgba(121, 116, 14, 0.45)",
    badge_safe_text="#79740e",
    badge_risk_bg="rgba(175, 58, 3, 0.16)",
    badge_risk_border="rgba(175, 58, 3, 0.45)",
    badge_risk_text="#af3a03",
    badge_warn_bg="rgba(181, 118, 20, 0.16)",
    badge_warn_border="rgba(181, 118, 20, 0.45)",
    badge_warn_text="#b57614",
    chart_bg="#fbf1c7",
    chart_grid="#ebdbb2",
    chart_border="#d5c4a1",
    chart_title="#282828",
    chart_text="#504945",
    sec_border="#d5c4a1",
)

# 3. Windows XP Light (Classic Luna desktop palette with readable high-contrast text)
WINDOWS_XP = ThemeTokens(
    key="windows_xp",
    name="Windows XP Light",
    group="Light",
    is_dark=False,
    background="#ece9d8",
    surface="#ece9d8",
    surface_alt="#d8e4f8",
    card="#ffffff",
    card_border="#0055ea",
    card_hover="#d8e4f8",
    card_shadow="0 2px 6px rgba(0, 60, 160, 0.12)",
    text="#000000",
    text_secondary="#0c3276",
    text_muted="#334466",
    accent="#0055ea",
    accent_secondary="#245edb",
    accent_blue="#0055ea",
    accent_purple="#6b21a8",
    accent_yellow="#854d0e",
    accent_green="#15803d",
    accent_red="#b91c1c",
    success="#15803d",
    warning="#854d0e",
    error="#b91c1c",
    info="#0055ea",
    button_bg="#ece9d8",
    button_hover="#f5f4ed",
    button_text="#000000",
    button_border="#7f9db9",
    input_bg="#ffffff",
    input_border="#7f9db9",
    input_text="#000000",
    table_header_bg="#1664e8",
    table_header_text="#ffffff",
    table_border="#d8e4f8",
    table_row_hover="#eef4ff",
    badge_safe_bg="rgba(21, 128, 61, 0.14)",
    badge_safe_border="#15803d",
    badge_safe_text="#15803d",
    badge_risk_bg="rgba(185, 28, 28, 0.14)",
    badge_risk_border="#b91c1c",
    badge_risk_text="#b91c1c",
    badge_warn_bg="rgba(133, 77, 14, 0.14)",
    badge_warn_border="#854d0e",
    badge_warn_text="#854d0e",
    chart_bg="#ffffff",
    chart_grid="#e5eefb",
    chart_border="#d8e4f8",
    chart_title="#003399",
    chart_text="#0c3276",
    sec_border="#7f9db9",
    custom_css="""
    /* ==========================================================================
       Windows XP Light Theme - Visual Reference Rebuild (Luna Blue)
       ========================================================================== */

    /* 1. App Window Outer Frame & Desktop Surface */
    .stApp {
        background-color: #ece9d8 !important;
        border: 3px solid #0055ea !important;
        border-radius: 8px !important;
        overflow: hidden !important;
        box-shadow: 0 10px 30px rgba(0, 50, 150, 0.25) !important;
    }

    /* 2. Sidebar Explorer Task Pane */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #dbe6fe 0%, #d8e5fe 50%, #eaf0fd 100%) !important;
        border-right: 2px solid #0055ea !important;
    }

    /* Brand Shield Logo Box */
    section[data-testid="stSidebar"] div[style*="linear-gradient(135deg"] {
        background: linear-gradient(180deg, #ffffff 0%, #d8e5fe 100%) !important;
        border: 1px solid #7f9db9 !important;
        border-radius: 6px !important;
        box-shadow: inset 0 1px 0 #ffffff, 0 1px 3px rgba(0, 0, 0, 0.1) !important;
    }
    section[data-testid="stSidebar"] div[style*="linear-gradient(135deg"] .nf-icon {
        color: #0055ea !important;
    }
    section[data-testid="stSidebar"] div[style*="letter-spacing: -0.3px;"] {
        color: #002277 !important;
        font-weight: 800 !important;
    }
    section[data-testid="stSidebar"] div[style*="font-size:0.68rem;"] {
        color: #334466 !important;
        font-weight: 500 !important;
    }

    /* Privilege Mode Sand Panel */
    section[data-testid="stSidebar"] div[style*="font-size: 0.75rem;"][style*="margin-bottom: 1.2rem;"] {
        background: #f2efdf !important;
        border: 1px solid #7f9db9 !important;
        border-radius: 4px !important;
        box-shadow: inset 0 1px 0 #ffffff !important;
    }
    section[data-testid="stSidebar"] div[style*="font-size: 0.75rem;"][style*="margin-bottom: 1.2rem;"] span:first-child {
        color: #003399 !important;
        font-weight: 700 !important;
    }
    section[data-testid="stSidebar"] div[style*="font-size: 0.75rem;"][style*="margin-bottom: 1.2rem;"] span:last-child {
        color: #705000 !important;
        font-weight: 700 !important;
    }

    /* Sidebar Navigation Links (stRadio) */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-testid="stRadioOption"] {
        background-color: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 4px !important;
        padding: 7px 10px !important;
        margin-bottom: 3px !important;
        transition: background 0.15s ease !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-testid="stRadioOption"] p,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-testid="stRadioOption"] span,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-testid="stRadioOption"] div {
        color: #003399 !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-testid="stRadioOption"]:hover {
        background-color: #cfe0fc !important;
        border-color: #b0cbf7 !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-testid="stRadioOption"]:hover p,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-testid="stRadioOption"]:hover span {
        color: #002288 !important;
    }

    /* Selected Active Navigation Item: Glossy Luna Blue Pill */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-testid="stRadioOption"]:has(input:checked),
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-testid="stRadioOption"][data-selected="true"] {
        background: linear-gradient(180deg, #2b77f9 0%, #1562e8 50%, #0050d8 100%) !important;
        border: 1px solid #003bb3 !important;
        border-radius: 6px !important;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.45), 0 2px 4px rgba(0, 50, 150, 0.2) !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-testid="stRadioOption"]:has(input:checked) p,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-testid="stRadioOption"]:has(input:checked) span,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-testid="stRadioOption"]:has(input:checked) div {
        color: #ffffff !important;
        font-weight: 700 !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.35) !important;
    }

    /* Sidebar Bottom Controls */
    section[data-testid="stSidebar"] div[style*="font-size:0.82rem;"] {
        color: #0c3276 !important;
        font-weight: 700 !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1px solid #7f9db9 !important;
        border-radius: 3px !important;
        box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.1) !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #000000 !important;
        font-weight: 500 !important;
    }

    /* Toggle Switch */
    section[data-testid="stSidebar"] div[data-testid="stToggle"] label div:has(input[type="checkbox"]) {
        background-color: #c41e3a !important;
        border: 1px solid #9e142b !important;
        border-radius: 12px !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stToggle"] label p,
    section[data-testid="stSidebar"] div[data-testid="stToggle"] label span {
        color: #0c3276 !important;
        font-weight: 600 !important;
    }

    /* AI Protection Active Pill */
    section[data-testid="stSidebar"] div[style*="padding: 0 4px;"] > div:first-child {
        background: linear-gradient(180deg, #e4f7dd 0%, #c2eeb4 100%) !important;
        border: 1px solid #60b044 !important;
        border-radius: 14px !important;
        padding: 5px 10px !important;
        color: #156015 !important;
        font-weight: 700 !important;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    }
    section[data-testid="stSidebar"] div[style*="padding: 0 4px;"] > div:last-child {
        color: #475569 !important;
        font-weight: 500 !important;
    }

    /* 3. Dashboard Top Header Banner */
    .dashboard-header-banner {
        background: linear-gradient(180deg, #3d88f6 0%, #1664e8 50%, #004ecc 100%) !important;
        border: 1px solid #003bb3 !important;
        border-radius: 6px !important;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.45), 0 2px 5px rgba(0, 60, 160, 0.2) !important;
        padding: 8px 14px !important;
        color: #ffffff !important;
    }
    .dashboard-header-shield {
        display: inline-flex !important;
        align-items: center !important;
        color: #ffffff !important;
        font-size: 1.5rem !important;
        margin-right: 10px !important;
        filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.35)) !important;
    }
    .dashboard-header-shield .nf-icon {
        color: #ffffff !important;
    }
    .dashboard-header-title {
        color: #ffffff !important;
        font-size: 1.45rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.3px !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.35) !important;
    }
    .dashboard-pill-updated {
        background: #ffffff !important;
        border: 1px solid #7f9db9 !important;
        border-radius: 14px !important;
        color: #0c3276 !important;
        padding: 4px 12px !important;
        font-weight: 600 !important;
        box-shadow: inset 0 1px 0 #ffffff, 0 1px 2px rgba(0, 0, 0, 0.1) !important;
    }
    .dashboard-pill-updated .dashboard-pill-time {
        color: #000000 !important;
        font-weight: 700 !important;
    }
    .dashboard-pill-active {
        background: linear-gradient(180deg, #109e38 0%, #0a7328 100%) !important;
        border: 1px solid #07591e !important;
        border-radius: 14px !important;
        color: #ffffff !important;
        padding: 4px 12px !important;
        font-weight: 700 !important;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.35), 0 1px 2px rgba(0, 0, 0, 0.15) !important;
    }
    .dashboard-header-subtitle {
        color: #0044aa !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        margin-top: 8px !important;
    }

    /* 4. Windows XP Luna Blue Card Containers */
    .cyber-card {
        background: #ffffff !important;
        border: 1px solid #0055ea !important;
        border-radius: 6px !important;
        box-shadow: 0 2px 5px rgba(0, 50, 150, 0.12) !important;
        padding: 0 !important;
        overflow: hidden !important;
        margin-bottom: 14px !important;
    }
    .cyber-card:hover {
        border-color: #0044cc !important;
    }

    /* Glossy Luna Blue Header Bar on Cards */
    .cyber-card .card-title-row,
    .cyber-card > .card-title {
        background: linear-gradient(180deg, #3d88f6 0%, #1664e8 50%, #004ecc 100%) !important;
        border-bottom: 1px solid #003bb3 !important;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.45) !important;
        border-radius: 5px 5px 0 0 !important;
        padding: 6px 12px !important;
        margin: 0 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
    }
    .cyber-card .card-title,
    .cyber-card .card-title span,
    .cyber-card .card-title .nf-icon {
        color: #ffffff !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
    }

    /* Card Subtitle */
    .cyber-card .card-subtitle {
        color: #0c3276 !important;
        font-weight: 600 !important;
        font-size: 0.74rem !important;
        padding: 6px 12px !important;
        margin: 0 !important;
        background: #f8fafd !important;
        border-bottom: 1px solid #e2ecf9 !important;
    }

    /* 5. Top Metric Cards */
    .metric-card {
        border-bottom: none !important;
        border-radius: 6px 6px 0 0 !important;
        margin-bottom: 0 !important;
    }
    .metric-card .metric-big-val {
        padding: 8px 12px 2px 12px !important;
        font-size: 1.85rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
        margin-bottom: 0 !important;
    }
    .metric-cpu .metric-big-val { color: #0c48b8 !important; }
    .metric-ram .metric-big-val { color: #6b21a8 !important; }
    .metric-disk .metric-big-val { color: #854d0e !important; }
    .metric-proc .metric-big-val { color: #15803d !important; }

    /* Sparklines connected to metric cards */
    div[data-testid="column"]:has(.metric-card) div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }
    div[data-testid="column"]:has(.chart-card-header) div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }
    div[data-testid="column"]:has(.metric-card) div[data-testid="stPlotlyChart"] {
        background: #ffffff !important;
        border: 1px solid #0055ea !important;
        border-top: none !important;
        border-radius: 0 0 6px 6px !important;
        box-shadow: 0 2px 4px rgba(0, 50, 150, 0.1) !important;
        margin-top: 0 !important;
        padding-bottom: 4px !important;
    }

    /* 6. Telemetry History Charts */
    .chart-card-header {
        background: linear-gradient(180deg, #3d88f6 0%, #1664e8 50%, #004ecc 100%) !important;
        color: #ffffff !important;
        border: 1px solid #0055ea !important;
        border-bottom: 1px solid #003bb3 !important;
        border-radius: 6px 6px 0 0 !important;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.45) !important;
        padding: 6px 12px !important;
        margin-bottom: 0 !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
    }
    .chart-card-header .nf-icon {
        color: #ffffff !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    div[data-testid="column"]:has(.chart-card-header) div[data-testid="stPlotlyChart"] {
        background: #ffffff !important;
        border: 1px solid #0055ea !important;
        border-top: none !important;
        border-radius: 0 0 6px 6px !important;
        box-shadow: 0 2px 4px rgba(0, 50, 150, 0.1) !important;
        overflow: hidden !important;
    }

    /* 7. Tables */
    .cyber-card .cyber-table {
        width: 100% !important;
        border-collapse: collapse !important;
    }
    .cyber-card .cyber-table th {
        background: linear-gradient(180deg, #3d88f6 0%, #1664e8 100%) !important;
        color: #ffffff !important;
        border-bottom: 1px solid #003bb3 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.25) !important;
        font-weight: 700 !important;
        font-size: 0.78rem !important;
        padding: 6px 10px !important;
        text-shadow: 0 1px 1px rgba(0, 0, 0, 0.25) !important;
    }
    .cyber-card .cyber-table th:last-child {
        border-right: none !important;
    }
    .cyber-card .cyber-table td {
        background: #ffffff !important;
        border-bottom: 1px solid #d8e4f8 !important;
        border-right: 1px solid #edf3fc !important;
        color: #0c3276 !important;
        font-size: 0.78rem !important;
        padding: 6px 10px !important;
    }
    .cyber-card .cyber-table td:last-child {
        border-right: none !important;
    }
    .cyber-card .cyber-table td.accent-blue {
        color: #003399 !important;
        font-weight: 700 !important;
    }
    .cyber-card .cyber-table td.accent-purple {
        color: #003399 !important;
        font-weight: 600 !important;
    }
    .cyber-card .cyber-table td.accent-yellow {
        color: #854d0e !important;
        font-weight: 700 !important;
    }
    .cyber-card .cyber-table tr:hover td {
        background-color: #eef4ff !important;
    }

    /* 8. XP Beveled Buttons & Inputs */
    div[data-testid="stButton"] > button,
    div[data-testid="stDownloadButton"] > button {
        background: linear-gradient(180deg, #ffffff 0%, #ece9d8 50%, #d8d4c2 100%) !important;
        border: 1px solid #7f9db9 !important;
        border-radius: 3px !important;
        color: #000000 !important;
        box-shadow: inset 0 1px 0 #ffffff !important;
        font-weight: 600 !important;
    }
    div[data-testid="stButton"] > button:hover,
    div[data-testid="stDownloadButton"] > button:hover {
        border-color: #0055ea !important;
        color: #003399 !important;
        box-shadow: 0 1px 3px rgba(0, 85, 234, 0.25) !important;
    }
    div[data-baseweb="input"] > div,
    div[data-testid="stTextInput"] div[data-baseweb="base-input"] {
        background-color: #ffffff !important;
        border: 1px solid #7f9db9 !important;
        border-radius: 2px !important;
        box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.1) !important;
    }
    div[data-baseweb="tab-list"] {
        border-bottom: 2px solid #0055ea !important;
    }
    button[data-baseweb="tab"] {
        color: #003399 !important;
        font-weight: 600 !important;
        background-color: #ece9d8 !important;
        border: 1px solid #7f9db9 !important;
        border-bottom: none !important;
        border-radius: 4px 4px 0 0 !important;
        margin-right: 4px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: #ffffff !important;
        color: #0055ea !important;
        font-weight: 700 !important;
        border-top: 3px solid #ff9900 !important;
        border-bottom: 1px solid #ffffff !important;
    }
    """,
)

# 4. Classic Light (Original Preserved Theme with enhanced contrast)
CLASSIC_LIGHT = ThemeTokens(
    key="classic_light",
    name="Classic Light",
    group="Light",
    is_dark=False,
    background="#f8fafc",
    surface="#f1f5f9",
    surface_alt="#e2e8f0",
    card="#ffffff",
    card_border="#cbd5e1",
    card_hover="#e2e8f0",
    card_shadow="0 2px 10px rgba(0, 0, 0, 0.06)",
    text="#0f172a",
    text_secondary="#1e293b",
    text_muted="#475569",
    accent="#0284c7",
    accent_secondary="#7c3aed",
    accent_blue="#0284c7",
    accent_purple="#7c3aed",
    accent_yellow="#b45309",
    accent_green="#15803d",
    accent_red="#b91c1c",
    success="#15803d",
    warning="#b45309",
    error="#b91c1c",
    info="#0284c7",
    button_bg="#ffffff",
    button_hover="#f1f5f9",
    button_text="#0f172a",
    button_border="#cbd5e1",
    input_bg="#ffffff",
    input_border="#cbd5e1",
    input_text="#0f172a",
    table_header_bg="#f1f5f9",
    table_header_text="#1e293b",
    table_border="#e2e8f0",
    table_row_hover="#f8fafc",
    badge_safe_bg="rgba(21, 128, 61, 0.12)",
    badge_safe_border="rgba(21, 128, 61, 0.35)",
    badge_safe_text="#15803d",
    badge_risk_bg="rgba(185, 28, 28, 0.12)",
    badge_risk_border="rgba(185, 28, 28, 0.35)",
    badge_risk_text="#b91c1c",
    badge_warn_bg="rgba(180, 83, 9, 0.12)",
    badge_warn_border="rgba(180, 83, 9, 0.35)",
    badge_warn_text="#b45309",
    chart_bg="#ffffff",
    chart_grid="#f1f5f9",
    chart_border="#e2e8f0",
    chart_title="#0f172a",
    chart_text="#475569",
    sec_border="#e2e8f0",
)
