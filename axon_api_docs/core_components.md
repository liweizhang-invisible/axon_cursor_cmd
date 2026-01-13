Core Components

GraphQL Client

The GraphQL client handles all communication with the Agentic Platform API. It abstracts HTTP request handling, header management, and error processing.
class GraphQLClient:
    """
    Simple HTTP GraphQL client for Agentic Platform communication.
    
    Responsibilities:
    - Maintain API connection details and authentication headers
    - Execute GraphQL queries and mutations
    - Handle HTTP errors and GraphQL response errors
    """
    
    def __init__(self, url: str, api_key: str):
        # Store the GraphQL endpoint URL
        self.url = url
        
        # Configure request headers with Bearer token authentication
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    
    def execute(self, query: str, variables: Optional[Dict] = None) -> Dict:
        """
        Execute a GraphQL query or mutation.
        
        Args:
            query: GraphQL query/mutation string
            variables: Optional dictionary of query variables
            
        Returns:
            Dictionary containing 'data' field with query results
            
        Raises:
            Exception: If HTTP or GraphQL errors occur
        """
        # Build the request payload
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        
        # Send HTTP POST request to GraphQL endpoint
        response = requests.post(self.url, json=payload, headers=self.headers)
        
        # Check for HTTP errors (network, auth failures, etc.)
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        
        # Parse JSON response
        result = response.json()
        
        # Check for GraphQL-level errors (query syntax, validation, etc.)
        if "errors" in result:
            raise Exception(f"GraphQL errors: {result['errors']}")
        
        return result


Workflow Orchestrator

The orchestrator manages the complete workflow lifecycle from setup through result retrieval.
class AxonOrchestrator:
    """
    Orchestrates the complete workflow execution lifecycle on the Agentic Platform.
    
    Responsibilities:
    - Manage workflow metadata (namespace, flow ID, version)
    - Upload files to the platform (optional)
    - Execute workflows with proper variable mapping
    - Monitor execution status and retrieve results (optional)
    """
    
    def __init__(self, workflow_name: str, api_key: str, tenant_id: str, 
                 namespace_name: str = "default"):
        """
        Initialize the orchestrator with workflow and tenant information.
        
        Args:
            workflow_name: Name of the workflow to execute
            api_key: Bearer token for API authentication
            tenant_id: Tenant ID from prerequisites
            namespace_name: Namespace containing the workflow
        """
        self.workflow_name = workflow_name
        self.namespace_name = namespace_name
        self.api_key = api_key
        self.tenant_id = tenant_id
        self.client = self._create_client()
        
        # These will be populated during setup
        self.namespace_id = None      # Workflow container ID
        self.flow_id = None           # Workflow definition ID
        self.flow_version_id = None   # Specific workflow version
        self.workflow_inputs = None   # Expected input parameters
        self.execution_id = None      # Current execution ID
    
    def _create_client(self) -> GraphQLClient:
        """Create and return a GraphQL client with production API URL."""
        url = "https://prod.agentic.inv.tech/graphql/"
        return GraphQLClient(url, self.api_key)

