# Copyright 2026 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

FROM python:3.10-slim

# Install Python dependencies
RUN pip install --no-cache-dir \
    grpcio \
    grpcio-tools \
    xds-protos \
    protobuf \
    httpx

# Copy MAS client library (for CFN integration)
WORKDIR /app
COPY src/ ./src/
COPY pyproject.toml ./

# Install MAS client library
RUN pip install --no-cache-dir -e .

# Copy IOC CFN L9 service code
COPY sidecar/shared/ ./sidecar/shared/
WORKDIR /app/sidecar/shared

# Set PYTHONPATH so absolute imports work
ENV PYTHONPATH=/app

# Run only IOC CFN L9 service (no Envoy, Istio provides the proxy)
# Use shell form to allow environment variable expansion
CMD python ioc_cfn_l9_service.py \
    --cfn-url="${CFN_URL}" \
    --workspace-id="${WORKSPACE_ID}" \
    --mas-id="${MAS_ID}"
