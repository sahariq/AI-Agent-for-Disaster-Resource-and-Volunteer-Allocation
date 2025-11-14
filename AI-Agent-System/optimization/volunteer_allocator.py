"""
Volunteer Allocation Optimizer

Mathematical optimization model for allocating volunteers across disaster zones.
Uses linear/integer programming to maximize impact while respecting constraints.
"""

from pulp import LpProblem, LpMaximize, LpVariable, LpInteger, lpSum, value, PULP_CBC_CMD
from typing import List, Dict
import time
from datetime import datetime


class VolunteerAllocator:
    """
    Optimizes volunteer allocation across disaster zones using integer programming.
    
    Features:
    - Severity-based prioritization
    - Capacity constraints (Phase 3)
    - Resource coupling (Phase 4)
    - Multi-objective fairness (Phase 5)
    - Integer decision variables (Phase 6)
    """
    
    def __init__(self, fairness_weight: float = 0.0):
        """
        Initialize the allocator.
        
        Args:
            fairness_weight: Lambda parameter for fairness penalty (0 = pure severity).
                           Will be used in Phase 5.
        """
        self.fairness_weight = fairness_weight
        self.model_version = "0.1.0"
    
    def allocate(
        self,
        zones: List[Dict],
        total_volunteers: int
    ) -> Dict:
        """
        Solve optimal volunteer allocation problem.
        
        Args:
            zones: List of zone dictionaries with keys:
                - id: Zone identifier (str)
                - severity: Priority level 1-10 (int)
                - required_volunteers: Desired volunteers (int)
                - capacity: Max volunteers zone can hold (int) [Phase 3]
                - resources_available: Total resource units (int) [Phase 4]
                - min_resources_per_volunteer: Resource ratio (float) [Phase 4]
            total_volunteers: Total volunteers available to allocate (int)
            
        Returns:
            Dictionary with:
                - allocation_plan: List of allocation results per zone
                - remaining_volunteers: Unallocated volunteers
                - objective_value: Optimal objective function value
                - solve_time_seconds: Time to solve (seconds)
                - model_type: "Integer Program" or "Linear Program"
                - timestamp: ISO format timestamp
        """
        
        # Start timing
        start_time = time.time()
        
        # Create the optimization problem
        prob = LpProblem("Disaster_Volunteer_Allocation", LpMaximize)
        
        # Decision variables: x[zone_id] = number of volunteers allocated
        # Phase 2: Start with continuous variables for simplicity
        # Phase 6: Will switch to LpInteger
        x = {
            zone['id']: LpVariable(
                f"x_{zone['id']}", 
                lowBound=0,
                upBound=zone.get('required_volunteers', total_volunteers),  # Basic upper bound
                cat=LpInteger  # Using integer from the start for realism
            )
            for zone in zones
        }
        
        # Objective function: Maximize severity-weighted impact
        # Phase 2: Simple severity-based objective
        # Phase 5: Will add fairness penalty
        objective = lpSum([zone['severity'] * x[zone['id']] for zone in zones])
        prob += objective, "Maximize_Severity_Weighted_Impact"
        
        # Constraint 1: Total volunteer budget
        prob += (
            lpSum([x[zone['id']] for zone in zones]) <= total_volunteers
        ), "Total_Volunteer_Budget"
        
        # Constraint 2: Per-zone capacity limits (Phase 3)
        for zone in zones:
            zone_id = zone['id']
            if 'capacity' in zone:
                prob += (
                    x[zone_id] <= zone['capacity']
                ), f"Capacity_Limit_{zone_id}"
        
        # Phase 4: Resource coupling constraints (to be added)
        # Phase 5: Fairness constraints (to be added)
        
        # Solve the problem
        prob.solve(PULP_CBC_CMD(msg=0))  # msg=0 suppresses solver output
        
        # Calculate solve time
        solve_time = time.time() - start_time
        
        # Extract results
        allocation_plan = []
        for zone in zones:
            allocated = int(value(x[zone['id']]))
            
            # Calculate satisfaction percentage
            satisfaction = 0
            if zone.get('required_volunteers', 0) > 0:
                satisfaction = (allocated / zone['required_volunteers']) * 100
            
            # Calculate capacity usage percentage
            capacity_used = 0
            if 'capacity' in zone and zone['capacity'] > 0:
                capacity_used = (allocated / zone['capacity']) * 100
            
            allocation_plan.append({
                "zone_id": zone['id'],
                "severity": zone['severity'],
                "required": zone.get('required_volunteers', 0),
                "capacity": zone.get('capacity', None),
                "allocated": allocated,
                "satisfaction_pct": round(satisfaction, 1),
                "capacity_used_pct": round(capacity_used, 1) if 'capacity' in zone else None
            })
        
        # Calculate totals
        total_allocated = sum(entry['allocated'] for entry in allocation_plan)
        
        # Build result dictionary
        result = {
            "allocation_plan": allocation_plan,
            "remaining_volunteers": total_volunteers - total_allocated,
            "objective_value": round(value(prob.objective), 2),
            "solve_time_seconds": round(solve_time, 4),
            "model_type": "Integer Program",
            "timestamp": datetime.utcnow().isoformat(),
            "fairness_weight": self.fairness_weight,
            "solver_status": prob.status
        }
        
        return result
    
    def get_model_info(self) -> Dict:
        """
        Get information about the optimization model.
        
        Returns:
            Dictionary with model metadata
        """
        return {
            "version": self.model_version,
            "fairness_weight": self.fairness_weight,
            "features": {
                "severity_optimization": True,
                "capacity_constraints": True,       # Phase 3 - ENABLED
                "resource_coupling": False,         # Phase 4
                "fairness_penalty": False,          # Phase 5
                "integer_variables": True           # Phase 6
            }
        }
