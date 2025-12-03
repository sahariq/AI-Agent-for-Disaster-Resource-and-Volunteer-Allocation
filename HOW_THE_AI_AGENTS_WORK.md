# 🤖 How the AI Agents Work - Step-by-Step Guide

## Overview

The system uses a **Supervisor-Worker pattern** where:
- **Supervisor Agent**: Coordinates tasks and manages workflow
- **Worker Agent**: Performs the actual optimization computation
- **Communication**: JSON-based message passing between agents

---

## 🔄 Complete Workflow (Step-by-Step)

### Step 1: Initialization

```python
# Supervisor creates a Worker
supervisor = SupervisorAgent()
worker = DisasterAllocationWorker("Worker_Disaster", "Supervisor_Main")
```

**What happens:**
- Worker sets up its **Long-Term Memory (LTM)** directory: `LTM/Worker_Disaster/allocations.json`
- Worker stores its `fairness_weight` (default: 0.6) for optimization
- Both agents are ready to communicate

---

### Step 2: Task Assignment

**Supervisor creates a task:**

```python
task = Task(
    name="allocate_resources",
    priority=1,
    parameters={
        "zones": [
            {"id": "Z1", "severity": 8, "required_volunteers": 10, ...},
            {"id": "Z2", "severity": 5, "required_volunteers": 6, ...}
        ],
        "available_volunteers": 12
    }
)
```

**Supervisor creates a message:**

```python
message = Message.new(
    sender="Supervisor_Main",
    recipient="Worker_Disaster",
    msg_type="task_assignment",
    task=task
)
```

**Message Structure:**
```json
{
  "message_id": "uuid-1234",
  "sender": "Supervisor_Main",
  "recipient": "Worker_Disaster",
  "type": "task_assignment",
  "task": {
    "name": "allocate_resources",
    "priority": 1,
    "parameters": {
      "zones": [...],
      "available_volunteers": 12
    }
  },
  "timestamp": "2025-12-02T10:00:00Z"
}
```

---

### Step 3: Worker Receives Message

**Worker's `handle_incoming_message()` method:**

```python
def handle_incoming_message(self, json_message: str):
    message = json.loads(json_message)  # Parse JSON
    msg_type = message.get("type")
    
    if msg_type == "task_assignment":
        task_params = message.get("task", {}).get("parameters", {})
        self._current_task_id = message.get("message_id")
        self._execute_task(task_params, self._current_task_id)
```

**What happens:**
1. Worker parses the JSON message
2. Extracts task parameters (zones, available_volunteers)
3. Stores the message ID for later reference
4. Calls `_execute_task()`

---

### Step 4: Worker Checks LTM Cache

**Before computing, worker checks if it's seen this exact scenario before:**

```python
def process_task(self, task_data: dict) -> dict:
    # Create cache key from task data + fairness_weight
    cache_data = {
        **task_data,
        "fairness_weight": self.fairness_weight
    }
    key = json.dumps(cache_data, sort_keys=True)
    
    # Check LTM cache
    cached_result = self.read_from_ltm(key)
    
    if cached_result:
        print("[Worker] Retrieved cached result from LTM.")
        return {"source": "LTM", **cached_result}  # Return cached result!
```

**LTM Cache Structure:**
- **Key**: JSON string of task parameters + fairness_weight
- **Value**: Complete allocation result (plan, metadata, etc.)
- **Location**: `LTM/Worker_Disaster/allocations.json`

**Example Cache Entry:**
```json
{
  "{\"available_volunteers\":12,\"fairness_weight\":0.6,\"zones\":[...]}": {
    "allocation_plan": [...],
    "remaining_volunteers": 0,
    "optimization_metadata": {...}
  }
}
```

**Why LTM?**
- **Performance**: Avoids recomputing identical scenarios
- **Consistency**: Same inputs = same outputs
- **Efficiency**: Saves computation time (optimization can take milliseconds)

---

### Step 5: Optimization (If Cache Miss)

**If no cached result, worker calls the optimization engine:**

