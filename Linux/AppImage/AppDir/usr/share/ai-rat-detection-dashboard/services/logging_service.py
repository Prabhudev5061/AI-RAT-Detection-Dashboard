"""
AI-RAT-Detection-Dashboard - Logging Service
Handles file logging, terminal logging, and SQLite security event auditing.
"""

import logging
from logging.handlers import RotatingFileHandler
from typing import Optional
from pathlib import Path

from config.config import APP_LOG_PATH
from database.database import db

# Setup standard logger
logger = logging.getLogger("AIRATDashboard")
logger.setLevel(logging.INFO)

if not logger.handlers:
    # Formatter
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Rotating File Handler (Max 5MB, 3 backups)
    APP_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    file_handler = RotatingFileHandler(
        str(APP_LOG_PATH),
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def log_event(
    event_type: str,
    description: str,
    severity: str = "INFO",
    source: str = "System",
    pid: Optional[int] = None,
    ip: Optional[str] = None,
    port: Optional[int] = None,
):
    """
    Log an event to the application log file and persist it in SQLite events table.
    """
    msg = f"[{event_type}] {description}"
    if pid:
        msg += f" (PID: {pid})"
    if ip:
        msg += f" (IP: {ip})"
    if port:
        msg += f" (Port: {port})"

    sev = severity.upper()
    if sev in ("HIGH", "CRITICAL"):
        logger.error(msg)
    elif sev == "WARNING":
        logger.warning(msg)
    else:
        logger.info(msg)

    try:
        db.insert_event(
            event_type=event_type,
            description=description,
            severity=sev,
            source=source,
            pid=pid,
            ip=ip,
            port=port,
        )
    except Exception as e:
        logger.error(f"Failed to record event to database: {e}")
