"""
Example: How to use the DisasterAllocationWorker with an external supervisor.

This demonstrates how to integrate the worker agent into a supervisor system.
The worker listens for task assignments and sends completion reports back.
"""

from agents.workers.disaster_worker import DisasterAllocationWorker
from communication.models import Message, Task
from communication import protocol
import json


def example_worker_integration():
    """
    Example showing how an external supervisor would interact with this worker.
    """
    # Initialize the worker (supervisor_id should match the external supervisor's ID)
    worker = DisasterAllocationWorker(
        agent_id="Worker_Disaster",
        supervisor_id="Supervisor_Main",  # This will be provided by external supervisor
        fairness_weight=0.6
    )
    
    # Example: External supervisor sends a task assignment message
    # This is what the external supervisor would send to your worker
    task = Task(
        name="allocate_resources",
        priority=1,
        parameters={
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
                },
            ],
            "available_volunteers": 12
        }
    )
    
    # Create message from supervisor (this would come from external supervisor)
    message = Message.new(
        sender="Supervisor_Main",
        recipient="Worker_Disaster",
        msg_type=protocol.TASK_ASSIGNMENT,
        task=task
    )
    
    # Worker processes the message and automatically sends completion report
    print("=" * 60)
    print("Example: Worker receiving task from external supervisor")
    print("=" * 60)
    worker.handle_incoming_message(message.model_dump_json())
    print("=" * 60)
    print("Worker has processed task and sent completion report back to supervisor")
    print("=" * 60)


if __name__ == "__main__":
    example_worker_integration()

