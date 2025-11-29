# AI-Agent-for-Disaster-Resource-and-Volunteer-Allocation

A Python + PuLP optimization agent with a Streamlit dashboard that allocates volunteers/resources across disaster zones based on severity and availability.

## Quick Start

### Setup

```bash
# 0) (Recommended) Create/activate a virtual env
python -m venv .venv

# Windows PowerShell
. .venv\Scripts\Activate.ps1

# Windows Command Prompt
.venv\Scripts\activate.bat

# macOS/Linux
source .venv/bin/activate

# 1) Install dependencies
pip install -r requirements.txt
```

### Running the HTTP API Server

```bash
# Activate virtual environment first (see above)
# Then navigate to AI-Agent-System directory
cd AI-Agent-System

# Start the server
python api/server.py

# Or use the helper script (PowerShell)
.\start_server.ps1

# Or use the helper script (Command Prompt)
start_server.bat
```

The server will start on **http://localhost:8000**

### Running the Worker Agent (Direct Usage)

```bash
# Activate virtual environment first
cd AI-Agent-System

# Run example worker usage
python example_worker_usage.py
```

## HTTP API Endpoints

The Disaster Allocation Worker exposes the following endpoints on **http://localhost:8000**:

### GET /health

Returns a JSON status:

```json
{ "status": "UP", "agent": "Worker_Disaster", "version": "0.1.0" }
```

### POST /invoke

Accepts a Supervisor-style task_assignment JSON and returns a completion_report. Example:

```bash
curl -X POST http://localhost:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "a4b8c9d0-1e2f-3g4h-5i6j-7k8l9m0n1o2p",
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
          }
        ],
        "available_volunteers": 12
      }
    },
    "timestamp": "2025-11-27T12:00:00Z"
  }'
```

### POST /query

Natural-language-friendly endpoint:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Prioritize the highest severity zones while keeping allocation fair.",
    "zones": [
      {
        "id": "Z1",
        "severity": 5,
        "required_volunteers": 8,
        "capacity": 8
      }
    ],
    "available_volunteers": 12
  }'
```

See `CODEBASE_DOCUMENTATION.md` for full details.
