# Supported Commands

This document lists all supported commands for the Axon workflow system. When a user requests to run a command, check this file first.

**Important:** All commands must start with a colon `:` prefix.

## Command: `:get_all_workflow`

**Description:** Lists all workflows in specified namespaces.

**Usage:**
```bash
python3 -m skills.get_all_workflow.get_all_workflow
python3 -m skills.get_all_workflow.get_all_workflow --namespace "MyNamespace"
python3 -m skills.get_all_workflow.get_all_workflow --namespace "default" --namespace "AnotherNamespace"
```

**Python API:**
```python
from skills.get_all_workflow.get_all_workflow import get_all_workflow

# List workflows in default namespace
result = get_all_workflow()

# List workflows in specific namespaces
result = get_all_workflow(
    namespace_names=["default", "MyNamespace"],
    include_archived=False
)

if result["success"]:
    print(f"Found {result['total_workflows']} workflows")
    for ns_name, ns_data in result["namespaces"].items():
        print(f"{ns_name}: {len(ns_data['workflows'])} workflows")
```

**Returns:**
- Dictionary with `success`, `total_workflows`, and `namespaces` keys
- Results saved to `workflows_list.json`

**When to use:**
- `:get_all_workflow`

---

## Command: `:trigger_workflow`

**Description:** Triggers/executes a workflow and returns execution information.

**Usage:**
```bash
# Basic usage
python3 -m skills.trigger_workflow.trigger_workflow "WorkflowName"

# With namespace
python3 -m skills.trigger_workflow.trigger_workflow "WorkflowName" --namespace "MyNamespace"

# With input parameters
python3 -m skills.trigger_workflow.trigger_workflow "WorkflowName" --input "param1" "value1" --input "param2" "value2"
```

**Python API:**
```python
from skills.trigger_workflow.trigger_workflow import trigger_workflow

result = trigger_workflow(
    workflow_name="MyWorkflow",
    namespace="MyNamespace",  # Optional, defaults to "default"
    param1="value1",  # Workflow input parameters
    param2="value2"
)

if result["success"]:
    print(f"Execution ID: {result['execution_id']}")
    # Use get_workflow_status to check status
else:
    print(f"Error: {result['error']}")
```

**Returns:**
- Dictionary with `success`, `execution_id`, `workflow_name`, `namespace`, and `setup_info`
- Results saved to `workflow_execution_result.json`
- **Note:** This command only starts the workflow. Use `:get_workflow_status` to check execution status.

**When to use:**
- `:trigger_workflow`

**Required:**
- `workflow_name`: Name of the workflow to execute

**Optional:**
- `namespace`: Namespace containing the workflow (default: "default")
- Additional keyword arguments: Workflow input parameters

---

## Command: `:get_workflow_status`

**Description:** Retrieves the status of a workflow execution by execution ID.

**Usage:**
```bash
# Check status once
python3 -m skills.get_workflow_status.get_workflow_status "execution-id-here"

# Monitor until completion
python3 -m skills.get_workflow_status.get_workflow_status "execution-id-here" --monitor

# Output as JSON
python3 -m skills.get_workflow_status.get_workflow_status "execution-id-here" --json
```

**Python API:**
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

**Returns:**
- Dictionary with `success`, `execution_id`, `status`, `start_time`, `end_time`, `token_usage`, `steps`, etc.
- Results saved to `workflow_status_result.json`
- Status values: `Running`, `Completed`, `Failed`, `Cancelled`, `Killed`

**When to use:**
- `:get_workflow_status "execution-id"`
- "check workflow status"
- "get workflow status"
- "monitor workflow"

**Required:**
- `flow_execution_id`: The workflow execution ID (returned by `:trigger_workflow`)

**Optional:**
- `monitor`: Whether to poll until completion (default: False)

---

## Command: `:get_workflow_outputs`

**Description:** Retrieves all output files from a workflow execution by execution ID.

**Usage:**
```bash
# List output files (metadata only)
python3 -m skills.get_workflow_outputs.get_workflow_outputs "execution-id-here"

# Download output files (output-dir is required)
python3 -m skills.get_workflow_outputs.get_workflow_outputs "execution-id-here" --download --output-dir "/path/to/save"

# Output as JSON
python3 -m skills.get_workflow_outputs.get_workflow_outputs "execution-id-here" --json
```

**Python API:**
```python
from skills.get_workflow_outputs.get_workflow_outputs import get_workflow_outputs

# List output files (metadata only)
result = get_workflow_outputs(flow_execution_id="execution-id-here")

# Download output files
result = get_workflow_outputs(
    flow_execution_id="execution-id-here",
    download=True,
    output_dir="/path/to/save"  # Required when download=True
)

if result["success"]:
    print(f"Found {result['output_files_count']} output file(s)")
    for file_info in result["output_files"]:
        print(f"  - {file_info['file_name']} ({file_info['file_size_bytes']} bytes)")
else:
    print(f"Error: {result.get('error')}")
```

**Returns:**
- Dictionary with `success`, `execution_id`, `execution_status`, `output_files_count`, `output_files`, etc.
- Results saved to `workflow_outputs_result.json`
- When `--download` is used, files are saved to the directory specified by `--output-dir` (required)

**When to use:**
- `:get_workflow_outputs "execution-id"`
- "get workflow outputs"
- "get workflow results"
- "download workflow files"
- "get output files [execution-id]"

**Required:**
- `flow_execution_id`: The workflow execution ID (returned by `:trigger_workflow`)

**Optional:**
- `download`: Whether to download files locally (default: False)
- `output_dir`: Directory to save downloaded files (required when `download=True`)

---

## Command Recognition

When a user requests an action, check if it matches these patterns:

### `:get_all_workflow` triggers:
- `:get_all_workflow`
- `:get_all_workflow --namespace "MyNamespace"`
- "list workflows"
- "get all workflows"
- "show workflows"
- "list all workflows"
- "get workflows"
- "what workflows are available"

### `:trigger_workflow` triggers:
- `:trigger_workflow "WorkflowName"`
- `:trigger_workflow "WorkflowName" --namespace "MyNamespace"`
- "run workflow"
- "execute workflow"
- "trigger workflow"
- "start workflow"
- "run [workflow name]"
- "execute [workflow name]"
- "trigger [workflow name]"

### `:get_workflow_status` triggers:
- `:get_workflow_status "execution-id"`
- `:get_workflow_status "execution-id" --monitor`
- "check workflow status"
- "get workflow status"
- "monitor workflow"
- "check status [execution-id]"

### `:get_workflow_outputs` triggers:
- `:get_workflow_outputs "execution-id"`
- `:get_workflow_outputs "execution-id" --download`
- "get workflow outputs"
- "get workflow results"
- "download workflow files"
- "get output files [execution-id]"

## Implementation Notes

- All commands use credentials from `.my_axon_data/mydata.json`
- Commands are implemented in the `skills/` directory
- Results are typically saved to JSON files for reference
- Always provide clear feedback to the user about command status

