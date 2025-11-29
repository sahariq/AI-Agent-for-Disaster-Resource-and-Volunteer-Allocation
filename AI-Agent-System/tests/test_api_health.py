"""
Test for the /health endpoint of the Flask API server.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.server import app


def test_health_endpoint():
    """Test that /health returns 200 with correct JSON structure."""
    with app.test_client() as client:
        response = client.get('/health')
        
        # Check status code
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Check response is JSON
        data = response.get_json()
        assert data is not None, "Response should be JSON"
        
        # Check required keys
        assert "status" in data, "Response should contain 'status' key"
        assert "agent" in data, "Response should contain 'agent' key"
        assert "version" in data, "Response should contain 'version' key"
        
        # Check values
        assert data["status"] == "UP", f"Expected status='UP', got '{data['status']}'"
        assert data["agent"] == "Worker_Disaster", f"Expected agent='Worker_Disaster', got '{data['agent']}'"
        assert isinstance(data["version"], str), "Version should be a string"
        assert len(data["version"]) > 0, "Version should not be empty"
        
        print("✓ /health endpoint test passed")
        print(f"  Status: {data['status']}")
        print(f"  Agent: {data['agent']}")
        print(f"  Version: {data['version']}")


if __name__ == "__main__":
    test_health_endpoint()

