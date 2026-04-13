# src/ioc_cfn_mas_client/client.py

from __future__ import annotations

from typing import Any, Dict, List, Optional

from generated.api.memory_operations_api import MemoryOperationsApi
from generated.api.semantic_negotiation_api import SemanticNegotiationApi
from generated.api.shared_memories_api import SharedMemoriesApi
from generated.api_client import ApiClient
from generated.configuration import Configuration
from generated.models.cognitionagentclient_extraction_payload import CognitionagentclientExtractionPayload
from generated.models.cognitionagentclient_extraction_payload_metadata import CognitionagentclientExtractionPayloadMetadata
from generated.models.memoryoperations_memory_operation_payload import MemoryoperationsMemoryOperationPayload
from generated.models.memoryoperations_memory_operation_request import MemoryoperationsMemoryOperationRequest
from generated.models.semanticnegotiation_agent import SemanticnegotiationAgent
from generated.models.semanticnegotiation_agent_reply import SemanticnegotiationAgentReply
from generated.models.semanticnegotiation_decide_request import SemanticnegotiationDecideRequest
from generated.models.semanticnegotiation_start_request import SemanticnegotiationStartRequest
from generated.models.sharedmemory_create_or_update_request import SharedmemoryCreateOrUpdateRequest
from generated.models.sharedmemory_header import SharedmemoryHeader
from generated.models.sharedmemory_query_request import SharedmemoryQueryRequest


