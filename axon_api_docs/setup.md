Prerequisites & Setup
Before implementing the Agentic Platform integration, ensure you have the following information:
API Endpoint: https://prod.agentic.inv.tech/graphql/
File Upload Service: https://prod.agentic.inv.tech/files/upload
Tenant ID: Unique identifier for your organization’s data partition within the platform. 
Namespace Name/ID: Dedicated workspace used to organize workflows and control access to them (e.g., “YourNamespace”, “default”, “AnotherNamespace”). While you can run workflows in the default namespace, it’s best practice to create separate namespaces for each project or use case.
Query Your Namespaces
To retrieve all namespaces you have access to, run the following query in the GraphQL Playground. When using the playground, you are automatically authenticated through Google SSO.


query {
  userNamespaces {
    id
    name
    everybody_read
    is_archived
    created_at
    created_by {
      id
      email
    }
  }
}
Response Example
{
  "data": {
    "userNamespaces": [
      {
        "id": "3042......ce1fe1f",
        "name": "YourNamespace",
        "everybody_read": false,
        "is_archived": false,
        "created_at": "2024-01-15T10:30:00Z",
        "created_by": {
          "id": "user_123",
          "email": "admin@company.com"
        }
      },
      {
        "id": "50c44890-95ff-5c79-d2h7-8g21i9ef51gh",
        "name": "default",
        "everybody_read": true,
        "is_archived": false,
        "created_at": "2024-01-01T00:00:00Z",
        "created_by": {
          "id": "system",
          "email": "system@agentic.platform"
        }
      }
    ]
  }
}
Look through the list for the namespace you want to use (e.g., "YourNamespace", "AnotherNamespace"). Copy the id field - you'll need it when creating secrets. If your namespace doesn't exist, request a new one in the Axon Support Channel. You can also execute this GraphQL query to list all tenants your account has access to:
query {
  userTenants {
    id
    name
    created_at
  }
}
Response Example:
{
  "data": {
    "userTenants": [
      {
        "id": "40eaf721-236a-407e-b0f5-6e09b7cd39d8",
        "name": "default",
        "created_at": "2024-01-15T10:30:00Z"
      }
    ]
  }
}
Create Secrets (If Required by Workflow)
Some workflows require sensitive credentials or configuration values to execute. These must be created as secrets in the namespace before the workflow can use them. Secrets are encrypted and securely stored on the platform.
Create Secret Mutation
mutation CreateSecret {
  createSecret(input: {
    namespaceId: "3042....e1fe1f",
    name: "PRIVATE_ID",
    secretValue: "27d……de0b3bbb"
  }) {
    name
    namespace {
      id
    }
  }
}
Parameters:
namespaceId: The ID of the namespace where the secret will be stored (obtained from previous step )
name: Human-readable name for the secret (e.g., "PRIVATE_ID", "DATABASE_PASSWORD")
secretValue: The actual secret value - this will be encrypted by Axon when storing in database and you will not be able to retrieve this value afterwards.




Response:
{
  "data": {
    "createSecret": {
      "name": "PRIVATE_ID",
      "namespace": {
        "id": "30425278-73dd-4a57-b934-bbfe5ce1fe1f"
      }
    }
  }
}
