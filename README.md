# 🖨️ PrintSingleSerialNumber

**Modular application for printing labels by serial number.**  
Designed with an emphasis on audit clarity, sustainable architecture, and ease of use.

---

## 📋 Description

A desktop application for printing labels by serial number.
Created in Python with PyQt6.
Structured according to MVC and distributed as an ".exe" file for Windows 11+.

---

## 🎯 Features

- ✅ User login with password authentication (SHA-256 + XOR decoding)
- ✅ Dynamic label loading from 'config.ini' (path, printer, copies)
- ✅ Printing via BarTender with automatic printer settings
- ✅ Writing to 'label.csv' with serial number, date, and signature (user prefix)
- ✅ Visually appealing GUI (PyQt6) with animations and icons
- ✅ Robust error handling and audit logging

---

## 🚀 Technologies

- **Python 3.11+**
- **PyQt6**
- **BarTender Integration**

---

## ⚙️ Configuration ('config.ini')

```ini
[Window]
title = Print label

[Paths]
szv_input_file = data/szv_login.txt

[Labels]
label1 = labels/label1.btw|Printer_X|1
label2 = labels/label2.btw|Printer_Y|2
```

---

## 📂 Structure

```
📦 PrintSingleSerialNumber/
│
├── audit/
│   ├── audit.py
│   ├── audit_report_xxxx-xx-xx_xx-xx.txt
│   └── vulture_whitelist.txt
│
├── controllers/
│   ├── login_controller.py
│   └── print_controller.py
│
├── docs/
│   ├── home_terminal.md
│   ├── scheme.txt
│   └── work_terminal.md
│
├── installer/
│   └── version.txt
│
├── models/
│   ├── user_info.py
│   └── user_model.py
│
├── settings/
│   ├── config.ini
│   └── create_config.py
│
├── src/
│   ├── logs/
│   │   ├── app.json
│   │   └── app.txt
│   │
│   ├── config.ini
│   └── main.py
│
├── utils/
│   ├── bartender_utils.py
│   ├── config_reader.py
│   ├── logger.py
│   ├── login_context.py
│   ├── login_services.py
│   ├── messenger.py
│   ├── path_validation.py
│   ├── resource_resolver.py
│   ├── set_printer.py
│   ├── single_instance.py
│   ├── startup_checker.py
│   ├── system_info.py
│   └── window_stack.py
│
├── views/
│   ├── assets/
│   │   ├── login.tiff
│   │   ├── main.ico
│   │   ├── message.ico
│   │   ├── print.png
│   │   └── splash_logo.png
│   │
│   ├── themes/
│   │   └── style.qss
│   │
│   ├── login_window.py
│   ├── print_window.py
│   └── splash_screen.py
│
├── .flake8
├── .gitignore
├── .pylintrc
├── dev-requirements.in
├── dev-requirements.txt
├── LICENSE
├── README.md
├── requirements.in
└── requirements.txt
```

---

## 🧑‍💻 Author

Developed with 💙 and precision by [Miloslav Hradecky]  
© 2025 — Built to print, parse & simplify 🎉