# Postman API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Root Endpoint
**GET** `/`

**Description:** Basic API information

**Request:**
- Method: `GET`
- URL: `http://localhost:8000/`
- Headers: None required

**Response (200 OK):**
```json
{
    "message": "Disaster Allocation Worker API",
    "status": "UP"
}
```

---

### 2. Health Check
**GET** `/health`

**Description:** Health check endpoint for supervisor

**Request:**
- Method: `GET`
- URL: `http://localhost:8000/health`
- Headers: None required

**Response (200 OK):**
```json
{
    "status": "UP",
    "agent": "Worker_Disaster",
    "version": "0.1.0"
}
```

---

### 3. Invoke (Task Assignment)
**POST** `/invoke`

**Description:** Accepts a task assignment message and returns a completion report

**Request:**
- Method: `POST`
- URL: `http://localhost:8000/invoke`
- Headers:
  - `Content-Type: application/json`

**Request Body (Basic Example):**
```json
{
    "message_id": "a4b8c9d0-1e2f-3g4h-5i6j-7k8l9test",
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
    "timestamp": "2025-11-27T12:00:00Z"
}
```

**Request Body (Realistic Scenario - Islamabad Earthquake):**
```json
{
    "message_id": "msg-001-islamabad-earthquake",
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
                    "severity": 8,
                    "required_volunteers": 20,
                    "capacity": 25,
                    "resources_available": 120,
                    "min_resources_per_volunteer": 3.5
                },
                {
                    "id": "Z2",
                    "severity": 6,
                    "required_volunteers": 15,
                    "capacity": 18,
                    "resources_available": 80,
                    "min_resources_per_volunteer": 4.0
                }
            ],
            "available_volunteers": 40,
            "constraints": {
                "fairness_weight": 0.6,
                "scenario_id": "SCENARIO_PK_001"
            }
        }
    },
    "timestamp": "2025-11-27T12:00:00Z"
}
```

**Request Body (Karachi Port Industrial Accident):**
```json
{
    "message_id": "msg-002-karachi-industrial",
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
                    "severity": 7,
                    "required_volunteers": 18,
                    "capacity": 20,
                    "resources_available": 90,
                    "min_resources_per_volunteer": 3.5
                },
                {
                    "id": "Z2",
                    "severity": 6,
                    "required_volunteers": 12,
                    "capacity": 15,
                    "resources_available": 70,
                    "min_resources_per_volunteer": 2.5
                }
            ],
            "available_volunteers": 30,
            "constraints": {
                "fairness_weight": 0.7,
                "scenario_id": "SCENARIO_PK_002"
            }
        }
    },
    "timestamp": "2025-11-27T12:00:00Z"
}
```

**Request Body (High Priority - Quetta Earthquake):**
```json
{
    "message_id": "msg-003-quetta-extreme",
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
                    "severity": 9,
                    "required_volunteers": 22,
                    "capacity": 25,
                    "resources_available": 140,
                    "min_resources_per_volunteer": 3.5
                },
                {
                    "id": "Z2",
                    "severity": 7,
                    "required_volunteers": 16,
                    "capacity": 20,
                    "resources_available": 100,
                    "min_resources_per_volunteer": 4.0
                }
            ],
            "available_volunteers": 30,
            "constraints": {
                "fairness_weight": 0.5,
                "scenario_id": "SCENARIO_PK_007",
                "prioritize_high_severity": true
            }
        }
    },
    "timestamp": "2025-11-27T12:00:00Z"
}
```

**Response (200 OK - Success):**
```json
{
    "message_id": "uuid-generated",
    "sender": "Worker_Disaster",
    "recipient": "Supervisor_Main",
    "type": "completion_report",
    "related_message_id": "a4b8c9d0-1e2f-3g4h-5i6j-7k8l9test",
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
    },
    "timestamp": "2025-11-27T12:00:05Z"
}
```

**Response (400 Bad Request - Validation Error):**
```json
{
    "message_id": "uuid-generated",
    "sender": "Worker_Disaster",
    "recipient": "Supervisor_Main",
    "type": "completion_report",
    "related_message_id": "a4b8c9d0-1e2f-3g4h-5i6j-7k8l9test",
    "status": "FAILURE",
    "results": {
        "error": "Expected type='task_assignment', got 'invalid_type'",
        "details": "Validation error in request"
    },
    "timestamp": "2025-11-27T12:00:00Z"
}
```

---

### 4. Query (Natural Language)
**POST** `/query`

**Description:** Natural-language friendly wrapper around the allocation engine

**Request:**
- Method: `POST`
- URL: `http://localhost:8000/query`
- Headers:
  - `Content-Type: application/json`

