"""L8 (A2A/MCP) to L9 converter."""
from typing import Dict, Any
from datetime import datetime, timezone


def a2a_to_l9(a2a_body: Dict[str, Any], direction: str, actor_id: str) -> Dict[str, Any]:
    """Convert A2A message to L9 format.

    Args:
        a2a_body: Original A2A message body
        direction: "outbound" or "inbound"
        actor_id: Agent identifier

    Returns:
        L9-formatted message
    """
    return {
        "header": {
            "direction": direction,
            "actor_id": actor_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        "payload": {
            "a2a": a2a_body
        }
    }


def mcp_to_l9(mcp_body: Dict[str, Any], direction: str, actor_id: str) -> Dict[str, Any]:
    """Convert MCP message to L9 format.

    Args:
        mcp_body: Original MCP message body
        direction: "outbound" or "inbound"
        actor_id: Agent identifier

    Returns:
        L9-formatted message
    """
    return {
        "header": {
            "direction": direction,
            "actor_id": actor_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        "payload": {
            "mcp": mcp_body
        }
    }
