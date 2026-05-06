"""L8 (A2A/MCP) to L9 converter.

Converts L8 protocol messages (A2A, MCP) to L9 format for CFN validation.
L9 format includes a header with metadata and a payload with the original protocol message.
"""
from datetime import datetime, timezone
from typing import Any, Dict


def a2a_to_l9(
    a2a_body: Dict[str, Any],
    direction: str,
    actor_id: str,
    source: str = None,
    destination: str = None,
    sidecar_id: str = None
) -> Dict[str, Any]:
    """Convert A2A message to L9 format.

    Args:
        a2a_body: Original A2A message body
        direction: "outbound" or "inbound"
        actor_id: Agent identifier
        source: Source IP:port (optional)
        destination: Destination IP:port (optional)
        sidecar_id: Sidecar identifier (optional)

    Returns:
        L9-formatted message
    """
    header = {
        "direction": direction,
        "actor_id": actor_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    # Add optional metadata
    if source:
        header["source"] = source
    if destination:
        header["destination"] = destination
    if sidecar_id:
        header["sidecar_id"] = sidecar_id

    return {
        "header": header,
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
