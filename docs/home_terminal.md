# Commands to create an exe file

## PackingLine

### 1. Open a session in a given folder

```Powershell
cd "C:\Users\MiloslavHradecky\GitHome\Python\PyQt\PrintSingleSerialNumber\"
```

### 2. Create a .spec file

```Powershell
& "C:\Users\MiloslavHradecky\GitHome\Python\PyQt\PrintSingleSerialNumber\.venv\Scripts\python.exe" "C:\Users\MiloslavHradecky\GitHome\Python\PyQt\PrintSingleSerialNumber\.venv\Scripts\pyinstaller.exe" --name=PrintSingleSN --version-file=installer\version.txt --noconfirm --onefile --noconsole --windowed --icon=views\assets\main.ico src\main.py
```

### 3. Edit the created .spec file

```Text
# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('views/assets/login.tiff', 'views/assets'),
        ('views/assets/main.ico', 'views/assets'),
        ('views/assets/message.ico', 'views/assets'),
        ('views/assets/splash_logo.png', 'views/assets'),
        ('views/themes/style.qss', 'views/themes'),
        ('controllers/', 'controllers'),
        ('models/', 'models'),
        ('utils/', 'utils'),
        ('views/', 'views'),
    ],
    hiddenimports=['logging.handlers', 'platform', 'win32com', 'win32com.client', 'win32print'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PrintSingleSN',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='installer/version.txt',
    icon=['views/assets/main.ico'],
)
```

### 4. Create an .exe

```Powershell
& "C:\Users\MiloslavHradecky\GitHome\Python\PyQt\PrintSingleSerialNumber\.venv\Scripts\python.exe" "C:\Users\MiloslavHradecky\GitHome\Python\PyQt\PrintSingleSerialNumber\.venv\Scripts\pyinstaller.exe" PrintSingleSN.spec
```
