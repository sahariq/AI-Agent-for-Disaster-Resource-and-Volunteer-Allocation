# main.py
from agents.supervisor.supervisor import SupervisorAgent

if __name__ == "__main__":
    supervisor = SupervisorAgent()

    zones = [
        {"id": "Z1", "severity": 5, "required_volunteers": 8},
        {"id": "Z2", "severity": 3, "required_volunteers": 6},
        {"id": "Z3", "severity": 4, "required_volunteers": 5},
    ]

    available_volunteers = 15

    print("=== System Startup ===")
    print(supervisor.health_check())
    supervisor.assign_task(zones, available_volunteers)
    print("=== End of Execution ===")
