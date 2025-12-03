"""
Process disaster scenarios from CSV file through the allocation system.

This script:
1. Loads scenarios from disaster_scenarios.csv
2. Processes each scenario through the volunteer allocation system
3. Displays results for each scenario
"""

import pandas as pd
import json
import os
import sys
from pathlib import Path

# Add AI-Agent-System to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'AI-Agent-System'))

from optimization.volunteer_allocator import run_allocation


def load_scenarios(csv_path='disaster_scenarios.csv'):
    """Load scenarios from CSV file."""
    if not os.path.exists(csv_path):
        # Try alternative path
        csv_path = os.path.join('AI-Agent-System', 'datasets', 'disaster_scenarios.csv')
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found. Tried: {csv_path}")
    
    df = pd.read_csv(csv_path)
    
    # Convert numeric columns
    numeric_cols = ['severity', 'required_volunteers', 'capacity', 'available_volunteers']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df


def process_scenario(df, scenario_id):
    """Process a single scenario through the allocation system."""
    # Filter zones for this scenario
    scenario_data = df[df['scenario_id'] == scenario_id].copy()
    
    if len(scenario_data) == 0:
        print(f"⚠️  No zones found for {scenario_id}")
        return None
    
    # Get available volunteers (should be same for all zones in scenario)
    available_volunteers = int(scenario_data['available_volunteers'].iloc[0])
    
    # Prepare zones in format expected by allocation system
    zones = []
    for _, row in scenario_data.iterrows():
        zone = {
            'id': str(row['zone_id']),
            'severity': int(row['severity']),
            'required_volunteers': int(row['required_volunteers']),
        }
        
        # Add optional fields if they exist
        if 'capacity' in row and pd.notna(row['capacity']):
            zone['capacity'] = int(row['capacity'])
        if 'resources_available' in row and pd.notna(row['resources_available']):
            zone['resources_available'] = int(row['resources_available'])
        if 'min_resources_per_volunteer' in row and pd.notna(row['min_resources_per_volunteer']):
            zone['min_resources_per_volunteer'] = float(row['min_resources_per_volunteer'])
        
        zones.append(zone)
    
    # Run allocation
    try:
        allocation_plan, metadata = run_allocation(
            zones=zones,
            available_volunteers=available_volunteers,
            fairness_weight=0.6,
            extra_constraints=None
        )
        
        return {
            'scenario_id': scenario_id,
            'scenario_name': scenario_data['scenario_name'].iloc[0],
            'zones': zones,
            'allocation_plan': allocation_plan,
            'metadata': metadata
        }
    except Exception as e:
        print(f"❌ Error processing {scenario_id}: {e}")
        return None


def display_results(result):
    """Display allocation results in a readable format."""
    if result is None:
        return
    
    print("\n" + "="*80)
    print(f"📊 SCENARIO: {result['scenario_name']} ({result['scenario_id']})")
    print("="*80)
    
    # Scenario summary
    total_required = sum(z['required_volunteers'] for z in result['zones'])
    available = result['metadata']['remaining_volunteers'] + sum(
        a['allocated'] for a in result['allocation_plan']
    )
    
    print(f"\n📋 Summary:")
    print(f"   Zones: {len(result['zones'])}")
    print(f"   Total Required: {total_required} volunteers")
    print(f"   Available: {available} volunteers")
    print(f"   Remaining: {result['metadata']['remaining_volunteers']} volunteers")
    
    # Allocation details
    print(f"\n🎯 Allocation Plan:")
    print(f"{'Zone':<15} {'Severity':<10} {'Required':<10} {'Allocated':<10} {'Satisfaction':<12}")
    print("-" * 70)
    
    for alloc in result['allocation_plan']:
        zone_id = alloc['zone_id']
        zone_info = next((z for z in result['zones'] if z['id'] == zone_id), None)
        required = zone_info['required_volunteers'] if zone_info else 0
        allocated = alloc['allocated']
        satisfaction = alloc.get('satisfaction_pct', 0)
        
        print(f"{zone_id:<15} {alloc['severity']:<10} {required:<10} {allocated:<10} {satisfaction:.1f}%")
    
    # Optimization metadata
    print(f"\n⚙️  Optimization:")
    print(f"   Objective Value: {result['metadata']['objective_value']:.2f}")
    print(f"   Solve Time: {result['metadata']['solve_time_seconds']:.4f}s")
    print(f"   Fairness Weight: {result['metadata']['fairness_weight']}")
    print(f"   Model Type: {result['metadata']['model_type']}")


def main():
    """Main function to process all scenarios."""
    print("🚨 Disaster Scenario Allocation Processor")
    print("="*80)
    
    # Load CSV
    try:
        print("\n📂 Loading scenarios from CSV...")
        df = load_scenarios()
        print(f"✅ Loaded {len(df)} zones from {df['scenario_id'].nunique()} scenarios")
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return
    
    # Get unique scenarios
    scenarios = df['scenario_id'].unique()
    print(f"\n📋 Found {len(scenarios)} scenarios to process")
    
    # Process each scenario
    results = []
    for scenario_id in scenarios:
        result = process_scenario(df, scenario_id)
        if result:
            results.append(result)
            display_results(result)
    
    # Summary
    print("\n" + "="*80)
    print(f"✅ Processing Complete!")
    print(f"   Processed: {len(results)}/{len(scenarios)} scenarios")
    print("="*80)
    
    # Optionally save results to JSON
    if results:
        output_file = 'allocation_results.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Results saved to: {output_file}")


if __name__ == "__main__":
    main()

