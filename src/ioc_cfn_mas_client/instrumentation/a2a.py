# src/ioc_cfn_mas_client/instrumentation.py
"""Auto-instrumentation for A2A agents using monkey patching.

This module provides an instrumentor that automatically logs A2A interactions
without requiring decorators. Currently uses a mock logging endpoint for testing
connectivity and instrumentation behavior.
"""

from __future__ import annotations

import functools
import importlib.util
import logging
import sys
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from ioc_cfn_mas_client.client import Client

logger = logging.getLogger(__name__)


class A2AInstrumentor:
    """Automatically instruments A2A AgentExecutor to log interactions.

    This instrumentor monkey-patches the A2A SDK's AgentExecutor.execute() method
    to automatically log A2A messages and tasks without requiring manual decorators.

    Currently uses client.log_a2a_interaction() for testing connectivity. In production,
    this can be replaced with actual CFN API calls.

    Example:
        >>> from ioc_cfn_mas_client import Client
        >>> from ioc_cfn_mas_client.instrumentation import A2AInstrumentor
        >>>
        >>> client = Client(base_url="http://localhost:9002")
        >>> instrumentor = A2AInstrumentor(
        ...     client=client,
        ...     workspace_id="ws1",
        ...     mas_id="mas1"
        ... )
        >>> instrumentor.instrument()
        >>>
        >>> # Now all AgentExecutor.execute() calls are automatically logged!
        >>> class MyExecutor(AgentExecutor):
        ...     async def execute(self, context, event_queue):
        ...         # Automatically logged - no decorator needed!
        ...         pass
    """

    def __init__(
        self,
        client: Client,
        workspace_id: str,
        mas_id: str,
        publish_input: bool = True,
        publish_output: bool = True,
    ):
        """Initialize the instrumentor.

        Args:
            client: CFN MAS client instance
            workspace_id: Workspace identifier
            mas_id: Multi-agent system identifier
            publish_input: If True, publish incoming messages
            publish_output: If True, publish task completions
        """
        self.client = client
        self.workspace_id = workspace_id
        self.mas_id = mas_id
        self.publish_input = publish_input
        self.publish_output = publish_output
        self._original_methods = {}
        self._instrumented = False

    def instrument(self) -> None:
        """Apply instrumentation by monkey-patching AgentExecutor."""
        if self._instrumented:
            logger.info("Already instrumented, skipping...")
            return

        # Check if A2A SDK is available
        if importlib.util.find_spec("a2a") is None:
            raise ImportError(
                "A2A SDK not found. Please install: pip install a2a-sdk"
            )

        # Patch AgentExecutor using __init_subclass__ to handle ABC pattern
        try:
            from a2a.server.agent_execution import AgentExecutor

            # Save original __init_subclass__ if it exists
            original_init_subclass = getattr(AgentExecutor, '__init_subclass__', None)
            self._original_methods["AgentExecutor.__init_subclass__"] = original_init_subclass

            # Create instrumented wrapper
            client = self.client
            workspace_id = self.workspace_id
            mas_id = self.mas_id
            publish_input = self.publish_input
            publish_output = self.publish_output

            def create_instrumented_execute(original_execute):
                """Create instrumented version of execute method."""
                @functools.wraps(original_execute)
                async def instrumented_execute(self, context, event_queue):
                    """Instrumented execute that publishes to CFN."""
                    agent_id = self.__class__.__name__

                    # 1. Publish input message
                    if publish_input and hasattr(context, "message"):
                        try:
                            _publish_a2a_message(
                                client=client,
                                workspace_id=workspace_id,
                                mas_id=mas_id,
                                agent_id=agent_id,
                                message=context.message,
                                task_id=getattr(context, "task_id", None),
                                context_id=getattr(context, "context_id", None),
                                direction="input",
                            )
                        except Exception as e:
                            logger.error(f"Input publish failed: {e}")

                    # 2. Call original execute
                    result = await original_execute(self, context, event_queue)

                    # 3. Publish output/completion
                    if publish_output:
                        try:
                            _publish_a2a_task_completion(
                                client=client,
                                workspace_id=workspace_id,
                                mas_id=mas_id,
                                agent_id=agent_id,
                                task_id=getattr(context, "task_id", None),
                                context_id=getattr(context, "context_id", None),
                                result=result,
                            )
                        except Exception as e:
                            logger.error(f"Output publish failed: {e}")

                    return result
                return instrumented_execute

            # Hook into __init_subclass__ to patch all subclasses
            def instrumented_init_subclass(cls, **kwargs):
                # Call original __init_subclass__ if it exists
                if original_init_subclass is not None:
                    original_init_subclass(**kwargs)

                # Patch the execute method of this subclass
                if hasattr(cls, 'execute') and callable(cls.execute):
                    original_execute = cls.execute
                    cls.execute = create_instrumented_execute(original_execute)

            # Replace __init_subclass__ for future subclasses
            AgentExecutor.__init_subclass__ = classmethod(instrumented_init_subclass)

            # Also patch all existing subclasses
            def patch_subclasses(base_class):
                """Recursively patch all subclasses."""
                for subclass in base_class.__subclasses__():
                    if hasattr(subclass, 'execute') and callable(subclass.execute):
                        original_execute = subclass.execute
                        subclass.execute = create_instrumented_execute(original_execute)
                    # Recursively patch subclasses of subclasses
                    patch_subclasses(subclass)

            patch_subclasses(AgentExecutor)
            self._instrumented = True

            logger.info(f"✓ Instrumented AgentExecutor for workspace={workspace_id}, mas={mas_id}")

        except ImportError as e:
            raise ImportError(f"Failed to instrument A2A SDK: {e}")

    def uninstrument(self) -> None:
        """Remove instrumentation and restore original methods."""
        if not self._instrumented:
            return

        try:
            from a2a.server.agent_execution import AgentExecutor

            # Restore original method
            if "AgentExecutor.execute" in self._original_methods:
                AgentExecutor.execute = self._original_methods["AgentExecutor.execute"]
                del self._original_methods["AgentExecutor.execute"]

            self._instrumented = False
            logger.info("✓ Uninstrumented AgentExecutor")

        except ImportError:
            pass


