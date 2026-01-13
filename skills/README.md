# Axon Workflow Skills

This directory contains skills for interacting with the Axon Agentic Platform. Each skill is self-contained with its own script and README.

## Skills

### [`get_all_workflow`](./get_all_workflow/)

Lists all workflows in specified namespaces.

**Quick Start:**
```bash
python3 -m skills.get_all_workflow.get_all_workflow
```

[Read full documentation →](./get_all_workflow/README.md)

---

### [`trigger_workflow`](./trigger_workflow/)

Triggers/executes a workflow and retrieves results.

**Quick Start:**
```bash
python3 -m skills.trigger_workflow.trigger_workflow "WorkflowName"
```

[Read full documentation →](./trigger_workflow/README.md)

---

## Shared Components

These modules are shared across all skills:

- **`axon_client.py`** - GraphQL client for API communication
- **`axon_orchestrator.py`** - Workflow orchestrator for managing workflow lifecycle
- **`credentials.py`** - Credentials management utility

## Credentials

All skills load credentials from `.my_axon_data/mydata.json` which should contain the response from the `createApiToken` mutation:

```json
{
  "data": {
    "createApiToken": {
      "token": "api_...",
      "api_token": {
        "tenant_id": "...",
        ...
      }
    }
  }
}
```

The `tenant_id` is automatically extracted from the `api_token` object in the response.

## Command Reference

See [`command.md`](../command.md) for the complete command reference and usage patterns.

## Project Structure

```
skills/
├── __init__.py
├── README.md (this file)
├── axon_client.py          # Shared: GraphQL client
├── axon_orchestrator.py    # Shared: Workflow orchestrator
├── credentials.py          # Shared: Credentials loader
├── get_all_workflow/
│   ├── __init__.py
│   ├── get_all_workflow.py
│   └── README.md
└── trigger_workflow/
    ├── __init__.py
    ├── trigger_workflow.py
    └── README.md
```

## Adding New Skills

To add a new skill:

1. Create a new directory: `skills/your_skill_name/`
2. Add `__init__.py` and `your_skill_name.py`
3. Create `README.md` with documentation
4. Update this README and `command.md` with the new skill

## Examples

See individual skill READMEs for detailed examples and usage patterns.
