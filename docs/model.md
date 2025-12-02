# Mathematical Formulation: Volunteer Allocation Optimization Model

## Overview

This document provides the complete mathematical formulation of the Integer Linear Programming (ILP) model used for optimal volunteer allocation across disaster zones.

**Model Type:** Integer Linear Programming (ILP)  
**Solver:** CBC (COIN-OR Branch and Cut)  
**Implementation:** PuLP Python library

---

## Table of Contents

1. [Problem Definition](#problem-definition)
2. [Mathematical Notation](#mathematical-notation)
3. [Decision Variables](#decision-variables)
4. [Objective Function](#objective-function)
5. [Constraints](#constraints)
6. [Fairness Mechanism](#fairness-mechanism)
7. [Complete Model Formulation](#complete-model-formulation)
8. [Computational Complexity](#computational-complexity)
9. [Example](#example)

---

## Problem Definition

Given a set of disaster zones with varying severity levels and a limited pool of volunteers, allocate volunteers to maximize the overall severity-weighted impact while ensuring:
- No zone exceeds its capacity
- Resource availability constraints are satisfied
- Fair distribution ensures no zone is completely neglected (configurable)

---

## Mathematical Notation

### Sets and Indices

| Symbol | Description |
|--------|-------------|
| $Z$ | Set of disaster zones, indexed by $i$ |
| $\|Z\|$ | Number of disaster zones (typically 4-50) |

### Parameters

| Symbol | Description | Units | Typical Range |
|--------|-------------|-------|---------------|
| $s_i$ | Severity level of zone $i$ | 1-10 scale | [1, 10] |
| $c_i$ | Maximum capacity of zone $i$ | volunteers | [10, 50] |
| $V$ | Total available volunteers | volunteers | [20, 500] |
| $r_i$ | Resources available in zone $i$ | units | [50, 200] |
| $\rho_i$ | Minimum resources per volunteer in zone $i$ | units/volunteer | [2, 5] |
| $\lambda$ | Fairness weight parameter | dimensionless | [0, 1] |

### Decision Variables

| Symbol | Description | Type | Domain |
|--------|-------------|------|--------|
| $x_i$ | Number of volunteers allocated to zone $i$ | Integer | $[0, c_i]$ |

---

## Decision Variables

The model uses a single type of decision variable:

$$
x_i \in \mathbb{Z}^+ \quad \forall i \in Z
$$

where:
- $x_i$ represents the number of volunteers assigned to zone $i$
- Integer constraint ensures realistic allocations (cannot split people)
- Non-negativity ensures no negative allocations

---

## Objective Function

The model **maximizes** the severity-weighted total impact:

$$
\max \quad z = \sum_{i \in Z} s_i \cdot x_i
$$

**Interpretation:**
- Each volunteer allocated to zone $i$ contributes $s_i$ units to the objective
- High-severity zones contribute more to the objective per volunteer
- Pure severity optimization when $\lambda = 0$

**Example:**
- Zone with severity 10: each volunteer contributes 10 to objective
- Zone with severity 3: each volunteer contributes 3 to objective
- Allocating 5 volunteers to severity-10 zone: contributes $10 \times 5 = 50$ to objective

---

## Constraints

### 1. Budget Constraint

Total volunteers allocated cannot exceed available volunteers:

$$
\sum_{i \in Z} x_i \leq V
$$

**Purpose:** Ensures we don't over-allocate beyond the volunteer pool.

**Example:** If $V = 40$, then $\sum x_i \leq 40$.

---

### 2. Capacity Constraints

Each zone has a maximum capacity it can handle:

$$
x_i \leq c_i \quad \forall i \in Z
$$

**Purpose:** 
- Physical infrastructure limits
- Coordination capacity limits
- Safety considerations

**Example:** Zone with capacity 20 cannot receive more than 20 volunteers.

---

### 3. Resource Coupling Constraints

Volunteers require minimum resources (equipment, supplies) to be effective:

$$
\rho_i \cdot x_i \leq r_i \quad \forall i \in Z
$$

**Purpose:**
- Ensures sufficient equipment for allocated volunteers
- Prevents allocating volunteers without adequate supplies
- Couples volunteer allocation with resource availability

**Example:**
- Zone has 60 units of resources available ($r_i = 60$)
- Each volunteer needs 5 units ($\rho_i = 5$)
- Maximum volunteers: $x_i \leq \frac{60}{5} = 12$

**Reformulation for LP:**
$$
x_i \leq \left\lfloor \frac{r_i}{\rho_i} \right\rfloor \quad \forall i \in Z
$$

---

### 4. Fairness Constraints (Optional, if $\lambda > 0$)

Ensures each zone receives a minimum baseline allocation proportional to its severity:

$$
x_i \geq \left( \frac{s_i}{\sum_{j \in Z} s_j} \right) \cdot (\lambda \cdot V) \quad \forall i \in Z
$$

**Purpose:**
- Prevents complete neglect of low-severity zones
- Guarantees minimum help to all affected areas
- Controlled by fairness parameter $\lambda \in [0, 1]$

**Interpretation of $\lambda$:**
- $\lambda = 0$: Pure severity optimization, no fairness constraints
- $\lambda = 0.6$: **Recommended** - reserves 60% of volunteers for proportional minimums
- $\lambda = 1.0$: Reserves 100% for proportional allocation (maximum fairness)

**Example:**
- Total volunteers: $V = 40$
- Fairness weight: $\lambda = 0.6$
- Reserved for minimums: $0.6 \times 40 = 24$ volunteers
- Zone $i$ severity: $s_i = 5$
- Total severity: $\sum s_j = 25$
- Minimum for zone $i$: $x_i \geq \frac{5}{25} \times 24 = 4.8$ (rounded to 5 in practice)

---

## Fairness Mechanism

### Design Rationale

The fairness mechanism addresses a critical challenge in disaster resource allocation: **ensuring all affected zones receive help while prioritizing severe cases**.

### Mathematical Formulation

The fairness constraint guarantees proportional minimum allocations:

$$
\text{min}_i = \left( \frac{s_i}{\sum_{j \in Z} s_j} \right) \cdot (\lambda \cdot V)
$$

### Proportional Allocation Table

For $V = 40$, $\lambda = 0.6$, with severities $[10, 7, 5, 3]$ (total = 25):

| Zone | Severity $s_i$ | Proportion | Min Allocation | Remaining Capacity |
|------|----------------|------------|----------------|--------------------|
| Z1   | 10             | 40%        | 9.6 ≈ 10       | 10 more available  |
| Z2   | 7              | 28%        | 6.7 ≈ 7        | 8 more available   |
| Z3   | 5              | 20%        | 4.8 ≈ 5        | 7 more available   |
| Z4   | 3              | 12%        | 2.9 ≈ 3        | 7 more available   |
| **Total** | **25**    | **100%**   | **24**         | **16 to optimize** |

### Trade-off Analysis

| $\lambda$ | Behavior | Variance | Zones with 0 | Use Case |
|-----------|----------|----------|--------------|----------|
| 0.0       | Pure severity | ~62 | Some zones | Emergency triage |
| 0.3       | Slight fairness | ~59 | Rare | Balanced approach |
| **0.6**   | **Recommended** | **~44** | **None** | **Production** |
| 1.0       | Maximum fairness | ~19 | None | Equity priority |

### Fairness vs Objective Trade-off

Benchmark results show:
- **Objective decrease:** ~4% average (acceptable cost)
- **Variance reduction:** ~29% average (significant improvement)
- **Critical benefit:** No zones receive zero allocation

$$
\text{Trade-off Ratio} = \frac{\Delta \text{Variance}}{\Delta \text{Objective}} = \frac{+29\%}{-4\%} \approx 7.25
$$

**Interpretation:** For every 1% decrease in objective, we gain ~7% improvement in fairness.

---

## Complete Model Formulation

### Integer Linear Program

$$
\begin{align}
\max \quad & z = \sum_{i \in Z} s_i \cdot x_i \\
\text{subject to:} \quad & \sum_{i \in Z} x_i \leq V && \text{(Budget)} \\
& x_i \leq c_i && \forall i \in Z \quad \text{(Capacity)} \\
& x_i \leq \left\lfloor \frac{r_i}{\rho_i} \right\rfloor && \forall i \in Z \quad \text{(Resources)} \\
& x_i \geq \left( \frac{s_i}{\sum_{j \in Z} s_j} \right) \cdot (\lambda \cdot V) && \forall i \in Z, \lambda > 0 \quad \text{(Fairness)} \\
& x_i \in \mathbb{Z}^+ && \forall i \in Z \quad \text{(Integrality)}
\end{align}
$$

### Model Characteristics

| Characteristic | Value |
|----------------|-------|
| **Type** | Integer Linear Program (ILP) |
| **Variables** | $\|Z\|$ integer variables |
| **Constraints** | $1 + 3\|Z\|$ (or $1 + 4\|Z\|$ with fairness) |
| **Objective** | Linear (severity-weighted sum) |
| **Feasibility** | Always feasible if $V \geq \|Z\|$ |

---

## Computational Complexity

### Theoretical Complexity

- **LP Relaxation:** $O(n^3)$ using simplex or interior-point methods
- **ILP (Branch & Bound):** $O(2^n)$ worst case, but highly dependent on problem structure

### Practical Performance

From Phase 6 benchmarking:

| Problem Size | Zones | Volunteers | Solve Time | Real-time? |
|--------------|-------|------------|------------|------------|
| Small        | 4     | 40         | 0.017s     | ✅ Yes     |
| Medium       | 10    | 100        | 0.034s     | ✅ Yes     |
| Large        | 50    | 500        | 0.038s     | ✅ Yes     |

**Key Insight:** Despite exponential worst-case complexity, the tight constraints (capacity, resources) create a small feasible region, allowing the solver to find optimal solutions quickly.

### Scalability Limits

- **Practical limit:** ~100 zones (sub-second solve time)
- **Theoretical limit:** ~1000 zones (may exceed real-time threshold)
- **Recommendation:** For 100+ zones, consider hierarchical decomposition

---

## Example

### Problem Instance

**Given:**
- 4 disaster zones: $Z = \{Z_1, Z_2, Z_3, Z_4\}$
- Total volunteers: $V = 40$
- Fairness weight: $\lambda = 0.6$ (recommended)

**Zone Data:**

| Zone | Severity $s_i$ | Capacity $c_i$ | Resources $r_i$ | Min Resources $\rho_i$ |
|------|----------------|----------------|-----------------|------------------------|
| Z1   | 10             | 20             | 100             | 3                      |
| Z2   | 7              | 15             | 80              | 4                      |
| Z3   | 5              | 12             | 60              | 5                      |
| Z4   | 3              | 10             | 50              | 3                      |

### Constraint Calculations

**Resource Limits:**
- Zone Z1: $x_1 \leq \lfloor 100/3 \rfloor = 33$ (but capacity limits to 20)
- Zone Z2: $x_2 \leq \lfloor 80/4 \rfloor = 20$ (but capacity limits to 15)
- Zone Z3: $x_3 \leq \lfloor 60/5 \rfloor = 12$ ✓
- Zone Z4: $x_4 \leq \lfloor 50/3 \rfloor = 16$ (but capacity limits to 10)

**Fairness Minimums** ($\lambda = 0.6$, reserved = 24):
- Total severity: $10 + 7 + 5 + 3 = 25$
- Zone Z1: $x_1 \geq (10/25) \times 24 = 9.6 \approx 10$
- Zone Z2: $x_2 \geq (7/25) \times 24 = 6.7 \approx 7$
- Zone Z3: $x_3 \geq (5/25) \times 24 = 4.8 \approx 5$
- Zone Z4: $x_4 \geq (3/25) \times 24 = 2.9 \approx 3$

### Solution Comparison

#### Pure Severity ($\lambda = 0$)

| Zone | Allocation | Objective Contribution | Total Allocated |
|------|------------|------------------------|-----------------|
| Z1   | 20         | $10 \times 20 = 200$   | 20              |
| Z2   | 15         | $7 \times 15 = 105$    | 35              |
| Z3   | 5          | $5 \times 5 = 25$      | 40              |
| Z4   | 0          | $3 \times 0 = 0$       | 40              |

- **Objective:** $z = 330$
- **Variance:** $62.5$
- **Problem:** Z4 receives no help

#### With Fairness ($\lambda = 0.6$)

| Zone | Allocation | Objective Contribution | Total Allocated |
|------|------------|------------------------|-----------------|
| Z1   | 20         | $10 \times 20 = 200$   | 20              |
| Z2   | 12         | $7 \times 12 = 84$     | 32              |
| Z3   | 5          | $5 \times 5 = 25$      | 37              |
| Z4   | 3          | $3 \times 3 = 9$       | 40              |

- **Objective:** $z = 318$ (3.6% lower)
- **Variance:** $44.5$ (28.8% better)
- **Benefit:** All zones receive help

### Trade-off Analysis

$$
\text{Objective Cost} = \frac{330 - 318}{330} = 3.6\%
$$

$$
\text{Fairness Gain} = \frac{62.5 - 44.5}{62.5} = 28.8\%
$$

$$
\text{Efficiency Ratio} = \frac{28.8\%}{3.6\%} = 8.0
$$

**Interpretation:** For a 3.6% reduction in objective, we achieve an 8× improvement in fairness metrics.

---

## Model Variants

### Variant 1: Pure Severity Optimization ($\lambda = 0$)

Removes fairness constraints for maximum objective value:

$$
\begin{align}
\max \quad & z = \sum_{i \in Z} s_i \cdot x_i \\
\text{subject to:} \quad & \sum_{i \in Z} x_i \leq V \\
& x_i \leq c_i && \forall i \in Z \\
& x_i \leq \left\lfloor \frac{r_i}{\rho_i} \right\rfloor && \forall i \in Z \\
& x_i \in \mathbb{Z}^+ && \forall i \in Z
\end{align}
$$

**Use Case:** Emergency triage when resources critically limited.

### Variant 2: Equal Distribution

Forces equal allocation to all zones (ignoring severity):

$$
x_i = \left\lfloor \frac{V}{|Z|} \right\rfloor \quad \forall i \in Z
$$

**Use Case:** Political equity requirements (not recommended for disaster response).

### Variant 3: Lexicographic Optimization

Two-stage optimization:
1. Maximize total severity impact
2. Among optimal solutions, minimize variance

Not implemented due to computational complexity and unclear benefit over single-objective approach.

---

## Implementation Notes

### Solver Configuration

```python
# PuLP solver settings
prob.solve(PULP_CBC_CMD(msg=0, timeLimit=60))
```

**Parameters:**
- `msg=0`: Suppresses solver output
- `timeLimit=60`: 60-second timeout (never reached in practice)

### Numerical Stability

- All coefficients are integers (severities, capacities)
- No floating-point precision issues
- Integer variables avoid rounding errors

### Feasibility Guarantee

The model is always feasible if:
$$
V \geq \sum_{i \in Z} \text{min}_i
$$

where $\text{min}_i$ is the fairness minimum for zone $i$.

**Infeasibility handling:** If fairness minimums exceed total volunteers, the solver will report infeasibility. In practice, set $\lambda$ such that:

$$
\lambda \leq \frac{V}{\sum_{i \in Z} c_i}
$$

---

## References

1. **Integer Programming Theory:**
   - Wolsey, L. A. (1998). *Integer Programming*. Wiley.
   
2. **Disaster Resource Allocation:**
   - Altay, N., & Green, W. G. (2006). OR/MS research in disaster operations management. *European Journal of Operational Research*, 175(1), 475-493.
   
3. **Fairness in Optimization:**
   - Bertsimas, D., Farias, V. F., & Trichakis, N. (2011). The price of fairness. *Operations Research*, 59(1), 17-31.

4. **PuLP Library:**
   - Mitchell, S., O'Sullivan, M., & Dunning, I. (2011). PuLP: A linear programming toolkit for Python. *The University of Auckland*.

---

## Appendix: Notation Summary

### Quick Reference Table

| Symbol | Description | Type |
|--------|-------------|------|
| $Z$ | Set of zones | Set |
| $i, j$ | Zone indices | Index |
| $s_i$ | Severity | Parameter |
| $c_i$ | Capacity | Parameter |
| $V$ | Total volunteers | Parameter |
| $r_i$ | Resources | Parameter |
| $\rho_i$ | Min resources/volunteer | Parameter |
| $\lambda$ | Fairness weight | Parameter |
| $x_i$ | Volunteers allocated | Decision Variable |
| $z$ | Objective value | Objective |

---

**Document Version:** 1.0  
**Last Updated:** November 14, 2025  
**Model Version:** 0.2.0 (with simplified fairness)
