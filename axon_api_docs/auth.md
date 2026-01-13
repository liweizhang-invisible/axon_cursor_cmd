Authentication
The Agentic Platform uses Bearer token authentication. Create a token with specific entitlements for your use case.
Create Token Mutation
mutation CreateApiToken {
  createApiToken(input: {
    name: "Client API Token"
    tenant_id: "40eaf721......cd39d8"
    expires_at: "2026-12-31T23:59:59Z"
    entitlements: [execute, read_data, audit]
  }) {
    token
    api_token {
      id
      name
      user_id
      tenant_id
      entitlements
      created_at
      expires_at
      is_active
    }
  }
}
Entitlements Explained
admin: Grants all permissions (automatically includes execute, read_data, write_data, audit)
audit: Includes read_data permissions for auditing purposes
execute: Requires read_data to view flows before execution
write_data: Requires read_data to view existing resources before modification
read_data: Base permission for viewing resources
API Token Response
{
  "data": {
    "createApiToken": {
      "token": "api_abc123...xyz789",
      "api_token": {
        "id": "token_id_12345",
        "name": "Client API Token",
        "user_id": "user_67890",
        "tenant_id": "40eaf721-236a-407e-b0f5-6e09b7cd39d8",
        "entitlements": ["execute", "read_data", "audit"],
        "created_at": "2024-01-15T10:30:00Z",
        "expires_at": "2026-12-31T23:59:59Z",
        "is_active": true
      }
    }
  }
}
