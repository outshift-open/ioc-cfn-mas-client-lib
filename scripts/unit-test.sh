# Copyright 2026 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

#!/bin/bash
# Run unit tests for L9 client

set -e

cd "$(dirname "$0")/.."

echo "Running L9 client unit tests..."
pytest tests/ -v --cov=ioc_cfn_mas_client --cov-report=term-missing

echo ""
echo "✓ All L9 client tests passed!"
