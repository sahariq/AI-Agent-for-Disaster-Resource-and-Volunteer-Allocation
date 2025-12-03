"""
Flask HTTP server for the Disaster Allocation Worker API.

This server will expose endpoints for:
- /health - Health check endpoint
- /invoke - Task invocation endpoint
- /query - Query endpoint
"""

import os
import sys
import uuid
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add parent directory to path for config imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from optimization.volunteer_allocator import run_allocation
from shared.utils import get_utc_timestamp

app = Flask(__name__)
CORS(app)  # Enable CORS for browser requests

# Agent ID from config
AGENT_ID = "Worker_Disaster"


def get_version() -> str:
    """
    Read version from config/settings.yaml or return default.
    
    Returns:
        Version string (default: "0.1.0")
    """
    try:
        import yaml
        config_path = Path(__file__).parent.parent / "config" / "settings.yaml"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                if config and 'system' in config and 'version' in config['system']:
                    return config['system']['version']
    except Exception:
        # If YAML parsing fails or file doesn't exist, use default
        pass
    
    return "0.1.0"


@app.route("/", methods=["GET"])
def root():
    """Root endpoint providing basic API information."""
    return jsonify({
        "message": "Disaster Allocation Worker API",
        "status": "UP"
    })


@app.route("/test", methods=["GET"])
def test_page():
    """Serve the browser test page."""
    # Look for api_test.html in project root (parent of AI-Agent-System)
    test_file_path = Path(__file__).parent.parent.parent / "api_test.html"
    if test_file_path.exists():
        with open(test_file_path, 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/html'}
    else:
        # Fallback: return a simple message
        return jsonify({
            "message": "Test page not found. Please ensure api_test.html is in the project root.",
            "endpoints": {
                "health": "/health",
                "invoke": "/invoke (POST)",
                "query": "/query (POST)"
            }
        }), 404


@app.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint for supervisor.
    
    Returns:
        JSON with status, agent, and version on success (200)
        JSON with error on failure (500)
    """
    try:
        version = get_version()
        return jsonify({
            "status": "UP",
            "agent": AGENT_ID,
            "version": version
        }), 200
    except Exception as e:
        return jsonify({
            "status": "DOWN",
            "error": str(e)
        }), 500


@app.route("/invoke", methods=["POST"])
def invoke():
    """
    Accepts a Supervisor-style task_assignment message and returns a completion_report.
    
    Expected request body:
    {
        "message_id": "uuid-1",
        "sender": "Supervisor_Main",
        "recipient": "Worker_Disaster",
        "type": "task_assignment",
        "task": {
            "name": "allocate_resources",
            "priority": 1,
            "parameters": {
                "zones": [...],
                "available_volunteers": 12,
                "constraints": {...}  # optional
            }
        },
        "timestamp": "2025-11-27T..."
    }
    
    Returns:
        HTTP 200 with completion_report on success
        HTTP 400/500 with error completion_report on failure
    """
    try:
        # Parse request body
        body = request.get_json(force=True)
        if not body:
            raise ValueError("Request body must be valid JSON")
        
        # Validate message type
        if body.get("type") != "task_assignment":
            raise ValueError(f"Expected type='task_assignment', got '{body.get('type')}'")
        
        # Validate task is present
        if "task" not in body:
            raise ValueError("Missing required field: 'task'")
        
        task = body["task"]
        
        # Validate task name
        if task.get("name") != "allocate_resources":
            raise ValueError(f"Unsupported task name: '{task.get('name')}'. Only 'allocate_resources' is supported")
        
        # Extract parameters
        parameters = task.get("parameters", {})
        zones = parameters.get("zones", [])
        available_volunteers = parameters.get("available_volunteers", 0)
        constraints = parameters.get("constraints", {})
        
        # Validate zones
        if not zones or not isinstance(zones, list):
            raise ValueError("'zones' must be a non-empty list")
        
        # Validate available_volunteers
        if not isinstance(available_volunteers, (int, float)) or available_volunteers < 0:
            raise ValueError("'available_volunteers' must be a non-negative number")
        
        # Call optimization engine
        allocation_plan, metadata = run_allocation(
            zones=zones,
            available_volunteers=int(available_volunteers),
            fairness_weight=constraints.get("fairness_weight", 0.6),
            extra_constraints=constraints if constraints else None
        )
        
        # Transform allocation_plan to match expected format
        # Similar to what worker does: extract zone_id, assigned_volunteers, severity
        plan = [
            {
                "zone_id": alloc["zone_id"],
                "assigned_volunteers": alloc["allocated"],
                "severity": next((z["severity"] for z in zones if z["id"] == alloc["zone_id"]), "N/A")
            }
            for alloc in allocation_plan
        ]
        
        # Build completion_report
        completion_report = {
            "message_id": str(uuid.uuid4()),
            "sender": AGENT_ID,
            "recipient": body.get("sender", "Supervisor_Main"),
            "type": "completion_report",
            "related_message_id": body.get("message_id"),
            "status": "SUCCESS",
            "results": {
                "allocation_plan": plan,
                "remaining_volunteers": metadata.get("remaining_volunteers", 0),
                "optimization_metadata": metadata
            },
            "timestamp": get_utc_timestamp()
        }
        
        return jsonify(completion_report), 200
        
    except ValueError as e:
        # Validation errors - return 400
        # Try to get sender and message_id from request, but handle gracefully if parsing fails
        try:
            body = request.get_json(silent=True) or {}
            sender = body.get("sender", "Supervisor_Main")
            msg_id = body.get("message_id")
        except Exception:
            sender = "Supervisor_Main"
            msg_id = None
        
        error_report = {
            "message_id": str(uuid.uuid4()),
            "sender": AGENT_ID,
            "recipient": sender,
            "type": "completion_report",
            "related_message_id": msg_id,
            "status": "FAILURE",
            "results": {
                "error": str(e),
                "details": "Validation error in request"
            },
            "timestamp": get_utc_timestamp()
        }
        return jsonify(error_report), 400
        
    except Exception as e:
        # Unexpected errors - return 500
        import traceback
        # Try to get sender and message_id from request, but handle gracefully if parsing fails
        try:
            body = request.get_json(silent=True) or {}
            sender = body.get("sender", "Supervisor_Main")
            msg_id = body.get("message_id")
        except Exception:
            sender = "Supervisor_Main"
            msg_id = None
        
        error_report = {
            "message_id": str(uuid.uuid4()),
            "sender": AGENT_ID,
            "recipient": sender,
            "type": "completion_report",
            "related_message_id": msg_id,
            "status": "FAILURE",
            "results": {
                "error": str(e),
                "details": traceback.format_exc()
            },
            "timestamp": get_utc_timestamp()
        }
        return jsonify(error_report), 500


@app.route("/query", methods=["POST"])
def query():
    """
    Natural-language friendly wrapper around the allocation engine.
    
    Expected request body:
    {
        "query": "Prioritize high-severity zones and distribute volunteers fairly.",
        "zones": [...],  # optional but required for now
        "available_volunteers": 12,  # optional but required for now
        "constraints": {...}  # optional
    }
    
    Returns:
        HTTP 200 with allocation results on success
        HTTP 400 with error message on validation failure
    """
    try:
        # Parse request body
        body = request.get_json(force=True)
        if not body:
            raise ValueError("Request body must be valid JSON")
        
        # Validate query is present
        query_text = body.get("query")
        if not query_text or not isinstance(query_text, str):
            raise ValueError("'query' is required and must be a non-empty string")
        
        # Extract zones and available_volunteers
        zones = body.get("zones", [])
        available_volunteers = body.get("available_volunteers")
        constraints = body.get("constraints", {})
        
        # For now, require zones and available_volunteers to be provided explicitly
        if not zones or not isinstance(zones, list):
            return jsonify({
                "error": "zones and available_volunteers must be provided for now.",
                "hint": "Pass pre-structured zones and available_volunteers along with the query."
            }), 400
        
        if available_volunteers is None or not isinstance(available_volunteers, (int, float)) or available_volunteers < 0:
            return jsonify({
                "error": "zones and available_volunteers must be provided for now.",
                "hint": "Pass pre-structured zones and available_volunteers along with the query."
            }), 400
        
        # Add natural language query to constraints so it flows through metadata
        if not isinstance(constraints, dict):
            constraints = {}
        constraints["natural_language_query"] = query_text
        
        # Call optimization engine (same as /invoke)
        allocation_plan, metadata = run_allocation(
            zones=zones,
            available_volunteers=int(available_volunteers),
            fairness_weight=constraints.get("fairness_weight", 0.6),
            extra_constraints=constraints if constraints else None
        )
        
        # Ensure metadata contains the natural_language_query
        metadata["natural_language_query"] = query_text
        
        # Build simplified response
        response = {
            "allocation_plan": allocation_plan,
            "summary": metadata
        }
        
        return jsonify(response), 200
        
    except ValueError as e:
        # Validation errors - return 400
        return jsonify({
            "error": str(e),
            "hint": "Ensure 'query' is provided and is a non-empty string."
        }), 400
        
    except Exception as e:
        # Unexpected errors - return 500
        import traceback
        return jsonify({
            "error": str(e),
            "details": traceback.format_exc()
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)

