"""
Phase 3 Test: Capacity Constraints
Tests that allocations respect zone capacity limits.
"""

import sys
sys.path.insert(0, '..')

from optimization.volunteer_allocator import VolunteerAllocator
import json


def test_capacity_constraints():
    """Test that capacity constraints are enforced."""
    
    print("=" * 60)
    print("PHASE 3 TEST: Capacity Constraints")
    print("=" * 60)
    
    # Create allocator
    allocator = VolunteerAllocator(fairness_weight=0.0)
    
    # Test scenario: Zone needs MORE than it can hold
    zones = [
        {
            "id": "Z1",
            "severity": 10,
            "required_volunteers": 20,  # Needs 20
            "capacity": 12              # Can only fit 12 ← KEY TEST
        },
        {
            "id": "Z2",
            "severity": 7,
            "required_volunteers": 15,  # Needs 15
            "capacity": 10              # Can only fit 10 ← KEY TEST
        },
        {
            "id": "Z3",
            "severity": 5,
            "required_volunteers": 8,
            "capacity": 8               # Exact match
        }
    ]
    
    total_volunteers = 25  # Enough to test constraints
    
    print("\n📋 Input Data:")
    print(f"   Total Volunteers Available: {total_volunteers}")
    print("\n   Zone Details:")
    for zone in zones:
        print(f"   {zone['id']}: Severity={zone['severity']}, " +
              f"Required={zone['required_volunteers']}, " +
              f"Capacity={zone['capacity']}")
        if zone['required_volunteers'] > zone['capacity']:
            print(f"      ⚠️  Needs {zone['required_volunteers']} but can only fit {zone['capacity']}")
    
    # Run optimization
    print("\n🔧 Running optimization with capacity constraints...")
    result = allocator.allocate(zones, total_volunteers)
    
    # Display results
    print("\n✅ Optimization Complete!")
    print(f"   Solve Time: {result['solve_time_seconds']}s")
    print(f"   Objective Value: {result['objective_value']}")
    
    print("\n📊 Allocation Results:")
    for entry in result['allocation_plan']:
        capacity_info = f", Capacity Used: {entry['capacity_used_pct']}%" if entry['capacity'] else ""
        print(f"   {entry['zone_id']}: {entry['allocated']} volunteers " +
              f"(Severity: {entry['severity']}, " +
              f"Required: {entry['required']}, " +
              f"Capacity: {entry['capacity']}{capacity_info})")
    
    print(f"\n   Remaining Volunteers: {result['remaining_volunteers']}")
    
    # Verification Tests
    print("\n🧪 Verification Tests:")
    
    test_passed = True
    
    # Test 1: No allocation exceeds capacity
    print("\n   Test 1: Capacity Limits Respected")
    for entry in result['allocation_plan']:
        zone_id = entry['zone_id']
        allocated = entry['allocated']
        capacity = entry['capacity']
        
        if capacity is not None:
            if allocated <= capacity:
                print(f"      ✅ {zone_id}: {allocated} <= {capacity} (OK)")
            else:
                print(f"      ❌ {zone_id}: {allocated} > {capacity} (VIOLATED!)")
                test_passed = False
        else:
            print(f"      ⚠️  {zone_id}: No capacity limit set")
    
    # Test 2: High severity zones prioritized
    print("\n   Test 2: Severity Prioritization")
    z1_allocated = result['allocation_plan'][0]['allocated']
    z2_allocated = result['allocation_plan'][1]['allocated']
    z3_allocated = result['allocation_plan'][2]['allocated']
    
    if z1_allocated >= z2_allocated >= z3_allocated:
        print(f"      ✅ Priority order maintained (Z1:{z1_allocated} >= Z2:{z2_allocated} >= Z3:{z3_allocated})")
    else:
        print(f"      ⚠️  Priority order: Z1:{z1_allocated}, Z2:{z2_allocated}, Z3:{z3_allocated}")
    
    # Test 3: Z1 should be capped at 12 (not 20)
    print("\n   Test 3: Critical Capacity Enforcement")
    if z1_allocated == 12:
        print(f"      ✅ Z1 correctly capped at capacity (12), not requirement (20)")
    elif z1_allocated < 12:
        print(f"      ⚠️  Z1 got {z1_allocated} (less than capacity due to other constraints)")
    else:
        print(f"      ❌ Z1 got {z1_allocated} which exceeds capacity of 12")
        test_passed = False
    
    # Test 4: Total budget respected
    print("\n   Test 4: Budget Constraint")
    total_allocated = sum(e['allocated'] for e in result['allocation_plan'])
    if total_allocated <= total_volunteers:
        print(f"      ✅ Total allocated ({total_allocated}) <= Budget ({total_volunteers})")
    else:
        print(f"      ❌ Budget exceeded: {total_allocated} > {total_volunteers}")
        test_passed = False
    
    # Model info
    print("\n📝 Model Information:")
    model_info = allocator.get_model_info()
    print(f"   Version: {model_info['version']}")
    print(f"   Features Enabled:")
    for feature, enabled in model_info['features'].items():
        status = "✅" if enabled else "⏸️"
        print(f"      - {feature}: {status}")
    
    print("\n" + "=" * 60)
    if test_passed:
        print("PHASE 3 TEST PASSED ✅")
    else:
        print("PHASE 3 TEST FAILED ❌")
    print("=" * 60)
    
    return result


if __name__ == "__main__":
    test_capacity_constraints()
