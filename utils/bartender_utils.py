"""
📦 Module: bartender_utils.py

Provides utility methods for managing BarTender processes (Cmdr.exe, bartend.exe),
including termination and optional user feedback via Messenger.

Author: Miloslav Hradecky
"""

# 🧱 Standard library
import subprocess
from pathlib import Path

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
            subprocess.run(
                "taskkill /f /im cmdr.exe 1>nul 2>nul",
                shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            subprocess.run(
                "taskkill /f /im bartend.exe 1>nul 2>nul",
                shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        except subprocess.CalledProcessError as e:
            self.logger.error("Chyba při ukončování BarTender procesů: %s", str(e))
            if self.messenger:
                self.messenger.error(
                    f"Chyba při ukončování BarTender procesů: {str(e)}",
                    "Bartender Utils"
                )

    def print_label(self, label_path: str, printer_name: str, copies: int = 1):
        """
        Launches BarTender to print a label using the specified printer.

        Args:
            label_path (str): Full path to the .btw label template.
            printer_name (str): Name of the printer to use.
        """
        label_file = Path(label_path)

        if not label_file.exists():
            self.logger.error("Šablona neexistuje: %s", label_file)
            if self.messenger:
                self.messenger.error(f"Šablona neexistuje: {label_file}", "Bartender Utils")
            return

        if not self.config:
            self.logger.error("Chybí config pro získání cesty k BarTenderu.")
            if self.messenger:
                self.messenger.error("Chybí config pro BarTender path.", "Bartender Utils")
            return

        bartender_path = Path(self.config.get("Paths", "bartender_path", fallback=""))

        if not bartender_path.exists():
            self.logger.error("BarTender nebyl nalezen: %s", bartender_path)
            if self.messenger:
                self.messenger.error(f"BarTender nebyl nalezen: {bartender_path}", "Bartender Utils")
            return

        command = (
            f'"{bartender_path}" '
            f'/P '
            f'/AF="{label_file}" '
            f'/C={copies} '
            f'/X'
        )

        try:
            subprocess.run(command, shell=True, check=True)
            self.logger.info("Etiketa vytisknuta: %s → %s", label_file.name, printer_name)
        except subprocess.CalledProcessError as e:
            self.logger.error("Chyba při tisku BarTenderem: %s", str(e))
            if self.messenger:
                self.messenger.error(f"Tisk se nezdařil: {str(e)}", "Bartender Utils")
