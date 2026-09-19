"""
AI-RAT-Detection-Dashboard - UI Stylesheet & Theme System
Provides complete modular theme integration, embedding JetBrains Mono Nerd Font
locally as Base64 for 100% offline, production-ready desktop execution with zero external network dependencies.
"""

import base64
import logging
from pathlib import Path
from config.config import ASSETS_DIR
from ui.themes.manager import generate_theme_css, get_theme, CYBER_DARK, CLASSIC_LIGHT

logger = logging.getLogger("UIStyles")

# Global font cache to avoid re-reading disk
_FONT_FACE_CSS = ""


def _load_embedded_fonts() -> str:
    """
    Encodes local JetBrains Mono and JetBrains Mono Nerd Font TTF files into @font-face base64 CSS.
    Provides local OS fallback and system monospace fallback.
    """
    global _FONT_FACE_CSS
    if _FONT_FACE_CSS:
        return _FONT_FACE_CSS

    css_parts = []
    fonts_dir = ASSETS_DIR / "fonts"

    # 1. JetBrains Mono Nerd Font (includes thousands of icon glyphs)
    nf_reg_path = fonts_dir / "JetBrainsMonoNerdFont-Regular.ttf"
    nf_bold_path = fonts_dir / "JetBrainsMonoNerdFont-Bold.ttf"

    try:
        if nf_reg_path.exists():
            b64_nf_reg = base64.b64encode(nf_reg_path.read_bytes()).decode("ascii")
            css_parts.append(
                f"""
                @font-face {{
                    font-family: 'JetBrainsMono Nerd Font';
                    src: local('JetBrainsMono Nerd Font'),
                         local('JetBrainsMono NF'),
                         url('data:font/ttf;charset=utf-8;base64,{b64_nf_reg}') format('truetype');
                    font-weight: 400;
                    font-style: normal;
                    font-display: swap;
                }}
                """
            )
        if nf_bold_path.exists():
            b64_nf_bold = base64.b64encode(nf_bold_path.read_bytes()).decode("ascii")
            css_parts.append(
                f"""
                @font-face {{
                    font-family: 'JetBrainsMono Nerd Font';
                    src: local('JetBrainsMono Nerd Font Bold'),
                         local('JetBrainsMono NF Bold'),
                         url('data:font/ttf;charset=utf-8;base64,{b64_nf_bold}') format('truetype');
                    font-weight: 700;
                    font-style: normal;
                    font-display: swap;
                }}
                """
            )
    except Exception as e:
        logger.warning(f"Could not load Nerd Font files: {e}")

    # 2. Standard JetBrains Mono (for backward compatibility and font chain)
    reg_path = fonts_dir / "JetBrainsMono-Regular.ttf"
    bold_path = fonts_dir / "JetBrainsMono-Bold.ttf"

    try:
        if reg_path.exists():
            b64_reg = base64.b64encode(reg_path.read_bytes()).decode("ascii")
            css_parts.append(
                f"""
                @font-face {{
                    font-family: 'JetBrains Mono';
                    src: local('JetBrains Mono'),
                         url('data:font/ttf;charset=utf-8;base64,{b64_reg}') format('truetype');
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
                    src: local('JetBrains Mono Bold'),
                         url('data:font/ttf;charset=utf-8;base64,{b64_bold}') format('truetype');
                    font-weight: 700;
                    font-style: normal;
                    font-display: swap;
                }}
                """
            )
    except Exception as e:
        logger.warning(f"Could not load standard JetBrains Mono font files: {e}")

    _FONT_FACE_CSS = "\n".join(css_parts)
    return _FONT_FACE_CSS


# Backward-compatible palette variables for legacy references and tests
DARK_VARS = CYBER_DARK.to_css_variables()
LIGHT_VARS = CLASSIC_LIGHT.to_css_variables()


def get_theme_css(theme: str = "dark") -> str:
    """
    Generates complete injected CSS stylesheet with embedded JetBrains Mono Nerd Font
    and CSS variable tokens for the specified theme.
    Supports all 8 themes (Catppuccin, Dracula, Nord, Cyber Dark, White Slur, Gruvbox, Windows XP, Classic Light)
    as well as aliases 'dark', 'light', and 'system'.
    """
    fonts_css = _load_embedded_fonts()
    normalized_theme = theme.lower().strip() if theme else "dark"

    # Support 'system' mode with media query
    if normalized_theme == "system":
        dark_vars = CYBER_DARK.to_css_variables()
        light_vars = CLASSIC_LIGHT.to_css_variables()
        system_root = f"""
        :root {{
            {dark_vars}
        }}
        @media (prefers-color-scheme: light) {{
            :root {{
                {light_vars}
            }}
        }}
        """
        base_css = generate_theme_css("cyber_dark", fonts_css=fonts_css)
        # Replace the :root block with media query root
        return base_css.replace(f":root {{\n    {dark_vars}\n    }}", system_root)

    return generate_theme_css(normalized_theme, fonts_css=fonts_css)


# Backward-compatible constant
DARK_THEME_CSS = get_theme_css("dark")
