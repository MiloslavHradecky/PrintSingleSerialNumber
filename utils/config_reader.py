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

    def get_all_labels(self) -> dict:
        """
        Parses all label entries from config and returns a dict:
        {label_key: (label_path, printer, copies)}
        """
        if not self.config.has_section("Labels"):
            raise ValueError("Sekce [Labels] chybí v config.ini")

        labels = {}
        for key in self.config.options("Labels"):
            raw = self.config.get("Labels", key)
            parts = raw.split("|")

            if len(parts) != 3:
                raise ValueError(f"Etiketa '{key}' má neplatný formát: '{raw}' (očekáváno: path|printer|copies)")

            label_path = parts[0].strip()
            printer = parts[1].strip()
            try:
                copies = int(parts[2])
            except ValueError:
                raise ValueError(f"Etiketa '{key}' má nečíselný počet kopií: '{parts[2]}'")

            labels[key] = (label_path, printer, copies)

        return labels
