# Refactoring: Centralized Allocation Logic

## Summary

The resource allocation logic has been centralized into a single reusable function `run_allocation()` that can be used by both:
- The `DisasterAllocationWorker` (existing)
- Future HTTP API servers (new)

## Changes Made

### 1. New Function: `run_allocation()`

**Location**: `AI-Agent-System/optimization/volunteer_allocator.py`

**Signature**:
```python
def run_allocation(
    zones: List[Dict],
    available_volunteers: int,
    *,
    fairness_weight: float = 0.6,
    extra_constraints: Optional[Dict] = None
) -> Tuple[List[Dict], Dict]:
```

**Returns**:
- `allocation_plan`: List of per-zone allocation dictionaries
- `metadata`: Dictionary with optimization metadata (objective_value, fairness_metrics, etc.)

### 2. Refactored `VolunteerAllocator.allocate()`

The class method now internally calls `run_allocation()` to avoid code duplication while maintaining backward compatibility.

**Before**: All logic was in `allocate()` method
**After**: `allocate()` wraps `run_allocation()` and formats the result

### 3. Updated Module Exports

**Location**: `AI-Agent-System/optimization/__init__.py`

Now exports both:
- `VolunteerAllocator` (class-based interface)
- `run_allocation` (function-based interface)

## Benefits

1. **Reusability**: Same logic can be used by worker and HTTP API
2. **No Code Duplication**: Single source of truth for allocation logic
3. **Backward Compatibility**: Existing worker code continues to work
4. **Extensibility**: `extra_constraints` parameter reserved for future enhancements
5. **Clean API**: Function signature is simple and clear

## Usage Examples

### For Worker Agent (Existing)
```python
from optimization.volunteer_allocator import VolunteerAllocator

optimizer = VolunteerAllocator(fairness_weight=0.6)
result = optimizer.allocate(zones, available_volunteers)
# Works exactly as before
```

### For HTTP API (New)
```python
from optimization import run_allocation

allocation_plan, metadata = run_allocation(
    zones=zones,
    available_volunteers=available_volunteers,
    fairness_weight=0.6
)
# Clean, simple interface
```

## Testing

- ✅ Existing worker tests pass
- ✅ New function works correctly
- ✅ Backward compatibility maintained
- ✅ No mathematical model changes

## Files Modified

1. `AI-Agent-System/optimization/volunteer_allocator.py`
   - Added `run_allocation()` function
   - Refactored `VolunteerAllocator.allocate()` to use it

2. `AI-Agent-System/optimization/__init__.py`
   - Added `run_allocation` to exports

3. `AI-Agent-System/optimization/example_usage.py` (new)
   - Example demonstrating direct function usage

## Next Steps

When building the HTTP API server, you can now use:

```python
from optimization import run_allocation

@app.post("/api/allocate")
def allocate_endpoint(request: AllocationRequest):
    allocation_plan, metadata = run_allocation(
        zones=request.zones,
        available_volunteers=request.available_volunteers,
        fairness_weight=request.fairness_weight or 0.6
    )
    return {
        "allocation_plan": allocation_plan,
        "metadata": metadata
    }
```

