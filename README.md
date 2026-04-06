# AI-Agent-for-Disaster-Resource-and-Volunteer-Allocation

<div align="center">

### Disaster Response, But Smarter and Kinder

An AI-inspired multi-agent system that allocates volunteers to disaster zones using optimization, fairness controls, and long-term memory caching.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PuLP](https://img.shields.io/badge/Optimization-PuLP-0A7A0A?style=for-the-badge)
![Status](https://img.shields.io/badge/Project-Active-2ea44f?style=for-the-badge)
![Architecture](https://img.shields.io/badge/Pattern-Supervisor%20%2B%20Worker-ff7f50?style=for-the-badge)

</div>

# AI-Agent-for-Disaster-Resource-and-Volunteer-Allocation

An agent-based disaster response system that allocates volunteers across zones using integer optimization, fairness constraints, and cache-backed long-term memory.

## Overview

This project models a Supervisor-Worker architecture for disaster volunteer allocation.

- The supervisor sends allocation tasks.
- The worker either reuses a cached result or computes a new optimized plan.
- The optimizer solves an integer program with budget, capacity, and resource constraints.
- Fairness can be tuned so lower-priority zones are not entirely ignored.

## Features

- Multi-agent task flow (Supervisor -> Worker)
- Integer programming with PuLP/CBC
- Severity-based objective function
- Capacity and resource coupling constraints
- Configurable fairness weight
- Long-Term Memory cache keyed by input and fairness settings
- Phase-based test suite and benchmark scripts

## Architecture

```text
SupervisorAgent
  -> task_assignment
DisasterAllocationWorker
  -> LTM lookup
     -> cache hit: return cached result
     -> cache miss: run VolunteerAllocator
  -> completion_report
```

## Project Structure

```text
AI-Agent-for-Disaster-Resource-and-Volunteer-Allocation/
|- AI-Agent-System/
|  |- main.py
|  |- agents/
|  |  |- supervisor/supervisor.py
|  |  '- workers/
|  |     |- worker_base.py
|  |     '- disaster_worker.py
|  |- communication/
|  |  |- models.py
|  |  '- protocol.py
|  |- optimization/
|  |  '- volunteer_allocator.py
|  |- datasets/
|  |  '- disaster_scenarios.json
|  |- tests/
|  |  |- test_phase2.py
|  |  |- test_phase3.py
|  |  |- test_phase4.py
|  |  |- test_phase5.py
|  |  |- test_phase6.py
|  |  |- test_phase7.py
|  |  '- benchmark.py
|  '- LTM/
|     '- Worker_Disaster/allocations.json
|- requirements.txt
|- pyproject.toml
'- README.md
```

## Optimization Model

The allocator maximizes severity-weighted impact:

$$
\max \sum_{z} severity_z \cdot x_z
$$

Subject to:

$$
\sum_{z} x_z \le total\_volunteers
$$

$$
x_z \le capacity_z
$$

$$
x_z \cdot min\_resources\_per\_volunteer_z \le resources\_available_z
$$

When fairness is enabled (`fairness_weight > 0`), each zone receives a minimum baseline proportional to severity from a reserved pool.

## Dataset

Primary scenario file:

- `AI-Agent-System/datasets/disaster_scenarios.json`

Expected per-zone fields for full optimization behavior:

- `id`
- `severity`
- `required_volunteers`
- `capacity`
- `resources_available`
- `min_resources_per_volunteer`

## Setup

### 1) Clone

```bash
git clone https://github.com/sahariq/AI-Agent-for-Disaster-Resource-and-Volunteer-Allocation
cd AI-Agent-for-Disaster-Resource-and-Volunteer-Allocation
```

### 2) Create and activate virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

Optional (Poetry):

```bash
poetry install
```

## Usage

Run main system flow:

```bash
cd AI-Agent-System
python main.py
```

## Tests

Run phase tests:

```bash
cd AI-Agent-System/tests
python test_phase2.py
python test_phase3.py
python test_phase4.py
python test_phase5.py
python test_phase6.py
python test_phase7.py
```

Phase coverage:

- Phase 2: base optimization behavior
- Phase 3: capacity constraints
- Phase 4: resource coupling
- Phase 5: fairness behavior across lambda values
- Phase 6: integer variable performance suitability
- Phase 7: worker integration, metadata, and LTM caching

## Benchmark

Compare optimizer vs greedy baseline:

```bash
cd AI-Agent-System/tests
python benchmark.py
```

Reported metrics include:

- solve time
- objective value
- variance/fairness indicators
- allocation comparisons across scenarios

## Configuration

Fairness is configured when constructing the worker:

```python
worker = DisasterAllocationWorker(
    agent_id="Worker_Disaster",
    supervisor_id="Supervisor_Main",
    fairness_weight=0.6
)
```

Common settings:

- `0.0`: pure severity optimization
- `0.3`: light fairness
- `0.6`: balanced fairness/severity
- `1.0+`: stronger minimum guarantees

LTM cache behavior:

- Same task payload + same fairness weight -> cache reuse
- Same task payload + different fairness weight -> recompute

## Troubleshooting

- If imports fail, verify your working directory and virtual environment.
- If optimization fails, confirm PuLP is installed.
- If you need fresh runs, clear `AI-Agent-System/LTM/Worker_Disaster/allocations.json`.
- If `AI-Agent-System/main.py` contains merge markers, resolve them before execution.

## Roadmap

- Add HTTP/message-queue transport between agents
- Add multiple workers and dispatch policies
- Add geospatial and travel-time constraints
- Add explainability reports for allocation decisions

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Add or update tests.
4. Run phase tests and benchmark.
5. Open a pull request with a clear summary.
## Run the System
