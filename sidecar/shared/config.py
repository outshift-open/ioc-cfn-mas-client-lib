# Copyright 2026 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

"""Configuration for A2A ext_authz service."""

import os
from dataclasses import dataclass, field
from typing import List


@dataclass
class NetworkConfig:
    """Network-level configuration for traffic detection.

    Attributes:
        service_ip_ranges: CIDR ranges for Kubernetes service IPs (outbound detection)
        pod_ip_ranges: CIDR ranges for pod IPs (inbound detection)
        app_ports: Application ports to intercept for inbound traffic
        envoy_admin_port: Envoy admin interface port
        ext_authz_port: gRPC port for ext_authz service
        envoy_inbound_port: Envoy listener for inbound traffic
        envoy_outbound_port: Envoy listener for outbound traffic
    """

    service_ip_ranges: List[str] = field(default_factory=lambda: ["10.96.0.0/12"])
    pod_ip_ranges: List[str] = field(default_factory=lambda: ["10.244.0.0/16"])
    app_ports: List[int] = field(default_factory=lambda: [8000, 8001])
    envoy_admin_port: int = 9000
    ext_authz_port: int = 9001
    envoy_inbound_port: int = 15001
    envoy_outbound_port: int = 15002

    def is_service_ip(self, ip: str) -> bool:
        """Check if IP belongs to service CIDR ranges."""
        import ipaddress
        try:
            ip_obj = ipaddress.ip_address(ip)
            return any(ip_obj in ipaddress.ip_network(cidr) for cidr in self.service_ip_ranges)
        except ValueError:
            return False

    def is_pod_ip(self, ip: str) -> bool:
        """Check if IP belongs to pod CIDR ranges."""
        import ipaddress
        try:
            ip_obj = ipaddress.ip_address(ip)
            return any(ip_obj in ipaddress.ip_network(cidr) for cidr in self.pod_ip_ranges)
        except ValueError:
            return False


@dataclass
class ProxyConfig:
    """Configuration for the A2A ext_authz service.

    Attributes:
        cfn_url: CFN API endpoint URL (required)
        workspace_id: CFN workspace ID (required)
        mas_id: CFN MAS ID (required)
        sidecar_id: Sidecar identifier (optional, defaults to mas_id)
        network: Network configuration for traffic detection
        cfn_timeout_seconds: Timeout for CFN API calls
    """

    cfn_url: str
    workspace_id: str
    mas_id: str
    sidecar_id: str = None
    network: NetworkConfig = field(default_factory=NetworkConfig)
    cfn_timeout_seconds: float = 1.0

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
