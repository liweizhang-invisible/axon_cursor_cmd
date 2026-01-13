# Trigger Workflow Skill

Triggers/executes a workflow and returns execution information.

## Description

This skill executes a workflow on the Axon Agentic Platform. It handles:
1. Sets up the workflow (finds namespace, workflow definition, version)
2. Executes the workflow with provided inputs
3. Returns execution ID and basic information

**Note:** This skill only starts the workflow. Use `get_workflow_status` to check execution status and retrieve results.

## Usage

### Command Line

```bash
# Basic usage - execute a workflow
python3 -m skills.trigger_workflow.trigger_workflow "WorkflowName"

# With namespace
python3 -m skills.trigger_workflow.trigger_workflow "WorkflowName" --namespace "MyNamespace"

# With input parameters
python3 -m skills.trigger_workflow.trigger_workflow "WorkflowName" --input "param1" "value1" --input "param2" "value2"

# Output as JSON
python3 -m skills.trigger_workflow.trigger_workflow "WorkflowName" --json
```

### Python API

```python
from skills.trigger_workflow.trigger_workflow import trigger_workflow

# Execute workflow
result = trigger_workflow(
    workflow_name="MyWorkflow",
    namespace="MyNamespace",  # Optional, defaults to "default"
    param1="value1",  # Workflow input parameters
    param2="value2"
)

if result["success"]:
    print(f"Execution ID: {result['execution_id']}")
    # Use get_workflow_status to check status
    from skills.get_workflow_status.get_workflow_status import get_workflow_status
    status = get_workflow_status(result['execution_id'], monitor=True)
else:
    print(f"Error: {result['error']}")
```

## Parameters

### Required

- `workflow_name` (str): Name of the workflow to execute

### Optional

- `namespace` (str): Namespace containing the workflow. Defaults to `"default"`.
- `**workflow_inputs`: Additional keyword arguments are treated as workflow input parameters. The parameter names must match the workflow's expected inputs.

### Interactive Parameter Collection

When running from the command line, if the workflow requires input parameters that weren't provided, the skill will **interactively prompt** you for each missing parameter:

```
⚠️  Missing required inputs. Please provide:

Enter position_report_file (File path): /path/to/file.json
   ✓ position_report_file = /path/to/file.json
Enter fund_name (String): My Fund
   ✓ fund_name = My Fund
```

This makes it easy to run workflows without needing to specify all parameters upfront.

## Returns

Dictionary with the following structure:

```python
{
    "success": True,
    "execution_id": "execution_123...",
    "workflow_name": "MyWorkflow",
    "namespace": "default",
    "setup_info": {
        "namespace_id": "...",
        "flow_id": "...",
        "flow_version_id": "...",
        "inputs": [...]
    }
}
```

If workflow start fails:

```python
{
    "success": False,
    "error": "Error message"
}
```

**Note:** To get execution status, token usage, and output files, use `get_workflow_status` with the `execution_id`.

## Output Files

Results are saved to `workflow_execution_result.json` in the project root directory.

## Examples

```bash
# Execute a simple workflow
python3 -m skills.trigger_workflow.trigger_workflow "Hello World"

# Execute with inputs
python3 -m skills.trigger_workflow.trigger_workflow "DataProcessor" \
    --input "input_file" "/path/to/file.json" \
    --input "config" "production"
```

## Checking Execution Status

After triggering a workflow, use `get_workflow_status` to check the execution status:

```python
from skills.get_workflow_status.get_workflow_status import get_workflow_status

# Check status once
status = get_workflow_status(execution_id)

# Monitor until completion
status = get_workflow_status(execution_id, monitor=True)
```

## Error Handling

The skill will:
- Validate workflow exists before execution
- Check required inputs are provided
- Handle network errors gracefully
- Provide detailed error messages for debugging

## Related Skills

- `get_all_workflow` - List available workflows
- `get_workflow_status` - Check workflow execution status

