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
        """
        Retrieves the application window title from the config file.

        Returns:
            str: Window title or fallback if missing.
        """
        return self.get_value("Window", "title", fallback="Chybí titulek app v config!")

    def get_orders_path(self) -> str:
        """
        Retrieves the path to the orders directory from the config file.

        Returns:
            str: Orders path.
        """
        return self.get_value("Paths", "orders_path")

    def get_szv_input_file(self) -> str:
        """
        Retrieves the path to the SZV input file from the config file.

        Returns:
            str: SZV input file path.
        """
        return self.get_value("Paths", "szv_input_file")

    def get_bartender_path(self) -> str:
        """
        Retrieves the path to the BarTender executable from the config file.

        Returns:
            str: BarTender executable path.
        """
        return self.get_value("Paths", "bartender_path")

    def get_all_labels(self) -> dict[str, tuple[str, str]]:
        """
        Retrieves all label definitions from the config.

        Returns:
            dict: {label_key: (template_path, printer_name)}
        """
        label_map = {}
        if self.config.has_section("Labels"):
            for key in self.config["Labels"]:
                raw = self.config.get("Labels", key)
                if "|" in raw:
                    path, printer = raw.split("|", maxsplit=1)
                    label_map[key] = (path.strip(), printer.strip())
        return label_map
