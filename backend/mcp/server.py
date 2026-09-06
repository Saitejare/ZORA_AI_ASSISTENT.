import logging

from backend.mcp.registry import MCPRegistry
from backend.mcp.tools import MCPTools

logger = logging.getLogger(__name__)


class MCPServer:

    def __init__(
        self,
        registry=None,
        tools=None,
    ):

        self.registry = registry or MCPRegistry()
        self.tools = tools or MCPTools()

    def call(
        self,
        capability,
        action,
        parameters,
    ):

        logger.info(
            "MCP Call -> %s/%s",
            capability,
            action,
        )

        return self.tools.execute(
            capability,
            action,
            parameters,
        )

    def shutdown(self):

        logger.info("Shutting down MCP Server")

        try:

            self.tools.shutdown()

        except Exception:

            logger.exception(
                "Failed to shutdown MCP Tools"
            )