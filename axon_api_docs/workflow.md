Workflow Execution Process

The workflow execution follows these key stages. Note that file upload and download operations are optional - workflows can execute with parameters passed directly.

Step 1: Retrieve Workflow Metadata
Before executing a workflow, the system must locate and validate the workflow definition.

Get Namespace
def get_namespace(self) -> str:
    """
    Query for the namespace by name.
    
    The namespace is a container that organizes related workflows.
    Multiple workflows can exist within a single namespace.
    
    Returns:
        namespace_id: Unique identifier for the namespace
    """
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

Get Workflow Definition
def get_workflow(self) -> str:
    """
    Query for the workflow by name within the namespace.
    
    Workflows are identified by name within their namespace.
    Multiple versions of a workflow can exist; we retrieve the definition ID.
    
    Returns:
        flow_id: Unique identifier for the workflow definition
    """
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

Get Latest Workflow Version
def get_latest_flow_version(self) -> str:
    """
    Retrieve the most recent published version of the workflow.
    
    Workflows have versions to support iterative development and testing.
    This retrieves the latest published version for execution.
    Falls back to latest version including drafts if no published version exists.
    
    Returns:
        flow_version_id: Version identifier for the workflow
    """
    query = """
    query GetLatestPublishedFlowVersion($flowId: ID!) {
        latestPublishedFlow(flowId: $flowId) {
            version_id
            is_draft
            description
        }
    }
    """
    
    variables = {"flowId": self.flow_id}
    result = self.client.execute(query, variables)
    latest_version = result["data"]["latestPublishedFlow"]
    
    # Fallback mechanism for workflows without published versions
    if not latest_version:
        fallback_query = """
        query GetLatestFlowVersion($flowId: ID!) {
            latestFlowVersion(flowId: $flowId) {
                version_id
                is_draft
                description
            }
        }
        """
        fallback_result = self.client.execute(fallback_query, variables)
        latest_version = fallback_result["data"]["latestFlowVersion"]
        
        if not latest_version:
            raise Exception(f"No versions found for workflow {self.flow_id}")
    
    self.flow_version_id = latest_version["version_id"]
    return self.flow_version_id

Step 2: Upload Files (Optional)

File upload is optional. Use the upload API if you need to transfer files to the platform. Files must be uploaded to the platform's file storage before being passed to workflows.
Generate Upload Token
def generate_upload_token(self, filename: str) -> Dict:
    """
    Request a file upload token from the platform.
    
    Upload tokens are temporary, single-use credentials that allow
    secure file uploads without exposing the main API token.
    
    Args:
        filename: Name of the file to upload
        
    Returns:
        Dictionary containing:
        - token: Temporary upload authorization token
        - tenantFile: File metadata including generated filename and path
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
    
Upload File to Storage
def upload_file(self, file_path: str, upload_response: Dict) -> str:
    """
    Upload file binary data to the platform file service.
    
    Uses the upload token to authenticate the file transfer.
    The platform generates a consistent filename for reference.
    
    Args:
        file_path: Local path to the file being uploaded
        upload_response: Response from generate_upload_token()
        
    Returns:
        tenant_filename: Platform path reference for the uploaded file
        Example: "/tenants/40eaf721.../source.json"
    """
    # Extract upload credentials from the token response
    upload_token = upload_response["token"]
    tenant_file = upload_response["tenantFile"]
    generated_filename = tenant_file["file_name"]
    
    # File service endpoint
    upload_url = "https://prod.agentic.inv.tech/files/upload"
    
    # Include upload token as URL parameter for this request
    params = {"upload-token": upload_token}
    
    # Read and upload the file
    with open(file_path, 'rb') as f:
        files = {'file': (generated_filename, f, 'application/json')}
        
        response = requests.post(
            upload_url,
            files=files,
            params=params,
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
    
    if response.status_code != 200:
        raise Exception(f"File upload failed: HTTP {response.status_code}")
    
    # Return tenant-scoped path for use in workflow execution
    tenant_filename = f"/tenants/{self.tenant_id}/{os.path.basename(file_path)}"
    return tenant_filename

Step 3: Map Workflow Inputs
Workflows expect specific input parameters. These must be matched to the files and secrets being passed.
Get Expected Workflow Inputs
def get_workflow_inputs(self) -> List[Dict]:
    """
    Query for the workflow's expected input parameters.
    
    Returns information about each input:
    - name: Parameter name
    - type: Data type (File, String, Secret, etc.)
    - stepId: Which workflow step requires this input
    - direction: Whether this is an Input or Output parameter
    
    Returns:
        List of input variable specifications
    """
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
Build Execution Variables
def build_execution_variables(self, config_file_path: str, source_file_path: str, 
                             private_key: str, private_key_id: str) -> List[Dict]:
    """
    Map provided files and secrets to workflow input parameters.
    
    This function creates the variable bindings that connect actual data
    to the workflow's expected inputs. Each variable specifies which step
    receives the data and what type of data it is.
    
    Args:
        config_file_path: Path to configuration file (uploaded to platform)
        source_file_path: Path to source data file (uploaded to platform)
        private_key: Private key secret for authentication
        private_key_id: Private key ID secret for authentication
        
    Returns:
        List of FlowExecutionVariableInput objects for the workflow
    """
    flow_variables = []
    
    # Iterate through expected inputs and map to provided data
    for var in self.workflow_inputs:
        var_name = var['name']
        var_type = var['type']
        step_id = var['stepId']
        
        # Match workflow inputs to our provided parameters
        if var_name == 'config_file' and var_type == 'File':
            flow_variables.append({
                'step_id': step_id,
                'variable_name': var_name,
                'variable_type': var_type,
                'variable_value': config_file_path  # Platform file path
            })
        elif var_name == 'source_file' and var_type == 'File':
            flow_variables.append({
                'step_id': step_id,
                'variable_name': var_name,
                'variable_type': var_type,
                'variable_value': source_file_path  # Platform file path
            })
        elif var_name == 'private_key' and var_type == 'Secret':
            flow_variables.append({
                'step_id': step_id,
                'variable_name': var_name,
                'variable_type': var_type,
                'variable_value': private_key  # Secret reference
            })
        elif var_name == 'private_key_id' and var_type == 'Secret':
            flow_variables.append({
                'step_id': step_id,
                'variable_name': var_name,
                'variable_type': var_type,
                'variable_value': private_key_id  # Secret reference
            })
    
    return flow_variables

Step 4: Execute Workflow
Submit the workflow execution with all parameters.
def execute_workflow(self, config_file_path: str, source_file_path: str,
                    private_key: str, private_key_id: str) -> str:
    """
    Trigger workflow execution on the platform.
    
    Submits the workflow with all bound variables to the platform.
    The platform queues the execution and returns an execution ID
    for tracking and monitoring.
    
    Returns:
        execution_id: Unique identifier for this workflow run
    """
    # Build the variable mappings for this execution
    variables = self.build_execution_variables(
        config_file_path, source_file_path, private_key, private_key_id
    )
    
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
    return self.execution_id