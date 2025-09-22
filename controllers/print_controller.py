"""
📦 Module: print_controller.py

Manages print operations in the PackingLine application.

Handles serial validation, .lbl parsing, and dynamic printing logic
based on configuration mappings. Supports multiple product types and protocols
(product, control4, my2n), and interacts with the PrintWindow UI.

Author: Miloslav Hradecky
"""

# 🧱 Standard library
import configparser

# 🧩 Third-party libraries
from PyQt6.QtCore import QTimer, QCoreApplication

# 🧠 First-party (project-specific)
from utils.logger import get_logger
from utils.messenger import Messenger
from utils.resource_resolver import ResourceResolver
from utils.bartender_utils import BartenderUtils

from views.print_window import PrintWindow


class PrintController:
    """
    Coordinates print logic, UI interaction, and trigger-based workflows.
    """

    def __init__(self, window_stack):
        """
        Initializes print controller, services, and connects UI signals.
        """
        # 📌 Loading the configuration file
        resolver = ResourceResolver()
        config_path = resolver.config()
        self.config = configparser.ConfigParser()
        self.config.optionxform = str  # 💡 Ensures letter size is maintained
        self.config.read(config_path)

        # 📌 Initialization
        self.window_stack = window_stack
        self.print_window = PrintWindow(controller=self)
        self.messenger = Messenger(self.print_window)
        self.bartender_utils = BartenderUtils()
        self.logger = get_logger("PrintController")

        # 🔗 linking the button to the method
        self.print_window.print_button.clicked.connect(self.print_button_click)
        self.print_window.back_button.clicked.connect(self.handle_back)
        self.print_window.exit_button.clicked.connect(self.handle_exit)

    @property
    def serial_input(self) -> str:
        """
        Returns trimmed, uppercase serial number from input field.
        """
        return self.print_window.serial_number_input.text().strip().upper()

    def handle_print(self):
        """
        Executes product-type save-and-print workflow.

        Validates input lines, extracts header and record, injects prefix,
        retrieves trigger values, and performs the print operation.
        """
        pass

    def print_button_click(self):
        """
        Main print workflow triggered by user.
        """
        self.print_window.disable_inputs()

        self.messenger.auto_info_dialog("Zpracovávám požadavek...", timeout_ms=3000)
        self.restore_ui()

    def handle_back(self):
        """
        Closes the product window and returns to the previous window in the stack.
        """
        self.print_window.close()
        self.window_stack.show_previous()

    def handle_exit(self):
        """
        Terminates the application and fades out the product window.
        """
        self.logger.info("Aplikace byla ukončena uživatelem.")
        self.bartender_utils.kill_processes()
        self.window_stack.mark_exiting()
        self.print_window.close()
        QCoreApplication.instance().quit()

    def delayed_restore_ui(self, delay_ms=500):
        """
        Restores UI controls after a short delay (default 500 ms).
        """
        QTimer.singleShot(delay_ms,  self.print_window.restore_inputs)

    def restore_ui(self, delay_ms=3000):
        """
        Restores UI controls after a longer delay (default 3000 ms).
        """
        QTimer.singleShot(delay_ms,  self.print_window.restore_inputs)
