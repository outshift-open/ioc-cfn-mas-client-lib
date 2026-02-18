# examples/memory_examples.py
"""Example memory structures with different attribute patterns."""
from typing import Any, Dict, List

CONTEXT_MEMORIES: List[Dict[str, Any]] = [
    {
        "id": "ctx_001",
        "context": "User is working on a Python data pipeline project",
        "memory": "User prefers pandas over polars for data manipulation",
    },
]

MESSAGE_MEMORIES: List[Dict[str, Any]] = [
    {
        "id": "msg_001",
        "messages": [
            {"role": "user", "content": "How do I optimize this query?"},
            {"role": "assistant", "content": "Consider adding an index"},
        ],
        "context": "Database optimization",
        "timestamp": "2024-02-17T10:30:00Z",
    },
]

AGENT_INFO_MEMORIES: List[Dict[str, Any]] = [
    {
        "id": "agent_001",
        "agent_info": {
            "agent_id": "agent_code_reviewer",
            "agent_type": "code_analysis",
            "capabilities": ["python", "javascript"],
        },
        "memory": "Agent specializes in security vulnerabilities",
    },
]

SESSION_INFO_MEMORIES: List[Dict[str, Any]] = [
    {
        "id": "session_001",
        "session_info": {
            "session_id": "sess_abc123",
            "status": "active",
        },
        "memory": "Debugging session for payment service",
    },
]

WORKFLOW_RUN_MEMORIES: List[Dict[str, Any]] = [
    {
        "id": "workflow_001",
        "workflow_run_details": {
            "run_id": "run_xyz789",
            "workflow_name": "CI/CD Pipeline",
            "status": "success",
        },
        "memory": "Successful deployment to production",
    },
]

USER_DETAILS_MEMORIES: List[Dict[str, Any]] = [
    {
        "id": "user_001",
        "user_details": {
            "user_id": "user_john_doe",
            "role": "senior_developer",
        },
        "memory": "Prefers dark mode and VSCode",
    },
]
