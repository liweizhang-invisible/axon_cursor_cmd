Error Handling & Monitoring
Polling for Execution Status

def monitor_execution(self) -> Dict:
    """
    Poll for workflow execution completion.
    
    Workflow execution is asynchronous. This method polls the platform
    at intervals until the workflow reaches a terminal state:
    - Completed: Workflow finished successfully
    - Failed: Workflow encountered an error
    - Cancelled: User manually stopped execution
    - Killed: Platform terminated the execution
    
    Returns:
        Dictionary containing final execution status, results, and any errors
    """
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
            
            # Validate response structure - raise exception if invalid
            if not result or "data" not in result:
                raise Exception(f"Invalid API response: {result}")
            
            status = result["data"]["flowExecutionStatus"]
            
            # Handle null status responses - raise exception if not found
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
            time.sleep(1)
            
        except KeyError as e:
            print(f"   ⚠️  Missing key in response: {e}, retrying...")
            time.sleep(2)
        except Exception as e:
            print(f"   ⚠️  Error during monitoring: {e}, retrying...")
            time.sleep(2)



Retrieving Output Files (Optional)

Output file retrieval is optional. Workflows may store results in external systems. Return data directly in execution response. Only use this API if outputs are stored on the Agentic Platform and need to be retrieved

def get_output_files(self) -> List[Dict]:
    """
    Query for files created during workflow execution.
    
    Workflows can create output files during execution.
    This retrieves metadata for all artifact files created,
    which can then be downloaded for inspection.
    
    Returns:
        List of file metadata for files created during execution
    """
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

Download Output File
def download_file(self, file_name: str, storage_path: str) -> str:
    """
    Download the content of an output file from platform storage.
    
    Two-step process:
    1. Request a download token for the specific file
    2. Use token to download file content
    
    Args:
        file_name: Name of the file to download
        storage_path: Platform storage path for the file
        
    Returns:
        File content as a string
    """
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
