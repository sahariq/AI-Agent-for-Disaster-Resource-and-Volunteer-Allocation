#!/usr/bin/env python
"""
Simple script to test all API endpoints.
Make sure the server is running on http://localhost:8000 before running this.
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_endpoint(name, method, url, data=None, headers=None):
    """Test an endpoint and print results."""
    print(f"\nTesting {name}...")
    print(f"  {method} {url}")
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=5)
        else:
            print(f"  ❌ Unsupported method: {method}")
            return False
        
        print(f"  Status Code: {response.status_code}")
        
        try:
            response_json = response.json()
            print(f"  Response:")
            print(json.dumps(response_json, indent=4))
            
            if response.status_code < 400:
                print(f"  ✅ SUCCESS")
                return True
            else:
                print(f"  ⚠️  Error response (but endpoint is working)")
                return False
                
        except json.JSONDecodeError:
            print(f"  Response (not JSON): {response.text}")
            return response.status_code < 400
            
    except requests.exceptions.ConnectionError:
        print(f"  ❌ Connection Error: Server is not running!")
        print(f"     Start the server with: python AI-Agent-System/api/server.py")
        return False
    except requests.exceptions.Timeout:
        print(f"  ❌ Timeout: Server took too long to respond")
        return False
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return False

def main():
    """Run all endpoint tests."""
    print_section("API Endpoint Tester")
    print(f"Base URL: {BASE_URL}")
    print("Make sure the server is running before testing!")
    
    results = []
    
    # Test 1: Root endpoint
    results.append(("Root", test_endpoint(
        "Root Endpoint",
        "GET",
        f"{BASE_URL}/"
    )))
    
    # Test 2: Health check
    results.append(("Health", test_endpoint(
        "Health Check",
        "GET",
        f"{BASE_URL}/health"
    )))
    
    # Test 3: Invoke endpoint
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
    results.append(("Invoke", test_endpoint(
        "Invoke Endpoint",
        "POST",
        f"{BASE_URL}/invoke",
        data=invoke_data,
        headers={"Content-Type": "application/json"}
    )))
    
    # Test 4: Query endpoint
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
    results.append(("Query", test_endpoint(
        "Query Endpoint",
        "POST",
        f"{BASE_URL}/query",
        data=query_data,
        headers={"Content-Type": "application/json"}
    )))
    
    # Print summary
    print_section("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {name:15} {status}")
    
    print(f"\n  Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n  🎉 All tests passed!")
        return 0
    else:
        print(f"\n  ⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)

