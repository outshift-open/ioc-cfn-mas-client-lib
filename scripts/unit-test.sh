# Copyright 2026 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

#!/bin/bash
# Run unit tests for L9 client

set -e

cd "$(dirname "$0")/.."

echo "Running L9 client unit tests..."

# Use python -m pytest if available (CI), otherwise use uv run (local dev)
if command -v python &> /dev/null; then
    python -m pytest tests/ -v --cov=ioc_cfn_mas_client --cov-report=term-missing
elif command -v uv &> /dev/null; then
    uv run python -m pytest tests/ -v --cov=ioc_cfn_mas_client --cov-report=term-missing
else
    echo "Error: Neither python nor uv found in PATH"
    exit 1
fi

echo ""
echo "✓ All L9 client tests passed!"
