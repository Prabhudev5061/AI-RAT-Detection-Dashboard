"""
AI-RAT-Detection-Dashboard - Themes Package
Exports ThemeTokens, themes, and theme manager utilities.
"""

from ui.themes.tokens import ThemeTokens
from ui.themes.manager import (
    THEMES,
    THEME_ALIASES,
    get_theme,
    normalize_theme_key,
    get_grouped_themes,
    get_theme_names_list,
    get_key_from_display_name,
    get_plotly_theme_config,
    generate_theme_css,
)

__all__ = [
    "ThemeTokens",
    "THEMES",
    "THEME_ALIASES",
    "get_theme",
    "normalize_theme_key",
    "get_grouped_themes",
    "get_theme_names_list",
    "get_key_from_display_name",
    "get_plotly_theme_config",
    "generate_theme_css",
]
