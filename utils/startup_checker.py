"""
📦 Module: startup_checker.py

Ensures that the application environment is ready to launch.

Responsibilities:
    - Verify existence of config.ini
    - Ensure logs directory is writable
    - Log and notify user of any critical issues

Used during application startup to validate environment integrity.

Author: Miloslav Hradecky
"""

# 🧱 Standard library
import sys

# 🧠 First-party
from utils.resource_resolver import ResourceResolver
from utils.logger import get_logger
from utils.messenger import Messenger


class StartupChecker:
    """
    Performs startup checks for configuration file and logs directory.
    """

    def __init__(self, config_filename="config.ini", logs_dir="logs"):
        self.resolver = ResourceResolver(config_filename)
        self.config_path = self.resolver.config()
        self.logs_path = self.resolver.writable(logs_dir)
        self.logger = get_logger("StartupChecker")
        self.messenger = Messenger(None)

    def check_config_or_exit(self):
        """
        Verifies that the configuration file exists.
        """
        if not self.config_path.exists():
            self.logger.error("Konfigurační soubor chybí: %s", self.config_path)
            self.messenger.error(
                "Konfigurační soubor nebyl nalezen. Aplikace bude ukončena.",
                "StartupChecker"
            )
            sys.exit(1)
        else:
            self.logger.info("Konfigurační soubor nalezen: %s", self.config_path)

    def ensure_logs_dir(self):
        """
        Ensures that the logs directory exists and is writable.
        """
        self.logs_path.mkdir(parents=True, exist_ok=True)
        self.logger.info("Logovací složka připravena: %s", self.logs_path)
