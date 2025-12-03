# How to Test API Endpoints

This guide shows you multiple ways to test the Disaster Allocation API endpoints.

## Prerequisites

1. **Start the API Server** first:
   ```bash
   # Windows (PowerShell)
   .\start_api_server.ps1
   
   # Windows (Command Prompt)
   start_api_server.bat
   
   # Or manually:
   cd AI-Agent-System
   python api\server.py
   ```

   The server will run on `http://localhost:8000`

---

## Method 1: Web Browser Interface (Easiest) 🌐

You already have a built-in test interface!

1. **Start the server** (see above)
2. **Open your browser** and go to:
   ```
   http://localhost:8000/test
   ```
   OR open the file directly:
   ```
   file:///G:/multi_agent_system/api_test.html
   ```

3. **Features:**
   - Search and filter endpoints
   - Pre-filled example requests
   - Click to test any endpoint
   - See formatted JSON responses
   - Change base URL if needed

---

## Method 2: Using cURL (Command Line) 💻

### Test Root Endpoint
```bash
curl http://localhost:8000/
```

### Test Health Check
```bash
curl http://localhost:8000/health
```

### Test Invoke Endpoint
```bash
curl -X POST http://localhost:8000/invoke \
  -H "Content-Type: application/json" \
  -d @- << 'EOF'
{
    "message_id": "test-001",
    "sender": "Supervisor_Main",
    "recipient": "Worker_Disaster",
    "type": "task_assignment",
    "task": {
        "name": "allocate_resources",
        "priority": 1,
        "parameters": {
            "zones": [
                {
                    "id": "Z1",
                    "severity": 5,
                    "required_volunteers": 8,
                    "capacity": 8,
                    "resources_available": 50,
                    "min_resources_per_volunteer": 4
                },
                {
                    "id": "Z2",
                    "severity": 3,
                    "required_volunteers": 4,
                    "capacity": 6,
                    "resources_available": 30,
                    "min_resources_per_volunteer": 3
                }
            ],
            "available_volunteers": 10,
            "constraints": {
                "fairness_weight": 0.6
            }
        }
    },
    "timestamp": "2025-01-27T12:00:00Z"
}
EOF
```

### Test Query Endpoint
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Prioritize high-severity zones and distribute volunteers fairly.",
    "zones": [
        {
            "id": "Z1",
            "severity": 5,
            "required_volunteers": 8,
            "capacity": 8,
            "resources_available": 50,
            "min_resources_per_volunteer": 4
        },
        {
            "id": "Z2",
            "severity": 3,
            "required_volunteers": 4,
            "capacity": 6,
            "resources_available": 30,
            "min_resources_per_volunteer": 3
        }
    ],
    "available_volunteers": 10,
    "constraints": {
        "fairness_weight": 0.6
    }
}'
```

**Windows PowerShell Note:** Use `Invoke-WebRequest` instead:
```powershell
Invoke-WebRequest -Uri http://localhost:8000/health -Method GET
```

---

## Method 3: Using Postman 📮

1. **Import the Collection:**
   - Open Postman
   - Click "Import"
   - Copy the JSON from `POSTMAN_API_DOCUMENTATION.md` (lines 435-541)
   - Or import `Disaster_Allocation_API.postman_collection.json` if it exists

2. **Or Create Manually:**
   - Create a new request
   - Set method (GET or POST)
   - Enter URL: `http://localhost:8000/health` (or other endpoint)
   - For POST requests:
     - Go to "Body" tab
     - Select "raw" and "JSON"
     - Paste JSON from examples in `POSTMAN_API_DOCUMENTATION.md`

---

## Method 4: Using Python Script 🐍

Create a test script:

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Test 1: Root endpoint
print("Testing Root Endpoint...")
response = requests.get(f"{BASE_URL}/")
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}\n")

# Test 2: Health check
print("Testing Health Check...")
response = requests.get(f"{BASE_URL}/health")
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}\n")

