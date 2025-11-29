
import sys
import os
import json
import shutil
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.workers.disaster_worker import DisasterAllocationWorker

def test_worker_agent():
    print("=" * 60)
    print("TESTING WORKER AGENT (DisasterAllocationWorker)")
    print("=" * 60)

    # Setup: Clean up LTM for this test agent
    agent_id = "Test_Worker_01"
    ltm_dir = Path("LTM") / agent_id
    if ltm_dir.exists():
        shutil.rmtree(ltm_dir)
        print(f"🧹 Cleaned up LTM directory: {ltm_dir}")

    # 1. Initialize Worker
    print("\n🤖 Initializing Worker Agent...")
    worker = DisasterAllocationWorker(agent_id=agent_id, supervisor_id="Supervisor_Main")
    
    # 2. Define Task
    task_data = {
        "zones": [
            {"id": "Z1", "severity": 8, "required_volunteers": 10},
            {"id": "Z2", "severity": 5, "required_volunteers": 5}
        ],
        "available_volunteers": 10
    }
    
    # 3. Process Task (First Run - Should Compute)
    print("\nRUN 1: Processing Task (Expect Computation)...")
    result1 = worker.process_task(task_data)
    
    print("\n📝 Result 1:")
    print(json.dumps(result1, indent=2))
    
    # Verification 1
    if result1.get("source") == "LIVE":
        print("✅ Correctly computed LIVE result.")
    else:
        print(f"❌ Expected LIVE source, got {result1.get('source')}")

    # 4. Process Task (Second Run - Should Cache Hit)
    print("\nRUN 2: Processing Same Task (Expect Cache Hit)...")
    result2 = worker.process_task(task_data)
    
    print("\n📝 Result 2:")
    print(json.dumps(result2, indent=2))
    
    # Verification 2
    if result2.get("source") == "LTM":
        print("✅ Correctly retrieved from LTM.")
    else:
        print(f"❌ Expected LTM source, got {result2.get('source')}")

    # 5. Verify LTM File Content
    ltm_file = ltm_dir / "allocations.json"
    if ltm_file.exists():
        print(f"\n✅ LTM file exists at {ltm_file}")
        content = json.loads(ltm_file.read_text())
        print(f"   Entries in LTM: {len(content)}")
    else:
        print(f"\n❌ LTM file not found at {ltm_file}")

    print("\n" + "=" * 60)
    print("WORKER AGENT TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_worker_agent()
