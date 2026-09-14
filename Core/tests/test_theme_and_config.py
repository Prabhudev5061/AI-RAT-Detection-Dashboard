"""
Unit tests for UI Theme System, Embedded Fonts, and Persistent Settings
"""

import pytest
from pathlib import Path
from config.config import load_settings, save_settings, SETTINGS_FILE, ASSETS_DIR
from ui.styles import get_theme_css, DARK_THEME_CSS
from desktop_app import find_free_port


def test_embedded_jetbrains_mono_font():
    """Verifies that JetBrains Mono font files exist and are base64-embedded."""
    fonts_dir = ASSETS_DIR / "fonts"
    assert (fonts_dir / "JetBrainsMono-Regular.ttf").exists()
    assert (fonts_dir / "JetBrainsMono-Bold.ttf").exists()

    css = get_theme_css("dark")
    assert "font-family: 'JetBrains Mono'" in css
    assert "data:font/ttf;charset=utf-8;base64," in css


def test_theme_css_palettes():
    """Verifies Dark, Light, and System theme CSS palettes."""
    # Dark Mode
    dark_css = get_theme_css("dark")
    assert "--app-bg: #0b0f19;" in dark_css
    assert "--card-bg: #111827;" in dark_css
    assert "--text-primary: #f8fafc;" in dark_css

    # Light Mode
    light_css = get_theme_css("light")
    assert "--app-bg: #f8fafc;" in light_css
    assert "--card-bg: #ffffff;" in light_css
    assert "--text-primary: #0f172a;" in light_css

    # System Mode
    sys_css = get_theme_css("system")
    assert "prefers-color-scheme: light" in sys_css
    assert "--app-bg: #f8fafc;" in sys_css


def test_settings_load_and_save(tmp_path):
    """Verifies persistent settings loading and saving."""
    settings = load_settings()
    assert "theme" in settings
    assert "refresh_interval" in settings
    assert "auto_refresh_enabled" in settings

    # Modify and save
    test_settings = dict(settings)
    test_settings["theme"] = "light"
    test_settings["refresh_interval"] = 10
    assert save_settings(test_settings) is True

    reloaded = load_settings()
    assert reloaded["theme"] == "light"
    assert reloaded["refresh_interval"] == 10

    # Restore default dark
    test_settings["theme"] = "dark"
    test_settings["refresh_interval"] = 5
    save_settings(test_settings)


def test_find_free_port():
    """Verifies free TCP port allocator."""
    port = find_free_port(start_port=8501)
    assert isinstance(port, int)
    assert 1024 <= port <= 65535
