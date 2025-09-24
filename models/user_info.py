"""
📦 Module: user_info.py

Dataclass representing user metadata extracted during login.
Used by SzvDecrypt and LoginController.

Author: Miloslav Hradecky
"""

# 🧱 Standard library
from dataclasses import dataclass


@dataclass
class UserInfo:
    """Holds user metadata extracted during login: surname, name, and prefix."""
    surname: str = ""
    name: str = ""
    prefix: str = ""
