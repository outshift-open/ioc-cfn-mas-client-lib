# Copyright 2026 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

# examples/example.py
"""Example usage of L9 protocol message forwarding.

This script demonstrates how to:
1. Initialize the client
2. Forward L9 protocol messages to cognition engines
3. Handle different message kinds (intent, contingency, exchange, commit, knowledge)
"""

import os
from typing import Any, Dict

from ioc_cfn_mas_client.client import Client


def create_l9_message(
    kind: str,
    workspace_id: str,
    mas_id: str,
    payload_data: Dict[str, Any],
    subkind: str = "",
    actors: list = None,
) -> Dict[str, Any]:
    """Helper to create a properly formatted L9 message.

    Args:
        kind: Message kind (intent, contingency, exchange, commit, knowledge)
        workspace_id: Workspace UUID
        mas_id: Multi-agent system UUID
        payload_data: Message payload data
        subkind: Optional message subkind
        actors: Optional list of actor dictionaries with 'id' field

    Returns:
        L9 protocol message dictionary conforming to SSTP spec
    """
    message = {
        "header": {
            "protocol": "sstp",
            "version": "1.0",
            "subprotocol": "ioc",
            "kind": kind,
            "participants": {
                "actors": actors if actors else [],
                "groups": {
                    "workspace_id": workspace_id,
                    "mas_id": mas_id,
                }
            }
        },
        "payload": {
            "type": "application/json",
            "data": payload_data
        }
    }

    if subkind:
        message["header"]["subkind"] = subkind

    return message


def main() -> None:
    """Run L9 message forwarding examples."""

    # Initialize the client
    client = Client(
        cfn_url=os.getenv("CFN_URL", "http://localhost:9002"),
    )

    # Configuration - using UUIDs as required by the API
    workspace_id = "550e8400-e29b-41d4-a716-446655440000"
    mas_id = "660e8400-e29b-41d4-a716-446655440001"

    print("=" * 70)
    print("IoC CFN MAS Client Library - L9 Message Examples")
    print("=" * 70)

    # ========================================================================
    # Example 1: Intent Message
    # ========================================================================
    print("\n[1] Forwarding intent message...")

    intent_message = create_l9_message(
        kind="intent",
        workspace_id=workspace_id,
        mas_id=mas_id,
        payload_data={
            "intent": "Analyze the authentication flow for security vulnerabilities",
            "context": {
                "service": "auth-service",
                "priority": "high"
            }
        },
        actors=[{"id": "security-agent"}, {"id": "analyzer-agent"}]
    )

    try:
        response = client.forward_l9_message(message=intent_message)
        print(f"✓ Intent message forwarded successfully")
        print(f"  Response: {response}")
    except Exception as e:
        print(f"✗ Error forwarding intent message: {e}")

    # ========================================================================
    # Example 2: Exchange Message
    # ========================================================================
    print("\n[2] Forwarding exchange message...")

    exchange_message = create_l9_message(
        kind="exchange",
        workspace_id=workspace_id,
        mas_id=mas_id,
        subkind="proposal",
        payload_data={
            "proposal": {
                "action": "deploy",
                "strategy": "blue-green",
                "estimated_duration": "30m"
            },
            "sender": "planner-agent",
            "recipients": ["executor-agent"]
        },
        actors=[{"id": "planner-agent"}, {"id": "executor-agent"}]
    )

    try:
        response = client.forward_l9_message(message=exchange_message)
        print(f"✓ Exchange message forwarded successfully")
        print(f"  Response: {response}")
    except Exception as e:
        print(f"✗ Error forwarding exchange message: {e}")

    # ========================================================================
    # Example 3: Commit Message
    # ========================================================================
    print("\n[3] Forwarding commit message...")

    commit_message = create_l9_message(
        kind="commit",
        workspace_id=workspace_id,
        mas_id=mas_id,
        payload_data={
            "decision": "accepted",
            "commitment": {
                "action": "deploy",
                "strategy": "blue-green",
                "deadline": "2026-07-15T18:00:00Z"
            },
            "participants": ["planner-agent", "executor-agent"]
        }
    )

    try:
        response = client.forward_l9_message(message=commit_message)
        print(f"✓ Commit message forwarded successfully")
        print(f"  Response: {response}")
    except Exception as e:
        print(f"✗ Error forwarding commit message: {e}")

    # ========================================================================
    # Example 4: Knowledge Message
    # ========================================================================
    print("\n[4] Forwarding knowledge message...")

    knowledge_message = create_l9_message(
        kind="knowledge",
        workspace_id=workspace_id,
        mas_id=mas_id,
        payload_data={
            "type": "learned_pattern",
            "content": {
                "pattern": "authentication_flow_optimization",
                "description": "Learned optimal cache TTL for auth tokens",
                "parameters": {
                    "ttl": "3600s",
                    "confidence": 0.95
                }
            },
            "source": "learning-agent"
        }
    )

    try:
        response = client.forward_l9_message(message=knowledge_message)
        print(f"✓ Knowledge message forwarded successfully")
        print(f"  Response: {response}")
    except Exception as e:
        print(f"✗ Error forwarding knowledge message: {e}")

    # ========================================================================
    # Example 5: Contingency Message
    # ========================================================================
    print("\n[5] Forwarding contingency message...")

    contingency_message = create_l9_message(
        kind="contingency",
        workspace_id=workspace_id,
        mas_id=mas_id,
        payload_data={
            "trigger": "deployment_failure",
            "condition": "health_check_failed",
            "action": {
                "type": "rollback",
                "target": "previous_version",
                "automated": True
            },
            "severity": "critical"
        },
        actors=[{"id": "monitor-agent"}, {"id": "executor-agent"}]
    )

    try:
        response = client.forward_l9_message(message=contingency_message)
        print(f"✓ Contingency message forwarded successfully")
        print(f"  Response: {response}")
    except Exception as e:
        print(f"✗ Error forwarding contingency message: {e}")

    # ========================================================================
    # Example 6: Advanced - Direct API Access
    # ========================================================================
    print("\n[6] Advanced: Direct L9 API access...")
    print("  Note: For power users, you can access the underlying API via:")
    print("  - client.l9_messages_api  (L9MessagesApi)")
    print("  This gives you full control over the L9 protocol message structure.")

    print("\n" + "=" * 70)
    print("L9 Examples completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