```python
if not cached_result:
    print("[Worker] Computing optimal allocation plan...")
    
    # Call the mathematical optimization engine
    allocation_plan, metadata = run_allocation(
        zones=zones,
        available_volunteers=available_volunteers,
        fairness_weight=self.fairness_weight,
        extra_constraints=None
    )
```

**What `run_allocation()` does:**

1. **Creates Integer Linear Programming (ILP) problem:**
   ```python
   prob = LpProblem("Disaster_Volunteer_Allocation", LpMaximize)
   ```

2. **Creates decision variables:**
   ```python
   x = {
       "Z1": LpVariable("x_Z1", lowBound=0, upBound=capacity, cat=LpInteger),
       "Z2": LpVariable("x_Z2", lowBound=0, upBound=capacity, cat=LpInteger)
   }
   ```
   - Each variable = number of volunteers allocated to that zone

3. **Sets objective function:**
   ```python
   # Maximize: Σ(severity × volunteers_allocated)
   prob += lpSum([zone['severity'] * x[zone['id']] for zone in zones])
   ```

4. **Adds constraints:**
   - **Budget**: Total volunteers ≤ available_volunteers
   - **Capacity**: Per-zone ≤ capacity limit
   - **Resources**: Volunteers × min_resources ≤ available resources
   - **Fairness**: Each zone gets minimum baseline (when fairness_weight > 0)

5. **Solves using CBC solver:**
   ```python
   prob.solve(PULP_CBC_CMD(msg=0))
   ```

6. **Extracts results:**
   ```python
   allocation_plan = [
       {"zone_id": "Z1", "allocated": 8, ...},
       {"zone_id": "Z2", "allocated": 4, ...}
   ]
   metadata = {
       "objective_value": 64.0,
       "solve_time_seconds": 0.05,
       "remaining_volunteers": 0,
       ...
   }
   ```

---

### Step 6: Worker Stores Result in LTM

**After computing, worker saves result for future use:**

```python
result = {
    "allocation_plan": plan,
    "remaining_volunteers": metadata["remaining_volunteers"],
    "timestamp": metadata["timestamp"],
    "optimization_metadata": {...}
}

# Save to LTM
self.write_to_ltm(key, result)
return {"source": "LIVE", **result}
```

**LTM Write Process:**
```python
def write_to_ltm(self, key: str, value: Any) -> bool:
    # Load existing cache
    if self.ltm_file.exists():
        data = json.loads(self.ltm_file.read_text())
    else:
        data = {}
    
    # Add new entry
    data[key] = value
    
    # Save back to file
    self.ltm_file.write_text(json.dumps(data, indent=2))
    return True
```

---

### Step 7: Worker Sends Completion Report

**Worker automatically constructs and sends a completion report:**

```python
def _report_completion(self, related_msg_id: str, status: str, results: dict):
    report = {
        "message_id": str(uuid.uuid4()),  # New unique ID
        "sender": self._id,  # "Worker_Disaster"
        "recipient": self._supervisor_id,  # "Supervisor_Main"
        "type": "completion_report",
        "related_message_id": related_msg_id,  # Links back to original task
        "status": "SUCCESS",  # or "FAILURE"
        "results": results,  # Allocation plan + metadata
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    self.send_message(self._supervisor_id, report)
```

**Completion Report Structure:**
```json
{
  "message_id": "uuid-5678",
  "sender": "Worker_Disaster",
  "recipient": "Supervisor_Main",
  "type": "completion_report",
  "related_message_id": "uuid-1234",
  "status": "SUCCESS",
  "results": {
    "source": "LIVE",  # or "LTM" if from cache
    "allocation_plan": [
      {
        "zone_id": "Z1",
        "assigned_volunteers": 8,
        "severity": 8
      },
      {
        "zone_id": "Z2",
        "assigned_volunteers": 4,
        "severity": 5
      }
    ],
    "remaining_volunteers": 0,
    "optimization_metadata": {
      "objective_value": 64.0,
      "solve_time_seconds": 0.05,
      "fairness_weight": 0.6,
      ...
    }
  },
  "timestamp": "2025-12-02T10:00:05Z"
}
```

