"""
📦 Module: login_controller.py

Controller for managing user login in the PackingLine application.

Handles password validation, post-authentication transitions, and process cleanup.
Interacts with the LoginWindow UI and launches the WorkOrderController upon successful login.

Author: Miloslav Hradecky
"""

# 🧩 Third-party libraries
from PyQt6.QtCore import QCoreApplication

# 🧠 First-party (project-specific)
import models.user_model

from utils.login_context import LoginContext

from controllers.print_controller import PrintController


class LoginController:
    """
    Handles login validation and transitions to the work order phase.
    """

    def __init__(self, login_window, window_stack):
        """
        Initializes login logic, UI bindings, and supporting services.
        """
        self.login_window = login_window
        self.window_stack = window_stack
        self.value_prefix = None
        self.context = LoginContext(login_window)

        # 📌 Linking the button to the method
        self.login_window.login_button.clicked.connect(self.handle_login)
        self.login_window.exit_button.clicked.connect(self.handle_exit)

    def handle_login(self):
        """
        Processes login input and opens the next window if credentials are valid.
        """
        password = self.login_window.get_password()
        self.login_window.clear_password()

        try:
            if self.context.services.check_login(password):
                self.value_prefix = models.user_model.get_value_prefix()
                self.context.services.kill_bartender_processes()
                self.open_print_window()
            else:
                self.context.logger.warning("Zadané heslo '%s' není správné!", password)
                self.context.messenger.warning("Zadané heslo není správné!", "Login Ctrl")
                self.login_window.reset_password_input()
        except (FileNotFoundError, ValueError, OSError, RuntimeError) as e:
            self.context.logger.error("Neočekávaný problém: %s", str(e))
            self.context.messenger.error(str(e), "Login Ctrl")
            self.login_window.reset_password_input()

    def open_print_window(self):
        """
        Instantiates and opens the WorkOrderController window.
        """
        print_controller = PrintController(self.window_stack)
        self.window_stack.push(print_controller.print_window)

    def handle_exit(self):
        """
        Closes the LoginWindow and exits the application.
        """
        self.context.logger.info("Aplikace byla ukončena uživatelem.")
        self.context.bartender_utils.kill_processes()
        self.window_stack.mark_exiting()
        self.login_window.close()
        QCoreApplication.instance().quit()
