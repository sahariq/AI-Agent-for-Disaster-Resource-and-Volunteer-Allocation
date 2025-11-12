from abc import ABC, abstractmethod
import json
import uuid
from typing import Any, Optional

class AbstractWorkerAgent(ABC):
    """
    Abstract Base Class for all worker agents, including LTM functionality.
    """

    def __init__(self, agent_id: str, supervisor_id: str):
        self._id = agent_id
        self._supervisor_id = supervisor_id
        self._current_task_id = None 

    # --- Abstract Methods (Must be Implemented by Subclasses) ---

    @abstractmethod
    def process_task(self, task_data: dict) -> dict:
        """
        The worker's unique business logic. Must return a dictionary of results.
        """
        pass

    @abstractmethod
    def send_message(self, recipient: str, message_obj: dict):
        """
        Sends the final JSON message object through the communication layer.
        """
        pass
    
    @abstractmethod
    def write_to_ltm(self, key: str, value: Any) -> bool:
        """
        Writes a key-value pair to the agent's Long-Term Memory (LTM).
        Returns True on success, False otherwise.
        """
        pass

    @abstractmethod
    def read_from_ltm(self, key: str) -> Optional[Any]:
        """
        Reads a value from the agent's LTM based on the key.
        Returns the stored value or None if the key is not found.
        """
        pass

    # --- Concrete Methods (Shared Communication Protocol) ---

    def handle_incoming_message(self, json_message: str):
        """Receives and processes an incoming JSON message from the supervisor."""
        try:
            message = json.loads(json_message)
            msg_type = message.get("type")
            
            if msg_type == "task_assignment":
                task_params = message.get("task", {}).get("parameters", {})
                self._current_task_id = message.get("message_id")
                print(f"[{self._id}] received task: {message['task']['name']}")
                self._execute_task(task_params, self._current_task_id)
            
        except json.JSONDecodeError as e:
            print(f"[{self._id}] ERROR decoding message: {e}")

    def _execute_task(self, task_data: dict, related_msg_id: str):
        """Executes the concrete process_task logic and handles result reporting."""
        status = "FAILURE"
        results = {}
        
        try:
            results = self.process_task(task_data)
            status = "SUCCESS"
        except Exception as e:
            results = {"error": str(e), "details": "Task processing failed."}
            print(f"[{self._id}] Task FAILED: {e}")
            
        self._report_completion(related_msg_id, status, results)

    def _report_completion(self, related_msg_id: str, status: str, results: dict):
        """Constructs and sends a task completion report."""
        report = {
            "message_id": str(uuid.uuid4()),
            "sender": self._id,
            "recipient": self._supervisor_id,
            "type": "completion_report",
            "related_message_id": related_msg_id,
            "status": status,
            "results": results,
            "timestamp": "..." 
        }
        self.send_message(self._supervisor_id, report)
        self._current_task_id = None