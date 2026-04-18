#!/usr/bin/env python3
"""Example: A2A Direct Communication with CFN Instrumentation.

This example shows the typical A2A pattern with automatic CFN instrumentation:
1. Agent B runs as an A2A HTTP server
2. Agent A acts as a client that calls Agent B
3. Direct request-response communication
4. All interactions are automatically logged to CFN via monkey patching

Prerequisites:
    pip install a2a-sdk[http-server]

Usage:
    # Terminal 1 - Start Agent B server
    python examples/instrumentation/a2a/multi_agent_example.py --server

    # Terminal 2 - Run Agent A client
    python examples/instrumentation/a2a/multi_agent_example.py --client
"""

import asyncio
import argparse
import logging
import os
from uuid import uuid4

# CFN Client imports
from ioc_cfn_mas_client import Client, A2AInstrumentor

# A2A SDK imports
from a2a.client import A2ACardResolver, ClientConfig
from a2a.client.client_factory import ClientFactory
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.apps import A2AStarletteApplication
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCard,
    AgentCapabilities,
    AgentSkill,
    Message,
    Part,
    Role,
    TextPart,
    TransportProtocol,
)
from a2a.utils import AGENT_CARD_WELL_KNOWN_PATH, new_agent_text_message

import httpx
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# Agent B: Trend Analyzer (Server-side A2A Agent)
# ============================================================================

class TrendAnalyzerAgent:
    """Simple trend analyzer agent."""

    async def analyze(self, topic: str) -> str:
        """Analyze a trending topic."""
        # Simulate analysis
        await asyncio.sleep(0.5)
        return f"Analysis: '{topic}' is trending with 10K mentions. Sentiment: 80% positive."


class TrendAnalyzerExecutor(AgentExecutor):
    """A2A AgentExecutor for Trend Analyzer."""

    def __init__(self):
        self.agent = TrendAnalyzerAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Execute the agent and return result."""
        # Extract message text
        message_text = ""
        if context.message and context.message.parts:
            for part in context.message.parts:
                if hasattr(part, 'root') and hasattr(part.root, 'text'):
                    message_text = part.root.text
                    break

        # Run analysis
        result = await self.agent.analyze(message_text)

        # Send response message
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Cancel not supported."""
        raise NotImplementedError("Cancel not supported")


# ============================================================================
# Agent B Server Setup
# ============================================================================

def create_trend_analyzer_server():
    """Create A2A server for Trend Analyzer agent."""

    # Define AgentCard (agent's capabilities and metadata)
    agent_card = AgentCard(
        name="Trend Analyzer Agent",
        url="http://localhost:10020",
        description="Analyzes trending topics and provides sentiment analysis",
        version="1.0.0",
        capabilities=AgentCapabilities(streaming=True),
        default_input_modes=["text/plain"],
        default_output_modes=["text/plain"],
        preferred_transport=TransportProtocol.jsonrpc,
        skills=[
            AgentSkill(
                id="analyze_trend",
                name="Analyze Trend",
                description="Analyzes a trending topic and provides metrics",
                tags=["trends", "analysis", "sentiment"],
                examples=[
                    "Analyze the AI trend",
                    "What's trending about climate change?",
                ],
            )
        ],
    )

    # Create executor and request handler
    executor = TrendAnalyzerExecutor()
    request_handler = DefaultRequestHandler(
        agent_executor=executor,
        task_store=InMemoryTaskStore(),
    )

    # Create A2A application
    app = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

    return app.build()


async def run_agent_b_server():
    """Run Agent B as an A2A HTTP server with CFN instrumentation."""
    logger.info("Starting Trend Analyzer Agent (Agent B) on http://localhost:10020")

    # Apply CFN instrumentation to automatically log all A2A interactions
    logger.info("Applying CFN instrumentation (monkey patching)...")
    cfn_client = Client(base_url=os.getenv("CFN_BASE_URL", "http://localhost:9010"))
    instrumentor = A2AInstrumentor(
        client=cfn_client,
        workspace_id="demo-workspace",
        mas_id="trend-analyzer-mas",
        publish_input=True,
        publish_output=True,
    )
    instrumentor.instrument()
    logger.info("✓ Instrumentation applied - all agents will be automatically tracked\n")

    app = create_trend_analyzer_server()

    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=10020,
        log_level="info",
    )

    server = uvicorn.Server(config)
    await server.serve()


# ============================================================================
# Agent A: Client Agent (also instrumented)
# ============================================================================

