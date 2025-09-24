"""
📦 Module: print_window.py

Defines the PrintWindow class — a GUI for printing labels based on scanned serial numbers.

Includes:
- Display of work order and product info
- Input field for serial number
- Buttons for printing and exiting
- Visual effects via WindowEffectsManager

Used with a controller to handle print logic.

Author: Miloslav Hradecky
"""

# 🧩 Third-party libraries
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton
)
from PyQt6.QtGui import QPalette, QColor, QPixmap, QIcon

# 🧠 First-party (project-specific)
from utils.config_reader import ConfigReader
from utils.resource_resolver import ResourceResolver


class PrintWindow(QWidget):
    """
    GUI window for printing product labels based on serial number input.
    Displays order and product info, input field, and navigation buttons.
    Triggers print logic and applies fade-in animation.
    """

    def __init__(self, controller=None):
        """
        Initializes PrintWindow and sets up visual components.
        Configures layout, input field, buttons, labels, and fade-in effect.
        """
        super().__init__()
        self.controller = controller
        self.resolver = ResourceResolver()
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        config = ConfigReader()
        title = config.get_window_title()

        # 🪟 Title and size
        self.setWindowTitle(title)
        self.setFixedSize(360, 500)
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)

        # 📌 Window icon settings
        icon_path = self.resolver.resource("views/assets/main.ico")
        self.setWindowIcon(QIcon(str(icon_path)))

        # 📌 Setting the window background colour
        self.setObjectName("PrintWindow")

        # 🧱 Layout definition
        layout = QVBoxLayout()

        # 📌 Logo
        print_logo = self.resolver.resource("views/assets/print.png")
        logo = QLabel(self)
        pixmap = QPixmap(str(print_logo)).scaled(
            self.width() - 20, 200,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 📌 Serial number input
        self.serial_number_input: QLineEdit = QLineEdit()
        self.serial_number_input.setPlaceholderText('Naskenujte serial number')
        self._style_serial_input()

        # 📌 Buttons
        self.print_button: QPushButton = QPushButton('Tisk')
        self.back_button: QPushButton = QPushButton('Zpět')
        self.exit_button: QPushButton = QPushButton("Ukončit")

        # 📌 Enter triggers print
        self.serial_number_input.returnPressed.connect(self.print_button.click)

        # 📌 Add elements to the main layout
        layout.addWidget(logo)
        layout.addWidget(self.serial_number_input)
        layout.addWidget(self.print_button)

        # 📌 Bottom layout for navigation buttons
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.back_button)
        bottom_layout.addWidget(self.exit_button)

        layout.addLayout(bottom_layout)
        layout.setContentsMargins(10, 10, 10, 50)  # left, top, right, bottom

        # 📦 Finalize layout
        self.setLayout(layout)
        self.activateWindow()
        self.raise_()
        self.serial_number_input.setFocus()

    def _style_serial_input(self):
        """Applies placeholder color styling to the serial number input field."""
        palette = self.serial_number_input.palette()
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("#FFFFFF"))
        self.serial_number_input.setPalette(palette)

    def reset_input_focus(self):
        """Clears the serial number input field and sets focus back to it."""
        self.serial_number_input.clear()
        self.serial_number_input.setFocus()

    def disable_inputs(self):
        """Disables all interactive input controls."""
        self.print_button.setDisabled(True)
        self.back_button.setDisabled(True)
        self.exit_button.setDisabled(True)
        self.serial_number_input.setDisabled(True)
        QApplication.processEvents()

    def restore_inputs(self):
        """Enables all interactive input controls and resets focus."""
        self.print_button.setDisabled(False)
        self.back_button.setDisabled(False)
        self.exit_button.setDisabled(False)
        self.serial_number_input.setDisabled(False)
        self.reset_input_focus()
