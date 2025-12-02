# main.py
import json
import os
from agents.supervisor.supervisor import SupervisorAgent

if __name__ == "__main__":
    supervisor = SupervisorAgent()

<<<<<<< HEAD
    # Load dataset with absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(script_dir, "datasets", "disaster_scenarios.json")
    
    with open(dataset_path, "r") as f:
        data = json.load(f)

    # Process first scenario
    scenario = data["scenarios"][0]
    zones = scenario["zones"]
    available_volunteers = scenario["available_volunteers"]
=======
    # Updated zones with optimization-required fields
    zones = [
        {
            "id": "Z1", 
            "severity": 5, 
            "required_volunteers": 8,
            "capacity": 8,  # Maximum volunteers this zone can handle
            "resources_available": 50,  # Equipment/supplies available
            "min_resources_per_volunteer": 4  # Resources needed per volunteer
        },
        {
            "id": "Z2", 
            "severity": 3, 
            "required_volunteers": 6,
            "capacity": 6,
            "resources_available": 30,
            "min_resources_per_volunteer": 3
        },
        {
            "id": "Z3", 
            "severity": 4, 
            "required_volunteers": 5,
            "capacity": 5,
            "resources_available": 40,
            "min_resources_per_volunteer": 5
        },
    ]

    available_volunteers = 15
>>>>>>> eb60f8bbc87e5d24faaa317e25dcc14086fd335d

    print("=== System Startup ===")
    print(f"Scenario: {scenario['name']}")
    print(supervisor.health_check())
    supervisor.assign_task(zones, available_volunteers)
    print("=== End of Execution ===")
