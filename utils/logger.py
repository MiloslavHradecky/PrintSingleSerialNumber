"""
📦 Module: logger.py

Utility for initializing and configuring application-wide logging.

Responsibilities:
    - Provide rotating log handlers for both plain-text and JSON formats
    - Format logs with timestamps, levels, and module names
    - Ensure log directory exists before writing

Used throughout the application for consistent logging.

Author: Miloslav Hradecky
"""

# 🧱 Standard library
import logging
import json
from pathlib import Path
from logging.handlers import RotatingFileHandler

# 🧠 First-party (project-specific)
from utils.resource_resolver import ResourceResolver


# --- Custom JSON formatter ---
class JsonFormatter(logging.Formatter):
    """
    Custom formatter for logging in JSON format.
    Formats log records with timestamp, level, module, and message.
    """

    def format(self, record):  # noqa
        log_record = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "module": record.name,
            "message": record.getMessage()
        }
        return json.dumps(log_record, ensure_ascii=False)


# --- Logger initialization ---
def get_logger(name: str) -> logging.Logger:
    """Initializes and returns a logger with both TXT and JSON rotating handlers."""
    resolver = ResourceResolver()
    log_file_txt = resolver.writable("logs/app.txt")
    log_file_json = resolver.writable("logs/app.json")

    # 🛡️ Ensure the existence of a folder
    Path(log_file_txt).parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.DEBUG)

    # 📌 TXT log with rotation
    txt_handler = RotatingFileHandler(
        log_file_txt,
        maxBytes=1_000_000,
        backupCount=5,
        encoding="utf-8"
    )
    txt_formatter = logging.Formatter("%(asctime)s | %(levelname)-7s | %(name)-17s | %(message)s")
    txt_handler.setFormatter(txt_formatter)
    logger.addHandler(txt_handler)

    # 📌 JSON log with rotation
    json_handler = RotatingFileHandler(
        log_file_json,
        maxBytes=1_000_000,
        backupCount=5,
        encoding="utf-8"
    )
    json_handler.setFormatter(JsonFormatter())
    logger.addHandler(json_handler)

    return logger
