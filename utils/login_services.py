"""
📦 Module: login_services.py

Provides shared services for login logic, including decryption and BarTender process control.

Author: Miloslav Hradecky
"""

# 🧱 Standard library
import configparser

# 🧠 First-party (project-specific)
from utils.bartender_utils import BartenderUtils
from utils.messenger import Messenger

from models.user_model import SzvDecrypt


class LoginServices:
    """
    Container for login-related services.
    Provides methods for password validation and BarTender process control.
    """

    def __init__(self, config: configparser.ConfigParser, messenger: Messenger):
        """
        Initializes login services with config and messenger.

        Args:
            config (ConfigParser): Loaded configuration file.
            messenger (Messenger): Messenger instance for user feedback.
        """
        self._decrypter = SzvDecrypt()
        self._bartender = BartenderUtils(messenger=messenger, config=config)

    def check_login(self, password: str) -> bool:
        """
        Checks whether the given password is valid using the decryption service.

        Args:
            password (str): The password to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        return self._decrypter.check_login(password)

    def kill_bartender_processes(self):
        """Terminates any running BarTender processes."""
        self._bartender.kill_processes()
