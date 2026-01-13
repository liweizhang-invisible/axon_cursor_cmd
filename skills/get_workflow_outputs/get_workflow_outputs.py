"""
Get Workflow Outputs Skill - Retrieves all output files from a workflow execution.
"""
import json
import os
import sys
import requests
from pathlib import Path
from typing import Dict, List, Optional

# Import shared modules from parent
parent_dir = Path(__file__).parent.parent
if str(parent_dir.parent) not in sys.path:
    sys.path.insert(0, str(parent_dir.parent))

from skills.axon_client import GraphQLClient
from skills.credentials import load_credentials


def download_file_content(api_key: str, file_name: str, storage_path: str) -> str:
    """
    Download the content of an output file from platform storage.
    
    Args:
        api_key: API key for authentication
        file_name: Name of the file
        storage_path: Storage path of the file
        
    Returns:
        File content as string
    """
    client = GraphQLClient("https://prod.agentic.inv.tech/graphql/", api_key)
    
    # Step 1: Get download authorization token
    token_mutation = """
    mutation GetDownloadToken($path: String!) {
        getFileDownloadTokenByPath(path: $path)
    }
    """
    
    variables = {"path": storage_path}
    result = client.execute(token_mutation, variables)
    download_token = result["data"]["getFileDownloadTokenByPath"]
    
    if not download_token:
        raise Exception(f"Failed to get download token for: {file_name}")
    
    # Step 2: Download file using token
    base_url = client.url.replace('/graphql/', '/').replace('/graphql', '/')
    download_url = f"{base_url}files/download?file_name={file_name}&download-token={download_token}"
    
    response = requests.get(download_url, headers=client.headers)
    
    if response.status_code == 200:
        content = response.text
        return content
    else:
        raise Exception(f"Download failed: HTTP {response.status_code}")


def get_workflow_outputs(flow_execution_id: str, download: bool = False, 
                        output_dir: Optional[str] = None) -> Dict:
    """
    Get all output files from a workflow execution by execution ID.
    
    Args:
        flow_execution_id: The workflow execution ID
        download: Whether to download the files locally (default: False)
        output_dir: Directory to save downloaded files (required when download=True)
        
    Returns:
        Dictionary containing output files list and metadata
        
    Raises:
        ValueError: If download=True but output_dir is not provided
    """
    print("=" * 70)
    print("📁 Get Workflow Outputs")
    print("=" * 70)
    print()
    
    try:
        # Load credentials
        print("🔑 Loading credentials...")
        creds = load_credentials()
        api_key = creds["api_key"]
        tenant_id = creds["tenant_id"]
        print(f"   ✓ Tenant ID: {tenant_id}")
        print()
        
        # Create client
        client = GraphQLClient("https://prod.agentic.inv.tech/graphql/", api_key)
        
        # Query for execution status and output files
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
        
        variables = {"flow_execution_id": flow_execution_id}
        
        print(f"🔍 Retrieving output files for execution: {flow_execution_id}")
        print()
        
        result = client.execute(query, variables)
        
        if not result or "data" not in result:
            raise Exception(f"Invalid API response: {result}")
        
        status = result["data"]["flowExecutionStatus"]
        
        if status is None:
            raise Exception(f"Execution not found for ID: {flow_execution_id}")
        
        execution_status = status.get("result")
        print(f"   Execution Status: {execution_status}")
        print()
        
        # Collect artifact files from all execution steps
        all_files = []
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
        
        if not output_files:
            print("   ⚠️  No output files found")
            print()
        else:
            print(f"   ✓ Found {len(output_files)} output file(s):")
            for i, file_info in enumerate(output_files, 1):
                size_mb = file_info["file_size_bytes"] / (1024 * 1024) if file_info["file_size_bytes"] else 0
                size_str = f"{size_mb:.2f} MB" if size_mb > 0 else "unknown size"
                print(f"      {i}. {file_info['file_name']} ({size_str})")
            print()
        
        # Download files if requested
        downloaded_files = []
        if download and output_files:
            if not output_dir:
                raise ValueError("output_dir is required when download=True")
            
            download_path = Path(output_dir)
            download_path.mkdir(parents=True, exist_ok=True)
            
            print(f"📥 Downloading files to: {download_path}")
            print()
            
            for file_info in output_files:
                try:
                    print(f"   Downloading: {file_info['file_name']}...")
                    content = download_file_content(
                        api_key=api_key,
                        file_name=file_info["file_name"],
                        storage_path=file_info["storage_path"]
                    )
                    
                    # Save file
                    file_path = download_path / file_info["file_name"]
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    
                    downloaded_files.append({
                        "file_name": file_info["file_name"],
                        "local_path": str(file_path),
                        "size_bytes": len(content.encode("utf-8"))
                    })
                    print(f"      ✓ Saved to: {file_path}")
                except Exception as e:
                    print(f"      ❌ Failed to download {file_info['file_name']}: {e}")
                    downloaded_files.append({
                        "file_name": file_info["file_name"],
                        "error": str(e)
                    })
            print()
        
        # Build result dictionary
        result_dict = {
            "success": True,
            "execution_id": flow_execution_id,
            "execution_status": execution_status,
            "output_files_count": len(output_files),
            "output_files": output_files
        }
        
        if download:
            result_dict["download_dir"] = str(download_path) if download else None
            result_dict["downloaded_files"] = downloaded_files
        
        print("=" * 70)
        if output_files:
            print(f"✅ Retrieved {len(output_files)} output file(s)")
            if download:
                print(f"📥 Downloaded {len([f for f in downloaded_files if 'local_path' in f])} file(s)")
        else:
            print("⚠️  No output files found")
        print("=" * 70)
        
        return result_dict
        
    except Exception as e:
        print()
        print("=" * 70)
        print(f"❌ Error: {str(e)}")
        print("=" * 70)
        return {
            "success": False,
            "error": str(e),
            "execution_id": flow_execution_id
        }


def main():
    """Main entry point for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Get workflow execution output files")
    parser.add_argument("execution_id", help="Workflow execution ID")
    parser.add_argument("--download", action="store_true",
                       help="Download output files locally")
    parser.add_argument("--output-dir", type=str, required=False,
                       help="Directory to save downloaded files (required when --download is used)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    # Validate: output-dir is required when download is enabled
    if args.download and not args.output_dir:
        parser.error("--output-dir is required when --download is used")
    
    # Get outputs
    result = get_workflow_outputs(
        flow_execution_id=args.execution_id,
        download=args.download,
        output_dir=args.output_dir
    )
    
    # Output as JSON if requested
    if args.json:
        print()
        print(json.dumps(result, indent=2))
    else:
        # Save results
        output_file = "workflow_outputs_result.json"
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Results saved to: {output_file}")
    
    # Exit with error code if failed
    if not result.get("success"):
        sys.exit(1)


if __name__ == "__main__":
    main()
