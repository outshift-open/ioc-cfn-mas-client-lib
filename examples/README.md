# Examples

This directory contains example scripts demonstrating how to use the IOC CFN MAS Client Library.

## Setup

### 1. Install Dependencies

```bash
# From project root
uv pip install -e ".[examples]"  # Installs python-dotenv
```

### 2. Configure Environment Variables

Copy the example environment file and edit with your values:

```bash
cd examples
cp .env.example .env
# Edit .env with your actual configuration
```

The `.env.example` file contains:

```bash
# CFN Service Configuration
CFN_BASE_URL=http://localhost:9010
CFN_API_KEY=                              # Optional

# Management Plane Configuration
MANAGEMENT_PLANE_BASE_URL=http://localhost:8080
API_KEY=your-api-key-here
```

### 3. Run Examples

```bash
# From project root or examples directory
python examples/example.py
python examples/simple_mgmt_example.py
```

## Examples Overview

### `example.py`
Demonstrates CFN service operations:
- Initializing the Client
- Upserting shared memories
- Querying shared memories with semantic search
- Advanced: Direct API access for power users

**Usage:**
```bash
python examples/example.py
```

### `simple_mgmt_example.py`
Demonstrates Management Plane operations:
- Listing workspaces
- Listing multi-agentic systems in a workspace
- Integrating Management Plane with CFN Client

**Usage:**
```bash
python examples/simple_mgmt_example.py
```

## Configuration

### Using `.env` Files (Recommended)

The examples use `python-dotenv` to load configuration from `.env` files:

```python
from dotenv import load_dotenv
load_dotenv()  # Loads .env from current directory or parent

import os
from ioc_cfn_mas_client import Client

client = Client(
    base_url=os.getenv("CFN_BASE_URL", "http://localhost:9010"),
    api_key=os.getenv("CFN_API_KEY"),
)
```

### Without `.env` Files

You can also set environment variables directly:

```bash
export CFN_BASE_URL="http://localhost:9010"
export CFN_API_KEY="your-api-key"
export MANAGEMENT_PLANE_BASE_URL="http://localhost:8080"
export API_KEY="your-mgmt-api-key"

python examples/example.py
```

Or hardcode values (not recommended for production):

```python
from ioc_cfn_mas_client import Client

client = Client(
    base_url="http://localhost:9010",
    api_key="your-api-key",
)
```

## Environment Variables Reference

| Variable | Description | Default | Used By |
|----------|-------------|---------|---------|
| `CFN_BASE_URL` | CFN service API endpoint | `http://localhost:9010` | `example.py`, `simple_mgmt_example.py` |
| `CFN_API_KEY` | CFN authentication token | - (optional) | `example.py`, `simple_mgmt_example.py` |
| `MANAGEMENT_PLANE_BASE_URL` | Management Plane endpoint | `http://localhost:8080` | `simple_mgmt_example.py` |
| `API_KEY` | Management Plane auth key | - (required) | `simple_mgmt_example.py` |

## Troubleshooting

### Import Error: No module named 'dotenv'

Install the examples dependencies:
```bash
uv pip install -e ".[examples]"
# or
pip install python-dotenv
```

### Connection Errors

Ensure the services are running:
- CFN service should be accessible at `CFN_BASE_URL`
- Management Plane should be accessible at `MANAGEMENT_PLANE_BASE_URL`

Check connectivity:
```bash
curl $CFN_BASE_URL/health
curl $MANAGEMENT_PLANE_BASE_URL/health
```

### Authentication Errors

Verify your API keys are correct:
- CFN service may or may not require `CFN_API_KEY` depending on deployment
- Management Plane requires valid `API_KEY` for X-API-Key header

## Notes

- `.env` files are **only for examples** - the library itself doesn't use them
- Never commit `.env` files with real credentials to version control
- `.env` is already in `.gitignore` for safety
