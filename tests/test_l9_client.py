# Copyright 2026 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

# tests/test_l9_client.py
"""Unit tests for L9 Client API contract.

These tests verify the client API contract using mocks, ensuring:
1. Client initialization works correctly
2. L9 message structure is properly validated
3. API calls are made with correct parameters
4. Errors are handled appropriately
"""

import pytest
from unittest.mock import patch

from ioc_cfn_mas_client.client import Client
from generated.models.forward_l9_message_request import ForwardL9MessageRequest


class TestClientInitialization:
    """Test client initialization and configuration."""

    def test_client_init_with_url(self):
        """Test basic client initialization with URL."""
        client = Client(cfn_url="http://localhost:9002")

        assert client is not None
        assert client._configuration.host == "http://localhost:9002"
        assert client._timeout is None

    def test_client_init_with_timeout(self):
        """Test client initialization with custom timeout."""
        client = Client(cfn_url="http://localhost:9002", timeout=30.0)

        assert client._timeout == 30.0

    def test_client_init_with_both_config_and_api_client_raises_error(self):
        """Test that providing both configuration and api_client raises ValueError."""
        from generated.configuration import Configuration
        from generated.api_client import ApiClient

        config = Configuration()
        api_client = ApiClient()

        with pytest.raises(ValueError, match="Provide only one of api_client or configuration"):
            Client(
                cfn_url="http://localhost:9002",
                configuration=config,
                api_client=api_client
            )

    def test_client_properties(self):
        """Test client exposes necessary properties."""
        client = Client(cfn_url="http://localhost:9002")

        assert hasattr(client, "configuration")
        assert hasattr(client, "api_client")
        assert hasattr(client, "l9_messages_api")


class TestForwardL9Message:
    """Test L9 message forwarding functionality."""

    @pytest.fixture
    def client(self):
        """Create a test client instance."""
        return Client(cfn_url="http://localhost:9002")

    @pytest.fixture
    def valid_l9_message(self):
        """Create a valid L9 message for testing."""
        return {
            "header": {
                "protocol": "sstp",
                "version": "1.0",
                "subprotocol": "ioc",
                "kind": "intent",
                "participants": {
                    "actors": [],
                    "groups": {
                        "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
                        "mas_id": "660e8400-e29b-41d4-a716-446655440001"
                    }
                }
            },
            "payload": {
                "type": "application/json",
                "data": {
                    "intent": "Test intent"
                }
            }
        }

    def test_forward_l9_message_intent(self, client, valid_l9_message):
        """Test forwarding an intent message."""
        with patch.object(client._l9_messages_api, 'forward_l9_message') as mock_forward:
            mock_forward.return_value = {"status": "success"}

            result = client.forward_l9_message(message=valid_l9_message)

            assert result == {"status": "success"}
            mock_forward.assert_called_once()

            # Verify the request was created properly
            call_args = mock_forward.call_args
            assert 'forward_l9_message_request' in call_args.kwargs
            request = call_args.kwargs['forward_l9_message_request']
            assert isinstance(request, ForwardL9MessageRequest)

    def test_forward_l9_message_with_actors(self, client):
        """Test forwarding message with actors in participants."""
        message = {
            "header": {
                "protocol": "sstp",
                "version": "1.0",
                "subprotocol": "ioc",
                "kind": "intent",
                "participants": {
                    "actors": [
                        {"id": "agent-123"},
                        {"id": "agent-456"}
                    ],
                    "groups": {
                        "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
                        "mas_id": "660e8400-e29b-41d4-a716-446655440001"
                    }
                }
            },
            "payload": {
                "type": "application/json",
                "data": {"test": "value"}
            }
        }

        with patch.object(client._l9_messages_api, 'forward_l9_message') as mock_forward:
            mock_forward.return_value = {"status": "success"}

            result = client.forward_l9_message(message=message)

            assert result == {"status": "success"}
            mock_forward.assert_called_once()


class TestErrorHandling:
    """Test error handling and edge cases."""

    @pytest.fixture
    def client(self):
        """Create a test client instance."""
        return Client(cfn_url="http://localhost:9002")

    def test_forward_l9_message_api_exception(self, client):
        """Test that API exceptions are propagated."""
        from generated.exceptions import ApiException

        message = {
            "header": {
                "protocol": "sstp",
                "version": "1.0",
                "subprotocol": "ioc",
                "kind": "intent",
                "participants": {
                    "actors": [],
                    "groups": {
                        "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
                        "mas_id": "660e8400-e29b-41d4-a716-446655440001"
                    }
                }
            },
            "payload": {
                "type": "application/json",
                "data": {}
            }
        }

        with patch.object(client._l9_messages_api, 'forward_l9_message') as mock_forward:
            mock_forward.side_effect = ApiException(status=400, reason="Bad Request")

            with pytest.raises(ApiException):
                client.forward_l9_message(message=message)

    def test_forward_l9_message_invalid_format(self, client):
        """Test that invalid message format raises appropriate error."""
        invalid_message = {
            "invalid": "structure"
        }

        with pytest.raises((ValueError, KeyError, AttributeError)):
            client.forward_l9_message(message=invalid_message)

    def test_forward_l9_message_missing_header(self, client):
        """Test that missing header raises error."""
        message_no_header = {
            "payload": {"type": "application/json", "data": {}}
        }

        with pytest.raises((ValueError, KeyError, AttributeError)):
            client.forward_l9_message(message=message_no_header)


class TestAPIContract:
    """Test the API contract and method signatures."""

    def test_forward_l9_message_signature(self):
        """Test that forward_l9_message has the correct signature."""
        import inspect

        sig = inspect.signature(Client.forward_l9_message)
        params = list(sig.parameters.keys())

        assert 'self' in params
        assert 'message' in params
        assert len(params) == 2  # self and message only

    def test_client_has_required_methods(self):
        """Test that client has all required public methods."""
        client = Client(cfn_url="http://localhost:9002")

        # Public API methods
        assert hasattr(client, 'forward_l9_message')
        assert callable(client.forward_l9_message)

        # Properties for advanced access
        assert hasattr(client, 'configuration')
        assert hasattr(client, 'api_client')
        assert hasattr(client, 'l9_messages_api')

    def test_client_minimal_api_surface(self):
        """Test that client exposes minimal API surface (L9 only)."""
        client = Client(cfn_url="http://localhost:9002")

        # Should NOT have these methods (removed legacy APIs)
        assert not hasattr(client, 'create_shared_memories')
        assert not hasattr(client, 'query_shared_memories')
        assert not hasattr(client, 'memory_operation')
        assert not hasattr(client, 'start_alignment')
        assert not hasattr(client, 'advance_alignment')
        assert not hasattr(client, 'retain')
        assert not hasattr(client, 'recall')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
