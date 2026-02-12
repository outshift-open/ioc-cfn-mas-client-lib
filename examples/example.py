# examples/example.py

import os
from typing import Any, Dict

from ioc_cfn_mas_client.client import Client


def main() -> None:
    client = Client(
        base_url=os.getenv("CFN_BASE_URL", "http://localhost:9010"),
    )

    workspace_id = "test"
    system_id = "test"

    # 1) Upsert shared memories
    upsert_body: Dict[str, Any] = {
        # Adjust keys to match your OpenAPI schema if needed.
        "memories": [
            {
                "id": "m1",
                "content": "hello from sdk wrapper",
            }
        ]
    }

    upsert_res = client.shared_memories.api_workspaces_workspace_id_multi_agentic_systems_system_id_shared_memories_post_with_http_info(
        workspace_id=workspace_id,
        system_id=system_id,
        body=upsert_body,
    )
    print("Upsert response:")
    print(upsert_res)

    # 2) Query shared memories
    query_body: Dict[str, Any] = {
        # Adjust keys to match your OpenAPI schema if needed.
        "query": "hello",
        "topK": 5,
    }

    query_res = client.shared_memories.api_workspaces_workspace_id_multi_agentic_systems_system_id_shared_memories_query_post_with_http_info(
        workspace_id=workspace_id,
        system_id=system_id,
        body=query_body,
    )
    print("Query response:")
    print(query_res)


if __name__ == "__main__":
    main()