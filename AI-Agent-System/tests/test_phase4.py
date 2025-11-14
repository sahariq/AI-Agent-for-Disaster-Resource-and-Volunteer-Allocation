"""
Phase 4 Test: Resource Coupling
Tests that volunteers are only allocated when sufficient resources are available.
"""

import sys
sys.path.insert(0, '..')

from optimization.volunteer_allocator import VolunteerAllocator
import json


def test_resource_coupling():
    """Test that resource constraints are enforced."""
    
    print("=" * 60)
    print("PHASE 4 TEST: Resource Coupling")
    print("=" * 60)
    
    # Create allocator
    allocator = VolunteerAllocator(fairness_weight=0.0)
    
    # Test scenario: Limited resources constrain volunteer allocation
    zones = [
        {
            "id": "Z1",
            "severity": 10,
            "required_volunteers": 15,
            "capacity": 15,
            "resources_available": 30,           # 30 units available
            "min_resources_per_volunteer": 3    # Need 3 units per volunteer
            # Max effective volunteers: 30/3 = 10 (resource-limited!)
        },
        {
            "id": "Z2",
            "severity": 8,
            "required_volunteers": 12,
            "capacity": 12,
            "resources_available": 50,           # 50 units available
            "min_resources_per_volunteer": 5    # Need 5 units per volunteer
            # Max effective volunteers: 50/5 = 10 (resource-limited!)
        },
        {
            "id": "Z3",
            "severity": 6,
            "required_volunteers": 10,
            "capacity": 10,
            "resources_available": 40,           # 40 units available
            "min_resources_per_volunteer": 2    # Need 2 units per volunteer
            # Max effective volunteers: 40/2 = 20 (not resource-limited)
        }
    ]
    
    total_volunteers = 30  # Plenty of volunteers available
    
    print("\n📋 Input Data:")
    print(f"   Total Volunteers Available: {total_volunteers}")
    print("\n   Zone Details:")
    for zone in zones:
        max_with_resources = int(zone['resources_available'] / zone['min_resources_per_volunteer'])
        bottleneck = min(zone['required_volunteers'], zone['capacity'], max_with_resources)
        
        print(f"\n   {zone['id']}: Severity={zone['severity']}")
        print(f"      Required: {zone['required_volunteers']} volunteers")
        print(f"      Capacity: {zone['capacity']} volunteers")
        print(f"      Resources: {zone['resources_available']} units")
        print(f"      Need per volunteer: {zone['min_resources_per_volunteer']} units")
        print(f"      → Max with resources: {max_with_resources} volunteers")
        print(f"      → Effective limit: {bottleneck} volunteers")
        
        if max_with_resources < zone['required_volunteers']:
            print(f"      ⚠️  RESOURCE-LIMITED! (Can't equip all {zone['required_volunteers']} needed)")
    
    # Run optimization
    print("\n🔧 Running optimization with resource coupling...")
    result = allocator.allocate(zones, total_volunteers)
    
    # Display results
    print("\n✅ Optimization Complete!")
    print(f"   Solve Time: {result['solve_time_seconds']}s")
    print(f"   Objective Value: {result['objective_value']}")
    
    print("\n📊 Allocation Results:")
    for entry in result['allocation_plan']:
        print(f"\n   {entry['zone_id']}: {entry['allocated']} volunteers")
        print(f"      Severity: {entry['severity']}")
        print(f"      Required: {entry['required']}, Capacity: {entry['capacity']}")
        if entry['resources_used'] is not None:
            print(f"      Resources Used: {entry['resources_used']} units ({entry['resources_used_pct']}%)")
    
    print(f"\n   Remaining Volunteers: {result['remaining_volunteers']}")
    
    # Verification Tests
    print("\n🧪 Verification Tests:")
    
    test_passed = True
    
    # Test 1: Resource constraints respected
    print("\n   Test 1: Resource Coupling Constraints")
    for i, entry in enumerate(result['allocation_plan']):
        zone = zones[i]
        zone_id = entry['zone_id']
        allocated = entry['allocated']
        
        if 'resources_available' in zone and 'min_resources_per_volunteer' in zone:
            resources_needed = allocated * zone['min_resources_per_volunteer']
            resources_available = zone['resources_available']
            
            if resources_needed <= resources_available:
                print(f"      ✅ {zone_id}: {allocated} × {zone['min_resources_per_volunteer']} = " +
                      f"{resources_needed} <= {resources_available} (OK)")
            else:
                print(f"      ❌ {zone_id}: {resources_needed} > {resources_available} (VIOLATED!)")
                test_passed = False
    
    # Test 2: Z1 should be limited by resources (10, not 15)
    print("\n   Test 2: Z1 Resource Limitation")
    z1_allocated = result['allocation_plan'][0]['allocated']
    z1_max_with_resources = int(zones[0]['resources_available'] / zones[0]['min_resources_per_volunteer'])
    
    if z1_allocated <= z1_max_with_resources:
        print(f"      ✅ Z1 allocated {z1_allocated} <= {z1_max_with_resources} (resource limit respected)")
        if z1_allocated == z1_max_with_resources:
            print(f"      ✨ Z1 optimally used all available resources!")
    else:
        print(f"      ❌ Z1 allocated {z1_allocated} > {z1_max_with_resources} (resource limit violated!)")
        test_passed = False
    
    # Test 3: Z2 should be limited by resources (10, not 12)
    print("\n   Test 3: Z2 Resource Limitation")
    z2_allocated = result['allocation_plan'][1]['allocated']
    z2_max_with_resources = int(zones[1]['resources_available'] / zones[1]['min_resources_per_volunteer'])
    
    if z2_allocated <= z2_max_with_resources:
        print(f"      ✅ Z2 allocated {z2_allocated} <= {z2_max_with_resources} (resource limit respected)")
        if z2_allocated == z2_max_with_resources:
            print(f"      ✨ Z2 optimally used all available resources!")
    else:
        print(f"      ❌ Z2 allocated {z2_allocated} > {z2_max_with_resources} (resource limit violated!)")
        test_passed = False
    
    # Test 4: Z3 should NOT be resource-limited
    print("\n   Test 4: Z3 Resource Availability")
    z3_allocated = result['allocation_plan'][2]['allocated']
    z3_max_with_resources = int(zones[2]['resources_available'] / zones[2]['min_resources_per_volunteer'])
    
    print(f"      ℹ️  Z3 has enough resources for {z3_max_with_resources} volunteers")
    print(f"      ℹ️  Z3 allocated {z3_allocated} volunteers")
    if z3_allocated < z3_max_with_resources:
        print(f"      ✅ Z3 limited by other factors (severity priority), not resources")
    
    # Test 5: Total budget respected
    print("\n   Test 5: Budget Constraint")
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
        print("PHASE 4 TEST PASSED ✅")
    else:
        print("PHASE 4 TEST FAILED ❌")
    print("=" * 60)
    
    return result


if __name__ == "__main__":
    test_resource_coupling()
