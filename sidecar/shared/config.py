"""Configuration for A2A ext_authz service."""

import os
from dataclasses import dataclass


@dataclass
class ProxyConfig:
    """Configuration for the A2A ext_authz service.

    Attributes:
        cfn_url: CFN API endpoint URL (required)
        workspace_id: CFN workspace ID (required)
        mas_id: CFN MAS ID (required)
        sidecar_id: Sidecar identifier (optional, defaults to mas_id)
    """

    cfn_url: str
    workspace_id: str
    mas_id: str
    sidecar_id: str = None

    def __post_init__(self):
        """Set default sidecar_id if not provided."""
        if self.sidecar_id is None:
            self.sidecar_id = self.mas_id

    @classmethod
    def from_env(cls) -> "ProxyConfig":
        """Create configuration from environment variables.

        Environment variables:
            CFN_URL: CFN API endpoint
            WORKSPACE_ID: CFN workspace ID
            MAS_ID: CFN MAS ID

        Raises:
            ValueError: If any required environment variable is missing
        """
        cfn_url = os.getenv("CFN_URL")
        workspace_id = os.getenv("WORKSPACE_ID")
        mas_id = os.getenv("MAS_ID")

        if not cfn_url:
            raise ValueError("CFN_URL environment variable is required")
        if not workspace_id:
            raise ValueError("WORKSPACE_ID environment variable is required")
        if not mas_id:
            raise ValueError("MAS_ID environment variable is required")

        return cls(
            cfn_url=cfn_url,
            workspace_id=workspace_id,
            mas_id=mas_id,
        )
