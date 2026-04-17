@echo off
REM Run Marketing Planning Assistant without Docker
REM This script starts the application directly with Python

echo.
echo ==============================================
echo Marketing Planning Assistant - Quick Run
echo ==============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    echo Please install Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python found!
python --version
echo.

REM Navigate to project directory
cd /d "%~dp0"

REM Check if .env file exists
if not exist .env (
    echo [WARNING] .env file not found!
    echo Please create .env file with your API keys.
    echo.
    echo Example .env file:
    echo OPENROUTER_API_KEY=your-key-here
    echo.
    pause
)

REM Install dependencies if needed
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

echo.
echo ==============================================
echo Starting Marketing Planning Assistant
echo ==============================================
echo.
echo Access the application at:
echo   - API: http://localhost:8000
echo   - Health: http://localhost:8000/health
echo.
echo Press Ctrl+C to stop
echo ==============================================
echo.

REM Start the API server
python api.py

pause
