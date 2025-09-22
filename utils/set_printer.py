"""
📦 Module: set_printer.py

Assigns a printer to a BarTender label file (.btw) via COM automation.
Validates printer availability and updates label metadata.

Author: Miloslav Hradecky
"""

# 🧱 Standard library
from pathlib import Path
import win32com.client
import win32print
from pywintypes import com_error


def set_printer_in_label(label_path: str, printer_name: str, logger=None, messenger=None) -> bool:
    """
    Sets the printer for a BarTender label file (.btw) if the printer exists.

    Args:
        label_path (str): Full path to the .btw label file.
        printer_name (str): Name of the printer to assign.
        logger (Logger, optional): Logger for error reporting.
        messenger (Messenger, optional): Messenger for user feedback.

    Returns:
        bool: True if printer was successfully set, False otherwise.
    """
    label_file = Path(label_path)
    if not label_file.exists():
        if logger:
            logger.error("Soubor etikety neexistuje: %s", label_file)
        if messenger:
            messenger.error(f"Soubor etikety neexistuje: {label_file}", "Set Printer")
        return False

    printers = [p[2] for p in win32print.EnumPrinters(2)]
    if printer_name not in printers:
        if logger:
            logger.error("Tiskárna '%s' není dostupná v systému.", printer_name)
        if messenger:
            messenger.error(f"Tiskárna '{printer_name}' není dostupná.", "Set Printer")
        return False

    try:
        btapp = win32com.client.Dispatch("BarTender.Application")
        btapp.Visible = False

        btformat = btapp.Formats.Open(str(label_file), False, "")
        btformat.Printer = printer_name
        btformat.Save()
        btformat.Close(1)
        return True

    except com_error as e:
        if logger:
            logger.error("Chyba COM při nastavování tiskárny: %s", str(e))
        if messenger:
            messenger.error("Nepodařilo se nastavit tiskárnu v etiketě.", "Set Printer")
        return False
