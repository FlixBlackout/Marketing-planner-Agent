@echo off
REM Quick Setup Script for Marketing Planning Assistant

echo.
echo ======================================================================
echo           MARKETING PLANNING ASSISTANT - QUICK SETUP
echo ======================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [OK] Python found!
python --version
echo.

REM Navigate to project directory
cd /d "%~dp0"
echo [INFO] Working directory: %CD%
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [STEP 1/3] Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created!
) else (
    echo [OK] Virtual environment already exists.
)
echo.

REM Activate virtual environment
echo [STEP 2/3] Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated!
echo.

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install dependencies
echo [STEP 3/3] Installing dependencies...
echo.
echo This may take a few minutes...
echo.
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ======================================================================
    echo                      SETUP COMPLETE!
    echo ======================================================================
    echo.
    echo Next steps:
    echo.
    echo   1. Set your API key (optional):
    echo      - Get Gemini API key from: https://makersuite.google.com/app/apikey
    echo      - Create a file named ".env" in this folder
    echo      - Add this line: GEMINI_API_KEY=your-key-here
    echo.
    echo   2. Run the application:
    echo      - Double-click "web_run.bat" (RECOMMENDED)
    echo      - Or run: python api.py
    echo      - Or run: python main.py (for CLI mode)
    echo.
    echo   3. Test without API key:
    echo      - The app works WITHOUT any API key using Simple Planner mode!
    echo.
    echo   4. Access the Dashboard:
    echo      - Open your browser to: http://localhost:8000
    echo.
    echo ======================================================================
    echo.
) else (
    echo.
    echo [WARNING] Some dependencies may have failed to install.
    echo You can still try running the application.
    echo.
)

pause
