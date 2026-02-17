"""Simple Management Plane API client functions.

These functions provide direct access to Management Plane APIs for listing
workspaces and multi-agentic systems.
"""

import json
import urllib.request
from typing import Any, Dict, Optional
from urllib.error import HTTPError


def list_workspaces(
    mgmt_base_url: str,
    api_key: str,
    timeout: Optional[float] = None,
) -> Dict[str, Any]:
    """List workspaces from Management Plane.

    Args:
        mgmt_base_url: Management Plane base URL (e.g., "http://localhost:8080")
        api_key: API key for X-API-Key header authentication
        timeout: Optional request timeout in seconds

    Returns:
        Response dict with 'workspaces' list and 'total' count

    Raises:
        HTTPError: If the API returns an error status
        URLError: If there's a network error

    Example:
        >>> result = list_workspaces(
        ...     mgmt_base_url="http://localhost:8080",
        ...     api_key="your-api-key"
        ... )
        >>> for ws in result['workspaces']:
        ...     print(ws['id'], ws['name'])
    """
    url = f"{mgmt_base_url.rstrip('/')}/api/workspaces/"
    req = urllib.request.Request(url, headers={"X-API-Key": api_key})

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = response.read()
            return json.loads(data.decode("utf-8"))
    except HTTPError as e:
        # Re-raise with more context
        error_body = e.read().decode("utf-8") if e.fp else ""
        raise HTTPError(
            e.url,
            e.code,
            f"Failed to list workspaces: {e.reason}. {error_body}",
            e.hdrs,
            e.fp,
        )


def list_mas(
    mgmt_base_url: str,
    api_key: str,
    workspace_id: str,
    timeout: Optional[float] = None,
) -> Dict[str, Any]:
    """List multi-agentic systems in a workspace from Management Plane.

    Args:
        mgmt_base_url: Management Plane base URL (e.g., "http://localhost:8080")
        api_key: API key for X-API-Key header authentication
        workspace_id: UUID of the workspace
        timeout: Optional request timeout in seconds

    Returns:
        Response dict with 'systems' list and 'total' count

    Raises:
        HTTPError: If the API returns an error status
        URLError: If there's a network error

    Example:
        >>> result = list_mas(
        ...     mgmt_base_url="http://localhost:8080",
        ...     api_key="your-api-key",
        ...     workspace_id="workspace-uuid"
        ... )
        >>> for mas in result['systems']:
        ...     print(mas['id'], mas['name'])
    """
    url = f"{mgmt_base_url.rstrip('/')}/api/workspaces/{workspace_id}/multi-agentic-systems"
    req = urllib.request.Request(url, headers={"X-API-Key": api_key})

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = response.read()
            return json.loads(data.decode("utf-8"))
    except HTTPError as e:
        # Re-raise with more context
        error_body = e.read().decode("utf-8") if e.fp else ""
        raise HTTPError(
            e.url,
            e.code,
            f"Failed to list MAS: {e.reason}. {error_body}",
            e.hdrs,
            e.fp,
        )
