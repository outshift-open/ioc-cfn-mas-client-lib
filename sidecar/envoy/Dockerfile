FROM envoyproxy/envoy:v1.29-latest AS envoy

FROM python:3.10-slim

# Copy Envoy binary from official image
COPY --from=envoy /usr/local/bin/envoy /usr/local/bin/envoy

# Create envoy user (UID 1337)
RUN useradd -u 1337 -m envoy

# Install Python dependencies
RUN pip install --no-cache-dir \
    grpcio \
    grpcio-tools \
    xds-protos \
    protobuf

# Copy MAS client library (for CFN integration)
WORKDIR /app
COPY src/ ./src/
COPY pyproject.toml ./

# Install MAS client library
RUN pip install --no-cache-dir -e .

# Copy sidecar code
COPY sidecar/envoy/ ./sidecar/envoy/
WORKDIR /app/sidecar/envoy

# Set PYTHONPATH so absolute imports work
ENV PYTHONPATH=/app

# Copy Envoy config to standard location
RUN mkdir -p /etc/envoy && \
    cp envoy.yaml /etc/envoy/envoy.yaml

# Make entrypoint executable
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
