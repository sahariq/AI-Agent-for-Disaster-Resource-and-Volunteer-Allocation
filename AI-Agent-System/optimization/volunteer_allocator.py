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
            fairness_weight: Fairness parameter (0 = pure severity, 1 = guaranteed minimum).
                           When > 0, ensures each zone gets minimum baseline allocation
                           proportional to severity before optimizing remainder.
                           Recommended: 0.0 (pure optimization) or 0.2-0.3 (fair minimum).
        """
        self.fairness_weight = fairness_weight
        self.model_version = "0.2.0"  # Updated for simplified fairness
    
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
        x = {
            zone['id']: LpVariable(
                f"x_{zone['id']}", 
                lowBound=0,
                upBound=zone.get('required_volunteers', total_volunteers),
                cat=LpInteger
            )
            for zone in zones
        }
        
        # Objective function: Maximize severity-weighted impact
        severity_impact = lpSum([zone['severity'] * x[zone['id']] for zone in zones])
        prob += severity_impact, "Maximize_Severity_Impact"
        
        # Constraint 1: Total volunteer budget
        prob += (
            lpSum([x[zone['id']] for zone in zones]) <= total_volunteers
        ), "Total_Volunteer_Budget"
        
        # Constraint 1b: Fairness - Minimum allocation guarantee (Phase 5)
        # Each zone gets a minimum baseline proportional to its severity
        if self.fairness_weight > 0 and len(zones) > 0:
            total_severity = sum(zone['severity'] for zone in zones)
            if total_severity > 0:
                # Reserve a portion of volunteers for minimum allocations
                reserved_for_min = total_volunteers * self.fairness_weight
                
                for zone in zones:
                    # Minimum allocation: proportional share of reserved volunteers
                    # Using float to preserve precision, solver will round to int
                    min_allocation = (zone['severity'] / total_severity) * reserved_for_min
                    
                    # Ensure each zone gets at least this minimum (rounded up)
                    # This ensures no zone gets completely ignored
                    prob += (
                        x[zone['id']] >= min_allocation
                    ), f"Fairness_Minimum_{zone['id']}"
        
        # Constraint 2: Per-zone capacity limits (Phase 3)
        for zone in zones:
            zone_id = zone['id']
            if 'capacity' in zone:
                prob += (
                    x[zone_id] <= zone['capacity']
                ), f"Capacity_Limit_{zone_id}"
        
        # Constraint 3: Resource coupling (Phase 4)
        # Volunteers need minimum resources to be effective
        for zone in zones:
            zone_id = zone['id']
            if 'resources_available' in zone and 'min_resources_per_volunteer' in zone:
                prob += (
                    x[zone_id] * zone['min_resources_per_volunteer'] 
                    <= zone['resources_available']
                ), f"Resource_Coupling_{zone_id}"
        
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
            
            # Calculate resource usage
            resources_used = 0
            resources_used_pct = 0
            if 'min_resources_per_volunteer' in zone:
                resources_used = allocated * zone['min_resources_per_volunteer']
                if 'resources_available' in zone and zone['resources_available'] > 0:
                    resources_used_pct = (resources_used / zone['resources_available']) * 100
            
            allocation_plan.append({
                "zone_id": zone['id'],
                "severity": zone['severity'],
                "required": zone.get('required_volunteers', 0),
                "capacity": zone.get('capacity', None),
                "allocated": allocated,
                "satisfaction_pct": round(satisfaction, 1),
                "capacity_used_pct": round(capacity_used, 1) if 'capacity' in zone else None,
                "resources_used": round(resources_used, 1) if 'min_resources_per_volunteer' in zone else None,
                "resources_used_pct": round(resources_used_pct, 1) if 'resources_available' in zone else None
            })
        
        # Calculate totals
        total_allocated = sum(entry['allocated'] for entry in allocation_plan)
        
        # Calculate fairness metrics
        allocations = [entry['allocated'] for entry in allocation_plan]
        if len(allocations) > 0:
            mean_allocation = sum(allocations) / len(allocations)
            variance = sum((a - mean_allocation) ** 2 for a in allocations) / len(allocations)
            std_deviation = variance ** 0.5
        else:
            mean_allocation = 0
            variance = 0
            std_deviation = 0
        
        # Build result dictionary
        result = {
            "allocation_plan": allocation_plan,
            "remaining_volunteers": total_volunteers - total_allocated,
            "objective_value": round(value(prob.objective), 2),
            "solve_time_seconds": round(solve_time, 4),
            "model_type": "Integer Program",
            "timestamp": datetime.utcnow().isoformat(),
            "fairness_weight": self.fairness_weight,
            "fairness_metrics": {
                "mean_allocation": round(mean_allocation, 2),
                "variance": round(variance, 2),
                "std_deviation": round(std_deviation, 2),
                "coefficient_of_variation": round(std_deviation / mean_allocation * 100, 2) if mean_allocation > 0 else 0
            },
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
                "resource_coupling": True,          # Phase 4 - ENABLED
                "fairness_penalty": self.fairness_weight > 0,  # Phase 5 - ENABLED if λ > 0
                "integer_variables": True           # Phase 6
            }
        }
