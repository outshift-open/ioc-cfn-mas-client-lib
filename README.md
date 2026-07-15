# Internet of Cognition (IOC) - Cognition Fabric Node (CFN) MAS Client Library

[![PyPI version](https://badge.fury.io/py/ioc-cfn-mas-client-lib.svg)](https://badge.fury.io/py/ioc-cfn-mas-client-lib)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Python SDK client library for the Internet of Cognition (IoC) Cognition Fabric Node.

## Compatibility

**Current Version: 0.3.1** supports **CFN Public API v0.2.1**

## Overview

This library provides a Python client for forwarding **L9 protocol messages** to the CFN (Cognition Fabric Node) service, which routes them to appropriate Cognition Engines based on the message header.

The **L9 protocol (SSTP - Semantic State Transfer Protocol)** enables standardized communication between Multi-Agent Systems and Cognition Engines in the IoC ecosystem.

## Installation

**Requires Python >= 3.10**

```bash
pip install ioc-cfn-mas-client-lib
```

## Quick Start

### Forwarding L9 Messages

```python
from ioc_cfn_mas_client import Client

# Initialize the CFN client
client = Client(cfn_url="http://localhost:9002")

# Construct and forward an L9 message
response = client.forward_l9_message(
    message={
        "header": {
            "protocol": "sstp",           # Always "sstp" for L9
            "version": "1.0",              # Protocol version
            "subprotocol": "TFP",          # Subprotocol: TFP, CIP, SIEP, SAB, etc.
            "kind": "exchange",            # Message kind: intent, contingency, exchange, commit, knowledge
            "participants": {
                "actors": [                # Participating agents/actors
                    {
                        "id": "monitoring-agent",
                        "role": "sender"
                    },
                    {
                        "id": "metrics-processor",
                        "role": "receiver"
                    }
                ],
                "groups": {                # Routing information
                    "workspace_id": "550e8400-e29b-41d4-a716-446655440000",  # Target workspace UUID
                    "mas_id": "660e8400-e29b-41d4-a716-446655440001"         # Target MAS UUID
                }
            }
        },
        "payload": {
            "type": "application/json",    # Payload MIME type
            "data": {                      # Custom payload data
                "operation": "query_metrics",
                "parameters": {
                    "metric_types": ["cpu", "memory", "disk"],
                    "time_range": "last_hour"
                },
                "metadata": {
                    "source": "monitoring-agent",
                    "timestamp": "2026-07-15T10:30:00Z"
                }
            }
        }
    }
)

print(f"Message forwarded successfully: {response}")
```

### L9 Message Structure

L9 messages follow the **SSTP specification** and consist of two main components:

#### Header (Required)
- **`protocol`**: Always `"sstp"` for L9 messages
- **`version`**: Protocol version (e.g., `"1.0"`)
- **`subprotocol`**: Subprotocol identifier - one of:
  - `"TFP"` - Team Formation via Polling
  - `"CIP"` - Contingency Interaction Protocol
  - `"SIEP"` - Semantic Interaction Exchange Protocol
  - `"SAB"` - Semantic Alignment Broadcast
  - Or any custom subprotocol identifier
- **`kind`**: Message type - one of:
  - `intent` - Agent intentions and goals
  - `contingency` - Conditional actions and fallbacks
  - `exchange` - Data exchange between agents
  - `commit` - State commitments and confirmations
  - `knowledge` - Knowledge queries and updates
- **`subkind`** (optional): Additional message classification
- **`participants`**: Routing and actor information
  - **`actors`**: Array of participating agents/actors with `id` and `role`
  - **`groups`**: Routing groups with **`workspace_id`** and **`mas_id`** (both UUIDs)

#### Payload (Required)
- **`type`**: Payload MIME type (e.g., `"application/json"`, `"text/plain"`)
- **`data`**: Custom payload data (object or any JSON-serializable data)

### Routing Logic

CFN routes L9 messages to Cognition Engines based on:
1. **Workspace ID** - Identifies the workspace boundary
2. **MAS ID** - Identifies the specific Multi-Agent System
3. **Message kind** - Determines the type of processing required

The appropriate Cognition Engine is selected and the message is forwarded for processing.

## Configuration

The `Client` constructor accepts:

- **`cfn_url`** (required): CFN API endpoint URL (e.g., `"http://localhost:9002"`)
- **`timeout`** (optional): Request timeout in seconds
- **`configuration`** (optional): Pre-configured `Configuration` object (advanced)
- **`api_client`** (optional): Pre-configured `ApiClient` object (advanced)

### Environment Variables

Optional environment variable:

- **`CFN_URL`**: CFN API endpoint URL (defaults to `http://localhost:9002`)

## Development

For development setup, OpenAPI code generation, and contribution guidelines, see [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md).

## API Documentation

This SDK is auto-generated from the [CFN Public API OpenAPI specification](https://github.com/outshift-open/ioc-cfn-svc/tree/main/docs/public-api). For detailed API documentation, see the upstream repository.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `uv run pytest`
5. Submit a pull request

For more details, see [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md).

## License

This project is licensed under the Apache License, Version 2.0 - see the [LICENSE.md](LICENSE.md) file for full details.

Copyright (c) 2024-2026 Cisco Systems, Inc. and its affiliates. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
