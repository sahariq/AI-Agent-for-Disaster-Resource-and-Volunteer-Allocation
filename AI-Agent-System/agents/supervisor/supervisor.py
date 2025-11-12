# agents/supervisor/supervisor.py
import json
from datetime import datetime
from agents.workers.disaster_worker import DisasterAllocationWorker
from communication.models import Message, Task
from communication import protocol


class SupervisorAgent:
    """
    Supervisor controls the system: sends tasks to workers,
    receives completion reports, and logs results.
    """

    def __init__(self):
        self.id = "Supervisor_Main"
        self.worker = DisasterAllocationWorker("Worker_Disaster", self.id)
        self.log_file = "supervisor_log.jsonl"

    # ----------------------------------------------------------------------
    # CORE ACTIONS
    # ----------------------------------------------------------------------
    def assign_task(self, zones: list, available_volunteers: int):
        """Build a new message and send to worker."""
        task = Task(
            name="allocate_resources",
            priority=1,
            parameters={"zones": zones, "available_volunteers": available_volunteers},
        )

        msg = Message.new(
            sender=self.id,
            recipient=self.worker._id,
            msg_type=protocol.TASK_ASSIGNMENT,
            task=task,
        )

        print(f"[{self.id}] Sending task to worker...")
        self.worker.handle_incoming_message(msg.json())
        self._log("task_assignment", msg.dict())

    def receive_report(self, message_obj: dict):
        """Handles incoming completion reports from workers."""
        print(f"[{self.id}] Received completion report!")
        print(json.dumps(message_obj, indent=2))
        self._log("completion_report", message_obj)

    def _log(self, msg_type: str, content: dict):
        """Append logs with timestamps to JSONL file."""
        entry = {"time": datetime.utcnow().isoformat(), "type": msg_type, "data": content}
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    # ----------------------------------------------------------------------
    # HEALTH CHECK
    # ----------------------------------------------------------------------
    def health_check(self):
        return {"status": "OK", "timestamp": datetime.utcnow().isoformat()}
