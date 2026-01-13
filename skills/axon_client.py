"""
GraphQL client for Axon Agentic Platform API communication.
"""
import requests
from typing import Dict, Optional


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

