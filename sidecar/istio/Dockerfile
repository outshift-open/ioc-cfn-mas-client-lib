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

# Copy ext_authz service code
COPY sidecar/shared/ ./sidecar/shared/
WORKDIR /app/sidecar/shared

# Set PYTHONPATH so absolute imports work
ENV PYTHONPATH=/app

# Run only ext_authz service (no Envoy)
# Use shell form to allow environment variable expansion
CMD python ext_authz_service.py \
    --cfn-url="${CFN_URL}" \
    --workspace-id="${WORKSPACE_ID}" \
    --mas-id="${MAS_ID}"
