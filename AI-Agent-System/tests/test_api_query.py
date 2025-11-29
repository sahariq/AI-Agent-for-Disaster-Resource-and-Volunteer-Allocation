"""
Test for the /query endpoint of the Flask API server.
"""

import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.server import app


def test_query_happy_path():
    """Test /query with valid query, zones, and available_volunteers."""
    valid_request = {
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
    
    with app.test_client() as client:
        response = client.post(
            '/query',
            data=json.dumps(valid_request),
            content_type='application/json'
        )
        
        # Check status code
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Check response is JSON
        data = response.get_json()
        assert data is not None, "Response should be JSON"
        
        # Check response structure
        assert "allocation_plan" in data, "Response should contain 'allocation_plan'"
        assert "summary" in data, "Response should contain 'summary'"
        
        # Check allocation_plan
        allocation_plan = data["allocation_plan"]
        assert isinstance(allocation_plan, list), "allocation_plan should be a list"
        assert len(allocation_plan) == 2, "Should have 2 zones"
        
        # Check summary contains natural_language_query
        summary = data["summary"]
        assert "natural_language_query" in summary, "Summary should contain 'natural_language_query'"
        assert summary["natural_language_query"] == valid_request["query"], \
            f"natural_language_query should match input query. Expected '{valid_request['query']}', got '{summary['natural_language_query']}'"
        
        # Check summary contains other metadata fields
        assert "objective_value" in summary, "Summary should contain 'objective_value'"
        assert "solve_time_seconds" in summary, "Summary should contain 'solve_time_seconds'"
        assert "fairness_metrics" in summary, "Summary should contain 'fairness_metrics'"
        assert "remaining_volunteers" in summary, "Summary should contain 'remaining_volunteers'"
        
        print("✓ /query happy path test passed")
        print(f"  Query: {summary['natural_language_query']}")
        print(f"  Zones allocated: {len(allocation_plan)}")
        print(f"  Remaining volunteers: {summary['remaining_volunteers']}")


def test_query_missing_zones():
    """Test /query with missing zones."""
    invalid_request = {
        "query": "Allocate volunteers fairly.",
        "available_volunteers": 12
        # Missing zones!
    }
    
    with app.test_client() as client:
        response = client.post(
            '/query',
            data=json.dumps(invalid_request),
            content_type='application/json'
        )
        
        # Should return 400
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        
        data = response.get_json()
        assert data is not None, "Response should be JSON"
        assert "error" in data, "Should have error message"
        assert "hint" in data, "Should have hint"
        assert "zones and available_volunteers must be provided" in data["error"]
        
        print("✓ /query missing zones test passed")
        print(f"  Error: {data['error']}")


def test_query_missing_available_volunteers():
    """Test /query with missing available_volunteers."""
    invalid_request = {
        "query": "Allocate volunteers fairly.",
        "zones": [
            {"id": "Z1", "severity": 5, "required_volunteers": 8}
        ]
        # Missing available_volunteers!
    }
    
    with app.test_client() as client:
        response = client.post(
            '/query',
            data=json.dumps(invalid_request),
            content_type='application/json'
        )
        
        # Should return 400
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        
        data = response.get_json()
        assert data is not None, "Response should be JSON"
        assert "error" in data, "Should have error message"
        assert "zones and available_volunteers must be provided" in data["error"]
        
        print("✓ /query missing available_volunteers test passed")
        print(f"  Error: {data['error']}")


def test_query_missing_query():
    """Test /query with missing query field."""
    invalid_request = {
        "zones": [
            {"id": "Z1", "severity": 5, "required_volunteers": 8}
        ],
        "available_volunteers": 12
        # Missing query!
    }
    
    with app.test_client() as client:
        response = client.post(
            '/query',
            data=json.dumps(invalid_request),
            content_type='application/json'
        )
        
        # Should return 400
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        
        data = response.get_json()
        assert data is not None, "Response should be JSON"
        assert "error" in data, "Should have error message"
        assert "query" in data["error"].lower(), "Error should mention 'query'"
        
        print("✓ /query missing query test passed")
        print(f"  Error: {data['error']}")


if __name__ == "__main__":
    test_query_happy_path()
    test_query_missing_zones()
    test_query_missing_available_volunteers()
    test_query_missing_query()
    print("\n✓ All /query endpoint tests passed!")

