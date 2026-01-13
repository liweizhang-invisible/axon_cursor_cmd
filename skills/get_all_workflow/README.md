# Get All Workflow Skill

Lists all workflows in specified namespaces.

## Description

This skill queries and lists all workflows available in the specified namespaces. It's useful for discovering what workflows are available before executing them.

**Note:** API tokens can only query namespaces by name (not list all namespaces). You need to know the namespace names to query them.

## Usage

### Command Line

```bash
# List workflows in default namespace
python3 -m skills.get_all_workflow.get_all_workflow

# List workflows in specific namespace(s)
python3 -m skills.get_all_workflow.get_all_workflow --namespace "MyNamespace"
python3 -m skills.get_all_workflow.get_all_workflow --namespace "default" --namespace "AnotherNamespace"

# Include archived workflows
python3 -m skills.get_all_workflow.get_all_workflow --include-archived

# Output as JSON
python3 -m skills.get_all_workflow.get_all_workflow --json
```

### Python API

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
    print(f"Total workflows: {result['total_workflows']}")
    for ns_name, ns_data in result["namespaces"].items():
        print(f"{ns_name}: {len(ns_data['workflows'])} workflows")
        for workflow in ns_data["workflows"]:
            print(f"  - {workflow['name']}")
```

## Parameters

- `namespace_names` (List[str], optional): List of namespace names to query. Defaults to `["default"]`.
- `include_archived` (bool, optional): Whether to include archived workflows. Defaults to `False`.

## Returns

Dictionary with the following structure:

```python
{
    "success": True,
    "total_workflows": 141,
    "namespaces": {
        "default": {
            "namespace_id": "5320e9e9-...",
            "namespace_info": {
                "id": "5320e9e9-...",
                "name": "default"
            },
            "workflows": [
                {
                    "id": "...",
                    "name": "Workflow Name",
                    "description": "...",
                    "created_date": "...",
                    "is_archived": False
                },
                ...
            ]
        }
    }
}
```

## Output Files

Results are saved to `workflows_list.json` in the project root directory.

## Examples

```bash
# Get all workflows in default namespace
python3 -m skills.get_all_workflow.get_all_workflow

# Get workflows from multiple namespaces
python3 -m skills.get_all_workflow.get_all_workflow --namespace "default" --namespace "production"
```

## Error Handling

If a namespace is not found or not accessible, it will be skipped with a warning message. The function will continue processing other namespaces.

## Related Skills

- `trigger_workflow` - Execute a workflow

