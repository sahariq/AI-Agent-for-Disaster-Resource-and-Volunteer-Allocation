# PowerShell script to test API endpoints from command line
param(
    [string]$BaseUrl = "http://localhost:8000"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Testing API Endpoints" -ForegroundColor Cyan
Write-Host "Base URL: $BaseUrl" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Root endpoint
Write-Host "[1] Testing Root Endpoint (GET /)..." -ForegroundColor Green
try {
    $response = Invoke-WebRequest -Uri "$BaseUrl/" -Method GET -UseBasicParsing
    Write-Host "   Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "   Response:" -ForegroundColor Yellow
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
    Write-Host ""
} catch {
    Write-Host "   ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

# Test 2: Health check
Write-Host "[2] Testing Health Check (GET /health)..." -ForegroundColor Green
try {
    $response = Invoke-WebRequest -Uri "$BaseUrl/health" -Method GET -UseBasicParsing
    Write-Host "   Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "   Response:" -ForegroundColor Yellow
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
    Write-Host ""
} catch {
    Write-Host "   ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

# Test 3: Invoke endpoint
Write-Host "[3] Testing Invoke Endpoint (POST /invoke)..." -ForegroundColor Green
$invokeBody = @{
    message_id = "test-cli-001"
    sender = "Supervisor_Main"
    recipient = "Worker_Disaster"
    type = "task_assignment"
    task = @{
        name = "allocate_resources"
        priority = 1
        parameters = @{
            zones = @(
                @{
                    id = "Z1"
                    severity = 5
                    required_volunteers = 8
                    capacity = 8
                    resources_available = 50
                    min_resources_per_volunteer = 4
                },
                @{
                    id = "Z2"
                    severity = 3
                    required_volunteers = 4
                    capacity = 6
                    resources_available = 30
                    min_resources_per_volunteer = 3
                }
            )
            available_volunteers = 10
            constraints = @{
                fairness_weight = 0.6
            }
        }
    }
    timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
} | ConvertTo-Json -Depth 10

try {
    $response = Invoke-WebRequest -Uri "$BaseUrl/invoke" -Method POST -Body $invokeBody -ContentType "application/json" -UseBasicParsing
    Write-Host "   Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "   Response:" -ForegroundColor Yellow
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
    Write-Host ""
} catch {
    Write-Host "   ERROR: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "   Response Body:" -ForegroundColor Yellow
        Write-Host $responseBody
    }
    Write-Host ""
}

# Test 4: Query endpoint
Write-Host "[4] Testing Query Endpoint (POST /query)..." -ForegroundColor Green
$queryBody = @{
    query = "Prioritize high-severity zones and distribute volunteers fairly."
    zones = @(
        @{
            id = "Z1"
            severity = 5
            required_volunteers = 8
            capacity = 8
            resources_available = 50
            min_resources_per_volunteer = 4
        },
        @{
            id = "Z2"
            severity = 3
            required_volunteers = 4
            capacity = 6
            resources_available = 30
            min_resources_per_volunteer = 3
        }
    )
    available_volunteers = 10
    constraints = @{
        fairness_weight = 0.6
    }
} | ConvertTo-Json -Depth 10

try {
    $response = Invoke-WebRequest -Uri "$BaseUrl/query" -Method POST -Body $queryBody -ContentType "application/json" -UseBasicParsing
    Write-Host "   Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "   Response:" -ForegroundColor Yellow
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
    Write-Host ""
} catch {
    Write-Host "   ERROR: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "   Response Body:" -ForegroundColor Yellow
        Write-Host $responseBody
    }
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Testing Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

