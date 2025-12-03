@echo off
echo ========================================
echo Starting Disaster Allocation API Server
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "AI-Agent-System\api\server.py" (
    echo Error: Cannot find server.py
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

REM Change to AI-Agent-System directory
cd AI-Agent-System

REM Check if flask-cors is installed
python -c "import flask_cors" 2>nul
if errorlevel 1 (
    echo.
    echo Installing flask-cors...
    pip install flask-cors
    echo.
)

echo.
echo Starting server on http://localhost:8000...
echo Open http://localhost:8000/test in your browser
echo Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

python api\server.py

pause

