"""
Example: Using the centralized run_allocation() function directly.

This demonstrates how to use the optimization engine without the worker agent,
which is useful for HTTP API servers or standalone scripts.
"""

import sys
import os
# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from optimization import run_allocation


def example_direct_usage():
    """Example of using run_allocation() directly."""
    
    # Define disaster zones
    zones = [
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
    
    # Call the centralized function
    allocation_plan, metadata = run_allocation(
        zones=zones,
        available_volunteers=available_volunteers,
        fairness_weight=0.6,
        extra_constraints=None  # Reserved for future use
    )
    
    # Display results
    print("=" * 60)
    print("Allocation Plan")
    print("=" * 60)
    for zone in allocation_plan:
        print(f"Zone {zone['zone_id']}:")
        print(f"  Severity: {zone['severity']}")
        print(f"  Required: {zone['required']}")
        print(f"  Allocated: {zone['allocated']}")
        print(f"  Satisfaction: {zone['satisfaction_pct']}%")
        if zone['capacity']:
            print(f"  Capacity Used: {zone['capacity_used_pct']}%")
        print()
    
    print("=" * 60)
    print("Optimization Metadata")
    print("=" * 60)
    print(f"Objective Value: {metadata['objective_value']}")
    print(f"Solve Time: {metadata['solve_time_seconds']} seconds")
    print(f"Remaining Volunteers: {metadata['remaining_volunteers']}")
    print(f"Fairness Weight: {metadata['fairness_weight']}")
    print(f"\nFairness Metrics:")
    for key, value in metadata['fairness_metrics'].items():
        print(f"  {key}: {value}")
    print("=" * 60)
    
    return allocation_plan, metadata


if __name__ == "__main__":
    example_direct_usage()

