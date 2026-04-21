"""Configuration for A2A ext_authz service."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class ProxyConfig:
    """Configuration for the A2A ext_authz service.

    Attributes:
        cfn_url: CFN API endpoint URL (optional)
        workspace_id: CFN workspace ID (optional)
        mas_id: CFN MAS ID (optional)
    """

    cfn_url: Optional[str] = None
    workspace_id: Optional[str] = None
    mas_id: Optional[str] = None

    @classmethod
    def from_env(cls) -> "ProxyConfig":
        """Create configuration from environment variables.

        Environment variables:
            CFN_URL: CFN API endpoint
            WORKSPACE_ID: CFN workspace ID
            MAS_ID: CFN MAS ID
        """
        return cls(
            cfn_url=os.getenv("CFN_URL"),
            workspace_id=os.getenv("WORKSPACE_ID"),
            mas_id=os.getenv("MAS_ID"),
        )
