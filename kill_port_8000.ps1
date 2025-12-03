# PowerShell script to kill processes using port 8000
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Killing processes using port 8000" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Find processes using port 8000
$connections = netstat -ano | Select-String ":8000" | Select-String "LISTENING"

if ($connections) {
    foreach ($conn in $connections) {
        $parts = $conn.ToString().Split() | Where-Object { $_ -ne "" }
        if ($parts.Length -gt 0) {
            $processId = $parts[-1]
            Write-Host "Killing process $processId..." -ForegroundColor Yellow
            try {
                Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
                Write-Host "  Process $processId killed" -ForegroundColor Green
            } catch {
                Write-Host "  Could not kill process $processId" -ForegroundColor Red
            }
        }
    }
} else {
    Write-Host "No processes found listening on port 8000" -ForegroundColor Green
}

Write-Host ""
Write-Host "Waiting 2 seconds for port to be released..." -ForegroundColor Yellow
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "Done! Port 8000 should now be free." -ForegroundColor Green
Write-Host "You can now start the server with:" -ForegroundColor Yellow
Write-Host "  cd AI-Agent-System" -ForegroundColor Cyan
Write-Host '  python api\server.py' -ForegroundColor Cyan
Write-Host ""
