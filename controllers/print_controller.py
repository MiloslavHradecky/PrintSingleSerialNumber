"""
📦 Module: print_controller.py

Manages print operations in the PackingLine application.

Handles serial validation, .lbl parsing, and dynamic printing logic
based on configuration mappings. Supports multiple product types and protocols
(product, control4, my2n), and interacts with the PrintWindow UI.

Author: Miloslav Hradecky
"""

# 🧱 Standard library
import csv
import configparser
from pathlib import Path
from datetime import datetime

# 🧩 Third-party libraries
from PyQt6.QtCore import QTimer, QCoreApplication

# 🧠 First-party (project-specific)
from utils.logger import get_logger
from utils.messenger import Messenger
from utils.config_reader import ConfigReader
from utils.bartender_utils import BartenderUtils
from utils.set_printer import set_printer_in_label
from utils.resource_resolver import ResourceResolver

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
        self.bartender_utils = BartenderUtils(messenger=self.messenger, config=self.config)
        self.logger = get_logger("PrintController")
        self.config_reader = ConfigReader()

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

    def write_to_label_csv(self, serial_number: str, label_path: str):
        """
        Writes the serial number and current date to label.csv in the label's directory.

        Args:
            serial_number (str): The serial number entered by the user.
            label_path (str): Full path to the .btw label template.
        """
        # 📂 Získání složky, kde je etiketa
        label_file = Path(label_path)
        csv_path = label_file.parent / "label.csv"

        # 📅 Aktuální datum ve formátu YYYY-MM-DD
        today = datetime.today().strftime("%Y-%m-%d")

        # 🧾 Záznam, který chceme přidat
        row = [serial_number, today]

        # 🖊️ Zápis do souboru
        try:
            with csv_path.open(mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(["SerialNumber", "Date"])  # hlavička
                writer.writerow(row)
        except (OSError, IOError) as e:
            self.logger.error("Chyba při zápisu do label.csv: %s", str(e))
            self.messenger.error("Nepodařilo se zapsat do label.csv", "Print Ctrl")

    def print_button_click(self):
        """
        Main print workflow triggered by user.
        """
        serial = self.serial_input
        labels = self.config_reader.get_all_labels()

        if not serial:
            self.messenger.warning("Zadejte sériové číslo.", "Print Ctrl")
            return

        for label_key, (label_path, printer, copies) in labels.items():
            if not label_path:
                self.logger.warning("Etiketa '%s' nemá definovanou cestu.", label_key)
                self.messenger.warning(f"Etiketa {label_key} není definována v config.ini", "Print Ctrl")
                continue

            # 🖨️ Nastavení tiskárny v etiketě
            success = set_printer_in_label(label_path, printer)
            if not success:
                self.logger.warning("Tiskárnu '%s' se nepodařilo nastavit v etiketě '%s'", printer, label_path)
                self.messenger.warning(f"Tiskárnu {printer} se nepodařilo nastavit v etiketě {label_key}", "Print Ctrl")
                continue

            # 🧾 Zápis dat do label.csv
            self.write_to_label_csv(serial, label_path)

            # 🖨️ Tisk etikety
            self.bartender_utils.print_label(label_path, printer, copies)

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

    def restore_ui(self, delay_ms=3000):
        """
        Restores UI controls after a longer delay (default 3000 ms).
        """
        QTimer.singleShot(delay_ms,  self.print_window.restore_inputs)