# Helper functions (same as in decorators.py)


def _publish_a2a_message(
    client: Client,
    workspace_id: str,
    mas_id: str,
    agent_id: str,
    message,
    task_id: Optional[str],
    context_id: Optional[str],
    direction: str,
) -> None:
    """Publish A2A message to CFN shared memory."""
    timestamp = datetime.now(timezone.utc).isoformat()

    message_data = {
        "protocol": "google-a2a",
        "version": "0.3.0",
        "agent_id": agent_id,
        "message_id": getattr(message, "message_id", str(uuid4())),
        "task_id": task_id,
        "context_id": context_id,
        "timestamp": timestamp,
        "direction": direction,
        "type": "message",
        "data": {
            "role": str(getattr(message, "role", "UNKNOWN")),
            "parts": _serialize_parts(message),
            "metadata": getattr(message, "metadata", {}),
        },
    }

    # TODO: Store message in shared memory for agent-to-agent async communication
    # This enables the shared memory pattern where agents communicate via CFN storage:
    # - Agent A writes message → Agent B queries and reads → Agent B processes → Agent B writes result
    #
    # Uncomment to enable:
    # client.create_shared_memories(
    #     workspace_id=workspace_id,
    #     mas_id=mas_id,
    #     data={
    #         "to_agent": agent_id,
    #         "from_agent": "caller",  # Could extract from message metadata
    #         "message": message_data,
    #         "status": "pending" if direction == "input" else "completed",
    #         "direction": direction,
    #     },
    #     format="a2a-protocol",
    #     source_agent_id="system",
    #     agent_id=agent_id
    # )

    # For now: Use mock logging endpoint for testing (no CFN server required)
    client.log_a2a_interaction(
        workspace_id=workspace_id,
        mas_id=mas_id,
        agent_id=agent_id,
        interaction_type="message",
        data=message_data,
    )
    logger.info(f"Query from shared memory: workspace_id={workspace_id}, mas_id={mas_id}, agent_id={agent_id}")


def _publish_a2a_task_completion(
    client: Client,
    workspace_id: str,
    mas_id: str,
    agent_id: str,
    task_id: Optional[str],
    context_id: Optional[str],
    result,
) -> None:
    """Publish A2A task completion to CFN shared memory."""
    timestamp = datetime.now(timezone.utc).isoformat()

    task_data = {
        "protocol": "google-a2a",
        "version": "0.3.0",
        "agent_id": agent_id,
        "task_id": task_id,
        "context_id": context_id,
        "timestamp": timestamp,
        "type": "task_completion",
        "data": {
            "state": "TASK_STATE_COMPLETED",
            "result": str(result) if result else None,
        },
    }

    # TODO: Store task completion in shared memory
    # This completes the async communication pattern:
    # - Agent B stores completion result → Agent A can query for results
    #
    # Uncomment to enable:
    # client.create_shared_memories(
    #     workspace_id=workspace_id,
    #     mas_id=mas_id,
    #     data={
    #         "from_agent": agent_id,
    #         "task_completion": task_data,
    #         "status": "completed",
    #         "result": result,
    #     },
    #     format="a2a-protocol",
    #     source_agent_id=agent_id,
    #     agent_id=agent_id
    # )

    # For now: Use mock logging endpoint for testing (no CFN server required)
    client.log_a2a_interaction(
        workspace_id=workspace_id,
        mas_id=mas_id,
        agent_id=agent_id,
        interaction_type="task_completion",
        data=task_data,
    )
    logger.info(f"Update to shared memory: workspace_id={workspace_id}, mas_id={mas_id}, agent_id={agent_id}")


def _serialize_parts(message) -> list:
    """Serialize A2A Message parts."""
    parts = []
    if hasattr(message, "parts"):
        for part in message.parts:
            part_data = {}
            if hasattr(part, "text"):
                part_data["text"] = part.text
            if hasattr(part, "data"):
                part_data["data"] = part.data
            parts.append(part_data)
    return parts
