@echo off
setlocal

REM Set the version and download path
set PYTHON_VERSION=3.11.6
set DOWNLOAD_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe
set INSTALL_DIR=%cd%\python
set SCRIPT_PATH=%cd%\src\main.py

REM Check if the python directory exists, create if not
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Download Python installer
echo Downloading Python %PYTHON_VERSION%...
curl -o python_installer.exe %DOWNLOAD_URL%
if %errorlevel% neq 0 (
    echo Failed to download Python installer.
    exit /b 1
)

REM Install Python to the specified directory
echo Installing Python to %INSTALL_DIR%...
python_installer.exe /quiet InstallAllUsers=0 TargetDir="%INSTALL_DIR%" Include_launcher=0
if %errorlevel% neq 0 (
    echo Failed to install Python.
    del python_installer.exe
    exit /b 1
)

REM Clean up installer
del python_installer.exe
echo Python installed successfully in %INSTALL_DIR%.

REM Add Python installation to PATH temporarily
set PATH=%INSTALL_DIR%;%PATH%

REM Install required Python packages
echo Installing required Python packages...
python -m pip install --upgrade pip
python -m pip install requests
if %errorlevel% neq 0 (
    echo Failed to install required packages.
    exit /b 1
)

REM Change directory to the Python installation folder and run the script
cd /d "%INSTALL_DIR%"
cls
echo Running main.py script from %SCRIPT_PATH%...
python "%SCRIPT_PATH%"
if %errorlevel% neq 0 (
    echo Failed to run main.py.
    exit /b 1
)

endlocal
