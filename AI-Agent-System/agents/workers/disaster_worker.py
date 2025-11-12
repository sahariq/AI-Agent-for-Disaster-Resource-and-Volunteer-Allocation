# agents/workers/disaster_worker.py
import json
from pathlib import Path
from datetime import datetime
from typing import Any
from .worker_base import AbstractWorkerAgent


class DisasterAllocationWorker(AbstractWorkerAgent):
    """
    Concrete worker that allocates volunteers/resources to disaster zones.
    Implements LTM and messaging as per Supervisor–Worker protocol.
    """

    def __init__(self, agent_id: str, supervisor_id: str):
        super().__init__(agent_id, supervisor_id)
        self.ltm_dir = Path("LTM") / agent_id
        self.ltm_dir.mkdir(parents=True, exist_ok=True)
        self.ltm_file = self.ltm_dir / "allocations.json"

    # ----------------------------------------------------------------------
    # CORE LOGIC
    # ----------------------------------------------------------------------
    def process_task(self, task_data: dict) -> dict:
        """
        Executes allocation logic.
        Reads from LTM first; if not found, computes new plan and saves it.
        """
        key = json.dumps(task_data, sort_keys=True)
        cached_result = self.read_from_ltm(key)

        if cached_result:
            print(f"[{self._id}] Retrieved cached result from LTM.")
            return {"source": "LTM", **cached_result}

        print(f"[{self._id}] Computing new allocation plan...")
        zones = task_data.get("zones", [])
        available_volunteers = task_data.get("available_volunteers", 0)
        plan = []

        for zone in zones:
            required = zone.get("required_volunteers", 0)
            assigned = min(required, available_volunteers)
            available_volunteers -= assigned
            plan.append({
                "zone_id": zone["id"],
                "assigned_volunteers": assigned,
                "severity": zone.get("severity", "N/A")
            })

        result = {
            "allocation_plan": plan,
            "remaining_volunteers": available_volunteers,
            "timestamp": datetime.utcnow().isoformat()
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
