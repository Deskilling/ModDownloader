@echo off
setlocal

REM Define the Python directory
set "pythonDir=%~dp0python"
set "pythonExe=%pythonDir%\python.exe"

REM Check if Python is already installed
if exist "%pythonExe%" (
    echo Python is already installed in %pythonDir%.
) else (
    echo Python is not installed. Downloading and installing Python...
    
    REM Create a directory for Python in the same directory as run.bat
    mkdir "%pythonDir%"
    
    REM Download Python installer
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.13.1/python-3.13.1.exe' -OutFile '%pythonDir%\python-installer.exe'"
    
    REM Verify download success
    if not exist "%pythonDir%\python-installer.exe" (
        echo Failed to download Python installer. Exiting.
        exit /b 1
    )
    
    REM Install Python silently
    "%pythonDir%\python-installer.exe" /quiet InstallAllUsers=0 PrependPath=0 TargetDir="%pythonDir%"
    
    REM Check if Python was installed successfully
    if not exist "%pythonExe%" (
        echo Python installation failed. Exiting.
        exit /b 1
    )
    
    REM Clean up installer
    del "%pythonDir%\python-installer.exe"
    
    echo Python has been installed to %pythonDir%.
)

REM Ensure pip is installed and functional
"%pythonExe%" -m ensurepip --upgrade
if errorlevel 1 (
    echo Failed to ensure pip is installed. Exiting.
    exit /b 1
)

REM Install required Python packages
"%pythonExe%" -m pip install --upgrade pip
"%pythonExe%" -m pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install required packages. Exiting.
    exit /b 1
)

REM Run the main Python script
"%pythonExe%" src/main.py
if errorlevel 1 (
    echo Failed to execute the main Python script. Exiting.
    exit /b 1
)

endlocal
pause
