# PowerShell script to start Flask server with virtual environment
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
$venvPath = "$projectRoot\.venv"

# Check if virtual environment exists
if (-not (Test-Path "$venvPath\Scripts\Activate.ps1")) {
    Write-Host "Error: Virtual environment not found at $venvPath" -ForegroundColor Red
    Write-Host "Please create it with: python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
& "$venvPath\Scripts\Activate.ps1"

# Change to AI-Agent-System directory
Set-Location $scriptPath

Write-Host "Starting Flask server on http://localhost:8000..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the server
python api/server.py

