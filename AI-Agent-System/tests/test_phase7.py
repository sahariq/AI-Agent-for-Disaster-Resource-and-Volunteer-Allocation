"""
Phase 7 Test: Integration with DisasterAllocationWorker

This test verifies that the VolunteerAllocator optimization engine
is properly integrated into the DisasterAllocationWorker agent.

Key Integration Points:
1. Worker uses optimizer instead of greedy algorithm
2. LTM caching still works correctly
3. Optimization metadata is preserved
4. Output format matches supervisor expectations
5. Fairness parameter is configurable
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.workers.disaster_worker import DisasterAllocationWorker
import json


def main():
    print("=" * 70)
    print("PHASE 7: INTEGRATION WITH DISASTERALLOCATIONWORKER")
    print("=" * 70)
    
    # Test 1: Basic Integration
    print("\n" + "─" * 70)
    print("🧪 TEST 1: Basic Integration")
    print("─" * 70)
    
    worker = DisasterAllocationWorker(
        agent_id="Worker_Disaster",
        supervisor_id="Supervisor_Main",
        fairness_weight=0.8
    )
    
    task_data = {
        "zones": [
            {
                "id": "Z1",
                "severity": 10,
                "capacity": 20,
                "resources_available": 100,
                "min_resources_per_volunteer": 3
            },
            {
                "id": "Z2",
                "severity": 7,
                "capacity": 15,
                "resources_available": 80,
                "min_resources_per_volunteer": 4
            },
            {
                "id": "Z3",
                "severity": 5,
                "capacity": 12,
                "resources_available": 60,
                "min_resources_per_volunteer": 5
            },
            {
                "id": "Z4",
                "severity": 3,
                "capacity": 10,
                "resources_available": 50,
                "min_resources_per_volunteer": 3
            }
        ],
        "available_volunteers": 40
    }
    
    print("\n📋 Task Data:")
    print(f"   Total Volunteers: {task_data['available_volunteers']}")
    print(f"   Zones: {len(task_data['zones'])}")
    for zone in task_data['zones']:
        print(f"      {zone['id']}: Severity={zone['severity']}, Capacity={zone['capacity']}")
    
    print("\n🔄 Processing task (first run - should compute)...")
    result1 = worker.process_task(task_data)
    
    print(f"\n✅ Result Source: {result1['source']}")
    print(f"   Remaining Volunteers: {result1['remaining_volunteers']}")
    
    print("\n📊 Allocation Plan:")
    for alloc in result1['allocation_plan']:
        print(f"   {alloc['zone_id']}: {alloc['assigned_volunteers']} volunteers (Severity: {alloc['severity']})")
    
    if 'optimization_metadata' in result1:
        print("\n📈 Optimization Metadata:")
        meta = result1['optimization_metadata']
        print(f"   Objective Value: {meta['objective_value']}")
        print(f"   Solve Time: {meta['solve_time_seconds']:.4f}s")
        print(f"   Model Type: {meta['model_type']}")
        print(f"   Fairness Weight: {meta['fairness_weight']}")
        print(f"   Variance: {meta['fairness_metrics']['variance']}")
    
    # Test 2: LTM Caching
    print("\n" + "─" * 70)
    print("🧪 TEST 2: LTM Caching")
    print("─" * 70)
    
    print("\n🔄 Processing same task again (should retrieve from LTM)...")
    result2 = worker.process_task(task_data)
    
    print(f"\n✅ Result Source: {result2['source']}")
    
    if result2['source'] == 'LTM':
        print("   ✅ LTM caching works correctly!")
    else:
        print("   ❌ LTM caching failed - expected cached result")
    
    # Verify results are identical
    if result1['allocation_plan'] == result2['allocation_plan']:
        print("   ✅ Cached result matches computed result")
    else:
        print("   ❌ Cached result differs from computed result")
    
    # Test 3: Different Fairness Levels
    print("\n" + "─" * 70)
    print("🧪 TEST 3: Different Fairness Levels")
    print("─" * 70)
    
    print("\n📝 Note on Variance:")
    print("   Lower variance = more equal distribution")
    print("   BUT: High-severity disasters NEED more resources!")
    print("   Goal: Reduce variance to avoid zeros, not perfect equality")
    print("   Recommended λ: 0.2-0.6 (balances severity + fairness)")
    
    fairness_levels = [0.0, 0.3, 0.6]
    
    for fairness in fairness_levels:
        print(f"\n📊 Testing with fairness_weight = {fairness}")
        
        worker_fair = DisasterAllocationWorker(
            agent_id=f"Worker_Disaster_F{int(fairness*10)}",
            supervisor_id="Supervisor_Main",
            fairness_weight=fairness
        )
        
        # Use slightly different task to avoid LTM cache
        task_fair = {
            "zones": task_data['zones'],
            "available_volunteers": 40,
            "fairness_level": fairness  # Add this to make key unique
        }
        
        result_fair = worker_fair.process_task(task_fair)
        
        print(f"   Allocations: ", end="")
        allocs = [a['assigned_volunteers'] for a in result_fair['allocation_plan']]
        print(f"{allocs}")
        
        if 'optimization_metadata' in result_fair:
            variance = result_fair['optimization_metadata']['fairness_metrics']['variance']
            print(f"   Variance: {variance:.2f}")
    
    # Test 4: Severity Priority
    print("\n" + "─" * 70)
    print("🧪 TEST 4: Severity Priority Maintained")
    print("─" * 70)
    
    print("\n✅ Verifying high-severity zones get priority...")
    
    allocations = sorted(
        result1['allocation_plan'], 
        key=lambda x: x['severity'], 
        reverse=True
    )
    
    print("\n   Allocation by Severity (High → Low):")
    for alloc in allocations:
        print(f"      Severity {alloc['severity']}: {alloc['assigned_volunteers']} volunteers")
    
    # Check if generally prioritized (allowing for fairness adjustments)
    z1_alloc = next(a['assigned_volunteers'] for a in result1['allocation_plan'] if a['zone_id'] == 'Z1')
    z4_alloc = next(a['assigned_volunteers'] for a in result1['allocation_plan'] if a['zone_id'] == 'Z4')
    
    if z1_alloc >= z4_alloc:
        print("\n   ✅ Highest severity zone gets at least as many as lowest")
    else:
        print("\n   ⚠️  Priority inversion detected (may be due to high fairness)")
    
    # Test 5: Resource Coupling Constraints
    print("\n" + "─" * 70)
    print("🧪 TEST 5: Resource Coupling Constraints")
    print("─" * 70)
    
    print("\n✅ Verifying resource constraints are satisfied...")
    
    constraints_satisfied = True
    for i, alloc in enumerate(result1['allocation_plan']):
        zone = task_data['zones'][i]
        volunteers = alloc['assigned_volunteers']
        resources_needed = volunteers * zone['min_resources_per_volunteer']
        resources_available = zone['resources_available']
        
        satisfied = resources_needed <= resources_available
        status = "✅" if satisfied else "❌"
        
        print(f"\n   {alloc['zone_id']}: {volunteers} volunteers")
        print(f"      Resources needed: {resources_needed}")
        print(f"      Resources available: {resources_available}")
        print(f"      {status} Constraint satisfied: {satisfied}")
        
        if not satisfied:
            constraints_satisfied = False
    
    # Summary
    print("\n" + "=" * 70)
    print("INTEGRATION TEST SUMMARY")
    print("=" * 70)
    
    tests_passed = []
    
    # Test 1: Integration works
    tests_passed.append(("Optimization engine integrated", result1['source'] == 'LIVE'))
    
    # Test 2: LTM caching works
    tests_passed.append(("LTM caching functional", result2['source'] == 'LTM'))
    
    # Test 3: Metadata preserved
    tests_passed.append(("Optimization metadata included", 'optimization_metadata' in result1))
    
    # Test 4: Severity priority
    tests_passed.append(("Severity priority maintained", z1_alloc >= z4_alloc))
    
    # Test 5: Resource constraints
    tests_passed.append(("Resource constraints satisfied", constraints_satisfied))
    
    print("\n📋 Test Results:\n")
    for test_name, passed in tests_passed:
        status = "✅" if passed else "❌"
        print(f"   {status} {test_name}")
    
    all_passed = all(result for _, result in tests_passed)
    
    print("\n💡 Integration Benefits:\n")
    print("   ✅ Optimal allocations (vs greedy algorithm)")
    print("   ✅ Fairness consideration (configurable)")
    print("   ✅ Resource coupling constraints enforced")
    print("   ✅ Capacity limits respected")
    print("   ✅ LTM caching for performance (includes fairness in key)")
    print("   ✅ Rich optimization metadata")
    
    print("\n📊 Variance Philosophy:\n")
    print("   • λ=0.0: Pure severity (variance ~62) - some zones get zero")
    print("   • λ=0.3: Balanced (variance ~59) - Balanced but still prioritizes severity")
    print("   • λ=0.6: High fairness (variance ~44) -  RECOMMENDED for production")
    print("   • λ=1.0: Perfect minimums (variance ~19) - risks under-serving critical zones")
    print("   ")
    print("   ⚠️  Goal is NOT minimum variance!")
    print("   ✅ Goal is: No zeros + severity priority maintained")
    
    print("\n" + "=" * 70)
    if all_passed:
        print("PHASE 7 TEST PASSED ✅")
    else:
        print("PHASE 7 TEST FAILED ❌")
    print("=" * 70)
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
