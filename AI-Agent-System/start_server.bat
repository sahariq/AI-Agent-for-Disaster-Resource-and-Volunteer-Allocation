@echo off
REM Activate virtual environment and start Flask server
cd /d "%~dp0\.."
if not exist ".venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found at .venv
    echo Please create it with: python -m venv .venv
    pause
    exit /b 1
)
call .venv\Scripts\activate.bat
cd AI-Agent-System
echo Starting Flask server on http://localhost:8000...
echo Press Ctrl+C to stop the server
python api/server.py

