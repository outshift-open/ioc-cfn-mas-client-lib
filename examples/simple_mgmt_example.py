# examples/simple_mgmt_example.py
"""Simple Management Plane API Example.

Shows how to use the simple list_workspaces and list_mas functions.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

from ioc_cfn_mas_client import Client, list_mas, list_workspaces

# Load environment variables from .env file in examples directory
# Works whether you run from project root or examples directory
examples_dir = Path(__file__).parent
load_dotenv(examples_dir / ".env")


def main() -> None:
    """Demonstrate simple Management Plane functions."""

    print("=" * 70)
    print("Simple Management Plane API Example")
    print("=" * 70)
    print()

    # Configuration
    mgmt_base_url = os.getenv("MANAGEMENT_PLANE_BASE_URL", "http://localhost:8080")
    api_key = os.getenv("API_KEY", "your-api-key")

    # ========================================================================
    # Example 1: List Workspaces
    # ========================================================================
    print("Example 1: Listing workspaces...")
    print()

    try:
        result = list_workspaces(
            mgmt_base_url=mgmt_base_url,
            api_key=api_key,
        )

        print(f"✓ Found {result.get('total', 0)} workspace(s)")
        for workspace in result.get("workspaces", []):
            print(f"  • {workspace['name']} (ID: {workspace['id']})")

    except Exception as e:
        print(f"✗ Failed to list workspaces: {e}")
        print("  Make sure:")
        print("  1. Management Plane is running")
        print("  2. API_KEY environment variable is set correctly")
        return

    print()

    # ========================================================================
    # Example 2: List Multi-Agentic Systems
    # ========================================================================
    print("Example 2: Listing multi-agentic systems...")
    print()

    # Get the first workspace ID
    workspaces = result.get("workspaces", [])
    if not workspaces:
        print("⚠ No workspaces found. Create a workspace first.")
        return

    workspace_id = workspaces[0]["id"]
    print(f"Using workspace: {workspaces[0]['name']}")
    print()

    try:
        result = list_mas(
            mgmt_base_url=mgmt_base_url,
            api_key=api_key,
            workspace_id=workspace_id,
        )

        print(f"✓ Found {result.get('total', 0)} MAS")
        for mas in result.get("systems", []):
            print(f"  • {mas['name']} (ID: {mas['id']})")

    except Exception as e:
        print(f"✗ Failed to list MAS: {e}")

    print()

    # ========================================================================
    # Example 3: Using with CFN Client
    # ========================================================================
    print("Example 3: Using with CFN Client...")
    print()

    try:
        # Create CFN client for shared memories
        cfn_client = Client(
            base_url=os.getenv("CFN_BASE_URL", "http://localhost:9010")
        )

        # List workspaces from Management Plane
        workspaces = list_workspaces(mgmt_base_url, api_key)
        print(f"✓ Management Plane: {workspaces.get('total', 0)} workspace(s)")

        # Use CFN client for memories (if workspace and MAS exist)
        if workspaces.get("workspaces"):
            ws_id = workspaces["workspaces"][0]["id"]
            mas_list = list_mas(mgmt_base_url, api_key, ws_id)
            if mas_list.get("systems"):
                mas_id = mas_list["systems"][0]["id"]
                print(f"✓ CFN client ready for workspace {ws_id}, MAS {mas_id}")

    except Exception as e:
        print(f"✗ Error: {e}")

    print()
    print("=" * 70)
    print("Example completed!")
    print("=" * 70)
    print()
    print("Usage:")
    print("  from ioc_cfn_mas_client import list_workspaces, list_mas")
    print()
    print("  # List workspaces")
    print('  workspaces = list_workspaces("http://localhost:8080", "your-api-key")')
    print()
    print("  # List MAS in a workspace")
    print('  systems = list_mas("http://localhost:8080", "your-api-key", "workspace-id")')


if __name__ == "__main__":
    main()
