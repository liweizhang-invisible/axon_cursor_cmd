# Get Workflow Outputs Skill

Retrieves all output files from a workflow execution by execution ID.

## Description

This skill queries and retrieves all output files (artifacts) created during a workflow execution. It can optionally download the files to your local filesystem.

## Usage

### Command Line

```bash
# List output files (metadata only)
python3 -m skills.get_workflow_outputs.get_workflow_outputs "execution-id-here"

# Download output files (output-dir is required)
python3 -m skills.get_workflow_outputs.get_workflow_outputs "execution-id-here" --download --output-dir "/path/to/save"

# Output as JSON
python3 -m skills.get_workflow_outputs.get_workflow_outputs "execution-id-here" --json
```

### Python API

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
    
    if result.get("downloaded_files"):
        print("Downloaded files:")
        for file_info in result["downloaded_files"]:
            if "local_path" in file_info:
                print(f"  - {file_info['local_path']}")
else:
    print(f"Error: {result.get('error')}")
```

## Parameters

- `flow_execution_id` (str, required): The workflow execution ID
- `download` (bool, optional): Whether to download files locally. Defaults to `False`.
- `output_dir` (str, required when `download=True`): Directory to save downloaded files. Must be provided when downloading.

## Returns

Dictionary with the following structure:

```python
{
    "success": True,
    "execution_id": "execution-id-here",
    "execution_status": "Completed",
    "output_files_count": 2,
    "output_files": [
        {
            "file_name": "result.json",
            "file_path": "/tenants/.../result.json",
            "storage_path": "/storage/...",
            "operation": "create",
            "timestamp": "2026-01-12T21:09:10Z",
            "file_size_bytes": 1024,
            "step_id": "step-id",
            "entity_type": "Agent"
        },
        ...
    ],
    "download_dir": "/path/to/downloads",  # Only if download=True
    "downloaded_files": [  # Only if download=True
        {
            "file_name": "result.json",
            "local_path": "/path/to/downloads/result.json",
            "size_bytes": 1024
        },
        ...
    ]
}
```

## Output Files

Results are saved to `workflow_outputs_result.json` in the project root directory (unless `--json` flag is used).

When `--download` is used, files are saved to the directory specified by `--output-dir` (required).

## Examples

```bash
# List output files from a completed workflow
python3 -m skills.get_workflow_outputs.get_workflow_outputs "abc123-def456-ghi789"

# Download all output files to a directory
python3 -m skills.get_workflow_outputs.get_workflow_outputs "abc123-def456-ghi789" --download --output-dir "./results"
```

## File Filtering

The skill automatically:
- Only includes files marked as artifacts
- Filters out log files (`.log` extension)
- Only includes files with operations: `create`, `write`, or `modify`

## Related Skills

- `trigger_workflow` - Start a workflow execution (returns execution_id)
- `get_workflow_status` - Check workflow execution status
