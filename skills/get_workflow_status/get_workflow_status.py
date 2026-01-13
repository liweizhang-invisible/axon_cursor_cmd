"""
Get Workflow Status Skill - Retrieves the status of a workflow execution.
"""
import json
import sys
from pathlib import Path
from typing import Dict, Optional

# Import shared modules from parent
parent_dir = Path(__file__).parent.parent
if str(parent_dir.parent) not in sys.path:
    sys.path.insert(0, str(parent_dir.parent))

from skills.axon_client import GraphQLClient
from skills.credentials import load_credentials


def get_workflow_status(flow_execution_id: str, monitor: bool = False) -> Dict:
    """
    Get workflow execution status by execution ID.
    
    Args:
        flow_execution_id: The workflow execution ID to check
        monitor: Whether to poll until completion (default: False)
        
    Returns:
        Dictionary containing execution status and details
    """
    print("=" * 70)
    print("📊 Get Workflow Status")
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
        
        # Query for execution status
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
        
        variables = {"flowExecutionId": flow_execution_id}
        
        if monitor:
            # Poll until terminal state
            import time
            terminal_states = ['Completed', 'Failed', 'Cancelled', 'Killed']
            start_time = time.time()
            last_status = None
            
            print("⏳ Monitoring execution (polling every 10 seconds)...")
            print()
            
            while True:
                try:
                    result = client.execute(query, variables)
                    
                    if not result or "data" not in result:
                        raise Exception(f"Invalid API response: {result}")
                    
                    status = result["data"]["flowExecutionStatus"]
                    
                    if status is None:
                        raise Exception(f"Execution status not found for ID: {flow_execution_id}")
                    
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
                        print()
                        
                        if current_status == "Completed":
                            print(f"   Token Usage: {status.get('token_usage', 0)} tokens")
                        elif current_status == "Failed":
                            print(f"   ❌ Failure: {status.get('failure_reason', 'Unknown')}")
                            
                            # Log individual step failures
                            failed_steps = [s for s in status.get('steps', []) 
                                           if s.get('result') == 'Failed']
                            if failed_steps:
                                print(f"   Failed Steps: {len(failed_steps)} of {len(status.get('steps', []))}")
                                for i, step in enumerate(failed_steps, 1):
                                    print(f"     Step {i} ({step.get('entity_type', 'Unknown')}):")
                                    if step.get('failure_reason'):
                                        print(f"       Reason: {step['failure_reason']}")
                        print()
                        break
                    
                    # Wait before next poll
                    time.sleep(10)
                    
                except KeyError as e:
                    print(f"   ⚠️  Missing key in response: {e}, retrying...")
                    time.sleep(2)
                except Exception as e:
                    print(f"   ⚠️  Error during monitoring: {e}, retrying...")
                    time.sleep(2)
        else:
            # Single status check
            print(f"🔍 Checking status for execution: {flow_execution_id}")
            print()
            
            result = client.execute(query, variables)
            
            if not result or "data" not in result:
                raise Exception(f"Invalid API response: {result}")
            
            status = result["data"]["flowExecutionStatus"]
            
            if status is None:
                raise Exception(f"Execution status not found for ID: {flow_execution_id}")
            
            current_status = status.get("result")
            
            if not current_status:
                raise Exception(f"No result status in execution response")
            
            print(f"   Status: {current_status}")
            if status.get("start_time"):
                print(f"   Start Time: {status.get('start_time')}")
            if status.get("end_time"):
                print(f"   End Time: {status.get('end_time')}")
            if status.get("token_usage"):
                print(f"   Token Usage: {status.get('token_usage')} tokens")
            if current_status == "Failed":
                print(f"   ❌ Failure: {status.get('failure_reason', 'Unknown')}")
            print()
        
        # Build result dictionary
        result_dict = {
            "success": True,
            "execution_id": flow_execution_id,
            "status": status.get("result"),
            "start_time": status.get("start_time"),
            "end_time": status.get("end_time"),
            "token_usage": status.get("token_usage", 0),
            "steps": status.get("steps", [])
        }
        
        if status.get("result") == "Failed":
            result_dict["failure_reason"] = status.get("failure_reason")
            result_dict["failure_detail"] = status.get("failure_detail")
            result_dict["success"] = False
        
        print("=" * 70)
        if result_dict.get("success") and result_dict.get("status") == "Completed":
            print("✅ Workflow execution completed!")
        elif result_dict.get("status") == "Failed":
            print("❌ Workflow execution failed!")
        else:
            print(f"📊 Workflow status: {result_dict.get('status')}")
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
    
    parser = argparse.ArgumentParser(description="Get workflow execution status")
    parser.add_argument("execution_id", help="Workflow execution ID")
    parser.add_argument("--monitor", action="store_true", 
                       help="Monitor execution until completion")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    # Get status
    result = get_workflow_status(
        flow_execution_id=args.execution_id,
        monitor=args.monitor
    )
    
    # Output as JSON if requested
    if args.json:
        print()
        print(json.dumps(result, indent=2))
    else:
        # Save results
        output_file = "workflow_status_result.json"
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Results saved to: {output_file}")
    
    # Exit with error code if failed
    if not result.get("success"):
        sys.exit(1)


if __name__ == "__main__":
    main()