**Request Body (Basic Example):**
```json
{
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
```

**Request Body (Fairness Focus):**
```json
{
    "query": "Distribute volunteers as fairly as possible across all zones.",
    "zones": [
        {
            "id": "Z1",
            "severity": 8,
            "required_volunteers": 20,
            "capacity": 25,
            "resources_available": 120,
            "min_resources_per_volunteer": 3.5
        },
        {
            "id": "Z2",
            "severity": 6,
            "required_volunteers": 15,
            "capacity": 18,
            "resources_available": 80,
            "min_resources_per_volunteer": 4.0
        },
        {
            "id": "Z3",
            "severity": 4,
            "required_volunteers": 10,
            "capacity": 12,
            "resources_available": 60,
            "min_resources_per_volunteer": 3.0
        }
    ],
    "available_volunteers": 30,
    "constraints": {
        "fairness_weight": 0.8
    }
}
```

**Request Body (Efficiency Focus):**
```json
{
    "query": "Maximize efficiency by allocating volunteers to zones with highest severity first.",
    "zones": [
        {
            "id": "Z1",
            "severity": 9,
            "required_volunteers": 22,
            "capacity": 25,
            "resources_available": 140,
            "min_resources_per_volunteer": 3.5
        },
        {
            "id": "Z2",
            "severity": 7,
            "required_volunteers": 16,
            "capacity": 20,
            "resources_available": 100,
            "min_resources_per_volunteer": 4.0
        },
        {
            "id": "Z3",
            "severity": 5,
            "required_volunteers": 12,
            "capacity": 15,
            "resources_available": 70,
            "min_resources_per_volunteer": 3.5
        }
    ],
    "available_volunteers": 35,
    "constraints": {
        "fairness_weight": 0.3
    }
}
```

**Response (200 OK - Success):**
```json
{
    "allocation_plan": [
        {
            "zone_id": "Z1",
            "allocated": 6,
            "severity": 5
        },
        {
            "zone_id": "Z2",
            "allocated": 4,
            "severity": 3
        }
    ],
    "summary": {
        "total_volunteers_allocated": 10,
        "remaining_volunteers": 0,
        "fairness_score": 0.85,
        "efficiency_score": 0.92,
        "natural_language_query": "Prioritize high-severity zones and distribute volunteers fairly."
    }
}
```

**Response (400 Bad Request - Missing Query):**
```json
{
    "error": "'query' is required and must be a non-empty string",
    "hint": "Ensure 'query' is provided and is a non-empty string."
}
```

**Response (400 Bad Request - Missing Zones):**
```json
{
    "error": "zones and available_volunteers must be provided for now.",
    "hint": "Pass pre-structured zones and available_volunteers along with the query."
}
```

---

## Postman Collection JSON

You can import this JSON directly into Postman:

