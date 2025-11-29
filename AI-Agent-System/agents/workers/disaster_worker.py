# agents/workers/disaster_worker.py
import json
from pathlib import Path
from datetime import datetime
from typing import Any
from .worker_base import AbstractWorkerAgent

# Import optimization engine
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from optimization.volunteer_allocator import run_allocation


class DisasterAllocationWorker(AbstractWorkerAgent):
    """
    Concrete worker that allocates volunteers/resources to disaster zones.
    Implements LTM and messaging as per Supervisor–Worker protocol.
    """

    def __init__(self, agent_id: str, supervisor_id: str, fairness_weight: float = 0.6):
        super().__init__(agent_id, supervisor_id)
        self.ltm_dir = Path("LTM") / agent_id
        self.ltm_dir.mkdir(parents=True, exist_ok=True)
        self.ltm_file = self.ltm_dir / "allocations.json"
        
        # Store fairness weight for use in allocation
        # fairness_weight=0.6 balances fairness (no zeros) with severity priority
        self.fairness_weight = fairness_weight
        print(f"[{agent_id}] Initialized with optimization engine (fairness_weight={fairness_weight})")

    # ----------------------------------------------------------------------
    # CORE LOGIC
    # ----------------------------------------------------------------------
    def process_task(self, task_data: dict) -> dict:
        """
        Executes allocation logic using optimization engine.
        Reads from LTM first; if not found, computes optimal plan and saves it.
        
        Note: Cache key includes fairness_weight to ensure different fairness
        levels produce different allocations (not retrieved from cache).
        """
        # Include fairness_weight in cache key so different fairness levels recompute
        cache_data = {
            **task_data,
            "fairness_weight": self.fairness_weight
        }
        key = json.dumps(cache_data, sort_keys=True)
        cached_result = self.read_from_ltm(key)

        if cached_result:
            print(f"[{self._id}] Retrieved cached result from LTM.")
            return {"source": "LTM", **cached_result}

        print(f"[{self._id}] Computing optimal allocation plan...")
        zones = task_data.get("zones", [])
        available_volunteers = task_data.get("available_volunteers", 0)
        
        # Use centralized run_allocation function (pure allocation logic, no messages/LTM)
        allocation_plan, metadata = run_allocation(
            zones=zones,
            available_volunteers=available_volunteers,
            fairness_weight=self.fairness_weight,
            extra_constraints=None
        )
        
        # Transform optimizer output to match expected format
        plan = [
            {
                "zone_id": alloc["zone_id"],
                "assigned_volunteers": alloc["allocated"],
                "severity": next((z["severity"] for z in zones if z["id"] == alloc["zone_id"]), "N/A")
            }
            for alloc in allocation_plan
        ]

        result = {
            "allocation_plan": plan,
            "remaining_volunteers": metadata["remaining_volunteers"],
            "timestamp": metadata["timestamp"],
            "optimization_metadata": {
                "objective_value": metadata["objective_value"],
                "solve_time_seconds": metadata["solve_time_seconds"],
                "model_type": metadata["model_type"],
                "fairness_weight": metadata["fairness_weight"],
                "fairness_metrics": metadata["fairness_metrics"]
            }
        }

        self.write_to_ltm(key, result)
        return {"source": "LIVE", **result}

    # ----------------------------------------------------------------------
    # COMMUNICATION HANDLERS
    # ----------------------------------------------------------------------
    def send_message(self, recipient: str, message_obj: dict):
        """
        Sends JSON response to Supervisor (for demo, prints to console).
        Replace with socket or HTTP later if needed.
        """
        print(f"[{self._id}] Sending message to {recipient}:")
        print(json.dumps(message_obj, indent=2))

    # ----------------------------------------------------------------------
    # LONG-TERM MEMORY (LTM)
    # ----------------------------------------------------------------------
    def write_to_ltm(self, key: str, value: Any) -> bool:
        """Store key–value pair in allocations.json (LTM)."""
        try:
            if self.ltm_file.exists():
                data = json.loads(self.ltm_file.read_text())
            else:
                data = {}
            data[key] = value
            self.ltm_file.write_text(json.dumps(data, indent=2))
            return True
        except Exception as e:
            print(f"[{self._id}] ERROR writing to LTM: {e}")
            return False

    def read_from_ltm(self, key: str):
        """Retrieve stored value from allocations.json (LTM)."""
        try:
            if not self.ltm_file.exists():
                return None
            data = json.loads(self.ltm_file.read_text())
            return data.get(key)
        except Exception as e:
            print(f"[{self._id}] ERROR reading from LTM: {e}")
            return None
