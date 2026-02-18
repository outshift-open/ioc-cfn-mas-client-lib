# examples/example.py
"""Example usage of the IoC CFN MAS Client Library.

This script demonstrates how to:
1. Initialize the client
2. Upsert memories with relationships
3. Search shared memories using semantic similarity
"""

import os
from typing import Any, Dict, List

from ioc_cfn_mas_client.client import Client


def main() -> None:
    """Run example operations against the MAS API."""

    # Initialize the client (API key not required for standard deployments)
    client = Client(
        base_url=os.getenv("CFN_BASE_URL", "http://localhost:9010"),
    )

    # Configuration
    workspace_id = "test_workspace"
    system_id = "test_system"

    print("=" * 70)
    print("IoC CFN MAS Client Library - Example Usage")
    print("=" * 70)

    # ========================================================================
    # Example 1: Upsert Memories with Relationships
    # ========================================================================
    print("\n[1] Upserting memories with relationships...")

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

    relationships: List[Dict[str, Any]] = [
        {
            "source": "memory_001",
            "target": "memory_002",
            "type": "related_to",
        },
    ]

    try:
        upsert_response = client.upsert_memories(
            workspace_id=workspace_id,
            system_id=system_id,
            memories=memories,
            relationships=relationships,
        )
        print(f"✓ Successfully upserted {len(memories)} memories and {len(relationships)} relationships")
        print(f"  Response: {upsert_response}")
    except Exception as e:
        print(f"✗ Error upserting memories: {e}")

    # ========================================================================
    # Example 2: Search Memories
    # ========================================================================
    print("\n[2] Searching shared memories...")

    search_query = "user preferences"
    top_k = 5

    try:
        search_results = client.search_memories(
            workspace_id=workspace_id,
            system_id=system_id,
            query=search_query,
            top_k=top_k,
        )
        print(f"✓ Search completed for: '{search_query}'")
        print(f"  Results (top {top_k}):")
        print(f"  {search_results}")
    except Exception as e:
        print(f"✗ Error searching memories: {e}")

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
