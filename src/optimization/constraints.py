def total_volunteers_constraint(allocated_volunteers, available_volunteers):
    return sum(allocated_volunteers) <= available_volunteers

def severity_constraint(allocated_resources, severity_levels):
    return all(allocated_resources[i] >= severity_levels[i] for i in range(len(severity_levels)))

def resource_capacity_constraint(allocated_resources, resource_capacities):
    return all(allocated_resources[i] <= resource_capacities[i] for i in range(len(resource_capacities)))