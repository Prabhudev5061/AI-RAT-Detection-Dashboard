"""
AI-RAT-Detection-Dashboard - Configuration Module
Defines settings, paths, thresholds, and detection criteria.
Supports environment variables and optional .env files.
"""

import sys
import os
import json
from pathlib import Path

# Base and Bundle Directories
if getattr(sys, "frozen", False):
    BUNDLE_DIR = Path(sys._MEIPASS)
    APP_DIR = Path(sys.executable).resolve().parent
else:
    BUNDLE_DIR = Path(__file__).resolve().parent.parent
    APP_DIR = BUNDLE_DIR

BASE_DIR = APP_DIR
DATA_DIR = APP_DIR / "data"
LOGS_DIR = APP_DIR / "logs"
REPORTS_DIR = APP_DIR / "reports"
ASSETS_DIR = BUNDLE_DIR / "assets"
SETTINGS_FILE = DATA_DIR / "settings.json"

# Ensure directories exist
for d in (DATA_DIR, LOGS_DIR, REPORTS_DIR):
    d.mkdir(parents=True, exist_ok=True)

DEFAULT_SETTINGS = {
    "theme": "dark",
    "refresh_interval": 5,
    "auto_refresh_enabled": True,
    "enable_net": True,
    "enable_startup": True,
}

def load_settings() -> dict:
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {**DEFAULT_SETTINGS, **data}
        except Exception:
            pass
    return DEFAULT_SETTINGS.copy()

def save_settings(settings: dict) -> bool:
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)
        return True
    except Exception:
        return False

# Helper: simple .env parser without external dependencies
def _load_env_file():
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'\"")
                        if k not in os.environ:
                            os.environ[k] = v
        except Exception:
            pass

_load_env_file()

# Database and Logging Paths
DATABASE_PATH = Path(os.environ.get("DATABASE_PATH", str(DATA_DIR / "monitoring.db")))
APP_LOG_PATH = Path(os.environ.get("APP_LOG_PATH", str(LOGS_DIR / "app.log")))

# Application Meta
APP_TITLE = os.environ.get("APP_TITLE", "AI RAT Detection Dashboard")
APP_SUBTITLE = os.environ.get("APP_SUBTITLE", "Real-Time AI Powered Cyber Security Monitoring")
APP_VERSION = "1.0.0"

# Monitoring Parameters
DEFAULT_REFRESH_INTERVAL = int(os.environ.get("REFRESH_INTERVAL_SECONDS", 5))  # Seconds
MAX_HISTORY_DATAPOINTS = int(os.environ.get("MAX_HISTORY_POINTS", 50))         # Points in live charts
DB_RETENTION_MAX_RECORDS = int(os.environ.get("DB_RETENTION_MAX_RECORDS", 5000))

# Risk Score Bands (0 - 100)
RISK_LEVEL_LOW = "LOW"
RISK_LEVEL_MEDIUM = "MEDIUM"
RISK_LEVEL_HIGH = "HIGH"
RISK_LEVEL_CRITICAL = "CRITICAL"

RISK_THRESHOLDS = {
    RISK_LEVEL_LOW: (0, 24),
    RISK_LEVEL_MEDIUM: (25, 49),
    RISK_LEVEL_HIGH: (50, 74),
    RISK_LEVEL_CRITICAL: (75, 100),
}

# Suspicious RAT / Backdoor / Shell Ports
SUSPICIOUS_PORTS = {
    4444: ("Metasploit Default Listener", "HIGH"),
    5555: ("FreeMetasploit / ADB / RAT backdoor", "HIGH"),
    8080: ("Alternative HTTP / Proxy / Backdoor listener", "MEDIUM"),
    3389: ("Remote Desktop (RDP) / Remote Access", "MEDIUM"),
    5900: ("VNC Remote Framebuffer Server", "HIGH"),
    1337: ("Elite / Hacker default backdoor port", "HIGH"),
    6667: ("IRC / Botnet C2 communication", "HIGH"),
    8888: ("Fiddler / Web Proxy / Common C2 port", "MEDIUM"),
    9999: ("Urchin / Common backdoor listener", "HIGH"),
    31337: ("Back Orifice C2 default port", "CRITICAL"),
    1604: ("DarkComet RAT default port", "CRITICAL"),
    1177: ("NjRAT default port", "CRITICAL"),
    65432: ("Generic Reverse Shell listener", "HIGH"),
}

# Suspicious Directory Keywords for Executables (Windows)
SUSPICIOUS_PATHS = [
    r"AppData\Local\Temp",
    r"AppData\Roaming",
    r"Windows\Temp",
    r"Users\Public",
    r"$Recycle.Bin",
    r"ProgramData\Temp",
]

# Suspicious Parent-Child Process Hierarchies
SUSPICIOUS_SPAWNS = {
    "winword.exe": ["cmd.exe", "powershell.exe", "wscript.exe", "cscript.exe", "mshta.exe"],
    "excel.exe": ["cmd.exe", "powershell.exe", "wscript.exe", "cscript.exe", "mshta.exe"],
    "powerpnt.exe": ["cmd.exe", "powershell.exe", "wscript.exe", "cscript.exe"],
    "outlook.exe": ["cmd.exe", "powershell.exe", "certutil.exe", "bitsadmin.exe"],
    "svchost.exe": ["cmd.exe", "powershell.exe", "whoami.exe", "net.exe"],
    "explorer.exe": ["vssadmin.exe", "bcdedit.exe"],
}

# Known Remote Access Tools (Legitimate or Abused)
KNOWN_REMOTE_TOOLS = [
    "anydesk.exe",
    "teamviewer.exe",
    "tv_x64.exe",
    "vncserver.exe",
    "radmin.exe",
    "remotedesktop.exe",
    "logmein.exe",
    "parsec.exe",
    "rustdesk.exe",
]
