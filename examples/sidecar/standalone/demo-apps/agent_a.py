#!/usr/bin/env python3
"""
Demo Agent A - A2A SDK Agent (sends and receives A2A messages)
"""
import asyncio
import logging
import os
import time
from uuid import uuid4

import httpx
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
from a2a.utils import new_agent_text_message
import uvicorn

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class AgentAExecutor(AgentExecutor):
    """Agent A - Processes messages and forwards to Agent B."""

    def __init__(self, agent_b_url: str):
        self.agent_b_url = agent_b_url
        self.message_count = 0

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Execute Agent A - process message and optionally forward to B."""
        # Extract incoming message
        message_text = ""
        if context.message and context.message.parts:
            for part in context.message.parts:
                if hasattr(part, 'root') and hasattr(part.root, 'text'):
                    message_text = part.root.text
                    break

        logger.info("="*50)
        logger.info(f"Agent A: Received message from Agent B")
        logger.info("="*50)
        logger.info(f"Message: {message_text}")
        logger.info(f"Task ID: {context.task_id}")

        # Process and respond
        result = f"Agent A processed: {message_text}"
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Cancel not supported."""
        raise NotImplementedError("Cancel not supported")


async def send_messages_to_b():
    """Background task that sends A2A messages to Agent B."""
    agent_b_url = os.getenv("AGENT_B_URL", "http://agent-b:8000")

    await asyncio.sleep(5)  # Wait for everything to start

    message_count = 1
    while True:
        try:
            logger.info("\n" + "="*50)
            logger.info(f"Agent A: Sending message #{message_count} to Agent B")
            logger.info("="*50)

            async with httpx.AsyncClient() as httpx_client:
                # Discover Agent B
                resolver = A2ACardResolver(
                    httpx_client=httpx_client,
                    base_url=agent_b_url,
                )
                agent_b_card = await resolver.get_agent_card()

                # Create A2A client
                client_factory = ClientFactory(config=ClientConfig(streaming=False))
                client = client_factory.create(agent_b_card)

                # Send message
                message = Message(
                    role=Role.user,
                    parts=[Part(root=TextPart(text=f"Message #{message_count} from Agent A"))],
                    message_id=uuid4().hex,
                )

                response_chunks = client.send_message(message)

                # Collect response
                result_text = ""
                async for chunk in response_chunks:
                    if chunk and chunk.parts:
                        for part in chunk.parts:
                            if hasattr(part, 'root') and hasattr(part.root, 'text'):
                                result_text = part.root.text

                logger.info(f"✓ Response from Agent B: {result_text}")
                await client.close()

            message_count += 1

        except Exception as e:
            logger.error(f"✗ Failed to send message: {e}")

        await asyncio.sleep(10)


def create_agent_a_server():
    """Create A2A server for Agent A."""
    agent_card = AgentCard(
        name="Agent A",
        url="http://agent-a:8001",
        description="Demo Agent A - sends and receives A2A messages",
        version="1.0.0",
        capabilities=AgentCapabilities(streaming=True),
        default_input_modes=["text/plain"],
        default_output_modes=["text/plain"],
        preferred_transport=TransportProtocol.jsonrpc,
        skills=[
            AgentSkill(
                id="process_message",
                name="Process Message",
                description="Processes messages from other agents",
                tags=["demo", "messaging"],
                examples=["Process this message"],
            )
        ],
    )

    executor = AgentAExecutor(agent_b_url=os.getenv("AGENT_B_URL", "http://agent-b:8000"))
    request_handler = DefaultRequestHandler(
        agent_executor=executor,
        task_store=InMemoryTaskStore(),
    )

    app = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

    return app.build()


async def main():
    """Run Agent A server with background message sender."""
    logger.info("Agent A starting on port 8001...")

    # Start background message sender
    asyncio.create_task(send_messages_to_b())

    # Start A2A server
    app = create_agent_a_server()
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="error",  # Reduce uvicorn noise
    )

    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