class QueryAgentExecutor(AgentExecutor):
    """Agent A's executor - queries Agent B and returns result."""

    def __init__(self, agent_b_url: str):
        self.agent_b_url = agent_b_url

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Execute Agent A - query Agent B."""
        # Extract the query from incoming message
        query = ""
        if context.message and context.message.parts:
            for part in context.message.parts:
                if hasattr(part, 'root') and hasattr(part.root, 'text'):
                    query = part.root.text
                    break

        logger.info(f"[Agent A] Processing query: {query}")

        # Discover and call Agent B
        async with httpx.AsyncClient() as httpx_client:
            resolver = A2ACardResolver(
                httpx_client=httpx_client,
                base_url=self.agent_b_url,
            )
            agent_b_card = await resolver.get_agent_card()

            client_factory = ClientFactory(config=ClientConfig(streaming=False))
            client = client_factory.create(agent_b_card)

            # Create message for Agent B
            message = Message(
                role=Role.user,
                parts=[Part(root=TextPart(text=query))],
                message_id=uuid4().hex,
            )

            # Send to Agent B and get response
            response_chunks = client.send_message(message)
            result_text = ""

            async for chunk in response_chunks:
                if chunk and chunk.parts:
                    for part in chunk.parts:
                        if hasattr(part, 'root') and hasattr(part.root, 'text'):
                            result_text = part.root.text
                            break

            await client.close()

        # Return result
        await event_queue.enqueue_event(new_agent_text_message(result_text))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Cancel not supported."""
        raise NotImplementedError("Cancel not supported")


async def run_agent_a_client():
    """Agent A (as an instrumented agent) that calls Agent B."""

    logger.info("\n=== Agent A (Instrumented Client Agent) Starting ===\n")

    # Apply CFN instrumentation to Agent A
    logger.info("Applying CFN instrumentation to Agent A...")
    cfn_client = Client(base_url=os.getenv("CFN_BASE_URL", "http://localhost:9010"))
    instrumentor = A2AInstrumentor(
        client=cfn_client,
        workspace_id="demo-workspace",
        mas_id="query-agent-mas",
        publish_input=True,
        publish_output=True,
    )
    instrumentor.instrument()
    logger.info("✓ Agent A instrumentation applied\n")

    # Create Agent A's executor
    agent_a_executor = QueryAgentExecutor(agent_b_url="http://localhost:10020")

    # Create a mock context with the user's query
    class MockContext:
        def __init__(self, message):
            self.message = message
            self.task_id = f"task-{uuid4().hex}"
            self.context_id = f"ctx-{uuid4().hex}"

    class MockEventQueue:
        def __init__(self):
            self.events = []

        async def enqueue_event(self, event):
            self.events.append(event)

    # Simulate Agent A receiving a query
    user_message = Message(
        role=Role.user,
        parts=[Part(root=TextPart(text="AI in healthcare"))],
        message_id=uuid4().hex,
    )

    logger.info(f"User query to Agent A: 'AI in healthcare'\n")

    # Execute Agent A (this will call Agent B internally and be instrumented)
    context = MockContext(user_message)
    event_queue = MockEventQueue()

    try:
        await agent_a_executor.execute(context, event_queue)

        # Display result
        logger.info("\n=== Agent A Complete ===")
        if event_queue.events:
            for event in event_queue.events:
                if hasattr(event, 'parts'):
                    for part in event.parts:
                        if hasattr(part, 'root') and hasattr(part.root, 'text'):
                            logger.info(f"Final result: {part.root.text}")

        logger.info("\nNote: Check both terminals for [CFN] log messages!")
        logger.info("  - Agent A logs show query input and final output")
        logger.info("  - Agent B logs show message received and completion")

    except Exception as e:
        logger.error(f"✗ Agent A execution failed: {e}")
        logger.error("Make sure Agent B server is running: python examples/instrumentation/a2a/multi_agent_example.py --server")


# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="A2A Direct Communication Example")
    parser.add_argument(
        "--server",
        action="store_true",
        help="Run as Agent B (server)",
    )
    parser.add_argument(
        "--client",
        action="store_true",
        help="Run as Agent A (client)",
    )

    args = parser.parse_args()

    if args.server:
        # Run Agent B server
        asyncio.run(run_agent_b_server())
    elif args.client:
        # Run Agent A client
        asyncio.run(run_agent_a_client())
    else:
        print("Usage:")
        print("  Start server: python examples/instrumentation/a2a/multi_agent_example.py --server")
        print("  Run client:   python examples/instrumentation/a2a/multi_agent_example.py --client")


if __name__ == "__main__":
    main()
