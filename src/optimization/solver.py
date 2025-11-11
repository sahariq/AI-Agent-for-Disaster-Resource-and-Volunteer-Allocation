from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, value

def allocate_resources(severity_data, available_volunteers):
    # Create the optimization problem
    problem = LpProblem("Disaster_Resource_Allocation", LpMinimize)

    # Create decision variables for each zone
    zones = severity_data['zone'].unique()
    allocation_vars = LpVariable.dicts("Allocate", zones, lowBound=0, cat='Integer')

    # Objective function: Minimize the total unmet severity
    problem += lpSum((severity_data[severity_data['zone'] == zone]['severity'].values[0] - allocation_vars[zone]) 
                     for zone in zones), "Total_Unmet_Severity"

    # Constraints: Total allocated volunteers should not exceed available volunteers
    problem += lpSum(allocation_vars[zone] for zone in zones) <= available_volunteers, "Total_Volunteers_Constraint"

    # Solve the problem
    problem.solve()

    # Return the results
    allocation_results = {zone: allocation_vars[zone].varValue for zone in zones}
    return allocation_results, LpStatus[problem.status], value(problem.objective)