"""
Unit tests for UI Theme System, Embedded Fonts, Nerd Font Icons, and Persistent Settings
"""

import pytest
from pathlib import Path
from config.config import load_settings, save_settings, SETTINGS_FILE, ASSETS_DIR
from ui.styles import get_theme_css, DARK_THEME_CSS
from ui.icons import ICONS, get_icon, icon_html, icon_with_label
from ui.themes.manager import (
    THEMES,
    get_theme,
    normalize_theme_key,
    get_grouped_themes,
    get_theme_names_list,
    get_key_from_display_name,
    get_plotly_theme_config,
)
from desktop_app import find_free_port


def test_embedded_jetbrains_mono_nerd_font():
    """Verifies that JetBrains Mono and Nerd Font files exist and are base64-embedded."""
    fonts_dir = ASSETS_DIR / "fonts"
    assert (fonts_dir / "JetBrainsMono-Regular.ttf").exists()
    assert (fonts_dir / "JetBrainsMono-Bold.ttf").exists()
    assert (fonts_dir / "JetBrainsMonoNerdFont-Regular.ttf").exists()
    assert (fonts_dir / "JetBrainsMonoNerdFont-Bold.ttf").exists()

    css = get_theme_css("cyber_dark")
    assert "font-family: 'JetBrainsMono Nerd Font'" in css
    assert "font-family: 'JetBrains Mono'" in css
    assert "data:font/ttf;charset=utf-8;base64," in css


def test_all_eight_themes_generate_css():
    """Verifies that all 8 themes generate valid CSS with matching tokens."""
    expected_themes = [
        "catppuccin_dark",
        "dracula_dark",
        "nord_dark",
        "cyber_dark",
        "white_slur",
        "gruvbox_light",
        "windows_xp",
        "classic_light",
    ]

    for key in expected_themes:
        assert key in THEMES, f"Theme {key} missing from registry"
        theme = get_theme(key)
        css = get_theme_css(key)

        assert f"--app-bg: {theme.background};" in css
        assert f"--card-bg: {theme.card};" in css
        assert f"--text-primary: {theme.text};" in css
        assert f"--accent-blue: {theme.accent_blue};" in css
        assert ".cyber-card" in css
        assert ".cyber-table" in css


def test_sidebar_and_widgets_css_overrides():
    """Verifies that sidebar, stRadio, stToggle, selectbox popovers, and stAlert CSS rules are present."""
    css = get_theme_css("white_slur")
    assert 'section[data-testid="stSidebar"]' in css
    assert 'div[data-testid="stRadio"]' in css
    assert 'div[data-testid="stToggle"]' in css
    assert 'div[data-testid="stWidgetLabel"]' in css
    assert 'div[data-testid="stAlert"]' in css
    assert 'div[data-baseweb="popover"]' in css
    assert 'li[role="option"]' in css


def test_light_theme_text_contrast():
    """Verifies all Light themes use dark, high-contrast typography tokens."""
    light_keys = ["white_slur", "gruvbox_light", "windows_xp", "classic_light"]
    for key in light_keys:
        theme = get_theme(key)
        assert theme.group == "Light"
        assert not theme.is_dark
        # Ensure text color starts with dark values (not white or pale light grey)
        # e.g., #0f172a, #282828, #000000
        text_hex = theme.text.lstrip("#")
        assert len(text_hex) == 6
        r, g, b = int(text_hex[0:2], 16), int(text_hex[2:4], 16), int(text_hex[4:6], 16)
        # Relative luminance proxy: should be dark (sum of components < 300)
        assert r + g + b < 300, f"Theme {key} text color #{text_hex} is too bright for light background"



def test_white_slur_theme_translucency():
    """Verifies White Slur clean translucency and backdrop filter."""
    ws = get_theme("white_slur")
    assert ws.name == "White Slur"
    assert not ws.is_dark
    assert ws.group == "Light"
    assert "rgba" in ws.card

    css = get_theme_css("white_slur")
    assert "backdrop-filter: blur" in css
    assert ws.background in css


