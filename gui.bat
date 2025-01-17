@echo off
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python is installed.
    python --version

    cls

    py src/main_gui.py

) else (
    echo Python is not installed.
)
pause
