# main.py
from agents.supervisor.supervisor import SupervisorAgent

if __name__ == "__main__":
    supervisor = SupervisorAgent()

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

    print("=== System Startup ===")
    print(supervisor.health_check())
    supervisor.assign_task(zones, available_volunteers)
    print("=== End of Execution ===")
