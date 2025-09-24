"""
📦 Module: login_window.py

Defines the application's login window using PyQt6.

Responsibilities:
- Display password input field (ID card scan)
- Show login and exit buttons
- Apply custom styling, icons, and fade-in effects
- Connect input to controller logic

Used by ControllerApp to initiate authentication.

Author: Miloslav Hradecky
"""

# 🧩 Third-party libraries
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QPalette, QColor, QPixmap, QIcon

# 🧠 First-party (project-specific)
from utils.config_reader import ConfigReader
from utils.resource_resolver import ResourceResolver


class LoginWindow(QWidget):
    """
    Login window for user authentication.

    Displays password input, logo, and navigation buttons.
    Applies fade-in effect and connects input to controller logic.
    """

    def __init__(self, controller=None):
        """
        Initializes LoginWindow and sets up visual components.
        Configures layout, styling, input field, buttons, and fade-in animation.
        """
        super().__init__()

        self.controller = controller
        self.resolver = ResourceResolver()
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        config = ConfigReader()
        title = config.get_window_title()

        # 📌 Setting the window name and size
        self.setWindowTitle(title)
        self.setFixedSize(400, 500)

        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)

        # 📌 Window icon settings
        icon_path = self.resolver.resource("views/assets/main.ico")
        self.setWindowIcon(QIcon(str(icon_path)))

        # 📌 Setting the window background colour
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#D8E9F3"))
        self.setPalette(palette)

        # 📌 Main window layout
        layout = QVBoxLayout()

        # 📌 Application logo
        login_logo = self.resolver.resource("views/assets/login.tiff")
        self.logo = QLabel(self)
        pixmap = QPixmap(str(login_logo)).scaled(
            self.width() - 20, 256,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo)

        # 📌 Password field (ID card)
        self.password_input: QLineEdit = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Naskenujte svoji ID kartu")
        self._style_password_input()

        # 📌 Login button
        self.login_button: QPushButton = QPushButton("Přihlásit se")

        # 📌 "Exit" selection button
        self.exit_button: QPushButton = QPushButton("Ukončit")

        # 📌 Linking the button to the login action
        self.password_input.returnPressed.connect(self.login_button.click)

        # 📌 Adding elements to the main layout
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.exit_button)

        # 📌 Setting the window layout
        self.setLayout(layout)

        self.activateWindow()
        self.raise_()

        self.password_input.setFocus()

    def _style_password_input(self):
        """Applies placeholder color styling to the password input field."""
        palette = self.password_input.palette()
        placeholder_color = QColor("#757575")
        palette.setColor(QPalette.ColorRole.PlaceholderText, placeholder_color)
        self.password_input.setPalette(palette)

    def get_password(self) -> str:
        """Returns the entered password from the input field."""
        return self.password_input.text().strip()

    def clear_password(self):
        """Clears the password input field."""
        self.password_input.clear()

    def reset_password_input(self):
        """Clears the password field and sets focus for new input."""
        self.password_input.clear()
        self.password_input.setFocus()