# Test 3: Invoke endpoint
print("Testing Invoke Endpoint...")
invoke_data = {
    "message_id": "test-001",
    "sender": "Supervisor_Main",
    "recipient": "Worker_Disaster",
    "type": "task_assignment",
    "task": {
        "name": "allocate_resources",
        "priority": 1,
        "parameters": {
            "zones": [
                {
                    "id": "Z1",
                    "severity": 5,
                    "required_volunteers": 8,
                    "capacity": 8,
                    "resources_available": 50,
                    "min_resources_per_volunteer": 4
                },
                {
                    "id": "Z2",
                    "severity": 3,
                    "required_volunteers": 4,
                    "capacity": 6,
                    "resources_available": 30,
                    "min_resources_per_volunteer": 3
                }
            ],
            "available_volunteers": 10,
            "constraints": {
                "fairness_weight": 0.6
            }
        }
    },
    "timestamp": "2025-01-27T12:00:00Z"
}
response = requests.post(
    f"{BASE_URL}/invoke",
    json=invoke_data,
    headers={"Content-Type": "application/json"}
)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}\n")

# Test 4: Query endpoint
print("Testing Query Endpoint...")
query_data = {
    "query": "Prioritize high-severity zones and distribute volunteers fairly.",
    "zones": [
        {
            "id": "Z1",
            "severity": 5,
            "required_volunteers": 8,
            "capacity": 8,
            "resources_available": 50,
            "min_resources_per_volunteer": 4
        },
        {
            "id": "Z2",
            "severity": 3,
            "required_volunteers": 4,
            "capacity": 6,
            "resources_available": 30,
            "min_resources_per_volunteer": 3
        }
    ],
    "available_volunteers": 10,
    "constraints": {
        "fairness_weight": 0.6
    }
}
response = requests.post(
    f"{BASE_URL}/query",
    json=query_data,
    headers={"Content-Type": "application/json"}
)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}\n")
```

Run it:
```bash
python test_endpoints.py
```

---

## Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint - API information |
| GET | `/health` | Health check |
| POST | `/invoke` | Task assignment (Supervisor format) |
| POST | `/query` | Natural language query |

---

## Quick Test Scenarios

### Scenario 1: Basic Test
- 2 zones (severity 5 and 3)
- 10 volunteers
- Expected: Fair distribution

### Scenario 2: High Severity
- 2 zones (severity 8 and 6)
- 40 volunteers
- Expected: More volunteers to high-severity zone

### Scenario 3: Extreme Disaster
- 2 zones (severity 9 and 7)
- 30 volunteers (limited)
- Expected: Maximum allocation to highest severity

---

## Troubleshooting

### Server Not Starting or Endpoints Not Working?

**1. Port 8000 is already in use:**
```bash
# Windows PowerShell
.\kill_port_8000.ps1

# Windows Command Prompt
kill_port_8000.bat

# Or manually:
netstat -ano | findstr :8000
taskkill /F /PID <process_id>
```

**2. Run diagnostic script:**
```bash
python diagnose_server.py
```

**3. Common fixes:**
- Kill processes using port 8000 (see above)
- Make sure you're in the correct directory
- Install dependencies: `pip install -r requirements.txt`
- Restart the server cleanly

**CORS errors?**
- The server has CORS enabled, but if you see errors, check the browser console

**404 errors?**
- Make sure the server is running
- Check the base URL matches (default: `http://localhost:8000`)

**400/500 errors?**
- Check the request body format matches the examples
- Ensure all required fields are present
- Validate JSON syntax

**Server stuck/hanging?**
- Many CLOSE_WAIT connections indicate a stuck server
- Kill all processes on port 8000 and restart
- Use `kill_port_8000.ps1` or `kill_port_8000.bat` to clean up

---

## Example Responses

### Successful Health Check
```json
{
  "status": "UP",
  "agent": "Worker_Disaster",
  "version": "0.1.0"
}
```

### Successful Invoke
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
    "remaining_volunteers": 0,
    "optimization_metadata": {
      "total_volunteers_allocated": 10,
      "fairness_score": 0.85,
      "efficiency_score": 0.92
    }
  }
}
```

---

For more detailed examples, see `POSTMAN_API_DOCUMENTATION.md`

