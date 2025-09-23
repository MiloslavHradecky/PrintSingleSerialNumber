# 📦 Module: login_context.py

from utils.logger import get_logger
from utils.messenger import Messenger
from utils.config_reader import ConfigReader
from utils.login_services import LoginServices
from utils.bartender_utils import BartenderUtils


class LoginContext:
    """
    Holds shared services and configuration for LoginController.
    """
    def __init__(self, login_window):
        self.logger = get_logger("LoginController")
        self.messenger = Messenger(login_window)
        self.config_reader = ConfigReader.load()

        self.services = LoginServices(
            config=self.config_reader.config,
            messenger=self.messenger
        )

        self.bartender_utils = BartenderUtils(
            config=self.config_reader.config,
            messenger=self.messenger
        )
