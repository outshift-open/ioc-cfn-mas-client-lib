# Copyright 2026 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

# examples/example.py
"""Example usage of L9 protocol message forwarding.

This script demonstrates how to:
1. Initialize the client
2. Forward L9 protocol messages to cognition engines using real subprotocols
3. Handle different message kinds and subprotocols (TFP, CIP, SIEP)
"""

import os
from typing import Any, Dict

from ioc_cfn_mas_client.client import Client


def create_l9_message(
    kind: str,
    subprotocol: str,
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
        subprotocol: Subprotocol identifier (TFP, CIP, SIEP, etc.)
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
            "subprotocol": subprotocol,
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
    # Example 1: TFP (Team Formation via Polling) - Intent Message
    # ========================================================================
    print("\n[1] Forwarding TFP intent message (poll_open)...")

    tfp_intent = create_l9_message(
        kind="intent",
        subprotocol="TFP",
        subkind="team-formation",
        workspace_id=workspace_id,
        mas_id=mas_id,
        payload_data={
            "operation": "poll_open",
            "poll_id": "urn:ioc:tfp:poll:example-001",
            "task": {
                "task_id": "incident-2026-001",
                "description": "Investigate authentication service outage",
                "objective": "Identify root cause within 1 hour"
            },
            "required_skills": [
                {
                    "skill": "skill:debugging",
                    "min_proficiency": 0.7,
                    "weight": 2.0,
                    "mandatory": True
                },
                {
                    "skill": "skill:auth_systems",
                    "min_proficiency": 0.6,
                    "weight": 1.5,
                    "mandatory": True
                }
            ],
            "reasoning_summary": "Need debugging and auth systems expertise"
        },
        actors=[
            {"id": "team-coordinator", "role": "sender"}
        ],
        payload_type="json-schema"
    )

    try:
        response = client.forward_l9_message(message=tfp_intent)
        print(f"✓ TFP intent message forwarded successfully")
        print(f"  Response: {response}")
    except Exception as e:
        print(f"✗ Error forwarding TFP intent message: {e}")

    # ========================================================================
    # Example 2: TFP - Exchange Message (bid)
    # ========================================================================
    print("\n[2] Forwarding TFP exchange message (bid)...")

    tfp_exchange = create_l9_message(
        kind="exchange",
        subprotocol="TFP",
        subkind="team-formation",
        workspace_id=workspace_id,
        mas_id=mas_id,
        payload_data={
            "operation": "bid",
            "poll_id": "urn:ioc:tfp:poll:example-001",
            "offer": {
                "skills": [
                    {
                        "skill": "skill:debugging",
                        "proficiency": 0.85
                    },
                    {
                        "skill": "skill:auth_systems",
                        "proficiency": 0.75
                    }
                ],
                "fit_score": 0.8
            },
            "reasoning_summary": "Strong match for debugging and auth systems"
        },
        actors=[
            {"id": "senior-engineer-agent", "role": "sender"},
            {"id": "team-coordinator", "role": "receiver"}
        ],
        payload_type="json-schema"
    )

    try:
        response = client.forward_l9_message(message=tfp_exchange)
        print(f"✓ TFP exchange message forwarded successfully")
        print(f"  Response: {response}")
    except Exception as e:
        print(f"✗ Error forwarding TFP exchange message: {e}")

    # ========================================================================
    # Example 3: CIP (Contingency Interaction Protocol) - Contingency Message
    # ========================================================================
    print("\n[3] Forwarding CIP contingency message...")

    cip_contingency = create_l9_message(
        kind="contingency",
        subprotocol="CIP",
        workspace_id=workspace_id,
        mas_id=mas_id,
        payload_data={
            "utterance": {
                "text": "repair_required:reason=ambiguous_scope:target=msg-auth-analysis",
                "evidence": [],
                "addresses_evidence": [],
                "ring_round": 0
            },
            "grounding": {
                "contingency_verified": False,
                "contingency_score": 0.0,
                "repair_reason": "ambiguous_scope",
                "challenges": [
                    "concept:authentication_scope",
                    "urn:concept:auth:oauth2_vs_jwt"
                ]
            },
            "belief": {
                "prior": 0.5,
                "posterior": 0.5,
                "revision_cause": None
            }
        },
        actors=[
            {"id": "grounding-agent", "role": "sender"},
            {"id": "senior-engineer-agent", "role": "receiver"}
        ],
        payload_type="cip"
    )

    try:
        response = client.forward_l9_message(message=cip_contingency)
        print(f"✓ CIP contingency message forwarded successfully")
        print(f"  Response: {response}")
    except Exception as e:
        print(f"✗ Error forwarding CIP contingency message: {e}")

    # ========================================================================
    # Example 4: SIEP (Semantic Interaction Exchange Protocol) - Exchange Message
    # ========================================================================
    print("\n[4] Forwarding SIEP exchange message...")

    siep_exchange = create_l9_message(
        kind="exchange",
        subprotocol="SIEP",
        workspace_id=workspace_id,
        mas_id=mas_id,
        payload_data={
            "utterance": {
                "text": "The root cause is a race condition in the token refresh logic",
                "evidence": ["log:auth-service:line-442", "trace:span-id-7721"],
                "addresses_evidence": [],
                "ring_round": 1
            },
            "grounding": {
                "contingency_verified": None,
                "contingency_score": None,
                "repair_reason": None,
                "challenges": []
            },
            "belief": {
                "prior": 0.5,
                "posterior": 0.82,
                "revision_cause": "evidence_accumulation"
            }
        },
        actors=[
            {"id": "senior-engineer-agent", "role": "sender"},
            {"id": "team-coordinator", "role": "receiver"}
        ],
        payload_type="siep"
    )

    try:
        response = client.forward_l9_message(message=siep_exchange)
        print(f"✓ SIEP exchange message forwarded successfully")
        print(f"  Response: {response}")
    except Exception as e:
        print(f"✗ Error forwarding SIEP exchange message: {e}")

    # ========================================================================
    # Example 5: TFP - Commit Message (converged)
    # ========================================================================
    print("\n[5] Forwarding TFP commit message...")

    tfp_commit = create_l9_message(
        kind="commit",
        subprotocol="TFP",
        subkind="converged",
        workspace_id=workspace_id,
        mas_id=mas_id,
        payload_data={
            "operation": "select",
            "poll_id": "urn:ioc:tfp:poll:example-001",
            "selection": {
                "members": ["senior-engineer-agent", "auth-specialist-agent"],
                "roles": [
                    {
                        "agent_id": "senior-engineer-agent",
                        "role": "lead",
                        "responsible_for": ["skill:debugging", "skill:auth_systems"]
                    },
                    {
                        "agent_id": "auth-specialist-agent",
                        "role": "contributor",
                        "responsible_for": ["skill:auth_systems"]
                    }
                ],
                "coverage": 1.0,
                "unmet_skills": [],
                "aggregate_fit": 0.85
            },
            "reasoning_summary": "Team formed with full coverage of required skills"
        },
        actors=[
            {"id": "team-coordinator", "role": "sender"}
        ],
        payload_type="json-schema"
    )

    try:
        response = client.forward_l9_message(message=tfp_commit)
        print(f"✓ TFP commit message forwarded successfully")
        print(f"  Response: {response}")
    except Exception as e:
        print(f"✗ Error forwarding TFP commit message: {e}")

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
