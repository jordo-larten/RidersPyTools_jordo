@echo off
setlocal

cd /d "%~dp0"

set "PROJECT_ROOT=%CD%"
set "QT_DIR=%PROJECT_ROOT%\QtFiles"
set "VENV=%PROJECT_ROOT%\.venv"
set "PYTHONPATH=%PROJECT_ROOT%"

if not exist "%VENV%\Scripts\python.exe" (
    echo Creating virtual environment...

    py -3.13 -m venv "%VENV%" || py -3 -m venv "%VENV%"

    if errorlevel 1 (
        echo.
        echo Python could not be found.
        echo Install Python, then run this batch file again.
        pause
        exit /b 1
    )

    echo Installing requirements...
    "%VENV%\Scripts\python.exe" -m pip install --upgrade pip
    "%VENV%\Scripts\python.exe" -m pip install -r "%PROJECT_ROOT%\requirements.txt"

    if errorlevel 1 (
        echo.
        echo Failed to install requirements.
        pause
        exit /b 1
    )
)

cd /d "%QT_DIR%"

"%VENV%\Scripts\python.exe" "mainwindow.py"

pause