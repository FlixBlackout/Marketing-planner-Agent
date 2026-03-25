@echo off
REM Run Marketing Planning Assistant

cd /d "%~dp0"

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

echo.
echo ======================================================================
echo              MARKETING PLANNING ASSISTANT
echo ======================================================================
echo.

REM Ask user which mode to run
echo Choose running mode:
echo.
echo   1. Simple Planner (No API key required - FAST)
echo   2. Gemini Planner (AI-powered - requires Gemini API key)
echo   3. Exit
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="3" exit /b

if "%choice%"=="1" (
    echo.
    echo Starting Simple Planner...
    echo.
    python main.py
) else if "%choice%"=="2" (
    echo.
    echo Starting Gemini Planner...
    echo.
    python gemini_planner.py
) else (
    echo.
    echo Invalid choice. Please run again and select 1, 2, or 3.
    echo.
)

pause
