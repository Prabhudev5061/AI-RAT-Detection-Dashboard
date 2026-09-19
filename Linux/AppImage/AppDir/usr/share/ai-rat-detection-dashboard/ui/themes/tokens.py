"""
AI-RAT-Detection-Dashboard - Theme Tokens Definition
Defines the theme schema, tokens, and CSS variable generators.
"""

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class ThemeTokens:
    # Metadata
    key: str
    name: str
    group: str  # "Dark" or "Light"
    is_dark: bool

    # Surfaces & Containers
    background: str
    surface: str
    surface_alt: str
    card: str
    card_border: str
    card_hover: str
    card_shadow: str

    # Typography
    text: str
    text_secondary: str
    text_muted: str

    # Accents & Palettes
    accent: str
    accent_secondary: str
    accent_blue: str
    accent_purple: str
    accent_yellow: str
    accent_green: str
    accent_red: str

    # Status & Alerts
    success: str
    warning: str
    error: str
    info: str

    # Controls: Buttons & Inputs
    button_bg: str
    button_hover: str
    button_text: str
    button_border: str
    input_bg: str
    input_border: str
    input_text: str

    # Tables
    table_header_bg: str
    table_header_text: str
    table_border: str
    table_row_hover: str

    # Status Badges
    badge_safe_bg: str
    badge_safe_border: str
    badge_safe_text: str
    badge_risk_bg: str
    badge_risk_border: str
    badge_risk_text: str
    badge_warn_bg: str
    badge_warn_border: str
    badge_warn_text: str

    # Charts (Plotly)
    chart_bg: str
    chart_grid: str
    chart_border: str
    chart_title: str
    chart_text: str

    # Dividers
    sec_border: str

    # Optional special enhancements
    transparency_css: str = ""
    custom_css: str = ""

    def to_css_variables(self) -> str:
        """Converts tokens into CSS custom property declarations (:root)."""
        return f"""
    --background: {self.background};
    --app-bg: {self.background};
    --app-text: {self.text};
    --surface: {self.surface};
    --surface-alt: {self.surface_alt};
    --sidebar-bg: {self.surface};
    --sidebar-border: {self.sec_border};
    --card: {self.card};
    --card-bg: {self.card};
    --card-border: {self.card_border};
    --card-hover: {self.card_hover};
    --card-shadow: {self.card_shadow};
    --border: {self.card_border};
    --text: {self.text};
    --text-primary: {self.text};
    --text-secondary: {self.text_secondary};
    --text-muted: {self.text_muted};
    --text-disabled: {self.text_muted};
    --icon: {self.text};
    --icon-muted: {self.text_muted};
    --accent: {self.accent};
    --accent-hover: {self.accent_secondary};
    --accent-secondary: {self.accent_secondary};
    --accent-blue: {self.accent_blue};
    --accent-purple: {self.accent_purple};
    --accent-yellow: {self.accent_yellow};
    --accent-green: {self.accent_green};
    --accent-red: {self.accent_red};
    --success: {self.success};
    --warning: {self.warning};
    --error: {self.error};
    --info: {self.info};
    --status-success: {self.success};
    --status-warning: {self.warning};
    --status-error: {self.error};
    --status-info: {self.info};
    --navigation: {self.text_secondary};
    --navigation-hover: {self.accent_blue};
    --navigation-active: {self.accent_blue};
    --btn-bg: {self.button_bg};
    --btn-hover: {self.button_hover};
    --btn-text: {self.button_text};
    --btn-border: {self.button_border};
    --input-background: {self.input_bg};
    --input-bg: {self.input_bg};
    --input-border: {self.input_border};
    --input-text: {self.input_text};
    --input-placeholder: {self.text_muted};
    --table-background: {self.card};
    --table-header: {self.table_header_bg};
    --table-header-bg: {self.table_header_bg};
    --table-header-text: {self.table_header_text};
    --table-text: {self.text_secondary};
    --table-border: {self.table_border};
    --table-row-hover: {self.table_row_hover};
    --badge-safe-bg: {self.badge_safe_bg};
    --badge-safe-border: {self.badge_safe_border};
    --badge-safe-text: {self.badge_safe_text};
    --badge-risk-bg: {self.badge_risk_bg};
    --badge-risk-border: {self.badge_risk_border};
    --badge-risk-text: {self.badge_risk_text};
    --badge-warn-bg: {self.badge_warn_bg};
    --badge-warn-border: {self.badge_warn_border};
    --badge-warn-text: {self.badge_warn_text};
    --chart-bg: {self.chart_bg};
    --chart-grid: {self.chart_grid};
    --chart-border: {self.chart_border};
    --chart-title: {self.chart_title};
    --chart-text: {self.chart_text};
    --shadow: {self.card_shadow};
    --sec-border: {self.sec_border};
        """.strip()
