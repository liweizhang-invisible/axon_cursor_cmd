# Get Workflow Status Skill

Retrieves the status of a workflow execution by execution ID.

## Description

This skill queries the current status of a workflow execution. It can perform a single status check or continuously monitor the execution until it reaches a terminal state (Completed, Failed, Cancelled, or Killed).

## Usage

### Command Line

```bash
# Check status once
python3 -m skills.get_workflow_status.get_workflow_status "execution-id-here"

# Monitor until completion
python3 -m skills.get_workflow_status.get_workflow_status "execution-id-here" --monitor

# Output as JSON
python3 -m skills.get_workflow_status.get_workflow_status "execution-id-here" --json
```

### Python API

```python
from skills.get_workflow_status.get_workflow_status import get_workflow_status

# Check status once
result = get_workflow_status(flow_execution_id="execution-id-here")

# Monitor until completion
result = get_workflow_status(
    flow_execution_id="execution-id-here",
    monitor=True
)

if result["success"]:
    print(f"Status: {result['status']}")
    print(f"Token Usage: {result.get('token_usage', 0)}")
else:
    print(f"Error: {result.get('error')}")
```

## Parameters

- `flow_execution_id` (str, required): The workflow execution ID to check
- `monitor` (bool, optional): Whether to poll until completion. Defaults to `False`.

## Returns

Dictionary with the following structure:

```python
{
    "success": True,
    "execution_id": "execution-id-here",
    "status": "Completed",  # or "Running", "Failed", "Cancelled", "Killed"
    "start_time": "2025-01-12T10:30:00Z",
    "end_time": "2025-01-12T10:35:00Z",
    "token_usage": 12345,
    "steps": [
        {
            "id": "step-id",
            "result": "Completed",
            "entity_type": "Agent",
            "failure_reason": None,
            "failure_detail": None
        }
    ],
    "failure_reason": None,  # Only present if status is "Failed"
    "failure_detail": None   # Only present if status is "Failed"
}
```

## Output Files

Results are saved to `workflow_status_result.json` in the project root directory (unless `--json` flag is used).

## Examples

```bash
# Quick status check
python3 -m skills.get_workflow_status.get_workflow_status "abc123-def456-ghi789"

# Monitor workflow until it completes
python3 -m skills.get_workflow_status.get_workflow_status "abc123-def456-ghi789" --monitor
```

## Status Values

- `Running` - Workflow is currently executing
- `Completed` - Workflow finished successfully
- `Failed` - Workflow execution failed
- `Cancelled` - Workflow was cancelled
- `Killed` - Workflow was killed

## Monitoring Mode

When `monitor=True`, the skill will:
- Poll the execution status every 10 seconds
- Display status updates as they change
- Continue until a terminal state is reached
- Show elapsed time and final status

## Related Skills

- `trigger_workflow` - Start a workflow execution (returns execution_id)
- `get_all_workflow` - List available workflows
