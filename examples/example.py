# examples/example.py
"""Example usage of the IoC CFN MAS Client Library.

This script demonstrates how to:
1. Initialize the client
2. Create/update shared memories from trace data
3. Query shared memories using natural language intent
4. Proxy memory operations to remote providers
5. Start and advance semantic negotiation sessions
"""

import os

from ioc_cfn_mas_client.client import Client


def main() -> None:
    """Run example operations against the MAS API."""

    # Initialize the client
    client = Client(
        base_url=os.getenv("CFN_BASE_URL", "http://localhost:9010"),
    )

    # Configuration
    workspace_id = "test_workspace"
    mas_id = "test_system"
    agent_id = "test_agent"

    print("=" * 70)
    print("IoC CFN MAS Client Library - Example Usage")
    print("=" * 70)

    # ========================================================================
    # Example 1: Create Shared Memories from Trace Data
    # ========================================================================
    print("\n[1] Creating shared memories from trace data...")

    trace_data = [
        {
            "TraceId": "trace-001",
            "SpanId": "span-001",
            "ParentSpanId": "",
            "SpanName": "user_login",
            "ServiceName": "auth-service",
            "SpanAttributes": {"user_id": "user123", "action": "login"},
            "Duration": 150
        },
        {
            "TraceId": "trace-001",
            "SpanId": "span-002",
            "ParentSpanId": "span-001",
            "SpanName": "validate_credentials",
            "ServiceName": "auth-service",
            "SpanAttributes": {"user_id": "user123"},
            "Duration": 50
        }
    ]

    try:
        create_response = client.create_shared_memories(
            workspace_id=workspace_id,
            mas_id=mas_id,
            data=trace_data,
            format="observe-sdk-otel",
            agent_id=agent_id,
        )
        print(f"✓ Successfully created shared memories")
        print(f"  Response: {create_response}")
    except Exception as e:
        print(f"✗ Error creating shared memories: {e}")

    # ========================================================================
    # Example 2: Query Shared Memories with Natural Language
    # ========================================================================
    print("\n[2] Querying shared memories...")

    intent = "Find information about user login events and authentication"

    try:
        query_response = client.query_shared_memories(
            workspace_id=workspace_id,
            mas_id=mas_id,
            intent=intent,
            agent_id=agent_id,
            additional_context=[
                {"context": "Looking for authentication patterns"},
                {"time_range": "last 24 hours"}
            ],
        )
        print(f"✓ Query completed for: '{intent}'")
        print(f"  Results: {query_response}")
    except Exception as e:
        print(f"✗ Error querying memories: {e}")

    # ========================================================================
    # Example 3: Memory Operations (Proxy to Remote Provider)
    # ========================================================================
    print("\n[3] Memory operations via proxy...")

    # Example 3a: GET memories from remote provider
    print("\n  [3a] Getting memories from remote provider...")
    try:
        get_response = client.memory_operation(
            workspace_id=workspace_id,
            mas_id=mas_id,
            agent_id=agent_id,
            http_method="GET",
            http_url="v1/memories/?user_id=test-user",
        )
        print(f"  ✓ GET request successful")
        print(f"    Status: {get_response.get('http_status')}")
        print(f"    Body: {get_response.get('http_response_body')}")
    except Exception as e:
        print(f"  ✗ Error with GET request: {e}")

    # Example 3b: POST memories to remote provider
    print("\n  [3b] Posting memories to remote provider...")
    try:
        post_response = client.memory_operation(
            workspace_id=workspace_id,
            mas_id=mas_id,
            agent_id=agent_id,
            http_method="POST",
            http_url="/v1/memories/",
            http_body={
                "messages": [
                    {"role": "user", "content": "I prefer dark mode in all my apps"}
                ],
                "user_id": "test-user"
            },
        )
        print(f"  ✓ POST request successful")
        print(f"    Status: {post_response.get('http_status')}")
        print(f"    Body: {post_response.get('http_response_body')}")
    except Exception as e:
        print(f"  ✗ Error with POST request: {e}")

    # ========================================================================
    # Example 4: Semantic Negotiation
    # ========================================================================
    print("\n[4] Semantic negotiation...")

    session_id = "demo-session-001"

    # Example 4a: Start negotiation
    print("\n  [4a] Starting negotiation session...")
    try:
        start_response = client.start_negotiation(
            workspace_id=workspace_id,
            mas_id=mas_id,
            session_id=session_id,
            agents=[
                {"id": "planner", "name": "Planning Agent"},
                {"id": "executor", "name": "Execution Agent"},
            ],
            content_text="Plan a deployment strategy for the new microservice",
            n_steps=5,
        )
        print(f"  ✓ Negotiation started")
        print(f"    Status: {start_response.get('status')}")
        print(f"    Message: {start_response.get('message')}")
    except Exception as e:
        print(f"  ✗ Error starting negotiation: {e}")

    # Example 4b: Advance negotiation
    print("\n  [4b] Advancing negotiation with agent replies...")
    try:
        advance_response = client.advance_negotiation(
            workspace_id=workspace_id,
            mas_id=mas_id,
            session_id=session_id,
            agent_replies=[
                {
                    "agent_id": "planner",
                    "action": "counter_offer",
                    "offer": {"strategy": "blue-green deployment"}
                },
                {
                    "agent_id": "executor",
                    "action": "accept"
                },
            ],
        )
        print(f"  ✓ Negotiation advanced")
        print(f"    Status: {advance_response.get('status')}")
        print(f"    Message: {advance_response.get('message')}")
    except Exception as e:
        print(f"  ✗ Error advancing negotiation: {e}")

    # ========================================================================
    # Example 5: Advanced Usage - Direct API Access
    # ========================================================================
    print("\n[5] Advanced: Direct API access (for power users)...")
    print("  Note: You can access the underlying OpenAPI clients via:")
    print("  - client.shared_memories_api      (SharedMemoriesApi)")
    print("  - client.memory_operations_api    (MemoryOperationsApi)")
    print("  - client.semantic_negotiation_api (SemanticNegotiationApi)")
    print("  - client.api_client               (ApiClient)")
    print("  - client.configuration            (Configuration)")

    print("\n" + "=" * 70)
    print("Example completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
