@echo off
echo ========================================
echo Killing processes using port 8000
echo ========================================
echo.

REM Find and kill processes using port 8000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo Killing process %%a...
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo Waiting 2 seconds for port to be released...
timeout /t 2 /nobreak >nul

echo.
echo Done! Port 8000 should now be free.
echo You can now start the server with: python AI-Agent-System\api\server.py
echo.
pause

