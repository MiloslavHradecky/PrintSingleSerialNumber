# 🛠️ create_config.py – Generates default configuration file for the application

import configparser
from io import StringIO

config = configparser.ConfigParser()
config.optionxform = str  # ✅ Preserve key casing

# 📌 Section: Window – application title
config["Window"] = {
    "title": "Print Single Serial Number"
}

# 📁 Section: Paths – system paths and references
config["Paths"] = {
    "orders_path": "T:/Prikazy/",
    "szv_input_file": "T:/Prikazy/DataTPV/SZV.dat",
    "bartender_path": "C:/Program Files (x86)/Seagull/BarTender Suite/bartend.exe",
}

config["Labels"] = {
    "label01": "T:/Prikazy/DataTPV/PrintSingleSN/Etikety/50x45_SN.btw|50x45_ZD621",
}

# 🧪 For testing: preview config content
configfile = StringIO()
config.write(configfile)
print(configfile.getvalue())

# 💾 Save config to .ini file
with open("config.ini", mode="w") as file:
    file.write(configfile.getvalue())