def test_windows_xp_theme_styling():
    """Verifies Windows XP Luna desktop blue and classic panels."""
    xp = get_theme("windows_xp")
    assert xp.name == "Windows XP Light"
    assert xp.accent_blue == "#0055ea"
    assert xp.surface == "#ece9d8"

    css = get_theme_css("windows_xp")
    assert "--accent-blue: #0055ea;" in css
    assert "--sidebar-bg: #ece9d8;" in css


def test_centralized_icons_mapping():
    """Verifies that Nerd Font icons are mapped to valid non-empty Unicode characters."""
    critical_icons = [
        "shield", "dashboard", "desktop", "cpu", "memory", "disk", "process",
        "warning", "success", "error", "settings", "database", "search",
        "network", "terminal", "bolt", "clock", "camera", "microphone",
        "screen", "remote", "report", "folder", "download", "save", "palette",
        "chart_line", "chart_bar", "pulse", "startup", "parent_child", "brain",
    ]

    for name in critical_icons:
        glyph = get_icon(name)
        assert glyph, f"Icon {name} returned empty glyph"
        assert len(glyph) >= 1
        # Codepoint should be in Private Use Area (PUA) or standard unicode
        cp = ord(glyph[0])
        assert (0xE000 <= cp <= 0xF8FF) or (0xF0000 <= cp <= 0x10FFFF) or (0x2000 <= cp <= 0x2BFF), f"Icon {name} codepoint {hex(cp)} out of expected range"


def test_icon_html_generation():
    """Verifies icon_html and icon_with_label produce accessible HTML."""
    html = icon_html("shield", extra_classes="test-class", extra_styles="color:red;")
    assert 'class="nf-icon test-class"' in html
    assert 'aria-hidden="true"' in html
    assert "color:red;" in html

    labeled = icon_with_label("settings", "Configuration")
    assert "Configuration" in labeled
    assert "nf-icon" in labeled


def test_theme_normalization_and_aliases():
    """Verifies aliases and normalizations resolve cleanly."""
    assert normalize_theme_key("dark") == "cyber_dark"
    assert normalize_theme_key("light") == "classic_light"
    assert normalize_theme_key("catppuccin") == "catppuccin_dark"
    assert normalize_theme_key("dracula") == "dracula_dark"
    assert normalize_theme_key("nord") == "nord_dark"
    assert normalize_theme_key("white slur") == "white_slur"
    assert normalize_theme_key("gruvbox") == "gruvbox_light"
    assert normalize_theme_key("windows xp") == "windows_xp"
    assert normalize_theme_key("system") == "cyber_dark"
    assert normalize_theme_key("UNKNOWN_XYZ") == "cyber_dark"


def test_plotly_theme_config():
    """Verifies Plotly chart styling output for dark and light palettes."""
    dark_cfg = get_plotly_theme_config("nord_dark")
    assert dark_cfg["is_dark"] is True
    assert dark_cfg["bg_color"] == "#2e3440"
    assert dark_cfg["title_color"] == "#eceff4"

    light_cfg = get_plotly_theme_config("white_slur")
    assert light_cfg["is_dark"] is False
    assert light_cfg["bg_color"] == "#ffffff"
    assert light_cfg["title_color"] == "#0f172a"


def test_settings_load_and_save():
    """Verifies persistent settings loading and saving across themes."""
    settings = load_settings()
    assert "theme" in settings
    assert "refresh_interval" in settings
    assert "auto_refresh_enabled" in settings

    # Test saving each of the 8 themes
    for key in THEMES:
        test_settings = dict(settings)
        test_settings["theme"] = key
        test_settings["refresh_interval"] = 15
        assert save_settings(test_settings) is True

        reloaded = load_settings()
        assert reloaded["theme"] == key
        assert reloaded["refresh_interval"] == 15

    # Restore default
    test_settings["theme"] = "cyber_dark"
    test_settings["refresh_interval"] = 5
    save_settings(test_settings)


def test_find_free_port():
    """Verifies free TCP port allocator."""
    port = find_free_port(start_port=8501)
    assert isinstance(port, int)
    assert 1024 <= port <= 65535
