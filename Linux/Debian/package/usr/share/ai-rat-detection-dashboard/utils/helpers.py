"""
AI-RAT-Detection-Dashboard - Helper Utilities
String sanitization, formatting, and time helpers.
"""

import datetime
from pathlib import Path
from typing import Union


def format_bytes(bytes_value: Union[int, float]) -> str:
    """Format bytes into human-readable string (KB, MB, GB)."""
    if not bytes_value or bytes_value < 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    val = float(bytes_value)
    while val >= 1024.0 and i < len(units) - 1:
        val /= 1024.0
        i += 1
    return f"{val:.1f} {units[i]}"


def get_current_timestamp() -> str:
    """Return current timestamp in standard ISO-like display format."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def sanitize_string(val: str, max_len: int = 100) -> str:
    """Clean string of control characters and trim to length."""
    if not val:
        return ""
    clean = "".join(ch for ch in str(val) if ch.isprintable())
    return clean[:max_len]


def normalize_path(path_str: str) -> str:
    """Safely format and resolve a Windows path string."""
    if not path_str:
        return ""
    try:
        return str(Path(path_str).resolve())
    except Exception:
        return str(path_str)