---

### Step 8: Supervisor Receives Report

**Supervisor's `receive_report()` method:**

```python
def receive_report(self, message_obj: dict):
    print(f"[{self.id}] Received completion report!")
    print(json.dumps(message_obj, indent=2))
    self._log("completion_report", message_obj)
```

**What supervisor does:**
- Logs the completion report
- Can process the allocation plan
- Can trigger follow-up actions (e.g., notify other systems)

---

## 🧠 Key AI Concepts

### 1. **Abstract Base Class Pattern**

**`AbstractWorkerAgent`** defines the interface:

```python
class AbstractWorkerAgent(ABC):
    @abstractmethod
    def process_task(self, task_data: dict) -> dict:
        """Must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def write_to_ltm(self, key: str, value: Any) -> bool:
        """Must be implemented by subclasses"""
        pass
```

**Benefits:**
- **Extensibility**: Easy to add new worker types (e.g., `MedicalWorker`, `LogisticsWorker`)
- **Consistency**: All workers follow the same communication protocol
- **Type Safety**: Enforces required methods

### 2. **Long-Term Memory (LTM)**

**Purpose**: Cache optimization results to avoid recomputation

**How it works:**
- **Key**: Serialized task parameters (zones + available_volunteers + fairness_weight)
- **Value**: Complete allocation result
- **Storage**: JSON file in `LTM/{agent_id}/allocations.json`

**Cache Key Example:**
```json
{
  "available_volunteers": 12,
  "fairness_weight": 0.6,
  "zones": [
    {"id": "Z1", "severity": 8, ...},
    {"id": "Z2", "severity": 5, ...}
  ]
}
```

**Why include `fairness_weight` in key?**
- Different fairness weights produce different allocations
- Ensures cache doesn't return wrong results for different fairness settings

### 3. **Message Passing Protocol**

**Type-Safe Messages using Pydantic:**

```python
class Message(BaseModel):
    message_id: str
    sender: str
    recipient: str
    type: str
    task: Optional[Task] = None
    related_message_id: Optional[str] = None
    status: Optional[str] = None
    results: Optional[Dict[str, Any]] = None
    timestamp: str
```

**Benefits:**
- **Validation**: Pydantic ensures message structure is correct
- **Type Safety**: IDE autocomplete and type checking
- **Serialization**: Easy JSON conversion

### 4. **Mathematical Optimization**

**Integer Linear Programming (ILP):**

- **Decision Variables**: Integer number of volunteers per zone
- **Objective**: Maximize severity-weighted impact
- **Constraints**: Budget, capacity, resources, fairness
- **Solver**: CBC (COIN-OR Branch and Cut) via PuLP

**Why ILP?**
- **Optimal Solutions**: Guarantees mathematically optimal allocation
- **Fast**: Solves in milliseconds for typical scenarios
- **Flexible**: Easy to add new constraints

---

## 🔌 Alternative: HTTP API Mode

**Instead of direct agent communication, you can use the Flask API:**

### API Endpoint: `/invoke`

**Request:**
```bash
POST http://localhost:8000/invoke
Content-Type: application/json

{
  "message_id": "uuid-1234",
  "sender": "Supervisor_Main",
  "recipient": "Worker_Disaster",
  "type": "task_assignment",
  "task": {
    "name": "allocate_resources",
    "priority": 1,
    "parameters": {
      "zones": [...],
      "available_volunteers": 12
    }
  }
}
```

**Response:**
```json
{
  "message_id": "uuid-5678",
  "sender": "Worker_Disaster",
  "recipient": "Supervisor_Main",
  "type": "completion_report",
  "status": "SUCCESS",
  "results": {
    "allocation_plan": [...],
    "optimization_metadata": {...}
  }
}
```

