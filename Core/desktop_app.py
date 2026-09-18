"""
AI RAT Detection & System Network Monitoring Dashboard
Production Desktop Application Entrypoint.

Starts the embedded local monitoring service and Streamlit web engine,
then renders the application inside a native Windows desktop window using pywebview (Edge WebView2).
Includes fallback to Windows App Mode (msedge/chrome) if WebView2 runtime is unavailable.
"""

import os
import sys
import time
import socket
import signal
import logging
import threading
import urllib.request
import subprocess
from pathlib import Path

# Explicit imports so PyInstaller static analyzer bundles all dependencies used in app.py
import psutil
import pandas
import plotly
import plotly.graph_objects
import reportlab
import reportlab.lib
import reportlab.lib.pagesizes
import reportlab.lib.styles
import reportlab.lib.colors
import reportlab.platypus
import reportlab.pdfgen

# Guard against NoneType stdout/stderr in Windows GUI/noconsole mode
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w", encoding="utf-8")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w", encoding="utf-8")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("DesktopApp")

# Resolve bundle and app directories
if getattr(sys, "frozen", False):
    BUNDLE_DIR = Path(sys._MEIPASS)
    APP_DIR = Path(sys.executable).resolve().parent
else:
    BUNDLE_DIR = Path(__file__).resolve().parent
    APP_DIR = BUNDLE_DIR

APP_SCRIPT = str(BUNDLE_DIR / "app.py")
ICON_PATH = str(BUNDLE_DIR / "assets" / "icon.ico")


def find_free_port(start_port: int = 8501, max_attempts: int = 100) -> int:
    """Finds an available local TCP port starting from start_port."""
    for p in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", p))
                return p
            except OSError:
                continue
    # Ephemeral port fallback
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def patch_signal_handlers():
    """Allows streamlit bootstrap to run inside a background thread without raising ValueError."""
    orig_signal = signal.signal

    def safe_signal(sig, handler):
        try:
            return orig_signal(sig, handler)
        except (ValueError, OSError):
            return None

    signal.signal = safe_signal


def start_streamlit_server(port: int):
    """Launches the Streamlit server in a background thread."""
    patch_signal_handlers()

    # Crucial: Explicitly disable development mode so Streamlit serves bundled static assets
    # and does not redirect to Vite dev port 3000
    os.environ["STREAMLIT_GLOBAL_DEVELOPMENT_MODE"] = "false"
    os.environ["STREAMLIT_SERVER_PORT"] = str(port)
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    os.environ["STREAMLIT_SERVER_ADDRESS"] = "127.0.0.1"
    os.environ["STREAMLIT_BROWSER_SERVER_ADDRESS"] = "127.0.0.1"
    os.environ["STREAMLIT_BROWSER_SERVER_PORT"] = str(port)
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    os.environ["STREAMLIT_SERVER_ENABLE_CORS"] = "false"
    os.environ["STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION"] = "false"

    try:
        import streamlit.config as _st_config
        _st_config.set_option("global.developmentMode", False)
        _orig_get_option = _st_config.get_option
        def _safe_get_option(opt):
            if opt == "global.developmentMode":
                return False
            return _orig_get_option(opt)
        _st_config.set_option("server.port", port)
        _st_config.set_option("server.address", "127.0.0.1")
        _st_config.set_option("browser.serverPort", port)
    except Exception:
        pass

    flag_options = {
        "server.port": port,
        "server.headless": True,
        "server.address": "127.0.0.1",
        "browser.serverAddress": "127.0.0.1",
        "browser.serverPort": port,
        "browser.gatherUsageStats": False,
        "server.enableCORS": False,
        "server.enableXsrfProtection": False,
        "global.developmentMode": False,
        "client.showErrorDetails": False,
        "client.toolbarMode": "minimal",
    }

    from streamlit.web import bootstrap
    logger.info(f"Starting Streamlit engine on 127.0.0.1:{port}...")
    bootstrap.run(APP_SCRIPT, is_hello=False, args=[f"--server.port={port}"], flag_options=flag_options)


