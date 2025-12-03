#!/bin/bash
# Bash script to test API endpoints from command line (for Git Bash/WSL)
# Usage: bash test_endpoints_cli.sh

BASE_URL="${1:-http://localhost:8000}"

echo "========================================"
echo "Testing API Endpoints"
echo "Base URL: $BASE_URL"
echo "========================================"
echo ""

# Test 1: Root endpoint
echo "[1] Testing Root Endpoint (GET /)..."
response=$(curl -s -w "\n%{http_code}" "$BASE_URL/")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')
echo "   Status: $http_code"
echo "   Response:"
echo "$body" | python -m json.tool 2>/dev/null || echo "$body"
echo ""

# Test 2: Health check
echo "[2] Testing Health Check (GET /health)..."
response=$(curl -s -w "\n%{http_code}" "$BASE_URL/health")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')
echo "   Status: $http_code"
echo "   Response:"
echo "$body" | python -m json.tool 2>/dev/null || echo "$body"
echo ""

# Test 3: Invoke endpoint
echo "[3] Testing Invoke Endpoint (POST /invoke)..."
invoke_json='{
    "message_id": "test-cli-001",
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
}'

response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/invoke" \
    -H "Content-Type: application/json" \
    -d "$invoke_json")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')
echo "   Status: $http_code"
echo "   Response:"
echo "$body" | python -m json.tool 2>/dev/null || echo "$body"
echo ""

# Test 4: Query endpoint
echo "[4] Testing Query Endpoint (POST /query)..."
query_json='{
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

response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/query" \
    -H "Content-Type: application/json" \
    -d "$query_json")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')
echo "   Status: $http_code"
echo "   Response:"
echo "$body" | python -m json.tool 2>/dev/null || echo "$body"
echo ""

echo "========================================"
echo "Testing Complete!"
echo "========================================"

