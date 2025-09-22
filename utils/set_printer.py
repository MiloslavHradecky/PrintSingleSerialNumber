# 📦 Module: set_printer.py
# Provides utility to modify BarTender label files (.btw)

from pathlib import Path
import win32com.client
import win32print


def set_printer_in_label(label_path: str, printer_name: str) -> bool:
    """
    Sets the printer for a given BarTender label file (.btw) if the printer exists.

    Args:
        label_path (str): Full path to the .btw label file.
        printer_name (str): Name of the printer to set.

    Returns:
        bool: True if successful, False otherwise.
    """
    label_file = Path(label_path)
    if not label_file.exists():
        return False

    printers = [p[2] for p in win32print.EnumPrinters(2)]
    if printer_name not in printers:
        return False

    try:
        btapp = win32com.client.Dispatch("BarTender.Application")
        btapp.Visible = False

        btformat = btapp.Formats.Open(str(label_file), False, "")
        btformat.Printer = printer_name
        btformat.Save()
        btformat.Close(1)
        return True
    except Exception:
        return False
