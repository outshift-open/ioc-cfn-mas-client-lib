# Copyright 2026 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

"""A2A message logging utilities.

Provides formatted logging for A2A messages with relevant metadata.
"""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sidecar.shared.message_parser import A2AMessage

logger = logging.getLogger("a2a_sidecar")


def log_a2a_message(message: "A2AMessage", source: str, destination: str) -> None:
    direction_symbol = "→" if message.direction == "request" else "←"
    log_msg = (
        f"{direction_symbol} A2A {message.direction.upper()}: "
        f"{source} {direction_symbol} {destination} | "
        f"{message.method} {message.path} | "
        f"Protocol: {message.protocol_type.value}"
    )
    if message.task_id:
        log_msg += f" | Task: {message.task_id}"
    if message.message_id:
        log_msg += f" | MsgID: {message.message_id}"
    logger.info(log_msg)
