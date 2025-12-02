# main.py
import json
import os
from agents.supervisor.supervisor import SupervisorAgent

if __name__ == "__main__":
    supervisor = SupervisorAgent()

    # Load dataset with absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(script_dir, "datasets", "disaster_scenarios.json")
    
    with open(dataset_path, "r") as f:
        data = json.load(f)

    # Process first scenario
    scenario = data["scenarios"][0]
    zones = scenario["zones"]
    available_volunteers = scenario["available_volunteers"]

    print("=== System Startup ===")
    print(f"Scenario: {scenario['name']}")
    print(supervisor.health_check())
    supervisor.assign_task(zones, available_volunteers)
    print("=== End of Execution ===")
