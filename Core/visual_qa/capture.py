"""
AI-RAT-Detection-Dashboard - Visual QA Screenshot Capture Utility
Launches real Streamlit instance, iterates through pages and themes using Playwright,
and captures high-resolution screenshots for visual inspection.
Zero local AI models or external APIs - purely automates browser rendering.
"""

import os
import sys
import time
import socket
import urllib.request
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

CORE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CORE_DIR))

from desktop_app import find_free_port, start_streamlit_server, wait_for_server
from config.config import load_settings, save_settings

OUTPUT_DIR = CORE_DIR / "visual_qa" / "screenshots"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PAGES = [
    "Dashboard",
    "Live Monitor",
    "Process Analysis",
    "Network Monitor",
    "Security Tools",
    "Event Logs",
    "Reports",
    "Settings",
]

THEMES = [
    ("cyber_dark", "Cyber Dark"),
    ("catppuccin_dark", "Catppuccin Dark"),
    ("dracula_dark", "Dracula Dark"),
    ("nord_dark", "Nord Dark"),
    ("white_slur", "White Slur"),
    ("gruvbox_light", "Gruvbox Light"),
    ("windows_xp", "Windows XP Light"),
    ("classic_light", "Classic Light"),
]


def capture_all_views(port: int, theme_list=None, pages_list=None):
    """Launches Playwright headless Chromium to capture real application screenshots."""
    target_themes = theme_list or THEMES
    target_pages = pages_list or PAGES
    app_url = f"http://127.0.0.1:{port}"

    print(f"[Visual QA] Starting capture on {app_url}...")
    captured_files = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1366, "height": 850},
            device_scale_factor=1,
        )
        page = context.new_page()

        for theme_key, theme_name in target_themes:
            print(f"\n[Visual QA] Testing Theme: {theme_name} ({theme_key})...")
            clean_theme = theme_key.lower()

            for page_name in target_pages:
                clean_page = page_name.lower().replace(" ", "_")
                nav_url = f"{app_url}/?theme={theme_key}&page={clean_page}"
                try:
                    page.goto(nav_url, wait_until="networkidle", timeout=30000)
                    time.sleep(1.2)

                    filename = f"{clean_theme}_{clean_page}.png"
                    filepath = OUTPUT_DIR / filename

                    page.screenshot(path=str(filepath), full_page=False)
                    print(f"  Captured: {filename}")
                    captured_files.append(str(filepath))

                except Exception as e:
                    print(f"  Error capturing {page_name} in {theme_name}: {e}")

        browser.close()

    print(f"\n[Visual QA] Completed! Captured {len(captured_files)} screenshots in {OUTPUT_DIR}")
    return captured_files


if __name__ == "__main__":
    port = find_free_port(start_port=8580)
    server_thread = threading.Thread(
        target=start_streamlit_server,
        args=(port,),
        name="QAServerThread",
        daemon=True,
    )
    server_thread.start()

    if not wait_for_server(port, timeout=25.0):
        print("Failed to start Streamlit server for Visual QA.", file=sys.stderr)
        sys.exit(1)

    capture_all_views(port)