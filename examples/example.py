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
    payload_type: str = "application/json",
) -> Dict[str, Any]:
    """Helper to create a properly formatted L9 message.

    Args:
        kind: Message kind (intent, contingency, exchange, commit, knowledge)
        workspace_id: Workspace UUID
        mas_id: Multi-agent system UUID
        payload_data: Message payload data
        subkind: Optional message subkind
        actors: Optional list of actor dictionaries with 'id' and 'role' fields
        payload_type: Payload MIME type (default: application/json)

    Returns:
        L9 protocol message dictionary conforming to SSTP spec
    """
    # Default actors if none provided
    if actors is None:
        actors = [{"id": "system-agent", "role": "sender"}]

    message = {
        "header": {
            "protocol": "sstp",
            "version": "1.0",
            "subprotocol": "ioc",
            "kind": kind,
            "participants": {
                "actors": actors,
                "groups": {
                    "workspace_id": workspace_id,
                    "mas_id": mas_id,
                }
            }
        },
        "payload": {
            "type": payload_type,
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
            "operation": "analyze_security",
            "target": "authentication_flow",
            "parameters": {
                "service": "auth-service",
                "priority": "high",
                "scope": ["oauth2", "jwt", "session_management"]
            }
        },
        actors=[
            {"id": "security-analyzer-agent", "role": "sender"},
            {"id": "auth-service-agent", "role": "receiver"}
        ]
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
        payload_data={
            "operation": "share_analysis_results",
            "results": {
                "vulnerabilities_found": 3,
                "severity": "medium",
                "recommendations": [
                    "Implement rate limiting on login endpoint",
                    "Add CSRF token validation",
                    "Enable session timeout"
                ]
            },
            "metadata": {
                "analysis_id": "sec-2026-001",
                "timestamp": "2026-07-15T10:30:00Z"
            }
        },
        actors=[
            {"id": "security-analyzer-agent", "role": "sender"},
            {"id": "remediation-agent", "role": "receiver"}
        ]
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
            "operation": "commit_remediation_plan",
            "decision": "approved",
            "commitment": {
                "plan_id": "rem-2026-001",
                "actions": [
                    "Deploy rate limiter to auth service",
                    "Enable CSRF protection",
                    "Configure 30-minute session timeout"
                ],
                "schedule": {
                    "start": "2026-07-15T14:00:00Z",
                    "estimated_completion": "2026-07-15T16:00:00Z"
                }
            },
            "approvers": ["security-analyzer-agent", "ops-lead-agent"]
        },
        actors=[
            {"id": "remediation-agent", "role": "sender"},
            {"id": "deployment-agent", "role": "receiver"}
        ]
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
