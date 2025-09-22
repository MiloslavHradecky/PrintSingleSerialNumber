"""
📦 Module: config_reader.py

Provides a reusable class for reading values from config.ini.

Author: Miloslav Hradecky
"""

# 🧱 Standard library
import configparser

# 🧠 First-party (project-specific)
from utils.resource_resolver import ResourceResolver


class ConfigReader:
    """
    Reads and provides access to values from the configuration file.
    """

    def __init__(self):
        resolver = ResourceResolver()
        config_path = resolver.config()
        self.config = configparser.ConfigParser()
        self.config.optionxform = str
        self.config.read(config_path)

    def get_value(self, section: str, key: str, fallback=None) -> str:
        """
        Returns a value from the config file.

        Args:
            section (str): Section name (e.g. "Window", "Paths")
            key (str): Key name within the section
            fallback (Any): Value to return if key is missing

        Returns:
            str: Value from config or fallback
        """
        return self.config.get(section, key, fallback=fallback)

    def get_window_title(self) -> str:
        return self.get_value("Window", "title", fallback="Chybí titulek app v config!")

    def get_orders_path(self) -> str:
        return self.get_value("Paths", "orders_path")

    def get_szv_input_file(self) -> str:
        return self.get_value("Paths", "szv_input_file")

    def get_bartender_path(self) -> str:
        return self.get_value("Paths", "bartender_path")
