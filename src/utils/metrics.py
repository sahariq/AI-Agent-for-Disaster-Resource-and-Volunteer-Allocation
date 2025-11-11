def calculate_metrics(allocation_results, actual_needs):
    unmet_needs = {}
    total_unmet = 0

    for zone, needs in actual_needs.items():
        allocated = allocation_results.get(zone, 0)
        unmet = max(needs - allocated, 0)
        unmet_needs[zone] = unmet
        total_unmet += unmet

    return {
        "unmet_needs": unmet_needs,
        "total_unmet": total_unmet,
        "allocation_results": allocation_results
    }

def display_metrics(metrics):
    print("Metrics Summary:")
    print(f"Total Unmet Needs: {metrics['total_unmet']}")
    for zone, unmet in metrics['unmet_needs'].items():
        print(f"Zone: {zone}, Unmet Needs: {unmet}")
    print("Allocation Results:")
    for zone, allocated in metrics['allocation_results'].items():
        print(f"Zone: {zone}, Allocated: {allocated}")