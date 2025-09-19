"""
📦 Module: resource_resolver.py

Provides the ResourceResolver class for consistent and environment-aware file path resolution.

Purpose:
- Ensure reliable access to resource files in both development and bundled (.exe) environments
- Resolve paths from configuration (absolute or relative)
- Provide writable paths for logs, outputs, and temp files
- Centralize path logic for maintainability and testability

Highlights:
- Detects runtime context (standard vs PyInstaller)
- Supports config-driven path resolution
- Designed for future extensibility and mocking
- Keeps file access consistent across platforms

Usage:
    resolver = ResourceResolver()
    config_path = resolver.config()
    log_path = resolver.writable("logs/app.log")
    data_file = resolver.resource("data/items.json")

Author: Miloslav Hradecky
"""

from pathlib import Path
import sys


class ResourceResolver:
    """
    Resolves file paths for resources, config, and writable outputs.
    Supports both development and bundled (.exe) environments.
    """

    def __init__(self, config_filename: str = "config.ini"):
        self.base_path = self._detect_base_path()
        self.config_filename = config_filename

    def _detect_base_path(self) -> Path:  # noqa
        """
        Detects base path depending on runtime context (standard or PyInstaller).
        """
        try:
            return Path(sys._MEIPASS)  # type: ignore
        except AttributeError:
            fallback = Path(__file__).resolve().parent
            return fallback if fallback.exists() else Path.cwd()

    def resource(self, relative_path: str) -> Path:
        """
        Resolves relative resource path to absolute, based on detected base path.
        """
        return self.base_path / relative_path

    def resolve(self, config_value: str) -> Path:
        """
        Resolves config-defined path (absolute or relative) to absolute path.
        """
        path = Path(config_value)
        return path if path.is_absolute() else self.resource(config_value)

    def writable(self, relative_path: str) -> Path:  # noqa
        """
        Returns writable path relative to script or executable location.
        """
        return Path(sys.argv[0]).resolve().parent / relative_path

    def config(self) -> Path:
        """
        Returns absolute path to the configuration file.
        """
        return self.base_path / self.config_filename
