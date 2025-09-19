"""
📦 Module: config_checker.py

Utility for ensuring the existence of the application's configuration file.

If the config file is missing, this module creates it with default sections and values
required for the PrintSingleSN system to operate correctly.

Author: Miloslav Hradecky
"""

# 🧱 Standard library
import sys

# 🧠 First-party (project-specific)
from utils.resource_resolver import ResourceResolver
from utils.logger import get_logger
from utils.messenger import Messenger


class ConfigFileChecker:
    """
    Checks for the presence of the configuration file.
    If the file is missing, logs the issue, notifies the user, and exits the application.
    """

    def __init__(self, filename="config.ini"):
        """
        Initializes the checker with the given config filename.

        Args:
            filename (str): Name of the configuration file to verify.
        """
        self.resolver = ResourceResolver(filename)
        self.config_path = self.resolver.config()
        self.logger = get_logger("ConfigFileChecker")
        self.messenger = Messenger(None)

    def check_exists_or_exit(self):
        """
        Verifies that the configuration file exists.
        If not found, logs the error, shows a message, and exits the application.
        """
        if not self.config_path.exists():
            self.logger.error("Konfigurační soubor chybí: %s", self.config_path)
            self.messenger.error("Konfigurační soubor nebyl nalezen. Aplikace bude ukončena.", "ConfigFileChecker")
            sys.exit(1)
        else:
            self.logger.info("Konfigurační soubor nalezen: %s", self.config_path)
