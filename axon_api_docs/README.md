# Axon API Documentation

This folder contains API usage documentation for the Axon Agentic Platform that can be searched and referenced later.

## Documentation Files

- **[core_components.md](./core_components.md)** - Core components including GraphQL Client and Workflow Orchestrator
- **[workflow.md](./workflow.md)** - Workflow execution process, including metadata retrieval, file upload, input mapping, and execution
- **[result.md](./result.md)** - Error handling, execution monitoring, polling, and output file retrieval
- **[example.md](./example.md)** - Complete implementation example with configuration and main execution flow

## Quick Reference

### Core Components
- **GraphQLClient**: Handles HTTP communication with the Agentic Platform API
- **AxonOrchestrator**: Manages complete workflow lifecycle from setup through result retrieval

### Workflow Execution Flow
1. Retrieve workflow metadata (namespace, workflow definition, version)
2. Upload files (optional)
3. Map workflow inputs
4. Execute workflow
5. Monitor execution and retrieve results (optional)

### Key API Endpoints
- GraphQL endpoint: `https://prod.agentic.inv.tech/graphql/`
- File upload: `https://prod.agentic.inv.tech/files/upload`
- File download: `https://prod.agentic.inv.tech/files/download`

## Search

All files in this directory are searchable, making it easy to find relevant API usage examples, GraphQL queries, mutations, and implementation patterns.

###### Summary of Key Operations

| Operation                | Purpose                     | Key Details                                              |
|--------------------------|-----------------------------|----------------------------------------------------------|
| Retrieve Tenants         | Get org identifiers         | Lists all accessible organizations                       |
| Create API Token         | Authentication              | Enable execute, read_data, audit permissions              |
| Get Namespace            | Locate workflow             | Organizes related workflows                              |
| Get Workflow             | Find workflow definition    | Non-archived workflows in namespace                      |
| Get Latest Version       | Use current workflow        | Falls back from published to latest                      |
| Get Inputs               | Understand requirements     | Maps expected parameters                                 |
| Generate Upload Token    | Prepare file upload         | Single-use temporary credential                          |
| Upload File              | Store data on platform      | Returns tenant-scoped path reference                     |
| Execute Workflow         | Start processing            | Returns execution ID for tracking                        |
| Monitor Status           | Track progress              | Poll until terminal state reached                        |
| Get Output Files         | List results                | Retrieve artifact file metadata                          |
| Download File            | Get results                 | Requires download token                                  |
