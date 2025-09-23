"""
📦 Module: print_controller.py

Coordinates the label printing workflow in the PackingLine application.

Handles serial input validation, label preparation, printer assignment,
and execution of BarTender print commands. Integrates with the PrintWindow UI
and supports dynamic configuration of label paths, printers, and copy counts.

Designed for audit clarity, modularity, and seamless user interaction.

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

from models.user_model import get_value_prefix

from views.print_window import PrintWindow


class PrintController:
    """Handles label printing, UI events, and config-driven workflows."""

    def __init__(self, window_stack):
        """Initializes controller, services, and connects UI buttons."""

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
        """Returns cleaned serial number from input field."""

        return self.print_window.serial_number_input.text().strip().upper()

    def write_to_label_csv(self, serial_number: str, label_path: str):
        """Saves serial number, date, and user prefix to label.csv next to the label file."""

        label_file = Path(label_path)
        csv_path = label_file.parent / "label.csv"
        today = datetime.today().strftime("%Y-%m-%d")
        prefix = get_value_prefix() or "?"  # fallback pro případ, že není nastaven
        row = [serial_number, today, prefix]

        try:
            with csv_path.open(mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(["SerialNumber", "Date", "Signature"])  # hlavička
                writer.writerow(row)
        except (OSError, IOError) as e:
            self.logger.error("Chyba při zápisu do label.csv: %s", str(e))
            self.messenger.error("Nepodařilo se zapsat do label.csv", "Print Ctrl")

    def print_button_click(self):
        """Main workflow triggered by print button."""

        serial = self.serial_input

        if not serial:
            self.messenger.warning("Zadejte sériové číslo.", "Print Ctrl")
            return

        self.print_window.disable_inputs()
        try:
            labels = self.config_reader.get_all_labels()
        except ValueError as e:
            self.logger.error("Chyba v config.ini: %s", str(e))
            self.messenger.error(f"Chyba v config.ini:\n{str(e)}", "Print Ctrl")
            self.restore_ui()
            return

        if not labels:
            self.logger.warning("V config.ini nejsou definovány žádné etikety.")
            self.messenger.warning("V config.ini nejsou definovány žádné etikety.", "Print Ctrl")
            self.restore_ui()
            return

        for label_key, (label_path, printer, copies) in labels.items():
            if not label_path:
                self.logger.warning("Etiketa '%s' nemá definovanou cestu.", label_key)
                self.messenger.warning(
                    f"Etiketa {label_key} není definována v config.ini",
                    "Print Ctrl"
                )
                self.restore_ui()
                return

            success = set_printer_in_label(
                label_path,
                printer,
                logger=self.logger,
                messenger=self.messenger
            )
            if not success:
                self.logger.warning(
                    "Tiskárnu '%s' se nepodařilo nastavit v etiketě '%s'",
                    printer,
                    label_path
                )
                self.messenger.warning(
                    f"Tiskárnu {printer} se nepodařilo nastavit v etiketě {label_key}",
                    "Print Ctrl"
                )
                self.restore_ui()
                return

            self.write_to_label_csv(serial, label_path)
            self.bartender_utils.print_label(label_path, printer, copies)
            self.logger.info(
                "Etiketa '%s' úspěšně vytisknuta na '%s' (%d kopií)",
                label_key,
                printer,
                copies
            )

        self.messenger.auto_info_dialog("Zpracovávám požadavek...", timeout_ms=3000)
        self.restore_ui()

    def handle_back(self):
        """Returns to previous window in the stack."""

        self.print_window.close()
        self.window_stack.show_previous()

    def handle_exit(self):
        """Closes app and terminates BarTender processes."""

        self.logger.info("Aplikace byla ukončena uživatelem.")
        self.bartender_utils.kill_processes()
        self.window_stack.mark_exiting()
        self.print_window.close()
        QCoreApplication.instance().quit()

    def restore_ui(self, delay_ms=3000):
        """Re-enables UI inputs after a delay."""

        QTimer.singleShot(delay_ms,  self.print_window.restore_inputs)