def hide_console_window():
    """Hides the console window on Windows to prevent terminal flicker during desktop launch."""
    if sys.platform == "win32":
        try:
            import ctypes
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd:
                ctypes.windll.user32.ShowWindow(hwnd, 0)
        except Exception:
            pass


def wait_for_server(port: int, timeout: float = 30.0) -> bool:
    """Polls the Streamlit server health endpoint until healthy or timeout expires."""
    url = f"http://127.0.0.1:{port}/_stcore/health"
    start_time = time.time()
    logger.info("Waiting for telemetry server to report healthy status...")

    while time.time() - start_time < timeout:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AI-RAT-Monitor-HealthCheck"})
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                if resp.status == 200:
                    logger.info(f"Streamlit server is ready on port {port} (elapsed: {time.time() - start_time:.2f}s)")
                    return True
        except Exception:
            pass
        time.sleep(0.35)

    logger.error("Timed out waiting for Streamlit server.")
    return False


def on_window_closed():
    """Cleanly terminates background telemetry collectors and exits the application."""
    logger.info("Desktop window closed. Cleaning up background services...")
    try:
        from services.monitoring_service import monitoring_service
        monitoring_service.stop(timeout=1.0)
    except Exception:
        pass
    os._exit(0)


def launch_browser_fallback(url: str):
    """Fallback if pywebview fails: launches Edge or default browser in app mode."""
    logger.warning("Launching browser app mode fallback...")
    edge_paths = [
        os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
    ]
    for ep in edge_paths:
        if os.path.exists(ep):
            try:
                subprocess.Popen([ep, f"--app={url}", "--window-size=1366,850"])
                return
            except Exception:
                pass

    import webbrowser
    webbrowser.open(url)


def main():
    """Main desktop application entrypoint."""
    # Hide terminal/console window on Windows
    hide_console_window()

    # Ensure working directory is correct
    os.chdir(str(BUNDLE_DIR))

    # Allocate port
    port = find_free_port(start_port=8501)
    app_url = f"http://127.0.0.1:{port}"

    # Start server in background thread
    server_thread = threading.Thread(
        target=start_streamlit_server,
        args=(port,),
        name="StreamlitServerThread",
        daemon=True,
    )
    server_thread.start()

    # Wait for server ready
    if not wait_for_server(port, timeout=30.0):
        print("Error: Could not start application telemetry backend.", file=sys.stderr)
        sys.exit(1)

    # Resolve icon path
    if sys.platform == "win32":
        icon_file = BUNDLE_DIR / "assets" / "icon.ico"
    else:
        icon_file = BUNDLE_DIR / "assets" / "icon.png"
    icon_path_str = str(icon_file) if icon_file.exists() else None

    # Launch Desktop Webview
    try:
        import webview
        from config.config import load_settings
        from ui.themes.manager import get_theme, normalize_theme_key

        saved_cfg = load_settings()
        theme_key = normalize_theme_key(saved_cfg.get("theme", "cyber_dark"))
        window_bg = get_theme(theme_key).background
        if window_bg.startswith("rgba"):
            window_bg = "#f8fafc"

        logger.info("Initializing native desktop window container...")
        window = webview.create_window(
            title="AI RAT Detection Dashboard",
            url=app_url,
            width=1366,
            height=850,
            min_size=(1024, 680),
            background_color=window_bg,
            easy_drag=False,
        )

        # Attach clean exit handler
        window.events.closed += on_window_closed

        # Start native window
        webview.start(
            icon=icon_path_str,
            debug=False,
            http_server=False,
        )

    except Exception as e:
        logger.error(f"pywebview initialization failed ({e}). Falling back to browser app mode.")
        launch_browser_fallback(app_url)
        # Keep process alive until user closes
        try:
            while True:
                time.sleep(2)
        except KeyboardInterrupt:
            on_window_closed()


if __name__ == "__main__":
    main()
