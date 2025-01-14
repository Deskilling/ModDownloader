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
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.13.1/python-3.13.1.exe -OutFile %pythonDir%\python-installer.exe"
    REM Install Python silently
    "%pythonDir%\python-installer.exe" /quiet InstallAllUsers=1 PrependPath=0 TargetDir="%pythonDir%"
    REM Clean up installer
    del "%pythonDir%\python-installer.exe"
    echo Python has been installed to %pythonDir%.
)

%pythonExe% -m pip install -r requirements.txt
%pythonExe% src/main.py

endlocal
pause