```json
{
    "info": {
        "name": "Disaster Allocation Worker API",
        "description": "API endpoints for the Disaster Resource and Volunteer Allocation System",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": [
        {
            "name": "Root",
            "request": {
                "method": "GET",
                "header": [],
                "url": {
                    "raw": "http://localhost:8000/",
                    "protocol": "http",
                    "host": ["localhost"],
                    "port": "8000",
                    "path": [""]
                }
            }
        },
        {
            "name": "Health Check",
            "request": {
                "method": "GET",
                "header": [],
                "url": {
                    "raw": "http://localhost:8000/health",
                    "protocol": "http",
                    "host": ["localhost"],
                    "port": "8000",
                    "path": ["health"]
                }
            }
        },
        {
            "name": "Invoke - Basic Example",
            "request": {
                "method": "POST",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": "{\n    \"message_id\": \"a4b8c9d0-1e2f-3g4h-5i6j-7k8l9test\",\n    \"sender\": \"Supervisor_Main\",\n    \"recipient\": \"Worker_Disaster\",\n    \"type\": \"task_assignment\",\n    \"task\": {\n        \"name\": \"allocate_resources\",\n        \"priority\": 1,\n        \"parameters\": {\n            \"zones\": [\n                {\n                    \"id\": \"Z1\",\n                    \"severity\": 5,\n                    \"required_volunteers\": 8,\n                    \"capacity\": 8,\n                    \"resources_available\": 50,\n                    \"min_resources_per_volunteer\": 4\n                },\n                {\n                    \"id\": \"Z2\",\n                    \"severity\": 3,\n                    \"required_volunteers\": 4,\n                    \"capacity\": 6,\n                    \"resources_available\": 30,\n                    \"min_resources_per_volunteer\": 3\n                }\n            ],\n            \"available_volunteers\": 10,\n            \"constraints\": {\n                \"fairness_weight\": 0.6\n            }\n        }\n    },\n    \"timestamp\": \"2025-11-27T12:00:00Z\"\n}"
                },
                "url": {
                    "raw": "http://localhost:8000/invoke",
                    "protocol": "http",
                    "host": ["localhost"],
                    "port": "8000",
                    "path": ["invoke"]
                }
            }
        },
        {
            "name": "Invoke - Islamabad Earthquake",
            "request": {
                "method": "POST",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": "{\n    \"message_id\": \"msg-001-islamabad-earthquake\",\n    \"sender\": \"Supervisor_Main\",\n    \"recipient\": \"Worker_Disaster\",\n    \"type\": \"task_assignment\",\n    \"task\": {\n        \"name\": \"allocate_resources\",\n        \"priority\": 1,\n        \"parameters\": {\n            \"zones\": [\n                {\n                    \"id\": \"Z1\",\n                    \"severity\": 8,\n                    \"required_volunteers\": 20,\n                    \"capacity\": 25,\n                    \"resources_available\": 120,\n                    \"min_resources_per_volunteer\": 3.5\n                },\n                {\n                    \"id\": \"Z2\",\n                    \"severity\": 6,\n                    \"required_volunteers\": 15,\n                    \"capacity\": 18,\n                    \"resources_available\": 80,\n                    \"min_resources_per_volunteer\": 4.0\n                }\n            ],\n            \"available_volunteers\": 40,\n            \"constraints\": {\n                \"fairness_weight\": 0.6,\n                \"scenario_id\": \"SCENARIO_PK_001\"\n            }\n        }\n    },\n    \"timestamp\": \"2025-11-27T12:00:00Z\"\n}"
                },
                "url": {
                    "raw": "http://localhost:8000/invoke",
                    "protocol": "http",
                    "host": ["localhost"],
                    "port": "8000",
                    "path": ["invoke"]
                }
            }
        },
        {
            "name": "Query - Basic",
            "request": {
                "method": "POST",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": "{\n    \"query\": \"Prioritize high-severity zones and distribute volunteers fairly.\",\n    \"zones\": [\n        {\n            \"id\": \"Z1\",\n            \"severity\": 5,\n            \"required_volunteers\": 8,\n            \"capacity\": 8,\n            \"resources_available\": 50,\n            \"min_resources_per_volunteer\": 4\n        },\n        {\n            \"id\": \"Z2\",\n            \"severity\": 3,\n            \"required_volunteers\": 4,\n            \"capacity\": 6,\n            \"resources_available\": 30,\n            \"min_resources_per_volunteer\": 3\n        }\n    ],\n    \"available_volunteers\": 10,\n    \"constraints\": {\n        \"fairness_weight\": 0.6\n    }\n}"
                },
                "url": {
                    "raw": "http://localhost:8000/query",
                    "protocol": "http",
                    "host": ["localhost"],
                    "port": "8000",
                    "path": ["query"]
                }
            }
        }
    ]
}
```

---

## Quick Test Scenarios

### Scenario 1: Small Scale Disaster
- **Zones:** 2 zones with severity 5 and 3
- **Volunteers:** 10 available
- **Expected:** Fair distribution prioritizing higher severity

### Scenario 2: Large Scale Disaster (Islamabad)
- **Zones:** 2 zones with severity 8 and 6
- **Volunteers:** 40 available
- **Expected:** More volunteers to high-severity zone

### Scenario 3: Extreme Disaster (Quetta)
- **Zones:** 2 zones with severity 9 and 7
- **Volunteers:** 30 available (limited)
- **Expected:** Maximum allocation to highest severity zone

### Scenario 4: Multiple Zones
- **Zones:** 3+ zones with varying severity
- **Volunteers:** 30-50 available
- **Expected:** Balanced allocation based on fairness_weight

---

## Notes

1. **Server Port:** Default is `8000`. Make sure the server is running before testing.
2. **Zone Fields:** Required fields for zones:
   - `id` (string)
   - `severity` (number, 1-10)
   - `required_volunteers` (number)
   - `capacity` (number)
   - `resources_available` (number, optional but recommended)
   - `min_resources_per_volunteer` (number, optional but recommended)

3. **Constraints:**
   - `fairness_weight`: 0.0 to 1.0 (default: 0.6)
     - Higher value = more fair distribution
     - Lower value = more efficiency-focused (prioritize high severity)

4. **Error Handling:**
   - All endpoints return JSON error responses
   - Validation errors return 400 status
   - Server errors return 500 status

5. **Timestamps:** Use ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`

