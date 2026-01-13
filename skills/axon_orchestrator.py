"""
Workflow orchestrator for Axon Agentic Platform.
Manages complete workflow lifecycle from setup through result retrieval.
"""
import os
import time
import requests
from typing import Dict, List, Optional

from .axon_client import GraphQLClient


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
    
    def get_namespace(self) -> str:
        """Query for the namespace by name."""
        query = """
        query GetNamespace($name: String!) {
            namespace(name: $name) {
                id
                name
            }
        }
        """
        
        variables = {"name": self.namespace_name}
        result = self.client.execute(query, variables)
        namespace = result["data"]["namespace"]
        
        if not namespace:
            raise Exception(f"Namespace '{self.namespace_name}' not found")
        
        self.namespace_id = namespace["id"]
        return self.namespace_id
    
    def get_workflow(self) -> str:
        """Query for the workflow by name within the namespace."""
        query = """
        query GetWorkflow($namespaceId: ID!, $name: String!) {
            flows(namespaceId: $namespaceId, name: $name, archived: false) {
                id
                name
                description
            }
        }
        """
        
        variables = {"namespaceId": self.namespace_id, "name": self.workflow_name}
        result = self.client.execute(query, variables)
        flows = result["data"]["flows"]
        
        if not flows:
            raise Exception(f"Workflow '{self.workflow_name}' not found")
        
        flow = flows[0]
        self.flow_id = flow["id"]
        return self.flow_id
    
    def get_latest_flow_version(self) -> str:
        """
        Retrieve the most recent version of the workflow (published or draft).
        Prioritizes published versions but falls back to draft versions if needed.
        """
        variables = {"flowId": self.flow_id}
        
        # First, try to get the latest version (including drafts)
        # This ensures we can use draft versions when published versions don't exist
        latest_version_query = """
        query GetLatestFlowVersion($flowId: ID!) {
            latestFlowVersion(flowId: $flowId) {
                version_id
                is_draft
                description
            }
        }
        """
        
        try:
            result = self.client.execute(latest_version_query, variables)
            latest_version = result["data"]["latestFlowVersion"]
            
            if latest_version:
                self.flow_version_id = latest_version["version_id"]
                is_draft = latest_version.get("is_draft", False)
                
                if is_draft:
                    print(f"   ⚠️  Using draft version (no published version available)")
                else:
                    print(f"   ✓ Using published version")
                
                return self.flow_version_id
        except Exception as e:
            error_msg = str(e)
            if "errors" in error_msg.lower():
                # Try to extract error details
                pass
            else:
                raise  # Unexpected error, re-raise
        
        # Fallback: Try to get published version specifically
        published_query = """
        query GetLatestPublishedFlowVersion($flowId: ID!) {
            latestPublishedFlow(flowId: $flowId) {
                version_id
                is_draft
                description
            }
        }
        """
        
        try:
            result = self.client.execute(published_query, variables)
            published_version = result["data"]["latestPublishedFlow"]
            
            if published_version:
                self.flow_version_id = published_version["version_id"]
                print(f"   ✓ Using published version")
                return self.flow_version_id
        except Exception:
            # No published version available, which is fine if we already got latest
            pass
        
        # If we still don't have a version, raise an error
        if not self.flow_version_id:
            raise Exception(f"No versions found for workflow {self.flow_id}")
        
        return self.flow_version_id
    
    def get_workflow_inputs(self) -> List[Dict]:
        """Query for the workflow's expected input parameters."""
        query = """
        query GetUnmatchedInputs($flowVersionId: ID!) {
            flowVersionUnmatchedInputs(flowVersionId: $flowVersionId) {
                stepId
                name
                type
                direction
            }
        }
        """
        
        variables = {"flowVersionId": self.flow_version_id}
        result = self.client.execute(query, variables)
        inputs = result["data"]["flowVersionUnmatchedInputs"]
        
        # Filter to only input parameters (exclude outputs)
        return [var for var in inputs if var['direction'] == 'Input']
    
    def setup_workflow(self):
        """Setup workflow by retrieving namespace, workflow, and version."""
        print(f"📋 Setting up workflow: {self.workflow_name}")
        print(f"   Namespace: {self.namespace_name}")
        
        self.get_namespace()
        print(f"   ✓ Namespace ID: {self.namespace_id}")
        
        self.get_workflow()
        print(f"   ✓ Workflow ID: {self.flow_id}")
        
        self.get_latest_flow_version()
        print(f"   ✓ Version ID: {self.flow_version_id}")
        
        self.workflow_inputs = self.get_workflow_inputs()
        print(f"   ✓ Found {len(self.workflow_inputs)} input parameters")
        
        return {
            "namespace_id": self.namespace_id,
            "flow_id": self.flow_id,
            "flow_version_id": self.flow_version_id,
            "inputs": self.workflow_inputs
        }
    
    def generate_upload_token(self, filename: str) -> Dict:
        """
        Request a file upload token from the platform.
        
        Args:
            filename: Name of the file to upload
            
        Returns:
            Dictionary containing token and tenantFile metadata
        """
        mutation = """
        mutation GenerateFileUploadToken($fileName: String!, $tenantId: ID!) {
            fileUploadToken(fileName: $fileName, tenantId: $tenantId) {
                token
                tenantFile {
                    id
                    file_name
                    storage_path
                    upload_status
                }
            }
        }
        """
        
        variables = {"fileName": filename, "tenantId": self.tenant_id}
        result = self.client.execute(mutation, variables)
        upload_response = result["data"]["fileUploadToken"]
        
        return upload_response
    
    def upload_file(self, file_path: str) -> str:
        """
        Upload file binary data to the platform file service.
        
        Args:
            file_path: Local path to the file being uploaded
            
        Returns:
            tenant_filename: Platform path reference for the uploaded file
            Example: "/tenants/40eaf721.../source.json"
        """
        filename = os.path.basename(file_path)
        
        # Generate upload token
        upload_response = self.generate_upload_token(filename)
        upload_token = upload_response["token"]
        tenant_file = upload_response["tenantFile"]
        generated_filename = tenant_file["file_name"]
        
        # File service endpoint
        upload_url = "https://prod.agentic.inv.tech/files/upload"
        
        # Include upload token as URL parameter
        params = {"upload-token": upload_token}
        
        # Determine content type
        content_type = "application/octet-stream"
        if file_path.endswith('.json'):
            content_type = 'application/json'
        elif file_path.endswith('.csv'):
            content_type = 'text/csv'
        elif file_path.endswith('.png') or file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
            content_type = 'image/png' if file_path.endswith('.png') else 'image/jpeg'
        
        # Read and upload the file
        with open(file_path, 'rb') as f:
            files = {'file': (generated_filename, f, content_type)}
            
            response = requests.post(
                upload_url,
                files=files,
                params=params,
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
        
        if response.status_code != 200:
            raise Exception(f"File upload failed: HTTP {response.status_code}: {response.text}")
        
        # Return tenant-scoped path for use in workflow execution
        tenant_filename = f"/tenants/{self.tenant_id}/{filename}"
        return tenant_filename
    
    def build_execution_variables(self, **kwargs) -> List[Dict]:
        """
        Map provided parameters to workflow input parameters.
        
        Args:
            **kwargs: Key-value pairs matching workflow input names
            
        Returns:
            List of FlowExecutionVariableInput objects for the workflow
        """
        if not self.workflow_inputs:
            raise Exception("Workflow inputs not loaded. Call setup_workflow() first.")
        
        flow_variables = []
        
        # Iterate through expected inputs and map to provided data
        for var in self.workflow_inputs:
            var_name = var['name']
            var_type = var['type']
            step_id = var['stepId']
            
            # Check if we have a value for this input
            if var_name in kwargs:
                flow_variables.append({
                    'step_id': step_id,
                    'variable_name': var_name,
                    'variable_type': var_type,
                    'variable_value': kwargs[var_name]
                })
        
        return flow_variables
    
    def execute_workflow(self, **kwargs) -> str:
        """
        Trigger workflow execution on the platform.
        
        Args:
            **kwargs: Input parameters for the workflow
            
        Returns:
            execution_id: Unique identifier for this workflow run
        """
        if not self.flow_id:
            raise Exception("Workflow not set up. Call setup_workflow() first.")
        
        # Build the variable mappings for this execution
        variables = self.build_execution_variables(**kwargs)
        
        if not variables:
            print("⚠️  Warning: No variables provided for workflow execution")
        
        # Check if we're using a draft version
        # We need to check if the version is a draft by querying its status
        is_draft = False
        if self.flow_version_id:
            try:
                version_query = """
                query GetFlowVersion($flowVersionId: ID!) {
                    flowVersion(flowVersionId: $flowVersionId) {
                        version_id
                        is_draft
                    }
                }
                """
                version_result = self.client.execute(version_query, {"flowVersionId": self.flow_version_id})
                version_data = version_result.get("data", {}).get("flowVersion")
                if version_data:
                    is_draft = version_data.get("is_draft", False)
            except Exception:
                # If we can't check, assume it might be a draft and try with published=false
                pass
        
        # Execute workflow - include flowVersionId and published=false for draft versions
        if is_draft and self.flow_version_id:
            # For draft versions, we must specify flowVersionId AND published=false
            mutation = """
            mutation ExecuteWorkflowWithVersion($flowId: ID!, $flowVersionId: ID!, $tenantId: ID!, 
                                    $variables: [FlowExecutionVariableInput], $published: Boolean) {
                executeFlow(flowId: $flowId, flowVersionId: $flowVersionId, tenantId: $tenantId, 
                           variables: $variables, published: $published) {
                    id
                    result
                    flow {
                        id
                        name
                    }
                }
            }
            """
            
            mutation_variables = {
                "flowId": self.flow_id,
                "flowVersionId": self.flow_version_id,
                "tenantId": self.tenant_id,
                "variables": variables,
                "published": False  # Required for draft versions
            }
            print(f"   ℹ️  Executing draft version (flowVersionId + published=false)")
        else:
            # For published versions, use standard execution
            mutation = """
            mutation ExecuteWorkflow($flowId: ID!, $tenantId: ID!, 
                                    $variables: [FlowExecutionVariableInput]) {
                executeFlow(flowId: $flowId, tenantId: $tenantId, 
                           variables: $variables) {
                    id
                    result
                    flow {
                        id
                        name
                    }
                }
            }
            """
            
            mutation_variables = {
                "flowId": self.flow_id,
                "tenantId": self.tenant_id,
                "variables": variables
            }
        
        # Submit execution request
        result = self.client.execute(mutation, mutation_variables)
        execution = result["data"]["executeFlow"]
        
        # Store and return the execution ID
        self.execution_id = execution["id"]
        print(f"🚀 Workflow execution started: {self.execution_id}")
        return self.execution_id
    
    def monitor_execution(self) -> Dict:
        """
        Poll for workflow execution completion.
        
        Returns:
            Dictionary containing final execution status, results, and any errors
        """
        if not self.execution_id:
            raise Exception("No execution ID. Execute workflow first.")
        
        query = """
        query GetExecutionStatus($flowExecutionId: ID!) {
            flowExecutionStatus(flow_execution_id: $flowExecutionId) {
                id
                result
                failure_reason
                failure_detail
                start_time
                end_time
                token_usage
                steps {
                    id
                    result
                    entity_type
                    failure_reason
                    failure_detail
                }
            }
        }
        """
        
        # Terminal states where polling should stop
        terminal_states = ['Completed', 'Failed', 'Cancelled', 'Killed']
        start_time = time.time()
        last_status = None
        
        while True:
            try:
                variables = {"flowExecutionId": self.execution_id}
                result = self.client.execute(query, variables)
                
                # Validate response structure
                if not result or "data" not in result:
                    raise Exception(f"Invalid API response: {result}")
                
                status = result["data"]["flowExecutionStatus"]
                
                # Handle null status responses
                if status is None:
                    raise Exception(f"Execution status not found for ID: {self.execution_id}")
                
                # Extract current execution state
                current_status = status.get("result")
                
                if not current_status:
                    raise Exception(f"No result status in execution response")
                
                current_time = time.time()
                
                # Log status changes
                if current_status != last_status:
                    elapsed = current_time - start_time
                    print(f"   Status: {current_status} (elapsed: {elapsed:.1f}s)")
                    last_status = current_status
                
                # Check for terminal state
                if current_status in terminal_states:
                    elapsed = current_time - start_time
                    print(f"   🏁 Final status: {current_status} (took {elapsed:.1f}s)")
                    
                    if current_status == "Completed":
                        print(f"   Token Usage: {status.get('token_usage', 0)} tokens")
                    elif current_status == "Failed":
                        print(f"   ❌ Failure: {status.get('failure_reason', 'Unknown')}")
                        
                        # Log individual step failures for debugging
                        failed_steps = [s for s in status.get('steps', []) 
                                       if s.get('result') == 'Failed']
                        if failed_steps:
                            print(f"   Failed Steps: {len(failed_steps)} of {len(status.get('steps', []))}")
                            for i, step in enumerate(failed_steps, 1):
                                print(f"     Step {i} ({step.get('entity_type', 'Unknown')}):")
                                if step.get('failure_reason'):
                                    print(f"       Reason: {step['failure_reason']}")
                    
                    return status
                
                # Wait before next poll
                time.sleep(10)
                
            except KeyError as e:
                print(f"   ⚠️  Missing key in response: {e}, retrying...")
                time.sleep(2)
            except Exception as e:
                print(f"   ⚠️  Error during monitoring: {e}, retrying...")
                time.sleep(2)
    
    def get_output_files(self) -> List[Dict]:
        """Query for files created during workflow execution."""
        if not self.execution_id:
            raise Exception("No execution ID. Execute workflow first.")
        
        query = """
        query GetExecutionWithFiles($flow_execution_id: ID!) {
            flowExecutionStatus(flow_execution_id: $flow_execution_id) {
                id
                result
                steps {
                    id
                    entity_type
                    result
                    file_access_logs {
                        id
                        file_name
                        file_path
                        storage_path
                        operation
                        timestamp
                        file_size_bytes
                        artifact
                    }
                }
            }
        }
        """
        
        variables = {"flow_execution_id": self.execution_id}
        result = self.client.execute(query, variables)
        status = result["data"]["flowExecutionStatus"]
        
        all_files = []
        
        # Collect artifact files from all execution steps
        for step in status.get("steps", []):
            for file_log in step.get("file_access_logs", []):
                # Only include files that were created/modified and marked as artifacts
                if file_log["operation"] in ["create", "write", "modify"] and file_log.get("artifact", False):
                    all_files.append({
                        "file_name": file_log["file_name"],
                        "file_path": file_log["file_path"],
                        "storage_path": file_log["storage_path"],
                        "operation": file_log["operation"],
                        "timestamp": file_log["timestamp"],
                        "file_size_bytes": file_log.get("file_size_bytes", 0),
                        "step_id": step["id"],
                        "entity_type": step["entity_type"]
                    })
        
        # Filter out log files
        output_files = [f for f in all_files if not f["file_name"].endswith(".log")]
        
        return output_files
    
    def download_file(self, file_name: str, storage_path: str) -> str:
        """Download the content of an output file from platform storage."""
        # Step 1: Get download authorization token
        token_mutation = """
        mutation GetDownloadToken($path: String!) {
            getFileDownloadTokenByPath(path: $path)
        }
        """
        
        variables = {"path": storage_path}
        result = self.client.execute(token_mutation, variables)
        download_token = result["data"]["getFileDownloadTokenByPath"]
        
        if not download_token:
            raise Exception(f"Failed to get download token for: {file_name}")
        
        # Step 2: Download file using token
        base_url = self.client.url.replace('/graphql/', '/').replace('/graphql', '/')
        download_url = f"{base_url}files/download?file_name={file_name}&download-token={download_token}"
        
        response = requests.get(download_url, headers=self.client.headers)
        
        if response.status_code == 200:
            content = response.text
            return content
        else:
            raise Exception(f"Download failed: HTTP {response.status_code}")

