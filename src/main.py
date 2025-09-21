#!/usr/bin/env python3
"""
🎬 Main application launcher for the PrintSingleSN system.

Responsible for initializing the Qt application, validating configuration,
enforcing single-instance behavior, applying global styles, and launching
the splash screen and login window.

Version:
    1.0.0.0

Author: Miloslav Hradecky
"""

__version__ = "1.0.0.0"

# 🧱 Standard library
import sys
from configparser import ConfigParser

# 🧩 Third-party libraries
from PyQt6.QtWidgets import QApplication

# 🧠 First-party (project-specific)
from views.login_window import LoginWindow
from views.splash_screen import CustomSplash

from utils.logger import get_logger
from utils.messenger import Messenger
from utils.system_info import log_system_info
from utils.path_validation import PathValidator
from utils.ensure_logs_dir import ensure_logs_dir
from utils.window_stack import WindowStackManager
from utils.config_checker import ConfigFileChecker
from utils.resource_resolver import ResourceResolver
from utils.single_instance import SingleInstanceChecker

from controllers.login_controller import LoginController


class AppLauncher:
    """
    Orchestrates the startup sequence of the PrintSingleSN application.
    Handles logging, configuration validation, UI setup, and event loop execution.
    """

    def __init__(self, version: str):
        """
        Initializes the launcher with application version and shared components.

        Args:
            version (str): Application version string.
        """
        self.version = version
        self.logger = get_logger("Main")
        self.resolver = ResourceResolver()
        self.window_stack = WindowStackManager()
        self.app = None

    def run(self):
        """
        Executes the full startup sequence of the application.
        """
        ensure_logs_dir()
        self._add_blank_line_to_log()
        self._check_single_instance()
        self._create_qt_app()
        self._apply_global_stylesheet()
        log_system_info(self.version)
        self._check_config_file()
        self._validate_config_paths()
        self._launch_ui()
        self.app.exec()

    def _add_blank_line_to_log(self):
        """
        Adds a blank line to the TXT log for visual separation.
        """
        try:
            log_file_txt = self.resolver.writable("logs/app.txt")
            with open(log_file_txt, "a", encoding="utf-8") as f:
                f.write("\n")
        except (OSError, IOError) as e:
            self.logger.warning("Nepodařilo se zapsat prázdný řádek do logu: %s", e)

    def _check_single_instance(self):
        """
        Ensures that only one instance of the application is running.
        """
        checker = SingleInstanceChecker("PrintSingleSnUniqueAppKey")
        if checker.is_running():
            self.app = QApplication([])
            Messenger(None).error("Upozornění - Aplikace už běží!", "Main")
            sys.exit(0)

    def _create_qt_app(self):
        """
        Creates the QApplication instance.
        """
        self.app = QApplication([])

    def _apply_global_stylesheet(self):
        """
        Applies the global stylesheet if available.
        """
        style_path = self.resolver.resource("views/themes/style.qss")
        if style_path.exists():
            with open(style_path, encoding="utf-8") as f:
                self.app.setStyleSheet(f.read())

    def _check_config_file(self):  # noqa: method may use self.logger in future
        """
        Verifies that the configuration file exists.
        """
        checker = ConfigFileChecker()
        checker.check_exists_or_exit()

    def _validate_config_paths(self):  # noqa: method may use self.logger in future
        """
        Validates paths defined in the configuration file.
        """
        config = ConfigParser()
        config.read("config.ini")
        validator = PathValidator()
        if not validator.validate():
            Messenger(None).error(
                "Konfigurace obsahuje neplatné cesty. Aplikace bude ukončena.",
                "Main"
            )
            sys.exit(1)

    def _launch_ui(self):
        """
        Displays the splash screen and launches the login window.
        """
        login_window = LoginWindow()
        login_controller = LoginController(login_window, self.window_stack)
        login_window.controller = login_controller

        splash = CustomSplash(login_window)
        _ = Messenger(splash)
        splash.show()

        # 🎭 Block further execution until splash screen closes
        while splash.isVisible():
            self.app.processEvents()


def main():
    """
    Entry point for the PrintSingleSN application.
    """
    launcher = AppLauncher(__version__)
    launcher.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as startup_error:
        startup_logger = get_logger("Main")
        startup_logger.exception("Neočekávaná chyba při spuštění aplikace: %s", startup_error)
        Messenger(None).error("Neočekávaná chyba. Aplikace bude ukončena.", "Main")
        sys.exit(1)
