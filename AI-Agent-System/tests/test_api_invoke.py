"""
Test for the /invoke endpoint of the Flask API server.
"""

import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.server import app


def test_invoke_happy_path():
    """Test /invoke with a valid task_assignment message."""
    valid_request = {
        "message_id": "test-uuid-123",
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
                        "required_volunteers": 6,
                        "capacity": 6,
                        "resources_available": 30,
                        "min_resources_per_volunteer": 3
                    }
                ],
                "available_volunteers": 12,
                "constraints": {
                    "fairness_weight": 0.6
                }
            }
        },
        "timestamp": "2025-11-27T10:00:00Z"
    }
    
    with app.test_client() as client:
        response = client.post(
            '/invoke',
            data=json.dumps(valid_request),
            content_type='application/json'
        )
        
        # Check status code
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Check response is JSON
        data = response.get_json()
        assert data is not None, "Response should be JSON"
        
        # Check completion_report structure
        assert data["type"] == "completion_report", "Should return completion_report"
        assert data["status"] == "SUCCESS", "Status should be SUCCESS"
        assert data["sender"] == "Worker_Disaster", "Sender should be Worker_Disaster"
        assert data["recipient"] == "Supervisor_Main", "Recipient should match request sender"
        assert data["related_message_id"] == "test-uuid-123", "Should link to original message_id"
        assert "message_id" in data, "Should have message_id"
        assert "timestamp" in data, "Should have timestamp"
        
        # Check results structure
        assert "results" in data, "Should have results"
        results = data["results"]
        assert "allocation_plan" in results, "Results should contain allocation_plan"
        assert "remaining_volunteers" in results, "Results should contain remaining_volunteers"
        assert "optimization_metadata" in results, "Results should contain optimization_metadata"
        
        # Check allocation_plan format
        allocation_plan = results["allocation_plan"]
        assert isinstance(allocation_plan, list), "allocation_plan should be a list"
        assert len(allocation_plan) == 2, "Should have 2 zones"
        
        for zone_alloc in allocation_plan:
            assert "zone_id" in zone_alloc, "Each allocation should have zone_id"
            assert "assigned_volunteers" in zone_alloc, "Each allocation should have assigned_volunteers"
            assert "severity" in zone_alloc, "Each allocation should have severity"
        
        print("✓ /invoke happy path test passed")
        print(f"  Status: {data['status']}")
        print(f"  Zones allocated: {len(allocation_plan)}")
        print(f"  Remaining volunteers: {results['remaining_volunteers']}")


def test_invoke_missing_zones():
    """Test /invoke with missing zones parameter."""
    invalid_request = {
        "message_id": "test-uuid-456",
        "sender": "Supervisor_Main",
        "recipient": "Worker_Disaster",
        "type": "task_assignment",
        "task": {
            "name": "allocate_resources",
            "priority": 1,
            "parameters": {
                "available_volunteers": 12
                # Missing zones!
            }
        },
        "timestamp": "2025-11-27T10:00:00Z"
    }
    
    with app.test_client() as client:
        response = client.post(
            '/invoke',
            data=json.dumps(invalid_request),
            content_type='application/json'
        )
        
        # Should return 400 for validation error
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        
        data = response.get_json()
        assert data is not None, "Response should be JSON"
        assert data["status"] == "FAILURE", "Status should be FAILURE"
        assert "error" in data["results"], "Should have error message"
        
        print("✓ /invoke missing zones test passed")
        print(f"  Status: {data['status']}")
        print(f"  Error: {data['results']['error']}")


def test_invoke_wrong_type():
    """Test /invoke with wrong message type."""
    invalid_request = {
        "message_id": "test-uuid-789",
        "sender": "Supervisor_Main",
        "recipient": "Worker_Disaster",
        "type": "wrong_type",  # Wrong type!
        "task": {
            "name": "allocate_resources",
            "priority": 1,
            "parameters": {
                "zones": [{"id": "Z1", "severity": 5, "required_volunteers": 8}],
                "available_volunteers": 12
            }
        },
        "timestamp": "2025-11-27T10:00:00Z"
    }
    
    with app.test_client() as client:
        response = client.post(
            '/invoke',
            data=json.dumps(invalid_request),
            content_type='application/json'
        )
        
        # Should return 400 for validation error
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        
        data = response.get_json()
        assert data is not None, "Response should be JSON"
        assert data["status"] == "FAILURE", "Status should be FAILURE"
        assert "error" in data["results"], "Should have error message"
        assert "task_assignment" in data["results"]["error"], "Error should mention task_assignment"
        
        print("✓ /invoke wrong type test passed")
        print(f"  Status: {data['status']}")
        print(f"  Error: {data['results']['error']}")


if __name__ == "__main__":
    test_invoke_happy_path()
    test_invoke_missing_zones()
    test_invoke_wrong_type()
    print("\n✓ All /invoke endpoint tests passed!")

