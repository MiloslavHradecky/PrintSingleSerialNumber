"""
📦 Module: ensure_logs_dir.py

Ensures that the logs directory exists and is writable.

Responsibilities:
    - Resolve the writable path for logs
    - Create the directory if it doesn't exist
    - Used during application startup to prepare logging infrastructure

Author: Miloslav Hradecky
"""

# 🧠 First-party (project-specific)
from utils.resource_resolver import ResourceResolver


def ensure_logs_dir(path: str = "logs"):
    """
    Ensures that the logs directory exists. If not, creates it.

    Args:
        path (str): Relative or absolute path to the logs directory (default: "logs").
    """
    resolver = ResourceResolver()
    logs_path = resolver.writable(path)
    logs_path.mkdir(parents=True, exist_ok=True)
