# src/ioc_cfn_mas_client/client.py

from __future__ import annotations

from typing import Any, Dict, List, Optional

from generated.api.shared_memories_api import SharedMemoriesApi
from generated.api_client import ApiClient
from generated.configuration import Configuration


class Client:
    """User-friendly client for IoC CFN MAS Multi-Agent System API.

    This client provides convenient methods for interacting with the MAS API,
    wrapping the auto-generated OpenAPI client with a more intuitive interface.

    Args:
        base_url: API endpoint URL (e.g., "http://localhost:9010")
        api_key: Optional API key (not required for most deployments)
        api_key_name: Header name for API key (default: "Authorization")
        api_key_prefix: Token prefix (default: "Bearer")
        timeout: Request timeout in seconds
        debug: Enable debug logging
        configuration: Pre-configured Configuration object from generated client
        api_client: Pre-configured ApiClient object from generated client

    Example:
        >>> client = Client(base_url="http://localhost:9010")
        >>> memories = [{"id": "m1", "content": "hello world"}]
        >>> response = client.upsert_memories("ws1", "sys1", memories=memories)
    """

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        *,
        api_key_name: str = "Authorization",
        api_key_prefix: Optional[str] = "Bearer",
        timeout: Optional[float] = None,
        debug: bool = False,
        configuration: Optional[Configuration] = None,
        api_client: Optional[ApiClient] = None,
    ) -> None:
        if api_client is not None and configuration is not None:
            raise ValueError("Provide only one of api_client or configuration")

        cfg = configuration or (api_client.configuration if api_client else None) or Configuration()
        cfg.host = base_url
        cfg.debug = bool(debug)

        if api_key:
            cfg.api_key[api_key_name] = api_key
            if api_key_prefix:
                cfg.api_key_prefix[api_key_name] = api_key_prefix

        self._configuration = cfg
        self._api_client = api_client or ApiClient(configuration=cfg)
        self._timeout = timeout
        self._shared_memories_api = SharedMemoriesApi(api_client=self._api_client)

    # ============================================================================
    # Shared Memories Operations
    # ============================================================================

    def upsert_memories(
        self,
        workspace_id: str,
        system_id: str,
        memories: Optional[List[Dict[str, Any]]] = None,
        relationships: Optional[List[Dict[str, Any]]] = None,
    ) -> Any:
        """Upsert (insert or update) shared memories and relationships for a multi-agent system.

        Args:
            workspace_id: The workspace identifier
            system_id: The multi-agent system identifier
            memories: List of memory objects to upsert. Each memory should contain
                     at least 'id' and 'content' fields.
            relationships: List of relationship objects to upsert between memories.

        Returns:
            API response with upsert results containing status and message

        Example:
            >>> memories = [
            ...     {"id": "m1", "content": "User prefers dark mode"},
            ...     {"id": "m2", "content": "Last login: 2024-01-15"}
            ... ]
            >>> relationships = [
            ...     {"source": "m1", "target": "m2", "type": "related_to"}
            ... ]
            >>> response = client.upsert_memories(
            ...     workspace_id="workspace1",
            ...     system_id="system1",
            ...     memories=memories,
            ...     relationships=relationships
            ... )
        """
        body: Dict[str, Any] = {}
        if memories is not None:
            body["memories"] = memories
        if relationships is not None:
            body["relationships"] = relationships

        if not body:
            raise ValueError("At least one of 'memories' or 'relationships' must be provided")

        response = self._shared_memories_api.api_workspaces_workspace_id_multi_agentic_systems_system_id_shared_memories_post_with_http_info(
            workspace_id=workspace_id,
            system_id=system_id,
            body=body,
        )
        return response.data  # Return data from ApiResponse object

    def search_memories(
        self,
        workspace_id: str,
        system_id: str,
        query: str,
        top_k: int = 5,
    ) -> Any:
        """Search shared memories using semantic similarity.

        Args:
            workspace_id: The workspace identifier
            system_id: The multi-agent system identifier
            query: Search query string for semantic matching
            top_k: Maximum number of results to return (default: 5)

        Returns:
            API response containing matching memories ranked by relevance

        Example:
            >>> results = client.search_memories(
            ...     workspace_id="workspace1",
            ...     system_id="system1",
            ...     query="user preferences",
            ...     top_k=10
            ... )
        """
        body = {"query": query, "topK": top_k}
        response = self._shared_memories_api.api_workspaces_workspace_id_multi_agentic_systems_system_id_shared_memories_query_post_with_http_info(
            workspace_id=workspace_id,
            system_id=system_id,
            body=body,
        )
        return response.data  # Return data from ApiResponse object

    # ============================================================================
    # Advanced Access (for power users)
    # ============================================================================

    @property
    def configuration(self) -> Configuration:
        """Access the underlying OpenAPI configuration."""
        return self._configuration

    @property
    def api_client(self) -> ApiClient:
        """Access the underlying OpenAPI client."""
        return self._api_client

    @property
    def shared_memories_api(self) -> SharedMemoriesApi:
        """Direct access to the generated SharedMemoriesApi for advanced usage."""
        return self._shared_memories_api

    def request(
        self,
        method: str,
        path: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        body: Optional[Any] = None,
        timeout: Optional[float] = None,
    ) -> bytes:
        """Make a raw HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API path (must start with '/')
            headers: Optional HTTP headers
            body: Optional request body
            timeout: Optional request timeout (overrides client default)

        Returns:
            Response data as bytes

        Raises:
            ValueError: If path doesn't start with '/'
        """
        if not path.startswith("/"):
            raise ValueError("path must start with '/'")

        resp = self._api_client.call_api(
            method.upper(),
            path,
            header_params=headers or {},
            body=body,
            _request_timeout=self._timeout if timeout is None else timeout,
        )
        resp.read()
        return resp.data  # type: ignore[no-any-return]
