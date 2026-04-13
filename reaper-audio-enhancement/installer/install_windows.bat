@echo off
setlocal enabledelayedexpansion

set "PROJECT_ROOT=%~dp0.."

echo ==========================================
echo REAPER Audio Enhancement - Windows Installer
echo ==========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python !PYTHON_VERSION!
echo.

echo Creating virtual environment...
python -m venv "%PROJECT_ROOT%\venv"

echo Installing dependencies...
call "%PROJECT_ROOT%\venv\Scripts\activate.bat"
pip install --upgrade pip setuptools wheel
pip install -r "%PROJECT_ROOT%\requirements.txt"

echo.
echo ==========================================
echo Installation complete!
echo ==========================================
echo.
echo To launch the application:
echo   cd %PROJECT_ROOT%
echo   venv\Scripts\activate.bat
echo   python src\main.py
echo.
echo Or run the setup wizard:
echo   python installer\setup_wizard.py
echo.
pause
