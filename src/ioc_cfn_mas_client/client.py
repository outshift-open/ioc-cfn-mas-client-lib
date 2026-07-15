# Copyright 2026 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

# src/ioc_cfn_mas_client/client.py

from __future__ import annotations

from typing import Any, Dict, Optional

from generated.api.l9_messages_api import L9MessagesApi
from generated.api_client import ApiClient
from generated.configuration import Configuration
from generated.models.forward_l9_message_request import ForwardL9MessageRequest


class Client:
    """Client for forwarding L9 protocol messages to IoC CFN.

    This client provides a simple interface for forwarding L9 (SSTP - Semantic State
    Transfer Protocol) messages to the Cognition Fabric Node, which routes them to
    appropriate Cognition Engines.

    Args:
        cfn_url: CFN API endpoint URL (e.g., "http://localhost:9002")
        timeout: Request timeout in seconds (default: None)
        configuration: Pre-configured Configuration object (advanced usage)
        api_client: Pre-configured ApiClient object (advanced usage)

    Example:
        >>> client = Client(cfn_url="http://localhost:9002")
        >>> response = client.forward_l9_message(
        ...     message={
        ...         "header": {
        ...             "protocol": "sstp",
        ...             "version": "1.0",
        ...             "subprotocol": "ioc",
        ...             "kind": "intent",
        ...             "participants": {
        ...                 "actors": [{"id": "agent-1"}],
        ...                 "groups": {
        ...                     "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
        ...                     "mas_id": "660e8400-e29b-41d4-a716-446655440001"
        ...                 }
        ...             }
        ...         },
        ...         "payload": {
        ...             "type": "application/json",
        ...             "data": {"query": "Analyze system metrics"}
        ...         }
        ...     }
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
        """Initialize the L9 client.

        Args:
            cfn_url: CFN API endpoint URL
            timeout: Optional request timeout in seconds
            configuration: Optional pre-configured Configuration object
            api_client: Optional pre-configured ApiClient object

        Raises:
            ValueError: If both api_client and configuration are provided
        """
        if api_client is not None and configuration is not None:
            raise ValueError("Provide only one of api_client or configuration")

        cfg = configuration or (api_client.configuration if api_client else None) or Configuration()
        cfg.host = cfn_url

        self._configuration = cfg
        self._api_client = api_client or ApiClient(configuration=cfg)
        self._timeout = timeout
        self._l9_messages_api = L9MessagesApi(api_client=self._api_client)

    def forward_l9_message(
        self,
        message: Dict[str, Any],
    ) -> Any:
        """Forward L9 protocol message to cognition engines.

        Receives L9 (SSTP) protocol messages and routes them to the appropriate
        cognition engine based on message kind, subkind, workspace, and MAS.

        The message must conform to the L9/SSTP specification with:
        - header.kind: Message type (intent, contingency, exchange, commit, knowledge)
        - header.participants.groups: Routing information (workspace and mas)
        - payload: Message-specific data

        Args:
            message: L9 protocol message conforming to SSTP specification.
                Must include header with participants.groups for routing.

        Returns:
            Response from the cognition engine

        Raises:
            ApiException: If the API request fails
            ValueError: If the message format is invalid

        Example:
            >>> response = client.forward_l9_message(
            ...     message={
            ...         "header": {
            ...             "protocol": "sstp",
            ...             "version": "1.0",
            ...             "subprotocol": "ioc",
            ...             "kind": "intent",
            ...             "participants": {
            ...                 "actors": [{"id": "agent-1"}],
            ...                 "groups": {
            ...                     "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
            ...                     "mas_id": "660e8400-e29b-41d4-a716-446655440001"
            ...                 }
            ...             }
            ...         },
            ...         "payload": {
            ...             "type": "application/json",
            ...             "data": {
            ...                 "query": "Analyze system metrics",
            ...                 "context": {"service": "auth-service"}
            ...             }
            ...         }
            ...     }
            ... )
        """
        request = ForwardL9MessageRequest.from_dict(message)
        return self._l9_messages_api.forward_l9_message(
            forward_l9_message_request=request,
        )

    # ============================================================================
    # Advanced Access (for power users)
    # ============================================================================

    @property
    def configuration(self) -> Configuration:
        """Access the underlying OpenAPI configuration.

        Returns:
            Configuration: The OpenAPI client configuration object
        """
        return self._configuration

    @property
    def api_client(self) -> ApiClient:
        """Access the underlying OpenAPI client.

        Returns:
            ApiClient: The OpenAPI API client instance
        """
        return self._api_client

    @property
    def l9_messages_api(self) -> L9MessagesApi:
        """Direct access to the generated L9MessagesApi for advanced usage.

        Returns:
            L9MessagesApi: The generated L9 messages API client
        """
        return self._l9_messages_api
