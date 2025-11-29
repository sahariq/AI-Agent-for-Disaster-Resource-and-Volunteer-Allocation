# AI Agent for Disaster Resource and Volunteer Allocation - Codebase Documentation

**Version:** 0.1.0  
**Last Updated:** November 29, 2025  
**Purpose:** This document provides a comprehensive overview of the project's architecture, design patterns, and implementation details for AI models and developers.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture & Design Patterns](#architecture--design-patterns)
3. [Project Structure](#project-structure)
4. [Core Components](#core-components)
5. [Communication Protocol](#communication-protocol)
6. [Data Flow](#data-flow)
7. [Long-Term Memory (LTM) System](#long-term-memory-ltm-system)
8. [Software Engineering Principles Applied](#software-engineering-principles-applied)
9. [Dependencies & Configuration](#dependencies--configuration)
10. [Execution Flow](#execution-flow)
11. [Extension Points](#extension-points)

---

## Project Overview

### Purpose
This system is a multi-agent AI solution designed to allocate volunteers and resources across disaster zones based on severity levels and availability constraints. The system employs a **Supervisor-Worker** architecture pattern to coordinate tasks and maintain allocation history.

### Key Features
- **Multi-Agent System**: Hierarchical agent architecture with supervisor and worker agents
- **Resource Allocation**: Optimizes volunteer distribution across disaster zones
- **Long-Term Memory**: Caches allocation plans to improve performance on repeated scenarios
- **Message-Based Communication**: Structured protocol for inter-agent messaging
- **Audit Logging**: Comprehensive logging of all supervisor actions and decisions

### Technology Stack
- **Language**: Python 3.8+
- **Key Libraries**: 
  - `pydantic` - Data validation and settings management
  - `pulp` - Linear programming optimization (PuLP/CBC solver)
  - `flask` - HTTP API server for supervisor-worker communication
  - `pandas` - Data manipulation (planned)
  - `streamlit` - Dashboard UI (planned)

---

## Architecture & Design Patterns

### 1. **Supervisor-Worker Pattern**
The system implements a hierarchical multi-agent architecture:
- **Supervisor Agent**: Orchestrates task assignment, monitors completion, and logs activities
- **Worker Agents**: Execute specialized tasks and report results back to supervisor

**Benefits:**
- Separation of concerns between coordination and execution
- Scalability: New workers can be added without modifying supervisor logic
- Fault isolation: Worker failures don't crash the entire system

### 2. **Abstract Base Class Pattern**
The `AbstractWorkerAgent` defines a contract for all worker implementations:
- Enforces consistent interface across different worker types
- Enables polymorphism and extensibility
- Separates protocol handling from business logic

### 3. **Message-Oriented Communication**
All inter-agent communication uses structured JSON messages:
- Type-safe message contracts using Pydantic models
- Asynchronous communication pattern (ready for distributed systems)
- Protocol constants ensure consistent message types

### 4. **Repository Pattern (LTM)**
Long-Term Memory acts as a data persistence layer:
- Abstracts storage mechanism from business logic
- Enables caching and performance optimization
- File-based implementation (can be upgraded to database)

---

## Project Structure

```
AI-Agent-for-Disaster-Resource-and-Volunteer-Allocation/
│
├── pyproject.toml                 # Poetry project configuration
├── requirements.txt               # Pip dependency list
├── README.md                      # Quick start guide
├── sample_data.csv               # Sample disaster zone data
│
└── AI-Agent-System/              # Main system directory
    ├── main.py                   # Application entry point (deprecated - use API server)
    ├── supervisor_log.jsonl      # Audit log for supervisor actions
    │
    ├── agents/                   # Agent implementations
    │   ├── supervisor/
    │   │   └── supervisor.py     # Supervisor agent implementation
    │   │
    │   └── workers/
    │       ├── worker_base.py    # Abstract base class for workers
    │       └── disaster_worker.py # Disaster allocation worker
    │
    ├── api/                      # HTTP API server
    │   ├── __init__.py
    │   └── server.py             # Flask API endpoints (/health, /invoke, /query)
    │
    ├── communication/            # Communication layer
    │   ├── models.py             # Pydantic data models
    │   └── protocol.py           # Message type constants
    │
    ├── optimization/             # Optimization engine
    │   ├── __init__.py
    │   └── volunteer_allocator.py # PuLP-based allocation optimizer
    │
    └── LTM/                      # Long-Term Memory storage
        └── Worker_Disaster/
            └── allocations.json  # Cached allocation plans
```

### Directory Responsibilities

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| `AI-Agent-System/` | Core system implementation | `api/server.py` |
| `agents/workers/` | Worker agent implementations | `worker_base.py`, `disaster_worker.py` |
| `api/` | HTTP API server | `server.py` (Flask endpoints) |
| `communication/` | Inter-agent communication | `models.py`, `protocol.py` |
| `optimization/` | Allocation optimization engine | `volunteer_allocator.py` |
| `LTM/` | Persistent storage | `allocations.json` |

---

## Core Components

### 1. Supervisor Agent (`agents/supervisor/supervisor.py`)

**Responsibility**: Central coordinator for the entire system.

**Key Methods:**
- `assign_task(zones, available_volunteers)` - Creates and dispatches task assignments to workers
- `receive_report(message_obj)` - Handles completion reports from workers
- `health_check()` - Returns system status
- `_log(msg_type, content)` - Appends timestamped entries to audit log

**State Management:**
- Maintains reference to worker agent
- Logs all communications to `supervisor_log.jsonl`
- Tracks system health status

**Design Notes:**
- Single Responsibility: Only handles coordination and logging
- Currently supports one worker (extensible to multiple workers)
- Uses JSONL format for append-only audit trail

---

### 2. Abstract Worker Base (`agents/workers/worker_base.py`)

**Responsibility**: Defines the contract for all worker agents.

**Abstract Methods (Must Implement):**
```python
def process_task(task_data: dict) -> dict
    """Core business logic - returns results dictionary"""

def send_message(recipient: str, message_obj: dict)
    """Communication layer - sends JSON message"""

def write_to_ltm(key: str, value: Any) -> bool
    """Persistence layer - writes to long-term memory"""

def read_from_ltm(key: str) -> Optional[Any]
    """Persistence layer - reads from long-term memory"""
```

**Concrete Methods (Shared Protocol):**
- `handle_incoming_message(json_message)` - Parses and routes incoming messages
- `_execute_task(task_data, related_msg_id)` - Wraps task execution with error handling
- `_report_completion(related_msg_id, status, results)` - Sends completion report

**Design Pattern**: Template Method Pattern
- Framework provides message handling logic
- Subclasses implement domain-specific processing

---

### 3. Disaster Allocation Worker (`agents/workers/disaster_worker.py`)

**Responsibility**: Executes volunteer allocation algorithm.

**Business Logic (`process_task`):**
1. Generate cache key from input parameters (deterministic)
2. Check LTM for cached result
3. If cache hit: Return cached allocation plan
4. If cache miss:
   - Iterate through zones in order
   - Allocate volunteers based on requirement and availability
   - Track remaining volunteers
   - Store result in LTM for future use

**Allocation Algorithm:**
- **Strategy**: Greedy first-come-first-served allocation
- **Input**: List of zones (id, severity, required_volunteers) + available volunteer count
- **Output**: Allocation plan (zone_id, assigned_volunteers, severity) + remaining count
- **Optimization**: Simple sequential allocation (can be enhanced with severity prioritization)

**LTM Implementation:**
- **Storage**: JSON file per worker instance
- **Key**: Serialized task parameters (sorted JSON string)
- **Value**: Complete allocation result with timestamp
- **Cache Hit Rate**: Improves performance on repeated scenarios

---

## Communication Protocol

### Message Structure

All messages follow a standardized JSON schema defined by Pydantic models:

```python
{
    "message_id": "uuid-v4",              # Unique identifier
    "sender": "agent_id",                 # Source agent identifier
    "recipient": "agent_id",              # Target agent identifier
    "type": "message_type",               # Protocol constant
    "task": {                             # Optional: Task details
        "name": "task_name",
        "priority": 1,
        "parameters": {...}
    },
    "related_message_id": "uuid-v4",      # Optional: Links responses to requests
    "status": "SUCCESS|FAILURE",          # Optional: Task outcome
    "results": {...},                     # Optional: Task output
    "timestamp": "ISO-8601"               # Message creation time
}
```

### Message Types (`communication/protocol.py`)

| Constant | Value | Direction | Purpose |
|----------|-------|-----------|---------|
| `TASK_ASSIGNMENT` | "task_assignment" | Supervisor → Worker | Assign new task |
| `COMPLETION_REPORT` | "completion_report" | Worker → Supervisor | Report task result |
| `HEALTH_CHECK` | "health_check" | Bidirectional | System status query |

### Message Flow Sequence

```
Supervisor                          Worker
    |                                 |
    |------ TASK_ASSIGNMENT -------->|
    |   (zones, volunteers)           |
    |                                 |
    |                             process_task()
    |                             check LTM cache
    |                             compute allocation
    |                             store in LTM
    |                                 |
    |<---- COMPLETION_REPORT ---------|
    |   (status, results)             |
    |                                 |
   log to JSONL                      |
```

---

## Data Flow

### Task Assignment Flow

1. **Initialization** (`main.py`):
   - Create `SupervisorAgent` instance
   - Define disaster zones with severity and requirements
   - Specify available volunteer count

2. **Task Creation** (Supervisor):
   - Wrap parameters in `Task` object
   - Create `Message` with TASK_ASSIGNMENT type
   - Serialize to JSON and send to worker

3. **Task Processing** (Worker):
   - Deserialize message
   - Extract task parameters
   - Check LTM cache using parameter hash
   - Execute allocation algorithm if needed
   - Store result in LTM

4. **Result Reporting** (Worker):
   - Package results with status
   - Create COMPLETION_REPORT message
   - Send back to supervisor

5. **Logging** (Supervisor):
   - Append task assignment to log
   - Append completion report to log
   - Timestamp all entries

### Data Persistence

**Supervisor Log** (`supervisor_log.jsonl`):
- Format: JSON Lines (one object per line)
- Content: All task assignments and completion reports
- Purpose: Audit trail, debugging, analytics
- Schema:
  ```json
  {
    "time": "2025-11-12T18:32:03.104779",
    "type": "task_assignment|completion_report",
    "data": {...}  // Full message object
  }
  ```

**LTM Allocations** (`LTM/Worker_Disaster/allocations.json`):
- Format: JSON dictionary
- Key: Serialized task parameters (sorted for consistency)
- Value: Allocation result with timestamp
- Purpose: Performance optimization via caching

---

## Long-Term Memory (LTM) System

### Architecture

The LTM system provides persistent caching of allocation decisions:

**Design Principles:**
- **Deterministic Keys**: Task parameters serialized to sorted JSON
- **Immutable Values**: Once cached, results are not modified
- **Worker-Specific**: Each worker has its own LTM directory
- **File-Based**: Simple JSON file storage (upgradeable to database)

### Cache Strategy

**Cache Key Generation:**
```python
key = json.dumps(task_data, sort_keys=True)
```
- Ensures identical tasks produce identical keys
- Sort keys for consistency regardless of parameter order

**Cache Hit:**
- Returns stored result immediately
- Adds "source": "LTM" field to result
- Bypasses computation entirely

**Cache Miss:**
- Executes full allocation algorithm
- Stores result for future use
- Adds "source": "LIVE" field to result

### Performance Benefits

- **Reduced Latency**: Instant retrieval for repeated scenarios
- **Computational Savings**: Avoids re-running allocation algorithm
- **Scalability**: Handles high-frequency identical requests efficiently

### Future Enhancements

- **TTL (Time-To-Live)**: Expire stale cache entries
- **Cache Invalidation**: Update when zone data changes
- **Database Backend**: Replace JSON with SQLite/PostgreSQL
- **Distributed Cache**: Redis for multi-instance deployments

---

## Software Engineering Principles Applied

### 1. **SOLID Principles**

#### Single Responsibility Principle (SRP)
- **Supervisor**: Only coordinates and logs
- **Worker**: Only processes allocation tasks
- **Communication Models**: Only define message structure
- **Protocol**: Only defines message type constants

#### Open/Closed Principle (OCP)
- Abstract base class allows new worker types without modifying existing code
- Protocol constants enable new message types without breaking existing handlers

#### Liskov Substitution Principle (LSP)
- Any `AbstractWorkerAgent` subclass can replace the base class
- Supervisor works with any worker implementing the abstract interface

#### Interface Segregation Principle (ISP)
- Workers implement only required methods for their role
- Communication models are minimal and focused

#### Dependency Inversion Principle (DIP)
- Supervisor depends on worker abstraction, not concrete implementation
- Easy to swap worker implementations or add new ones

### 2. **Design Patterns**

| Pattern | Implementation | Benefit |
|---------|----------------|---------|
| **Template Method** | `AbstractWorkerAgent._execute_task()` | Consistent error handling |
| **Strategy** | Worker allocation algorithms | Swappable allocation strategies |
| **Factory** | `Message.new()` static method | Consistent message creation |
| **Repository** | LTM read/write methods | Abstracted persistence |

### 3. **Code Quality Practices**

- **Type Hints**: All method signatures include type annotations
- **Docstrings**: Clear documentation for classes and methods
- **Error Handling**: Try-catch blocks with meaningful error messages
- **Logging**: Comprehensive audit trail for debugging
- **Modularity**: Clear separation between layers (agents, communication, storage)

### 4. **Separation of Concerns**

```
Presentation Layer   → (Planned) Streamlit Dashboard
Business Logic       → Worker process_task() methods
Communication Layer  → Protocol + Models
Persistence Layer    → LTM read/write operations
```

---

## Dependencies & Configuration

### Python Dependencies

**Core Requirements (`requirements.txt`):**
```
Flask          # Web framework (planned for API)
pandas         # Data manipulation
numpy          # Numerical computations
scikit-learn   # ML algorithms (planned)
PuLP           # Linear programming optimization (planned)
streamlit      # Dashboard UI (planned)
geopandas      # Geospatial data (planned)
matplotlib     # Visualization (planned)
pytest         # Testing framework
jupyter        # Interactive development
```

**Current Usage:**
- Only Pydantic is actively used for data validation
- Other dependencies are prepared for future features

**Poetry Configuration (`pyproject.toml`):**
- Project metadata and versioning
- Dependency management with version constraints
- Development dependencies (pytest, black, mypy)

### Configuration Files

**Project Configuration:**
- `pyproject.toml` - Poetry/packaging configuration
- `requirements.txt` - Pip-installable dependencies

**Sample Data:**
- `sample_data.csv` - Example disaster zone data (zone, severity)

---

## Execution Flow

### Startup Sequence

```python
# main.py execution flow
1. Import SupervisorAgent class
2. Instantiate supervisor (creates worker internally)
3. Define test scenario (zones + available volunteers)
4. Run health check → Verify system operational
5. Assign task → Triggers full allocation workflow
6. Worker processes task → Returns results
7. Supervisor logs results → Appends to JSONL
8. Program exits
```

### Typical Execution

```bash
$ python AI-Agent-System/main.py

=== System Startup ===
{'status': 'OK', 'timestamp': '2025-11-14T12:00:00.000000'}

[Supervisor_Main] Sending task to worker...
[Worker_Disaster] received task: allocate_resources
[Worker_Disaster] Computing new allocation plan...
[Worker_Disaster] Sending message to Supervisor_Main:
{
  "message_id": "uuid",
  "sender": "Worker_Disaster",
  "recipient": "Supervisor_Main",
  "type": "completion_report",
  "status": "SUCCESS",
  "results": {
    "source": "LIVE",
    "allocation_plan": [...],
    "remaining_volunteers": 0,
    "timestamp": "2025-11-14T12:00:00.000000"
  }
}

=== End of Execution ===
```

### Current Test Scenario

**Input:**
- Zone Z1: Severity 5, Requires 8 volunteers
- Zone Z2: Severity 3, Requires 6 volunteers
- Zone Z3: Severity 4, Requires 5 volunteers
- Available: 12 volunteers

**Output:**
- Z1: Allocated 8 (fully satisfied)
- Z2: Allocated 4 (partially satisfied)
- Z3: Allocated 0 (not satisfied)
- Remaining: 0 volunteers

**Allocation Strategy:**
- Currently uses first-come-first-served (order in list)
- Does NOT prioritize by severity (enhancement opportunity)

---

## Extension Points

### Adding New Worker Types

To create a new specialized worker:

1. **Create new file** in `agents/workers/`:
   ```python
   from .worker_base import AbstractWorkerAgent
   
   class MyCustomWorker(AbstractWorkerAgent):
       def process_task(self, task_data: dict) -> dict:
           # Your business logic here
           return results
       
       def send_message(self, recipient: str, message_obj: dict):
           # Communication implementation
           pass
       
       def write_to_ltm(self, key: str, value: Any) -> bool:
           # Persistence implementation
           return True
       
       def read_from_ltm(self, key: str) -> Optional[Any]:
           # Retrieval implementation
           return None
   ```

2. **Register with Supervisor**:
   ```python
   # In supervisor.py
   self.custom_worker = MyCustomWorker("Worker_Custom", self.id)
   ```

3. **Add new task types** to `protocol.py` if needed

### Enhancing Allocation Algorithm

**Priority-Based Allocation:**
```python
# Sort zones by severity (descending) before allocation
sorted_zones = sorted(zones, key=lambda z: z['severity'], reverse=True)
```

**Optimization with PuLP:**
```python
import pulp

# Define linear programming problem
prob = pulp.LpProblem("Volunteer_Allocation", pulp.LpMaximize)
# Add objective function (e.g., maximize severity coverage)
# Add constraints (volunteer limits, zone requirements)
# Solve and extract solution
```

### Adding Communication Channels

**Current:** 
- **HTTP/REST API**: Flask endpoints for supervisor-worker communication ✅ **IMPLEMENTED**
  - `GET /health` - Health check endpoint
  - `POST /invoke` - Supervisor-style task_assignment → completion_report
  - `POST /query` - Natural-language-friendly allocation endpoint
- Console output (print statements) - For worker agent direct usage

**Future Options:**
- **Message Queue**: RabbitMQ or Kafka for async messaging
- **WebSockets**: Real-time bidirectional communication
- **gRPC**: High-performance RPC for distributed deployments

### HTTP API Integration

**Status:** ✅ **IMPLEMENTED**

The worker agent now exposes a Flask-based HTTP API server that implements the supervisor-worker communication protocol over HTTP.

**Endpoints:**

1. **GET /health** - Health check for supervisor monitoring
   - Returns: `{"status": "UP", "agent": "Worker_Disaster", "version": "0.1.0"}`
   - Status Code: 200 on success, 500 on error

2. **POST /invoke** - Supervisor handshake endpoint
   - Accepts: Supervisor-style `task_assignment` message
   - Returns: `completion_report` with allocation results
   - Status Code: 200 on success, 400/500 on error
   - Uses the same `run_allocation()` optimization engine as the worker agent

3. **POST /query** - Natural-language-friendly endpoint
   - Accepts: Natural language query + structured zones/volunteers
   - Returns: Simplified response with allocation plan and metadata
   - Status Code: 200 on success, 400/500 on error
   - Includes `natural_language_query` in response metadata

**Starting the Server:**

```bash
cd AI-Agent-System
python -m api.server
# Server runs on http://0.0.0.0:8000
```

**Example Supervisor Integration:**

The `/invoke` endpoint accepts the standard supervisor-worker message format:

```json
{
  "message_id": "uuid-1",
  "sender": "Supervisor_Main",
  "recipient": "Worker_Disaster",
  "type": "task_assignment",
  "task": {
    "name": "allocate_resources",
    "priority": 1,
    "parameters": {
      "zones": [...],
      "available_volunteers": 12,
      "constraints": {"fairness_weight": 0.6}
    }
  },
  "timestamp": "2025-11-27T12:00:00Z"
}
```

And returns a `completion_report`:

```json
{
  "message_id": "uuid-2",
  "sender": "Worker_Disaster",
  "recipient": "Supervisor_Main",
  "type": "completion_report",
  "related_message_id": "uuid-1",
  "status": "SUCCESS",
  "results": {
    "allocation_plan": [...],
    "remaining_volunteers": 0,
    "optimization_metadata": {...}
  },
  "timestamp": "2025-11-27T12:00:01Z"
}
```

**Architecture:**

The HTTP API uses the same centralized `run_allocation()` function as the worker agent, ensuring consistent optimization behavior across both interfaces. The API layer handles HTTP request/response formatting while delegating all optimization logic to the shared engine.

### Database Integration

**Replace file-based LTM:**
```python
import sqlite3

class DatabaseLTM:
    def write_to_ltm(self, key: str, value: Any) -> bool:
        conn = sqlite3.connect('allocations.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cache VALUES (?, ?)", (key, json.dumps(value)))
        conn.commit()
        conn.close()
        return True
```

### Dashboard Integration

**Planned Streamlit UI:**
- Real-time allocation visualization
- Zone severity heatmap
- Volunteer distribution charts
- Historical allocation trends
- Manual task triggering

---

## Key Insights for AI Models

### Understanding System Behavior

1. **Stateless Workers**: Each worker processes tasks independently
2. **Cached Results**: LTM improves performance but may return stale data
3. **Message Ordering**: Currently synchronous (worker processes before supervisor continues)
4. **Error Isolation**: Worker failures return error messages but don't crash system

### Common Modification Patterns

**To change allocation logic:**
- Modify `DisasterAllocationWorker.process_task()`
- LTM caching automatically works with new logic

**To add logging:**
- Update `Supervisor._log()` or add worker-specific logging
- Use JSONL format for consistency

**To add new message types:**
- Add constant to `protocol.py`
- Update `handle_incoming_message()` in worker base
- Create corresponding handler method

### Testing Strategy

**Unit Tests:**
- Test worker allocation logic with various scenarios
- Verify LTM cache hit/miss behavior
- Validate message serialization/deserialization

**Integration Tests:**
- End-to-end task assignment → processing → reporting
- Multiple task sequences
- Cache persistence across runs

**Performance Tests:**
- Measure cache hit ratio
- Benchmark allocation algorithm with large zone counts
- Stress test with concurrent tasks (future)

---

## Future Roadmap

### Immediate Enhancements
- [ ] Implement severity-based prioritization in allocation
- [ ] Add unit tests for all components
- [ ] Create CLI for dynamic task input
- [ ] Add configuration file for system settings

### Short-Term Features
- [ ] Streamlit dashboard for visualization
- [x] REST API for external integrations ✅ **COMPLETED**
- [ ] Multiple worker support in supervisor
- [ ] Enhanced logging with levels (INFO, WARNING, ERROR)

### Long-Term Goals
- [ ] Distributed system deployment
- [ ] Machine learning for allocation optimization
- [ ] Real-time disaster data integration
- [ ] Geographic visualization with mapping
- [ ] Historical analytics and reporting

---

## Conclusion

This codebase implements a well-structured multi-agent system following software engineering best practices. The modular architecture enables easy extension and maintenance while the message-based protocol ensures clear communication patterns. The LTM system provides performance optimization, and the logging mechanism ensures full auditability.

**Key Strengths:**
- Clear separation of concerns
- Extensible architecture (Abstract base classes)
- Comprehensive documentation
- Type-safe data models
- Performance optimization (LTM caching)
- HTTP API integration for supervisor communication ✅

**Areas for Improvement:**
- Test coverage (unit and integration tests)
- Error handling granularity
- Configuration management
- Production-ready deployment (Docker, load balancing)
- Advanced NLP parsing for /query endpoint

---

**Document Maintenance:**
- Update this document when adding new components
- Document all architectural decisions
- Keep execution examples current
- Maintain changelog for major modifications

**For Questions or Clarifications:**
- Review inline code comments
- Check supervisor logs for runtime behavior
- Examine LTM cache for allocation patterns
- Trace message flow in JSONL logs

---

*End of Documentation*
