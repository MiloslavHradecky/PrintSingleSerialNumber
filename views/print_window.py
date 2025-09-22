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
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QPalette, QColor, QPixmap, QIcon

# 🧠 First-party (project-specific)
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

        # 🪟 Title and size
        self.setWindowTitle("Print Line B")
        self.setFixedSize(400, 500)
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)

        # 📌 Window icon settings
        icon_path = self.resolver.resource("views/assets/main.ico")
        self.setWindowIcon(QIcon(str(icon_path)))

        # 📌 Setting the window background colour
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#D8E9F3'))
        self.setPalette(palette)

        # 🧱 Layout definition
        layout = QVBoxLayout()

        # 📌 Logo
        print_logo = self.resolver.resource("views/assets/print.png")
        self.logo = QLabel(self)
        pixmap = QPixmap(str(print_logo)).scaled(
            self.width() - 20,
            256,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 📌 Serial number input
        self.serial_number_input: QLineEdit = QLineEdit()
        self.serial_number_input.setPlaceholderText('Naskenujte serial number')

        # 📌 Placeholder color
        self.palette = self.serial_number_input.palette()
        self.placeholder_color = QColor('#757575')
        self.palette.setColor(QPalette.ColorRole.PlaceholderText, self.placeholder_color)
        self.serial_number_input.setPalette(self.palette)

        # 🖨️ Print button
        self.print_button: QPushButton = QPushButton('Tisk')

        # 📌 Back button
        self.back_button: QPushButton = QPushButton('Zpět')

        # 📌 Exit button
        self.exit_button: QPushButton = QPushButton("Ukončit")

        # 📌 Enter triggers print
        self.serial_number_input.returnPressed.connect(self.print_button.click)

        # 📌 Add elements to the main layout
        layout.addWidget(self.logo)
        layout.addWidget(self.serial_number_input)
        layout.addWidget(self.print_button)

        # 📌 Bottom layout for navigation buttons
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.back_button)
        bottom_layout.addWidget(self.exit_button)

        layout.addLayout(bottom_layout)

        # 📦 Finalize layout
        self.setLayout(layout)
        self.activateWindow()
        self.raise_()
        self.serial_number_input.setFocus()

    def reset_input_focus(self):
        """
        Clears the serial number input field and sets focus back to it.
        """
        self.serial_number_input.clear()
        self.serial_number_input.setFocus()

    def disable_inputs(self):
        """
        Disables all interactive input controls.
        """
        self.print_button.setDisabled(True)
        self.back_button.setDisabled(True)
        self.exit_button.setDisabled(True)
        self.serial_number_input.setDisabled(True)

    def restore_inputs(self):
        """
        Enables all interactive input controls and resets focus.
        """
        self.print_button.setDisabled(False)
        self.back_button.setDisabled(False)
        self.exit_button.setDisabled(False)
        self.serial_number_input.setDisabled(False)
        self.reset_input_focus()
