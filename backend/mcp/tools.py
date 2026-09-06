import logging

from backend.core.capability_registry import CapabilityRegistry

logger = logging.getLogger(__name__)


class MCPTools:

    def __init__(self, registry=None):

        self.registry = registry or CapabilityRegistry()

    def execute(
        self,
        capability,
        action,
        parameters,
    ):

        logger.info(
            "Dispatching capability '%s' action '%s'",
            capability,
            action,
        )

        return self.registry.execute(
            capability=capability,
            action=action,
            parameters=parameters,
        )

    def shutdown(self):

        logger.info("Shutting down MCP Tools")

        try:

            self.registry.shutdown()

        except Exception:

            logger.exception(
                "Failed to shutdown Capability Registry"
            )