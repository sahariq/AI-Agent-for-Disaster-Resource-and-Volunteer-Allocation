"""
Phase 2 Test: Basic Optimization Model
Tests the volunteer allocator with a simple 2-zone scenario.
"""

import sys
sys.path.insert(0, '..')

from optimization.volunteer_allocator import VolunteerAllocator
import json


def test_basic_allocation():
    """Test basic severity-based allocation."""
    
    print("=" * 60)
    print("PHASE 2 TEST: Basic Optimization Model")
    print("=" * 60)
    
    # Create allocator
    allocator = VolunteerAllocator(fairness_weight=0.0)
    
    # Simple test scenario: 2 zones
    zones = [
        {
            "id": "Z1",
            "severity": 8,
            "required_volunteers": 10
        },
        {
            "id": "Z2",
            "severity": 5,
            "required_volunteers": 8
        }
    ]
    
    total_volunteers = 12
    
    print("\n📋 Input Data:")
    print(f"   Total Volunteers Available: {total_volunteers}")
    print(f"\n   Zone Z1: Severity={zones[0]['severity']}, Required={zones[0]['required_volunteers']}")
    print(f"   Zone Z2: Severity={zones[1]['severity']}, Required={zones[1]['required_volunteers']}")
    
    # Run optimization
    print("\n🔧 Running optimization...")
    result = allocator.allocate(zones, total_volunteers)
    
    # Display results
    print("\n✅ Optimization Complete!")
    print(f"   Solve Time: {result['solve_time_seconds']}s")
    print(f"   Objective Value: {result['objective_value']}")
    print(f"   Model Type: {result['model_type']}")
    
    print("\n📊 Allocation Results:")
    for entry in result['allocation_plan']:
        print(f"   {entry['zone_id']}: {entry['allocated']} volunteers " +
              f"(Severity: {entry['severity']}, " +
              f"Satisfaction: {entry['satisfaction_pct']}%)")
    
    print(f"\n   Remaining Volunteers: {result['remaining_volunteers']}")
    
    # Verify expectations
    print("\n🧪 Verification:")
    
    # Expected: Higher severity zone should get priority
    z1_allocated = result['allocation_plan'][0]['allocated']
    z2_allocated = result['allocation_plan'][1]['allocated']
    
    if z1_allocated >= z2_allocated:
        print("   ✅ Higher severity zone (Z1) prioritized correctly")
    else:
        print("   ❌ Priority issue: Lower severity got more volunteers")
    
    # Total should not exceed available
    total_allocated = sum(e['allocated'] for e in result['allocation_plan'])
    if total_allocated <= total_volunteers:
        print(f"   ✅ Budget constraint satisfied ({total_allocated} <= {total_volunteers})")
    else:
        print(f"   ❌ Budget exceeded ({total_allocated} > {total_volunteers})")
    
    # Should allocate all available volunteers (greedy for severity)
    if total_allocated == total_volunteers:
        print(f"   ✅ All volunteers allocated (optimal resource usage)")
    else:
        print(f"   ⚠️  {result['remaining_volunteers']} volunteers unused")
    
    # Model info
    print("\n📝 Model Information:")
    model_info = allocator.get_model_info()
    print(f"   Version: {model_info['version']}")
    print(f"   Fairness Weight: {model_info['fairness_weight']}")
    print(f"   Features Enabled:")
    for feature, enabled in model_info['features'].items():
        status = "✅" if enabled else "⏸️ (Coming in later phases)"
        print(f"      - {feature}: {status}")
    
    print("\n" + "=" * 60)
    print("PHASE 2 TEST COMPLETE")
    print("=" * 60)
    
    return result


if __name__ == "__main__":
    test_basic_allocation()
