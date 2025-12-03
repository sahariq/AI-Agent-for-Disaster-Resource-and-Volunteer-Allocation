# Command Line Testing Guide

Test your API endpoints directly from PowerShell or Command Prompt.

## Prerequisites

**First, start your server:**
```powershell
# PowerShell
.\start_api_server.ps1

# Or manually:
cd AI-Agent-System
python api\server.py
```

Keep the server running in one terminal, then use another terminal to test.

---

## Quick Test Scripts

### PowerShell (Windows)
```powershell
.\test_endpoints_cli.ps1
```

### Bash/Git Bash/WSL
```bash
bash test_endpoints_cli.sh
```

### Python
```bash
python test_endpoints.py
```

---

## Individual Commands

### 1. Test Root Endpoint (GET /)

**PowerShell:**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/" -Method GET -UseBasicParsing | Select-Object StatusCode, Content
```

**PowerShell (JSON formatted):**
```powershell
(Invoke-WebRequest -Uri "http://localhost:8000/" -UseBasicParsing).Content | ConvertFrom-Json | ConvertTo-Json
```

**cURL (if installed):**
```bash
curl http://localhost:8000/
```

**Python:**
```bash
python -c "import requests; import json; r = requests.get('http://localhost:8000/'); print(json.dumps(r.json(), indent=2))"
```

---

### 2. Test Health Check (GET /health)

**PowerShell:**
```powershell
(Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing).Content | ConvertFrom-Json | ConvertTo-Json
```

**cURL:**
```bash
curl http://localhost:8000/health
```

**Python:**
```bash
python -c "import requests; import json; r = requests.get('http://localhost:8000/health'); print(json.dumps(r.json(), indent=2))"
```

---

### 3. Test Invoke Endpoint (POST /invoke)

**PowerShell:**
```powershell
$body = @{
    message_id = "test-001"
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
    timestamp = "2025-01-27T12:00:00Z"
} | ConvertTo-Json -Depth 10

Invoke-WebRequest -Uri "http://localhost:8000/invoke" -Method POST -Body $body -ContentType "application/json" -UseBasicParsing | Select-Object StatusCode, @{Name="Content";Expression={$_.Content | ConvertFrom-Json | ConvertTo-Json}}
```

**cURL:**
```bash
curl -X POST http://localhost:8000/invoke ^
  -H "Content-Type: application/json" ^
  -d "{\"message_id\":\"test-001\",\"sender\":\"Supervisor_Main\",\"recipient\":\"Worker_Disaster\",\"type\":\"task_assignment\",\"task\":{\"name\":\"allocate_resources\",\"priority\":1,\"parameters\":{\"zones\":[{\"id\":\"Z1\",\"severity\":5,\"required_volunteers\":8,\"capacity\":8,\"resources_available\":50,\"min_resources_per_volunteer\":4},{\"id\":\"Z2\",\"severity\":3,\"required_volunteers\":4,\"capacity\":6,\"resources_available\":30,\"min_resources_per_volunteer\":3}],\"available_volunteers\":10,\"constraints\":{\"fairness_weight\":0.6}},\"timestamp\":\"2025-01-27T12:00:00Z\"}"
```

**cURL (from file):**
```bash
# Save JSON to invoke.json, then:
curl -X POST http://localhost:8000/invoke -H "Content-Type: application/json" -d @invoke.json
```

**Python:**
```bash
python -c "import requests; import json; data={'message_id':'test-001','sender':'Supervisor_Main','recipient':'Worker_Disaster','type':'task_assignment','task':{'name':'allocate_resources','priority':1,'parameters':{'zones':[{'id':'Z1','severity':5,'required_volunteers':8,'capacity':8,'resources_available':50,'min_resources_per_volunteer':4},{'id':'Z2','severity':3,'required_volunteers':4,'capacity':6,'resources_available':30,'min_resources_per_volunteer':3}],'available_volunteers':10,'constraints':{'fairness_weight':0.6}},'timestamp':'2025-01-27T12:00:00Z'}; r=requests.post('http://localhost:8000/invoke',json=data); print(json.dumps(r.json(),indent=2))"
```

---

### 4. Test Query Endpoint (POST /query)

**PowerShell:**
```powershell
$body = @{
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

Invoke-WebRequest -Uri "http://localhost:8000/query" -Method POST -Body $body -ContentType "application/json" -UseBasicParsing | Select-Object StatusCode, @{Name="Content";Expression={$_.Content | ConvertFrom-Json | ConvertTo-Json}}
```

**cURL:**
```bash
curl -X POST http://localhost:8000/query ^
  -H "Content-Type: application/json" ^
  -d "{\"query\":\"Prioritize high-severity zones and distribute volunteers fairly.\",\"zones\":[{\"id\":\"Z1\",\"severity\":5,\"required_volunteers\":8,\"capacity\":8,\"resources_available\":50,\"min_resources_per_volunteer\":4},{\"id\":\"Z2\",\"severity\":3,\"required_volunteers\":4,\"capacity\":6,\"resources_available\":30,\"min_resources_per_volunteer\":3}],\"available_volunteers\":10,\"constraints\":{\"fairness_weight\":0.6}}"
```

---

## Quick One-Liners

### Check if server is running:
```powershell
# PowerShell
try { (Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing).StatusCode } catch { "Server not running" }

# cURL
curl http://localhost:8000/health
```

### Get formatted JSON response:
```powershell
# PowerShell
(Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing).Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

---

## Testing Workflow

1. **Start server** (Terminal 1):
   ```powershell
   cd AI-Agent-System
   python api\server.py
   ```

2. **Test endpoints** (Terminal 2):
   ```powershell
   # Quick test all endpoints
   .\test_endpoints_cli.ps1
   
   # Or test individually
   (Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing).Content | ConvertFrom-Json
   ```

---

## Troubleshooting

**"Unable to connect" error:**
- Make sure server is running
- Check port 8000 is not blocked
- Verify URL is correct: `http://localhost:8000`

**"Connection refused" error:**
- Server is not running - start it first
- Port might be in use - run `.\kill_port_8000.ps1`

**JSON parsing errors:**
- Make sure Content-Type header is set to `application/json` for POST requests
- Verify JSON syntax is correct

---

## Example Output

**Health Check:**
```json
{
  "status": "UP",
  "agent": "Worker_Disaster",
  "version": "0.1.0"
}
```

**Invoke Response:**
```json
{
  "message_id": "uuid-generated",
  "sender": "Worker_Disaster",
  "recipient": "Supervisor_Main",
  "type": "completion_report",
  "status": "SUCCESS",
  "results": {
    "allocation_plan": [
      {
        "zone_id": "Z1",
        "assigned_volunteers": 6,
        "severity": 5
      },
      {
        "zone_id": "Z2",
        "assigned_volunteers": 4,
        "severity": 3
      }
    ],
    "remaining_volunteers": 0
  }
}
```

