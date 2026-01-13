"""
Credentials management for Axon API.
Loads credentials from mydata.json file.
"""
import json
from pathlib import Path
from typing import Dict


def load_credentials(data_file: Path = None) -> Dict[str, str]:
    """
    Load credentials from mydata.json file.
    
    Expected JSON structure:
    {
      "data": {
        "createApiToken": {
          "token": "api_...",
          "api_token": {
            "tenant_id": "...",
            ...
          }
        }
      }
    }
    
    Args:
        data_file: Optional path to credentials file. If not provided,
                   defaults to .my_axon_data/mydata.json relative to project root.
    
    Returns:
        Dictionary with 'api_key' and 'tenant_id' keys.
    
    Raises:
        FileNotFoundError: If credentials file doesn't exist
        ValueError: If JSON structure is invalid or missing required fields
    """
    if data_file is None:
        # Default to .my_axon_data/mydata.json relative to project root
        project_root = Path(__file__).parent.parent
        data_file = project_root / ".my_axon_data" / "mydata.json"
    
    if not data_file.exists():
        raise FileNotFoundError(f"Credentials file not found: {data_file}")
    
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        # Validate structure
        if "data" not in data:
            raise ValueError("Missing 'data' field in JSON file")
        
        if "createApiToken" not in data["data"]:
            raise ValueError("Missing 'createApiToken' in data")
        
        token_response = data["data"]["createApiToken"]
        
        # Extract token
        if "token" not in token_response:
            raise ValueError("Missing 'token' in createApiToken response")
        token = token_response["token"]
        
        # Extract tenant_id from api_token object
        if "api_token" not in token_response:
            raise ValueError("Missing 'api_token' in createApiToken response")
        
        api_token = token_response["api_token"]
        if "tenant_id" not in api_token:
            raise ValueError("Missing 'tenant_id' in api_token")
        tenant_id = api_token["tenant_id"]
        
        return {
            "api_key": token,
            "tenant_id": tenant_id
        }
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in credentials file: {e}")
    except Exception as e:
        raise ValueError(f"Error loading credentials: {e}")


def get_api_key() -> str:
    """Get API key from credentials file."""
    creds = load_credentials()
    return creds["api_key"]


def get_tenant_id() -> str:
    """Get tenant ID from credentials file."""
    creds = load_credentials()
    return creds["tenant_id"]

