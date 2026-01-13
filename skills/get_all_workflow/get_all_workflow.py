"""
Get All Workflow Skill - Lists all workflows in specified namespaces.
"""
import json
import sys
from typing import Dict, List, Optional

# Import shared modules from parent
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
if str(parent_dir.parent) not in sys.path:
    sys.path.insert(0, str(parent_dir.parent))

from skills.axon_client import GraphQLClient
from skills.credentials import load_credentials


def get_namespace_by_name(api_key: str, namespace_name: str) -> Optional[Dict]:
    """
    Get namespace by name (works with API token authentication).
    
    Args:
        api_key: API token for authentication
        namespace_name: Name of the namespace
        
    Returns:
        Namespace dictionary with id, name, etc., or None if not found
    """
    client = GraphQLClient("https://prod.agentic.inv.tech/graphql/", api_key)
    
    query = """
    query GetNamespace($name: String!) {
      namespace(name: $name) {
        id
        name
      }
    }
    """
    
    try:
        variables = {"name": namespace_name}
        result = client.execute(query, variables)
        namespace = result["data"]["namespace"]
        return namespace if namespace else None
    except Exception:
        return None


def get_workflows_in_namespace(api_key: str, namespace_id: str, 
                                include_archived: bool = False) -> List[Dict]:
    """
    Get all workflows in a specific namespace.
    
    Args:
        api_key: API token for authentication
        namespace_id: ID of the namespace
        include_archived: Whether to include archived workflows
        
    Returns:
        List of workflow dictionaries
    """
    client = GraphQLClient("https://prod.agentic.inv.tech/graphql/", api_key)
    
    query = """
    query GetWorkflows($namespaceId: ID!, $archived: Boolean) {
      flows(namespaceId: $namespaceId, archived: $archived) {
        id
        name
        description
        created_date
        is_archived
      }
    }
    """
    
    variables = {
        "namespaceId": namespace_id,
        "archived": None if include_archived else False
    }
    
    result = client.execute(query, variables)
    return result["data"]["flows"]


def get_all_workflow(namespace_names: Optional[List[str]] = None, 
                    include_archived: bool = False) -> Dict:
    """
    Get all workflows in specified namespaces.
    
    Note: API tokens can only query namespaces by name (not list all namespaces). 
    Common namespace: "default". You can specify multiple namespaces.
    
    Args:
        namespace_names: List of namespace names to query. If None, defaults to ["default"].
        include_archived: Whether to include archived workflows
        
    Returns:
        Dictionary containing workflows organized by namespace
    """
    print("=" * 70)
    print("📋 Get All Workflows")
    print("=" * 70)
    print()
    
    try:
        # Load credentials
        print("🔑 Loading credentials...")
        creds = load_credentials()
        api_key = creds["api_key"]
        print("   ✓ Credentials loaded")
        print()
        
        # Default to "default" namespace if none specified
        if namespace_names is None:
            namespace_names = ["default"]
        
        # Get workflows for each namespace
        all_workflows = {}
        total_workflows = 0
        found_namespaces = []
        
        for ns_name in namespace_names:
            print(f"📁 Querying namespace: {ns_name}")
            
            # Get namespace by name
            namespace = get_namespace_by_name(api_key, ns_name)
            
            if not namespace:
                print(f"   ⚠️  Namespace '{ns_name}' not found or not accessible")
                print()
                continue
            
            ns_id = namespace["id"]
            found_namespaces.append(ns_name)
            
            print(f"   ✓ Namespace ID: {ns_id}")
            
            # Get workflows in this namespace
            workflows = get_workflows_in_namespace(api_key, ns_id, include_archived)
            
            all_workflows[ns_name] = {
                "namespace_id": ns_id,
                "namespace_info": namespace,
                "workflows": workflows
            }
            
            count = len(workflows)
            total_workflows += count
            print(f"   ✓ Found {count} workflow(s)")
            
            # Display workflow names
            if workflows:
                for workflow in workflows:
                    archived = " (archived)" if workflow.get("is_archived") else ""
                    print(f"      - {workflow['name']}{archived}")
            else:
                print("      (no workflows found)")
            print()
        
        if not found_namespaces:
            print("=" * 70)
            print("❌ No accessible namespaces found")
            print("=" * 70)
            return {
                "success": False,
                "error": "No accessible namespaces found. Check namespace names."
            }
        
        print("=" * 70)
        print(f"✅ Total: {total_workflows} workflow(s) in {len(found_namespaces)} namespace(s)")
        print("=" * 70)
        
        return {
            "success": True,
            "total_workflows": total_workflows,
            "namespaces": all_workflows
        }
        
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
    
    parser = argparse.ArgumentParser(
        description="Get all workflows in specified namespaces",
        epilog="Note: API tokens can only query namespaces by name. "
               "Common namespaces: 'default'. Specify multiple with --namespace multiple times."
    )
    parser.add_argument("--namespace", action="append", 
                       help="Namespace name to query (can be used multiple times). Default: 'default'")
    parser.add_argument("--include-archived", action="store_true", 
                       help="Include archived workflows")
    parser.add_argument("--json", action="store_true", 
                       help="Output as JSON")
    
    args = parser.parse_args()
    
    # Get workflows
    result = get_all_workflow(
        namespace_names=args.namespace,
        include_archived=args.include_archived
    )
    
    # Output as JSON if requested
    if args.json:
        print()
        print(json.dumps(result, indent=2))
    else:
        # Save results to file
        output_file = "workflows_list.json"
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Results saved to: {output_file}")
    
    # Exit with error code if failed
    if not result.get("success"):
        sys.exit(1)


if __name__ == "__main__":
    main()

