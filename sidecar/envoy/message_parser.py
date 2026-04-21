"""A2A Protocol Message Parser (JSON-RPC 2.0).

Official spec: https://github.com/google/a2a
"""

import json
from dataclasses import dataclass
from typing import Any, Dict, Optional, List
from enum import Enum


class A2AProtocolType(Enum):
    JSONRPC = "jsonrpc"
    REST = "rest"
    UNKNOWN = "unknown"


@dataclass
class A2AMessage:
    protocol_type: A2AProtocolType
    direction: str
    method: str
    path: str
    headers: Dict[str, str]
    body: Optional[Dict[str, Any]]
    raw_body: bytes
    agent_card_url: Optional[str] = None
    task_id: Optional[str] = None
    message_id: Optional[str] = None


class A2AMessageParser:
    # Official A2A JSON-RPC methods (v0.3.0)
    A2A_JSONRPC_METHODS = [
        "tasks/send",              # Send a task to an agent
        "tasks/sendSubscribe",     # Send task with streaming
        "tasks/get",               # Get task status
        "tasks/cancel",            # Cancel a task
        "tasks/resubscribe",       # Resubscribe to task updates
        "tasks/pushNotification/set",   # Set push notification endpoint
        "tasks/pushNotification/get",   # Get push notification settings
    ]

    # Official A2A REST endpoint
    AGENT_CARD_PATH = "/.well-known/agent.json"

    @classmethod
    def is_a2a_message(cls, method: str, path: str, headers: Dict[str, str]) -> bool:
        if path == cls.AGENT_CARD_PATH or path.endswith("/agent.json"):
            return True
        content_type = headers.get("content-type", "").lower()
        return method == "POST" and "application/json" in content_type

    @classmethod
    def parse_message(cls, method: str, path: str, headers: Dict[str, str], body: bytes, direction: str = "request") -> Optional[A2AMessage]:
        parsed_body = None
        if body:
            try:
                parsed_body = json.loads(body.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass

        protocol_type = cls._detect_protocol_type(method, path, parsed_body)
        task_id, message_id = None, None

        if protocol_type == A2AProtocolType.JSONRPC and parsed_body:
            message_id = str(parsed_body["id"]) if "id" in parsed_body else None
            if "params" in parsed_body:
                params = parsed_body.get("params", {})
                if isinstance(params, dict):
                    task_id = params.get("task_id") or params.get("taskId") or params.get("context_id") or params.get("contextId")

        return A2AMessage(
            protocol_type=protocol_type,
            direction=direction,
            method=method,
            path=path,
            headers=headers,
            body=parsed_body,
            raw_body=body,
            task_id=task_id,
            message_id=message_id,
        )

    @classmethod
    def _detect_protocol_type(cls, method: str, path: str, body: Optional[Dict[str, Any]]) -> A2AProtocolType:
        if body and isinstance(body, dict) and body.get("jsonrpc") == "2.0":
            method_name = body.get("method", "")
            if method_name in cls.A2A_JSONRPC_METHODS or "method" in body:
                return A2AProtocolType.JSONRPC
        if method == "GET" and (path == cls.AGENT_CARD_PATH or path.endswith("/agent.json")):
            return A2AProtocolType.REST
        return A2AProtocolType.UNKNOWN

    @classmethod
    def extract_agent_info(cls, message: A2AMessage) -> Dict[str, Any]:
        """Extract agent information from the message.

        Args:
            message: Parsed A2A message

        Returns:
            Dictionary with agent information
        """
        info: Dict[str, Any] = {
            "protocol": message.protocol_type.value,
            "direction": message.direction,
            "method": message.method,
            "path": message.path,
        }

        if message.agent_card_url:
            info["agent_card_url"] = message.agent_card_url

        if message.task_id:
            info["task_id"] = message.task_id

        if message.message_id:
            info["message_id"] = message.message_id

        # Extract additional context from body
        if message.body:
            if "message" in message.body:
                info["message_text"] = cls._extract_message_text(message.body["message"])

            if "result" in message.body:
                info["has_result"] = True

            if "error" in message.body:
                info["has_error"] = True
                info["error"] = message.body["error"]

        return info

    @staticmethod
    def _extract_message_text(message_obj: Any) -> Optional[str]:
        """Extract text from A2A message object.

        Args:
            message_obj: Message object from A2A protocol

        Returns:
            Extracted text or None
        """
        if isinstance(message_obj, str):
            return message_obj

        if isinstance(message_obj, dict):
            # A2A Message format
            if "parts" in message_obj:
                parts = message_obj["parts"]
                if isinstance(parts, list) and parts:
                    first_part = parts[0]
                    if isinstance(first_part, dict):
                        root = first_part.get("root", {})
                        if isinstance(root, dict):
                            return root.get("text")

        return None
