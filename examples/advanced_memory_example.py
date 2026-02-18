# examples/advanced_memory_example.py
"""Advanced example showing different memory attribute patterns."""
import os
from pathlib import Path
from dotenv import load_dotenv
from ioc_cfn_mas_client.client import Client
from memory_examples import (
    CONTEXT_MEMORIES, MESSAGE_MEMORIES, AGENT_INFO_MEMORIES,
    SESSION_INFO_MEMORIES, WORKFLOW_RUN_MEMORIES, USER_DETAILS_MEMORIES
)

# Load .env from examples directory
examples_dir = Path(__file__).parent
load_dotenv(examples_dir / ".env")

def main():
    client = Client(
        base_url=os.getenv("CFN_BASE_URL", "http://localhost:9010"),
        api_key=os.getenv("CFN_API_KEY"),
    )
    
    workspace_id = os.getenv("WORKSPACE_ID", "test_workspace")
    system_id = os.getenv("SYSTEM_ID", "test_system")
    
    print("Advanced Memory Patterns Example")
    print(f"Workspace: {workspace_id}, System: {system_id}")
    
    # Upsert different memory types
    examples = [
        ("Context & Memory", CONTEXT_MEMORIES),
        ("Messages", MESSAGE_MEMORIES),
        ("Agent Info", AGENT_INFO_MEMORIES),
        ("Session Info", SESSION_INFO_MEMORIES),
        ("Workflow Runs", WORKFLOW_RUN_MEMORIES),
        ("User Details", USER_DETAILS_MEMORIES),
    ]
    
    for name, memories in examples:
        print(f"\nUpserting {name}...")
        try:
            client.upsert_memories(workspace_id, system_id, memories=memories)
            print(f"✓ Upserted {len(memories)} {name} memories")
        except Exception as e:
            print(f"✗ Error: {e}")

if __name__ == "__main__":
    main()
