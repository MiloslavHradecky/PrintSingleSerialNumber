"""
📦 Module: bartender_utils.py

Provides utility methods for managing BarTender processes (Cmdr.exe, bartend.exe),
including termination and optional user feedback via Messenger.

Author: Miloslav Hradecky
"""

# 🧱 Standard library
import subprocess

# 🧠 First-party (project-specific)
from utils.logger import get_logger


class BartenderUtils:
    """
    Utility class for managing BarTender-related processes.
    Provides methods to kill, launch, and monitor BarTender components.
    """

    def __init__(self, messenger=None, config=None):
        """
        Initializes the utility with optional Messenger for user feedback.

        Args:
            messenger (Messenger | None): Optional messenger instance.
            config (ConfigParser | None): Optional config for path resolution.
        """
        self.logger = get_logger("BartenderUtils")
        self.messenger = messenger
        self.config = config

    def kill_processes(self):
        """
        Terminates all running BarTender instances (Cmdr.exe and bartend.exe).
        """
        try:
            subprocess.run("taskkill /f /im cmdr.exe 1>nul 2>nul", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run("taskkill /f /im bartend.exe 1>nul 2>nul", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        except subprocess.CalledProcessError as e:
            self.logger.error("Chyba při ukončování BarTender procesů: %s", str(e))
            if self.messenger:
                self.messenger.error(f"Chyba při ukončování BarTender procesů: {str(e)}", "Bartender Utils")
