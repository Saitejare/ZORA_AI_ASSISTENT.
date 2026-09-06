import logging

from backend.mcp.server import MCPServer
from backend.agent.models import (
    ExecutionResult,
    ExecutionStatus,
)

logger = logging.getLogger(__name__)


class Executor:

    def __init__(self, mcp=None):

        self.mcp = mcp or MCPServer()

    def execute(self, command: dict) -> ExecutionResult:
        """
        Execute a single command.
        """

        capability = command.get("capability")
        action = command.get("action")
        parameters = command.get("parameters", {})

        logger.info(
            "Executing capability=%s action=%s",
            capability,
            action,
        )

        try:

            result = self.mcp.call(
                capability=capability,
                action=action,
                parameters=parameters,
            )

            logger.info("Execution successful.")

            return ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                message="Execution completed successfully.",
                data=result,
            )

        except Exception as e:

            logger.exception("Execution failed.")

            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message=str(e),
                data=None,
            )

    def shutdown(self):

        logger.info("Shutting down Executor")

        try:
            self.mcp.shutdown()

        except Exception:
            logger.exception("Failed to shutdown MCP Server")