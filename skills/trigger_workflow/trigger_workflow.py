"""
Trigger Workflow Skill - Triggers a workflow execution and retrieves results.
"""
import json
import os
import sys
from pathlib import Path
from typing import Dict, Optional, List

# Import shared modules from parent
parent_dir = Path(__file__).parent.parent
if str(parent_dir.parent) not in sys.path:
    sys.path.insert(0, str(parent_dir.parent))

from skills.axon_orchestrator import AxonOrchestrator
from skills.credentials import load_credentials


def find_files_in_input_data(input_data_dir: Path, input_name: str) -> List[Path]:
    """
    Search for files in input_data directory that might match the input name.
    
    Args:
        input_data_dir: Path to input_data directory
        input_name: Name of the input parameter
        
    Returns:
        List of matching file paths
    """
    if not input_data_dir.exists():
        return []
    
    found_files = []
    
    # Search patterns based on input name
    search_patterns = [
        input_name.lower(),
        input_name.lower().replace('_', '-'),
        input_name.lower().replace('_', ' '),
        input_name.lower().replace('-', '_'),
    ]
    
    # Search recursively in input_data
    for root, dirs, files in os.walk(input_data_dir):
        for file in files:
            file_lower = file.lower()
            file_path = Path(root) / file
            
            # Check if filename matches any pattern
            for pattern in search_patterns:
                if pattern in file_lower or file_lower.startswith(pattern) or file_lower.endswith(pattern):
                    found_files.append(file_path)
                    break
    
    # Also try exact matches first
    exact_matches = []
    for root, dirs, files in os.walk(input_data_dir):
        for file in files:
            file_lower = file.lower()
            file_path = Path(root) / file
            
            # Exact match (case insensitive)
            if file_lower == input_name.lower() or file_lower == f"{input_name.lower()}.csv" or file_lower == f"{input_name.lower()}.json":
                exact_matches.append(file_path)
    
    # Return exact matches first, then others
    return exact_matches + [f for f in found_files if f not in exact_matches]


