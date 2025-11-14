"""
Phase 5 Test: Multi-Objective Optimization (Severity + Fairness)
Tests fairness through minimum allocation guarantees for all zones.
"""

import sys
sys.path.insert(0, '..')

from optimization.volunteer_allocator import VolunteerAllocator
import json


def test_fairness_comparison():
    """Test fairness with minimum allocation guarantees."""
    
    print("=" * 70)
    print("PHASE 5 TEST: Fairness with Minimum Allocation Guarantees")
    print("=" * 70)
    
    # Test scenario: Uneven severity distribution
    zones = [
        {
            "id": "Z1",
            "severity": 10,
            "required_volunteers": 20,
            "capacity": 20,
            "resources_available": 100,
            "min_resources_per_volunteer": 3
        },
        {
            "id": "Z2",
            "severity": 7,
            "required_volunteers": 15,
            "capacity": 15,
            "resources_available": 75,
            "min_resources_per_volunteer": 3
        },
        {
            "id": "Z3",
            "severity": 5,
            "required_volunteers": 12,
            "capacity": 12,
            "resources_available": 60,
            "min_resources_per_volunteer": 3
        },
        {
            "id": "Z4",
            "severity": 3,
            "required_volunteers": 10,
            "capacity": 10,
            "resources_available": 50,
            "min_resources_per_volunteer": 3
        }
    ]
    
    total_volunteers = 40
    
    print("\n📋 Input Data:")
    print(f"   Total Volunteers Available: {total_volunteers}")
    print("\n   Zone Details:")
    for zone in zones:
        print(f"   {zone['id']}: Severity={zone['severity']}, Required={zone['required_volunteers']}")
    
    # Test with different fairness weights
    # fairness_weight = portion of volunteers reserved for minimum guarantees
    fairness_weights = [0.0, 0.2, 0.4, 0.6, 1.0, 1.2]
    results = {}
    
    print("\n" + "=" * 70)
    print("COMPARING DIFFERENT FAIRNESS LEVELS")
    print("(λ = fraction of volunteers reserved for minimum guarantees)")
    print("=" * 70)
    
    for lambda_val in fairness_weights:
        print(f"\n{'─' * 70}")
        print(f"🧪 Testing with Fairness Weight λ = {lambda_val}")
        print(f"{'─' * 70}")
        
        allocator = VolunteerAllocator(fairness_weight=lambda_val)
        result = allocator.allocate(zones, total_volunteers)
        results[lambda_val] = result
        
        print(f"\n   Solve Time: {result['solve_time_seconds']}s")
        print(f"   Objective Value: {result['objective_value']}")
        
        print(f"\n   📊 Allocations:")
        for entry in result['allocation_plan']:
            print(f"      {entry['zone_id']}: {entry['allocated']:2d} volunteers " +
                  f"(Severity: {entry['severity']:2d})")
        
        print(f"\n   📈 Fairness Metrics:")
        metrics = result['fairness_metrics']
        print(f"      Mean Allocation: {metrics['mean_allocation']}")
        print(f"      Variance: {metrics['variance']}")
        print(f"      Std Deviation: {metrics['std_deviation']}")
        print(f"      Coeff. of Variation: {metrics['coefficient_of_variation']}%")
    
    # Comparative Analysis
    print("\n" + "=" * 70)
    print("COMPARATIVE ANALYSIS")
    print("=" * 70)
    
    print("\n📊 Allocation Distribution by Fairness Level:\n")
    print(f"   {'Zone':<6} | λ=0.0 | λ=0.2 | λ=0.4 | λ=0.6 | λ=1.0 | λ=1.2")
    print(f"   {'-' * 6}|{'-' * 7}|{'-' * 7}|{'-' * 7}|{'-' * 7}|{'-' * 7}|{'-' * 7}")
    
    for i, zone in enumerate(zones):
        zone_id = zone['id']
        row = f"   {zone_id:<6} |"  
        for lambda_val in fairness_weights:
            allocated = results[lambda_val]['allocation_plan'][i]['allocated']
            row += f" {allocated:5d} |"
        print(row)
    
    print("\n📈 Fairness Metrics Comparison:\n")
    print(f"   {'Metric':<25} | λ=0.0 | λ=0.2 | λ=0.4 | λ=0.6 | λ=1.0 | λ=1.2")
    print(f"   {'-' * 25}|{'-' * 7}|{'-' * 7}|{'-' * 7}|{'-' * 7}|{'-' * 7}|{'-' * 7}")
    
    metrics_to_compare = [
        ('Variance', 'variance'),
        ('Std Deviation', 'std_deviation'),
        ('Coeff. of Variation (%)', 'coefficient_of_variation')
    ]
    
    for label, key in metrics_to_compare:
        row = f"   {label:<25} |"
        for lambda_val in fairness_weights:
            value = results[lambda_val]['fairness_metrics'][key]
            row += f" {value:5.1f} |"
        print(row)
    
    # Verification Tests
    print("\n" + "=" * 70)
    print("VERIFICATION TESTS")
    print("=" * 70)
    
    test_passed = True
    
    # Test 1: Variance should decrease as fairness weight increases
    print("\n   Test 1: Fairness Impact on Distribution")
    variances = [results[lw]['fairness_metrics']['variance'] for lw in fairness_weights]
    
    print(f"      Variances: {[f'{v:.2f}' for v in variances]}")
    
    # Check if variance decreases
    if variances[0] > variances[-1]:
        reduction = ((variances[0] - variances[-1]) / variances[0]) * 100
        print(f"      ✅ Variance decreased from {variances[0]:.2f} to {variances[-1]:.2f}")
        print(f"      → {reduction:.1f}% reduction in inequality")
    elif variances[0] == variances[-1]:
        print(f"      ⚠️  Variance unchanged at {variances[0]:.2f}")
    else:
        print(f"      ⚠️  Variance trend: {variances[0]:.2f} → {variances[-1]:.2f}")
    
    # Test 2: Low severity zones should get more with higher fairness
    print("\n   Test 2: Impact on Low-Severity Zones")
    z4_no_fairness = results[0.0]['allocation_plan'][3]['allocated']
    z4_high_fairness = results[1.2]['allocation_plan'][3]['allocated']
    
    print(f"      Z4 (lowest severity) allocations:")
    print(f"      λ=0.0: {z4_no_fairness} volunteers (pure severity)")
    print(f"      λ=1.2: {z4_high_fairness} volunteers (120% reserved for minimums)")
    
    if z4_high_fairness > z4_no_fairness:
        print(f"      ✅ Low-severity zone benefits from fairness guarantee")
        print(f"      → Every zone now receives help")
    elif z4_high_fairness == z4_no_fairness:
        print(f"      ⚠️  Fairness not affecting allocation")
    else:
        print(f"      ⚠️  Low-severity zone allocation decreased")
    
    # Test 3: High severity zones should still be prioritized
    print("\n   Test 3: Severity Priority Maintained")
    for lambda_val in fairness_weights:
        allocations = [e['allocated'] for e in results[lambda_val]['allocation_plan']]
        # Check if generally decreasing (high severity → low severity)
        mostly_decreasing = sum(allocations[i] >= allocations[i+1] for i in range(len(allocations)-1)) >= len(allocations) - 2
        
        if mostly_decreasing:
            print(f"      ✅ λ={lambda_val}: Priority order generally maintained")
        else:
            print(f"      ⚠️  λ={lambda_val}: Priority order disrupted: {allocations}")
    
    # Test 4: All constraints still satisfied
    print("\n   Test 4: Constraint Satisfaction")
    for lambda_val in fairness_weights:
        total_allocated = sum(e['allocated'] for e in results[lambda_val]['allocation_plan'])
        if total_allocated <= total_volunteers:
            print(f"      ✅ λ={lambda_val}: Budget satisfied ({total_allocated} <= {total_volunteers})")
        else:
            print(f"      ❌ λ={lambda_val}: Budget violated ({total_allocated} > {total_volunteers})")
            test_passed = False
    
    # Model info
    print("\n📝 Model Information:")
    model_info = allocator.get_model_info()
    print(f"   Version: {model_info['version']}")
    print(f"   Features Enabled:")
    for feature, enabled in model_info['features'].items():
        status = "✅" if enabled else "⏸️"
        print(f"      - {feature}: {status}")
    
    print("\n" + "=" * 70)
    if test_passed:
        print("PHASE 5 TEST PASSED ✅")
    else:
        print("PHASE 5 TEST FAILED ❌")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    test_fairness_comparison()