**What happens:**
1. Flask server receives POST request
2. Validates message structure
3. Calls `run_allocation()` directly (bypasses LTM for now)
4. Returns completion report as JSON

**Benefits:**
- **Remote Access**: Can call from any language/system
- **Stateless**: No need to maintain agent instances
- **Scalable**: Can deploy multiple API servers

---

## 📊 Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    SUPERVISOR AGENT                          │
│  - Receives disaster scenario                                │
│  - Creates task assignment                                   │
│  - Sends message to worker                                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ JSON Message (task_assignment)
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    WORKER AGENT                               │
│  1. Receives message                                         │
│  2. Checks LTM cache                                         │
│     ├─ Cache HIT → Return cached result                      │
│     └─ Cache MISS → Continue                                │
│  3. Calls optimization engine                                │
│  4. Stores result in LTM                                     │
│  5. Sends completion report                                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ JSON Message (completion_report)
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              OPTIMIZATION ENGINE                              │
│  - Creates ILP problem                                       │
│  - Sets objective: Maximize Σ(severity × volunteers)         │
│  - Adds constraints (budget, capacity, resources, fairness)  │
│  - Solves using CBC solver                                   │
│  - Returns allocation plan + metadata                        │
└─────────────────────────────────────────────────────────────┘
                        │
                        │ Allocation Plan
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              LONG-TERM MEMORY (LTM)                          │
│  - Stores: {cache_key: allocation_result}                   │
│  - Location: LTM/Worker_Disaster/allocations.json           │
│  - Purpose: Avoid recomputation of identical scenarios       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Key Takeaways

1. **Supervisor-Worker Pattern**: Supervisor coordinates, Worker computes
2. **Message-Based Communication**: JSON messages with type safety (Pydantic)
3. **LTM Caching**: Avoids recomputation, improves performance
4. **Mathematical Optimization**: ILP solver finds optimal allocations
5. **Extensible Architecture**: Easy to add new worker types
6. **Multiple Interfaces**: Direct agent calls OR HTTP API

---

## 💡 Example: Real-World Scenario

**Scenario**: Earthquake hits 3 zones, 20 volunteers available

1. **Supervisor receives scenario:**
   - Zone A: Severity 9, needs 10 volunteers, capacity 10
   - Zone B: Severity 6, needs 8 volunteers, capacity 8
   - Zone C: Severity 4, needs 5 volunteers, capacity 5

2. **Supervisor creates task:**
   ```python
   task = Task(
       name="allocate_resources",
       parameters={
           "zones": [zone_a, zone_b, zone_c],
           "available_volunteers": 20
       }
   )
   ```

3. **Worker processes:**
   - Checks LTM: Cache miss (first time seeing this scenario)
   - Calls optimization: Allocates 10 to Zone A, 8 to Zone B, 2 to Zone C
   - Stores in LTM for future use
   - Returns completion report

4. **Result:**
   - Zone A: 10 volunteers (100% of need, highest severity)
   - Zone B: 8 volunteers (100% of need)
   - Zone C: 2 volunteers (40% of need, lowest severity)
   - **Total**: 20 volunteers allocated (optimal for severity-weighted impact)

5. **Next time same scenario:**
   - Worker checks LTM: **Cache HIT!**
   - Returns cached result instantly (no recomputation)

---

## 🔧 Customization

**To add a new worker type:**

1. Create new class inheriting from `AbstractWorkerAgent`:
   ```python
   class MedicalWorker(AbstractWorkerAgent):
       def process_task(self, task_data: dict) -> dict:
           # Your custom logic here
           pass
   ```

2. Implement required methods:
   - `process_task()`: Your business logic
   - `send_message()`: Communication method
   - `write_to_ltm()`: Cache storage
   - `read_from_ltm()`: Cache retrieval

3. Use it:
   ```python
   medical_worker = MedicalWorker("Worker_Medical", "Supervisor_Main")
   # Same communication protocol works!
   ```

---

This is how the AI agents work! The system is designed to be **modular**, **extensible**, and **efficient** through caching and mathematical optimization.