class Client:
    """User-friendly client for IoC CFN MAS Multi-Agent System API.

    This client provides convenient methods for interacting with the MAS API,
    wrapping the auto-generated OpenAPI client with a more intuitive interface.

    Args:
        base_url: API endpoint URL (e.g., "http://localhost:9010")
        timeout: Request timeout in seconds (default: None)
        configuration: Pre-configured Configuration object (for advanced users)
        api_client: Pre-configured ApiClient object (for advanced users)

    Example:
        >>> client = Client(base_url="http://localhost:9010")
        >>> response = client.create_shared_memories(
        ...     workspace_id="ws1",
        ...     mas_id="sys1",
        ...     data={"trace_data": [...]},
        ...     format="observe-sdk-otel"
        ... )
    """

    def __init__(
        self,
        base_url: str,
        *,
        timeout: Optional[float] = None,
        configuration: Optional[Configuration] = None,
        api_client: Optional[ApiClient] = None,
    ) -> None:
        if api_client is not None and configuration is not None:
            raise ValueError("Provide only one of api_client or configuration")

        cfg = configuration or (api_client.configuration if api_client else None) or Configuration()
        cfg.host = base_url

        self._configuration = cfg
        self._api_client = api_client or ApiClient(configuration=cfg)
        self._timeout = timeout
        self._shared_memories_api = SharedMemoriesApi(api_client=self._api_client)
        self._memory_operations_api = MemoryOperationsApi(api_client=self._api_client)
        self._semantic_negotiation_api = SemanticNegotiationApi(api_client=self._api_client)

    # ============================================================================
    # Shared Memories Operations
    # ============================================================================

    def create_shared_memories(
        self,
        workspace_id: str,
        mas_id: str,
        data: Dict[str, Any],
        format: str,
        agent_id: Optional[str] = None,
        request_id: Optional[str] = None,
    ) -> Any:
        """Create or update shared memories from trace or OpenClaw output.

        Args:
            workspace_id: The workspace identifier
            mas_id: The multi-agent system identifier
            data: The extraction payload data. Structure depends on format:
                - "observe-sdk-otel": JSON array of trace records
                - "openclaw": Opaque JSON payload
            format: Data format. Supported: "observe-sdk-otel", "openclaw"
            agent_id: Optional agent identifier
            request_id: Optional request identifier (UUID generated if not provided)

        Returns:
            API response with status and message

        Example:
            >>> response = client.create_shared_memories(
            ...     workspace_id="workspace1",
            ...     mas_id="system1",
            ...     data=[{"TraceId": "...", "SpanId": "..."}],
            ...     format="observe-sdk-otel",
            ...     agent_id="agent1"
            ... )
        """
        metadata = CognitionagentclientExtractionPayloadMetadata(format=format)
        payload = CognitionagentclientExtractionPayload(data=data, metadata=metadata)
        header = SharedmemoryHeader(agent_id=agent_id) if agent_id else None

        request = SharedmemoryCreateOrUpdateRequest(
            header=header,
            payload=payload,
            request_id=request_id
        )

        response = self._shared_memories_api.api_workspaces_workspace_id_multi_agentic_systems_mas_id_shared_memories_post_with_http_info(
            workspace_id=workspace_id,
            mas_id=mas_id,
            body=request,
        )
        return response.data

    def query_shared_memories(
        self,
        workspace_id: str,
        mas_id: str,
        intent: str,
        agent_id: str,
        additional_context: Optional[List[Dict[str, Any]]] = None,
        search_strategy: Optional[str] = None,
        request_id: Optional[str] = None,
    ) -> Any:
        """Query shared memories using natural language intent.

        Args:
            workspace_id: The workspace identifier
            mas_id: The multi-agent system identifier
            intent: Natural language query describing the information needed
            agent_id: Agent identifier (required)
            additional_context: Optional contextual information (conversation history, etc.)
            search_strategy: Search strategy (default: "semantic_graph_traversal")
            request_id: Optional request identifier (UUID generated if not provided)

        Returns:
            API response containing query results

        Example:
            >>> response = client.query_shared_memories(
            ...     workspace_id="workspace1",
            ...     mas_id="system1",
            ...     intent="Find user preferences about UI settings",
            ...     agent_id="agent1",
            ...     additional_context=[{"context": "previous conversation"}]
            ... )
        """
        header = SharedmemoryHeader(agent_id=agent_id)

        request = SharedmemoryQueryRequest(
            header=header,
            intent=intent,
            additional_context=additional_context,
            search_strategy=search_strategy,
            request_id=request_id
        )

        response = self._shared_memories_api.api_workspaces_workspace_id_multi_agentic_systems_mas_id_shared_memories_query_post_with_http_info(
            workspace_id=workspace_id,
            mas_id=mas_id,
            body=request,
        )
        return response.data

    # ============================================================================
    # Memory Operations (Proxy to Remote Providers)
    # ============================================================================

    def memory_operation(
        self,
        workspace_id: str,
        mas_id: str,
        agent_id: str,
        http_method: str,
        http_url: str,
        http_body: Optional[Dict[str, Any]] = None,
        http_headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """Proxy memory operations to remote provider (Mem0, Graphiti, etc.).

        Forwards REST API requests to a remote memory provider. The provider base URL
        and auth credentials are auto-resolved from management plane config.

        Args:
            workspace_id: The workspace identifier
            mas_id: The multi-agent system identifier
            agent_id: The agent identifier
            http_method: HTTP method (GET, POST, PUT, DELETE, etc.)
            http_url: Relative URL path with query parameters
            http_body: Optional request body
            http_headers: Optional custom headers

        Returns:
            Memory provider response with http-status, http-headers, http-response-body

        Example (GET memories):
            >>> response = client.memory_operation(
            ...     workspace_id="ws1",
            ...     mas_id="sys1",
            ...     agent_id="agent1",
            ...     http_method="GET",
            ...     http_url="v1/memories/?user_id=test-user"
            ... )

        Example (POST memories):
            >>> response = client.memory_operation(
            ...     workspace_id="ws1",
            ...     mas_id="sys1",
            ...     agent_id="agent1",
            ...     http_method="POST",
            ...     http_url="/v1/memories/",
            ...     http_body={
            ...         "messages": [{"role": "user", "content": "I prefer dark mode"}],
            ...         "user_id": "test-user"
            ...     }
            ... )
        """
        payload = MemoryoperationsMemoryOperationPayload(
            http_request_type=http_method,
            http_url=http_url,
            http_request_body=http_body or {},
            http_headers=http_headers or {}
        )

        request = MemoryoperationsMemoryOperationRequest(
            header={},
            payload=payload
        )

        response = self._memory_operations_api.api_workspaces_workspace_id_multi_agentic_systems_mas_id_agents_agent_id_memory_operations_post_with_http_info(
            workspace_id=workspace_id,
            mas_id=mas_id,
            agent_id=agent_id,
            body=request,
        )
        return response.data

    # ============================================================================
    # Semantic Negotiation
    # ============================================================================

    def start_negotiation(
        self,
        workspace_id: str,
        mas_id: str,
        session_id: str,
        agents: List[Dict[str, str]],
        content_text: str,
        n_steps: Optional[int] = None,
    ) -> Any:
        """Start a semantic negotiation session with multiple agents.

        Args:
            workspace_id: The workspace identifier
            mas_id: The multi-agent system identifier
            session_id: Client-provided session identifier (globally unique)
            agents: List of agents with 'id' and 'name' fields
            content_text: Negotiation prompt/context
            n_steps: Maximum negotiation steps (default: 20)

        Returns:
            Negotiation response with status, message, and result

        Example:
            >>> response = client.start_negotiation(
            ...     workspace_id="ws1",
            ...     mas_id="sys1",
            ...     session_id="session-123",
            ...     agents=[
            ...         {"id": "agent1", "name": "Planner Agent"},
            ...         {"id": "agent2", "name": "Executor Agent"}
            ...     ],
            ...     content_text="Plan a deployment strategy",
            ...     n_steps=10
            ... )
        """
        agent_objects = [
            SemanticnegotiationAgent(id=agent["id"], name=agent["name"])
            for agent in agents
        ]

        request = SemanticnegotiationStartRequest(
            session_id=session_id,
            agents=agent_objects,
            content_text=content_text,
            n_steps=n_steps
        )

        response = self._semantic_negotiation_api.api_workspaces_workspace_id_multi_agentic_systems_mas_id_semantic_negotiation_start_post_with_http_info(
            workspace_id=workspace_id,
            mas_id=mas_id,
            body=request,
        )
        return response.data

    def advance_negotiation(
        self,
        workspace_id: str,
        mas_id: str,
        session_id: str,
        agent_replies: List[Dict[str, Any]],
    ) -> Any:
        """Advance semantic negotiation session with agent replies.

        Args:
            workspace_id: The workspace identifier
            mas_id: The multi-agent system identifier
            session_id: Session identifier from start_negotiation
            agent_replies: List of agent replies with 'agent_id', 'action', and optional 'offer'
                - action: "accept", "reject", or "counter_offer"
                - offer: Required when action is "counter_offer"

        Returns:
            Negotiation response with status, message, and result

        Example:
            >>> response = client.advance_negotiation(
            ...     workspace_id="ws1",
            ...     mas_id="sys1",
            ...     session_id="session-123",
            ...     agent_replies=[
            ...         {"agent_id": "agent1", "action": "counter_offer", "offer": {...}},
            ...         {"agent_id": "agent2", "action": "accept"}
            ...     ]
            ... )
        """
        reply_objects = [
            SemanticnegotiationAgentReply(
                agent_id=reply["agent_id"],
                action=reply["action"],
                offer=reply.get("offer")
            )
            for reply in agent_replies
        ]

        request = SemanticnegotiationDecideRequest(
            session_id=session_id,
            agent_replies=reply_objects
        )

        response = self._semantic_negotiation_api.api_workspaces_workspace_id_multi_agentic_systems_mas_id_semantic_negotiation_decide_post_with_http_info(
            workspace_id=workspace_id,
            mas_id=mas_id,
            body=request,
        )
        return response.data

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

    @property
    def memory_operations_api(self) -> MemoryOperationsApi:
        """Direct access to the generated MemoryOperationsApi for advanced usage."""
        return self._memory_operations_api

    @property
    def semantic_negotiation_api(self) -> SemanticNegotiationApi:
        """Direct access to the generated SemanticNegotiationApi for advanced usage."""
        return self._semantic_negotiation_api

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