def trigger_workflow(workflow_name: str, namespace: str = "default", 
                    **workflow_inputs) -> Dict:
    """
    Trigger workflow skill - executes a workflow and returns execution info.
    
    Args:
        workflow_name: Name of the workflow to execute
        namespace: Namespace containing the workflow (default: "default")
        **workflow_inputs: Input parameters for the workflow
        
    Returns:
        Dictionary containing execution_id and basic workflow info
    """
    print("=" * 70)
    print("🚀 Trigger Workflow")
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
        
        # Create orchestrator
        orchestrator = AxonOrchestrator(
            workflow_name=workflow_name,
            api_key=api_key,
            tenant_id=tenant_id,
            namespace_name=namespace
        )
        
        # Setup workflow
        print("📋 Setting up workflow...")
        setup_info = orchestrator.setup_workflow()
        print()
        
        # Display workflow inputs and handle file uploads
        if orchestrator.workflow_inputs:
            print("📥 Workflow Inputs:")
            missing_inputs = []
            input_data_dir = Path(__file__).parent.parent.parent / "input_data"
            
            for inp in orchestrator.workflow_inputs:
                provided = "✓" if inp['name'] in workflow_inputs else "✗"
                value_preview = ""
                
                if inp['name'] in workflow_inputs:
                    val = str(workflow_inputs[inp['name']])
                    if len(val) > 50:
                        val = val[:47] + "..."
                    value_preview = f" = {val}"
                else:
                    missing_inputs.append(inp)
                
                print(f"   {provided} {inp['name']} ({inp['type']}){value_preview}")
            print()
            
            # Handle File inputs - upload local file paths to platform
            for inp in orchestrator.workflow_inputs:
                if inp['type'] == 'File':
                    input_name = inp['name']
                    file_value = workflow_inputs.get(input_name)
                    
                    # If file input is provided, check if it's a local path that needs uploading
                    if file_value:
                        file_path = Path(file_value)
                        # Check if it's a local file path (not already a platform path)
                        if file_path.exists() and not str(file_value).startswith('/tenants/'):
                            # Local file path - upload it
                            print(f"📤 Uploading local file for {input_name}: {file_path.name}")
                            try:
                                uploaded_path = orchestrator.upload_file(str(file_path))
                                workflow_inputs[input_name] = uploaded_path
                                print(f"   ✓ Uploaded: {uploaded_path}")
                            except Exception as e:
                                print(f"   ❌ Upload failed: {e}")
                                # Keep original path, might be handled by workflow
                        # If it's already a platform path or doesn't exist, skip upload
                        continue  # Skip the search logic below since file is already provided
                    
                    # If file input is not provided, search in input_data directory
                    if input_name not in workflow_inputs:
                        # Search for files in input_data directory
                        found_files = find_files_in_input_data(input_data_dir, input_name)
                        
                        if found_files:
                            if len(found_files) == 1:
                                # Single file found, use it
                                file_path = found_files[0]
                                print(f"📤 Found file for {input_name}: {file_path.name}")
                                print(f"   Uploading to platform...")
                                
                                try:
                                    uploaded_path = orchestrator.upload_file(str(file_path))
                                    workflow_inputs[input_name] = uploaded_path
                                    print(f"   ✓ Uploaded: {uploaded_path}")
                                except Exception as e:
                                    print(f"   ❌ Upload failed: {e}")
                                    missing_inputs.append(inp)
                            else:
                                # Multiple files found, ask user to choose
                                print(f"📁 Multiple files found for {input_name}:")
                                for i, file_path in enumerate(found_files, 1):
                                    print(f"   {i}. {file_path.relative_to(input_data_dir)}")
                                
                                try:
                                    choice = input(f"Select file number (1-{len(found_files)}) or enter path: ").strip()
                                    
                                    if choice.isdigit() and 1 <= int(choice) <= len(found_files):
                                        file_path = found_files[int(choice) - 1]
                                    else:
                                        # User provided a path
                                        file_path = Path(choice)
                                        if not file_path.is_absolute():
                                            file_path = input_data_dir / file_path
                                    
                                    if file_path.exists():
                                        print(f"   Uploading {file_path.name}...")
                                        uploaded_path = orchestrator.upload_file(str(file_path))
                                        workflow_inputs[input_name] = uploaded_path
                                        print(f"   ✓ Uploaded: {uploaded_path}")
                                    else:
                                        print(f"   ❌ File not found: {file_path}")
                                        missing_inputs.append(inp)
                                except (ValueError, KeyboardInterrupt, EOFError):
                                    print(f"   ⚠️  Skipping {input_name}")
                                    missing_inputs.append(inp)
                        else:
                            # No file found, will prompt user
                            missing_inputs.append(inp)
            
            # Prompt for remaining missing inputs (non-File types or files not found)
            if missing_inputs:
                print("⚠️  Missing required inputs. Please provide:")
                print()
                for inp in missing_inputs:
                    input_name = inp['name']
                    input_type = inp['type']
                    
                    # Skip if already provided (might have been uploaded)
                    if input_name in workflow_inputs:
                        continue
                    
                    # Prompt user for input
                    prompt = f"Enter {input_name} ({input_type}): "
                    if input_type == "File":
                        prompt = f"Enter {input_name} (File path in input_data/ or absolute path): "
                    elif input_type == "Secret":
                        prompt = f"Enter {input_name} (Secret name): "
                    elif input_type == "String":
                        prompt = f"Enter {input_name} (String): "
                    
                    try:
                        user_input = input(prompt).strip()
                        
                        if user_input:
                            # If it's a File type and looks like a path, try to upload it
                            if input_type == "File":
                                file_path = Path(user_input)
                                if not file_path.is_absolute():
                                    file_path = input_data_dir / file_path
                                
                                if file_path.exists():
                                    print(f"   Uploading {file_path.name}...")
                                    try:
                                        uploaded_path = orchestrator.upload_file(str(file_path))
                                        workflow_inputs[input_name] = uploaded_path
                                        print(f"   ✓ Uploaded: {uploaded_path}")
                                    except Exception as e:
                                        print(f"   ❌ Upload failed: {e}")
                                        workflow_inputs[input_name] = user_input  # Use as-is
                                else:
                                    # File doesn't exist, might be a platform path
                                    workflow_inputs[input_name] = user_input
                            else:
                                workflow_inputs[input_name] = user_input
                                print(f"   ✓ {input_name} = {user_input[:50]}{'...' if len(user_input) > 50 else ''}")
                        else:
                            print(f"   ⚠️  Skipping {input_name} (empty input)")
                    except (KeyboardInterrupt, EOFError):
                        print(f"   ⚠️  Skipping {input_name}")
                print()
        
        # Execute workflow
        print("🚀 Executing workflow...")
        execution_id = orchestrator.execute_workflow(**workflow_inputs)
        print()
        
        # Return execution info (no monitoring)
        print("✅ Workflow execution started")
        print(f"   Execution ID: {execution_id}")
        print("   Use get_workflow_status to check status")
        print()
        
        # Get results
        result = {
            "success": True,
            "execution_id": execution_id,
            "workflow_name": workflow_name,
            "namespace": namespace,
            "setup_info": setup_info
        }
        
        print("=" * 70)
        print("✅ Workflow execution started successfully!")
        print("=" * 70)
        
        return result
        
    except Exception as e:
        print()
        print("=" * 70)
        print(f"❌ Error: {str(e)}")
        print("=" * 70)
        return {
            "success": False,
            "error": str(e)
        }


def main():
    """Main entry point for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Trigger workflow execution")
    parser.add_argument("workflow_name", help="Name of the workflow to execute")
    parser.add_argument("--namespace", default="default", help="Namespace (default: default)")
    parser.add_argument("--input", action="append", nargs=2, metavar=("KEY", "VALUE"),
                       help="Workflow input parameter (can be used multiple times)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    # Parse inputs
    workflow_inputs = {}
    if args.input:
        for key, value in args.input:
            workflow_inputs[key] = value
    
    # Execute workflow
    result = trigger_workflow(
        workflow_name=args.workflow_name,
        namespace=args.namespace,
        **workflow_inputs
    )
    
    # Output as JSON if requested
    if args.json:
        print()
        print(json.dumps(result, indent=2))
    else:
        # Save results
        output_file = "workflow_execution_result.json"
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Results saved to: {output_file}")
    
    # Exit with error code if failed
    if not result.get("success"):
        sys.exit(1)


if __name__ == "__main__":
    main()
