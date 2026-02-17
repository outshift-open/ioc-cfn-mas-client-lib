# examples/example.py
"""Example usage of the IOC CFN MAS Client Library.

This script demonstrates how to:
1. Initialize the client
2. Upsert shared memories
3. Query shared memories using semantic search
"""

import os
from typing import Any, Dict, List

from ioc_cfn_mas_client.client import Client


def main() -> None:
    """Run example operations against the MAS API."""

    # Initialize the client
    # API key is optional - only needed if your deployment requires authentication
    client = Client(
        base_url=os.getenv("CFN_BASE_URL", "http://localhost:9010"),
        api_key=os.getenv("CFN_API_KEY"),  # Optional
    )

    # Configuration
    workspace_id = "test_workspace"
    system_id = "test_system"

    print("=" * 70)
    print("IOC CFN MAS Client Library - Example Usage")
    print("=" * 70)

    # ========================================================================
    # Example 1: Upsert Shared Memories
    # ========================================================================
    print("\n[1] Upserting shared memories...")

    memories: List[Dict[str, Any]] = [
        {
            "id": "memory_001",
            "content": "User prefers dark mode interface",
        },
        {
            "id": "memory_002",
            "content": "Last active session: 2024-01-15 10:30 UTC",
        },
        {
            "id": "memory_003",
            "content": "Preferred programming language: Python",
        },
    ]

    try:
        upsert_response = client.upsert_shared_memories(
            workspace_id=workspace_id,
            system_id=system_id,
            memories=memories,
        )
        print(f"✓ Successfully upserted {len(memories)} memories")
        print(f"  Response: {upsert_response}")
    except Exception as e:
        print(f"✗ Error upserting memories: {e}")

    # ========================================================================
    # Example 2: Query Shared Memories
    # ========================================================================
    print("\n[2] Querying shared memories...")

    search_query = "user preferences"
    top_k = 5

    try:
        query_response = client.query_shared_memories(
            workspace_id=workspace_id,
            system_id=system_id,
            query=search_query,
            top_k=top_k,
        )
        print(f"✓ Query completed for: '{search_query}'")
        print(f"  Results (top {top_k}):")
        print(f"  {query_response}")
    except Exception as e:
        print(f"✗ Error querying memories: {e}")

    # ========================================================================
    # Example 3: Advanced Usage - Direct API Access
    # ========================================================================
    print("\n[3] Advanced: Direct API access (for power users)...")
    print("  Note: You can access the underlying OpenAPI client via:")
    print("  - client.shared_memories_api  (SharedMemoriesApi)")
    print("  - client.api_client           (ApiClient)")
    print("  - client.configuration        (Configuration)")

    print("\n" + "=" * 70)
    print("Example completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
