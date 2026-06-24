# Copyright 2026 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

# src/ioc_cfn_mas_client/client.py

from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional

from generated.api.memory_operations_api import MemoryOperationsApi
from generated.api.semantic_alignment_api import SemanticAlignmentApi
from generated.api.shared_memories_api import SharedMemoriesApi
from generated.api_client import ApiClient
from generated.configuration import Configuration
from generated.models.agent import Agent
from generated.models.agent_reply import AgentReply
from generated.models.create_or_update_request import CreateOrUpdateRequest
from generated.models.decide_request import DecideRequest
from generated.models.extraction_payload import ExtractionPayload
from generated.models.extraction_payload_metadata import ExtractionPayloadMetadata
from generated.models.header import Header
from generated.models.memory_operation_payload import MemoryOperationPayload
from generated.models.memory_operation_request import MemoryOperationRequest
from generated.models.query_request import QueryRequest
from generated.models.start_request import StartRequest


class Client:
    """User-friendly client for IoC CFN MAS Multi-Agent System API.

    This client provides convenient methods for interacting with the MAS API,
    wrapping the auto-generated OpenAPI client with a more intuitive interface.

    Args:
        cfn_url: CFN API endpoint URL (e.g., "http://localhost:9002")
        timeout: Request timeout in seconds (default: None)
        configuration: Pre-configured Configuration object (for advanced users)
        api_client: Pre-configured ApiClient object (for advanced users)

    Example:
        >>> client = Client(cfn_url="http://localhost:9002")
        >>> response = client.create_shared_memories(
        ...     workspace_id="ws1",
        ...     mas_id="sys1",
        ...     data={"trace_data": [...]},
        ...     format="observe-sdk-otel"
        ... )
    """

    def __init__(
        self,
        cfn_url: str,
        *,
        timeout: Optional[float] = None,
        configuration: Optional[Configuration] = None,
        api_client: Optional[ApiClient] = None,
    ) -> None:
        if api_client is not None and configuration is not None:
            raise ValueError("Provide only one of api_client or configuration")

        cfg = configuration or (api_client.configuration if api_client else None) or Configuration()
        cfg.host = cfn_url

        self._configuration = cfg
        self._api_client = api_client or ApiClient(configuration=cfg)
        self._timeout = timeout
        self._shared_memories_api = SharedMemoriesApi(api_client=self._api_client)
        self._memory_operations_api = MemoryOperationsApi(api_client=self._api_client)
        self._semantic_alignment_api = SemanticAlignmentApi(api_client=self._api_client)

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
        metadata = ExtractionPayloadMetadata(format=format)
        payload = ExtractionPayload(data=data, metadata=metadata)
        header = Header(agent_id=agent_id) if agent_id else None

        request = CreateOrUpdateRequest(
            header=header,
            payload=payload,
            request_id=request_id
        )

        return self._shared_memories_api.create_or_update_shared_memories(
            workspace_id=workspace_id,
            mas_id=mas_id,
            create_or_update_request=request,
        )

    async def create_shared_memories_async(
        self,
        workspace_id: str,
        mas_id: str,
        data: Dict[str, Any],
        format: str,
        agent_id: Optional[str] = None,
        request_id: Optional[str] = None,
    ) -> Any:
        """Async version of create_shared_memories.

        Runs the synchronous SDK call in a thread pool to avoid blocking
        the event loop.

        Args:
            Same as create_shared_memories()

        Returns:
            API response with status and message
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.create_shared_memories(
                workspace_id=workspace_id,
                mas_id=mas_id,
                data=data,
                format=format,
                agent_id=agent_id,
                request_id=request_id,
            )
        )

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
        header = Header(agent_id=agent_id)

        request = QueryRequest(
            header=header,
            intent=intent,
            additional_context=additional_context,
            search_strategy=search_strategy,
            request_id=request_id
        )

        return self._shared_memories_api.fetch_shared_memories(
            workspace_id=workspace_id,
            mas_id=mas_id,
            query_request=request,
        )

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
        payload = MemoryOperationPayload(
            http_request_type=http_method,
            http_url=http_url,
            http_request_body=http_body or {},
            http_headers=http_headers or {}
        )

        request = MemoryOperationRequest(
            header={},
            payload=payload
        )

        return self._memory_operations_api.memory_operations(
            workspace_id=workspace_id,
            mas_id=mas_id,
            agent_id=agent_id,
            memory_operation_request=request,
        )

    # ============================================================================
    # Semantic Alignment
    # ============================================================================

    def start_alignment(
        self,
        workspace_id: str,
        mas_id: str,
        session_id: str,
        agents: List[Dict[str, str]],
        content_text: str,
        n_steps: Optional[int] = None,
    ) -> Any:
        """Start a semantic alignment session with multiple agents.

        Args:
            workspace_id: The workspace identifier
            mas_id: The multi-agent system identifier
            session_id: Client-provided session identifier (globally unique)
            agents: List of agents with 'id' and 'name' fields
            content_text: Alignment prompt/context
            n_steps: Maximum alignment steps (default: 20)

        Returns:
            Alignment response with status, message, and result

        Example:
            >>> response = client.start_alignment(
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
            Agent(id=agent["id"], name=agent["name"])
            for agent in agents
        ]

        request = StartRequest(
            session_id=session_id,
            agents=agent_objects,
            content_text=content_text,
            n_steps=n_steps
        )

        return self._semantic_alignment_api.start_semantic_alignment(
            workspace_id=workspace_id,
            mas_id=mas_id,
            start_request=request,
        )

    def advance_alignment(
        self,
        workspace_id: str,
        mas_id: str,
        session_id: str,
        agent_replies: List[Dict[str, Any]],
    ) -> Any:
        """Advance semantic alignment session with agent replies.

        Args:
            workspace_id: The workspace identifier
            mas_id: The multi-agent system identifier
            session_id: Session identifier from start_alignment
            agent_replies: List of agent replies with 'agent_id', 'action', and optional 'offer'
                - action: "accept", "reject", or "counter_offer"
                - offer: Required when action is "counter_offer"

        Returns:
            Alignment response with status, message, and result

        Example:
            >>> response = client.advance_alignment(
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
            AgentReply(
                agent_id=reply["agent_id"],
                action=reply["action"],
                offer=reply.get("offer")
            )
            for reply in agent_replies
        ]

        request = DecideRequest(
            session_id=session_id,
            agent_replies=reply_objects
        )

        return self._semantic_alignment_api.decide_semantic_alignment(
            workspace_id=workspace_id,
            mas_id=mas_id,
            decide_request=request,
        )

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
    def semantic_alignment_api(self) -> SemanticAlignmentApi:
        """Direct access to the generated SemanticAlignmentApi for advanced usage."""
        return self._semantic_alignment_api

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

    def log_a2a_interaction(
        self,
        workspace_id: str,
        mas_id: str,
        agent_id: str,
        interaction_type: str,
        data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Log A2A interaction to CFN (mock endpoint for testing).

        This is a lightweight endpoint for testing instrumentation without
        actually storing data in shared memory.

        Args:
            workspace_id: Workspace identifier
            mas_id: Multi-agent system identifier
            agent_id: Agent identifier
            interaction_type: Type of interaction ("message", "task_completion")
            data: Interaction data

        Returns:
            Dict with acknowledgment

        Example:
            >>> client.log_a2a_interaction(
            ...     workspace_id="ws1",
            ...     mas_id="mas1",
            ...     agent_id="agent-a",
            ...     interaction_type="message",
            ...     data={"text": "Hello"}
            ... )
            {'status': 'logged', 'workspace_id': 'ws1', ...}
        """
        # For now, just log and return success
        # In production, this could call a real CFN endpoint
        return {
            "status": "logged",
            "workspace_id": workspace_id,
            "mas_id": mas_id,
            "agent_id": agent_id,
            "interaction_type": interaction_type,
            "data_size": len(str(data)),
        }

    async def retain(
        self,
        workspace_id: str,
        mas_id: str,
        payload: Dict[str, Any],
        request_id: Optional[str] = None,
        agent_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retain shared memories using MCP client logic with mock response.
        In production, this could call a real CFN endpoint.

        Args:
            workspace_id: Workspace identifier
            mas_id: Multi-agent system identifier  
            payload: Data payload to retain (OpenClaw conversation format)
            request_id: Optional request identifier
            agent_id: Optional agent identifier
            
        Returns:
            Dict with retain operation result
            
        Example:
            >>> await client.retain(
            ...     workspace_id="my-workspace",
            ...     mas_id="my-mas",
            ...     payload={"data": "example"}
            ... )
            {'response_id': 'mock-retain-123', 'status': 'success', ...}
        """
        # Build tool arguments using same logic as MCP client sample
        tool_args = {
            "workspace_id": workspace_id,
            "mas_id": mas_id,
            "request_id": request_id or f"retain-{workspace_id}-{mas_id}",
            "payload": payload,
        }
        
        if agent_id:
            tool_args["header"] = {"agent_id": agent_id}
        
        # Return mock response in expected format
        return {
            "response_id": tool_args["request_id"],
            "status": "success", 
            "message": f"Successfully saved mock data to graph 'graph_{mas_id.replace('-', '_')}'",
            "workspace_id": workspace_id,
            "mas_id": mas_id,
            "nodes_saved": 6,
            "edges_saved": 8,
        }

    async def recall(
        self,
        workspace_id: str,
        mas_id: str,
        intent: str,
        search_strategy: Optional[str] = None,
        request_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        additional_context: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Recall shared memories using MCP client logic with mock response.
        In production, this could call a real CFN endpoint.
        
        Args:
            workspace_id: Workspace identifier
            mas_id: Multi-agent system identifier
            intent: User intent or natural-language query
            search_strategy: Search strategy (defaults to "semantic_graph_traversal")
            request_id: Optional request identifier
            agent_id: Optional agent identifier
            additional_context: Optional contextual information
            
        Returns:
            Dict with recall operation result
            
        Example:
            >>> await client.recall(
            ...     workspace_id="my-workspace",
            ...     mas_id="my-mas", 
            ...     intent="Find user preferences"
            ... )
            {'response_id': 'mock-recall-123', 'message': '...', ...}
        """
        # Build tool arguments using same logic as MCP client sample
        tool_args = {
            "workspace_id": workspace_id,
            "mas_id": mas_id,
            "intent": intent,
            "search_strategy": search_strategy or "semantic_graph_traversal",
            "request_id": request_id or f"recall-{workspace_id}-{mas_id}",
        }
        
        if agent_id:
            tool_args["header"] = {"agent_id": agent_id}
            
        if additional_context:
            tool_args["additional_context"] = additional_context
        
        # Return mock response in expected format
        return {
            "response_id": tool_args["request_id"],
            "message": f"Mock recall result for intent: '{intent}'. Found relevant information about the requested topic from shared memory graph.",
            "workspace_id": workspace_id,
            "mas_id": mas_id,
            "search_strategy": tool_args["search_strategy"],
            "results_found": 3,
            "confidence_score": 0.85,
        }
