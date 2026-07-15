# Copyright 2026 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

# src/ioc_cfn_mas_client/instrumentation/__init__.py
"""Instrumentation modules for various agent frameworks."""

import importlib.util

# A2A instrumentation is optional - only import if a2a-sdk is installed
if importlib.util.find_spec("a2a") is not None:
    from ioc_cfn_mas_client.instrumentation.a2a import A2AInstrumentor
    __all__ = ["A2AInstrumentor"]
else:
    __all__ = []
