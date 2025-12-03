# PowerShell script to start the API server
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Disaster Allocation API Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "AI-Agent-System\api\server.py")) {
    Write-Host "Error: Cannot find server.py" -ForegroundColor Red
    Write-Host "Please run this script from the project root directory" -ForegroundColor Yellow
    exit 1
}

# Change to AI-Agent-System directory
Set-Location "AI-Agent-System"

# Check if flask-cors is installed
try {
    python -c "import flask_cors" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installing flask-cors..." -ForegroundColor Yellow
        pip install flask-cors
    }
} catch {
    Write-Host "Installing flask-cors..." -ForegroundColor Yellow
    pip install flask-cors
}

Write-Host ""
Write-Host "Starting server on http://localhost:8000..." -ForegroundColor Green
Write-Host "Open http://localhost:8000/test in your browser" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start the server
python api\server.py

