# Copyright 2026 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

# examples/mcp/client_example.py
"""Example usage of the IoC CFN MAS Client Library MCP methods.

Run with: uv run python examples/mcp/client_example.py

This script demonstrates how to:
1. Initialize the client
2. Use retain method to store shared memories
3. Use recall method to query shared memories
4. Handle responses and errors
"""

import asyncio
import os

from ioc_cfn_mas_client.client import Client


async def main() -> None:
    """Run example MCP operations against the MAS API."""

    # Initialize the client
    client = Client(
        cfn_url=os.getenv("CFN_URL", "http://localhost:9002"),
    )

    # Configuration
    workspace_id = "mcp_test_workspace"
    mas_id = "mcp_test_system"
    agent_id = "mcp_test_agent"

    print("=" * 70)
    print("IoC CFN MAS Client Library - MCP Methods Example")
    print("=" * 70)

    try:
        # ========================================================================
        # Example 1: Retain Shared Memories
        # ========================================================================
        print("\n[1] Retaining shared memories...")

        # Example payload with OpenClaw conversation format
        retain_payload = {
            "metadata": {
                "format": "openclaw"
            },
            "data": [
                {
                    "schema": "openclaw-conversation-v1",
                    "extractedAt": "2026-04-20T21:00:00.000Z",
                    "session": {
                        "agentId": "example-agent",
                        "sessionId": "session-123",
                        "sessionKey": "agent:example:test:session",
                        "channel": "api",
                        "cwd": "/workspace"
                    },
                    "stats": {
                        "totalEntries": 2,
                        "turns": 1,
                        "toolCallCount": 1,
                        "thinkingTurnCount": 0,
                        "totalCost": 0
                    },
                    "turns": [
                        {
                            "index": 0,
                            "timestamp": "2026-04-20T21:00:00.000Z",
                            "model": "test-model",
                            "stopReason": "stop",
                            "usage": {
                                "input": 50,
                                "output": 100,
                                "totalTokens": 150,
                                "cost": {"total": 0}
                            },
                            "userMessage": "Example user message for MCP retain",
                            "thinking": None,
                            "toolCalls": [
                                {
                                    "id": "tool_example_123",
                                    "name": "example_tool",
                                    "input": {"query": "test"},
                                    "result": "Example tool result",
                                    "isError": False
                                }
                            ],
                            "response": "Example agent response for MCP retain operation"
                        }
                    ]
                }
            ]
        }

        try:
            retain_response = await client.retain(
                workspace_id=workspace_id,
                mas_id=mas_id,
                payload=retain_payload,
                agent_id=agent_id,
                request_id="example-retain-001"
            )
            print(f"  ✓ Retain operation successful")
            print(f"    Response ID: {retain_response.get('response_id')}")
            print(f"    Status: {retain_response.get('status')}")
            print(f"    Message: {retain_response.get('message')}")
            print(f"    Nodes Saved: {retain_response.get('nodes_saved')}")
            print(f"    Edges Saved: {retain_response.get('edges_saved')}")
        except Exception as e:
            print(f"  ✗ Error with retain operation: {e}")

        # ========================================================================
        # Example 2: Recall Shared Memories
        # ========================================================================
        print("\n[2] Recalling shared memories...")

        try:
            recall_response = await client.recall(
                workspace_id=workspace_id,
                mas_id=mas_id,
                intent="Find information about example tool usage",
                search_strategy="semantic_graph_traversal",
                agent_id=agent_id,
                request_id="example-recall-001"
            )
            print(f"  ✓ Recall operation successful")
            print(f"    Response ID: {recall_response.get('response_id')}")
            print(f"    Message: {recall_response.get('message')}")
            print(f"    Search Strategy: {recall_response.get('search_strategy')}")
            print(f"    Results Found: {recall_response.get('results_found')}")
            print(f"    Confidence Score: {recall_response.get('confidence_score')}")
        except Exception as e:
            print(f"  ✗ Error with recall operation: {e}")

        # ========================================================================
        # Example 3: Recall with Additional Context
        # ========================================================================
        print("\n[3] Recalling with additional context...")

        additional_context = [
            {"context_type": "previous_session", "session_id": "session-122"},
            {"context_type": "user_preference", "preference": "detailed_responses"}
        ]

        try:
            recall_with_context = await client.recall(
                workspace_id=workspace_id,
                mas_id=mas_id,
                intent="What are the user's preferences for tool interactions?",
                search_strategy="semantic_graph_traversal",
                agent_id=agent_id,
                additional_context=additional_context,
                request_id="example-recall-002"
            )
            print(f"  ✓ Recall with context successful")
            print(f"    Response ID: {recall_with_context.get('response_id')}")
            print(f"    Message: {recall_with_context.get('message')}")
            print(f"    Results Found: {recall_with_context.get('results_found')}")
        except Exception as e:
            print(f"  ✗ Error with contextual recall: {e}")

        # ========================================================================
        # Example 4: Multiple Retain Operations
        # ========================================================================
        print("\n[4] Multiple retain operations...")

        for i in range(3):
            try:
                multi_payload = {
                    "metadata": {"format": "openclaw"},
                    "data": [{
                        "schema": "openclaw-conversation-v1",
                        "extractedAt": "2026-04-20T21:00:00.000Z",
                        "session": {
                            "agentId": f"agent-{i}",
                            "sessionId": f"multi-session-{i}",
                            "sessionKey": f"agent:multi:session:{i}",
                            "channel": "batch",
                            "cwd": "/workspace"
                        },
                        "stats": {"totalEntries": 1, "turns": 1},
                        "turns": [{
                            "index": 0,
                            "timestamp": "2026-04-20T21:00:00.000Z",
                            "userMessage": f"Batch message {i}",
                            "response": f"Batch response {i}"
                        }]
                    }]
                }

                multi_response = await client.retain(
                    workspace_id=workspace_id,
                    mas_id=mas_id,
                    payload=multi_payload,
                    agent_id=f"batch-agent-{i}",
                    request_id=f"batch-retain-{i:03d}"
                )
                print(f"  ✓ Batch retain {i+1}/3 successful - {multi_response.get('status')}")
            except Exception as e:
                print(f"  ✗ Error with batch retain {i+1}: {e}")

        # ========================================================================
        # Example 5: Query Different Intents
        # ========================================================================
        print("\n[5] Querying different intents...")

        intents = [
            "What tools were used in recent sessions?",
            "Find conversations about user preferences",
            "Show me error patterns from tool calls"
        ]

        for idx, intent in enumerate(intents):
            try:
                intent_response = await client.recall(
                    workspace_id=workspace_id,
                    mas_id=mas_id,
                    intent=intent,
                    agent_id=agent_id,
                    request_id=f"intent-query-{idx:03d}"
                )
                print(f"  ✓ Intent {idx+1}: '{intent[:30]}...'")
                print(f"    Results: {intent_response.get('results_found')}, "
                      f"Confidence: {intent_response.get('confidence_score')}")
            except Exception as e:
                print(f"  ✗ Error with intent {idx+1}: {e}")

    finally:
        # Clean up - Client doesn't require explicit cleanup
        pass

    print("\n" + "=" * 70)
    print("MCP Client Example Complete")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
