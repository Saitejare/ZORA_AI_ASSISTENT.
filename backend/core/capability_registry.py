import logging
from typing import Any, Callable

logger = logging.getLogger(__name__)


class CapabilityRegistry:
    """
    Lazy capability registry.

    Capabilities are instantiated only when first used.
    """

    def __init__(self):

        self.capabilities: dict[str, Any] = {}

        self.factories: dict[str, Callable[[], Any]] = {
            "application": self._application_service,
            "browser": self._browser_service,
            "filesystem": self._filesystem_service,
            "desktop": self._desktop_service,
            "system": self._system_service,
            "vision": self._vision_service,
        }

    # --------------------------------------------------

    def register(
        self,
        name: str,
        capability: Any,
    ):

        logger.info(
            "Registering capability '%s'",
            name,
        )

        self.capabilities[name.lower()] = capability

    # --------------------------------------------------

    def unregister(
        self,
        name: str,
    ):

        self.capabilities.pop(
            name.lower(),
            None,
        )

    # --------------------------------------------------

    def exists(
        self,
        name: str,
    ) -> bool:

        return name.lower() in self.factories

    # --------------------------------------------------

    def get(
        self,
        name: str,
    ):

        name = name.lower()

        if name in self.capabilities:

            return self.capabilities[name]

        factory = self.factories.get(name)

        if factory is None:

            raise Exception(
                f"Unknown capability '{name}'."
            )

        logger.info(
            "Initializing capability '%s'",
            name,
        )

        capability = factory()

        self.capabilities[name] = capability

        return capability

    # --------------------------------------------------

    def execute(
        self,
        capability: str,
        action: str,
        parameters: dict,
    ):

        service = self.get(capability)

        logger.info(
            "Executing %s/%s",
            capability,
            action,
        )

        return service.execute(
            action,
            parameters,
        )

    # --------------------------------------------------

    def list_capabilities(self):

        return sorted(
            self.factories.keys()
        )

    # --------------------------------------------------

    def shutdown(self):

        logger.info(
            "Shutting down Capability Registry"
        )

        for name, capability in list(
            self.capabilities.items()
        ):

            shutdown = getattr(
                capability,
                "shutdown",
                None,
            )

            if callable(shutdown):

                try:

                    shutdown()

                except Exception:

                    logger.exception(
                        "Failed to shutdown capability '%s'",
                        name,
                    )

        self.capabilities.clear()

    # ==================================================
    # Factories
    # ==================================================

    def _application_service(self):

        from backend.capabilities.application.service import (
            ApplicationService,
        )

        return ApplicationService()

    def _browser_service(self):

        from backend.capabilities.browser.service import (
            BrowserService,
        )

        return BrowserService()

    def _filesystem_service(self):

        from backend.capabilities.filesystem.service import (
            FileSystemService,
        )

        return FileSystemService()

    def _desktop_service(self):

        from backend.capabilities.desktop.service import (
            DesktopService,
        )

        return DesktopService()

    def _system_service(self):

        from backend.capabilities.system.service import (
            SystemService,
        )

        return SystemService()

    def _vision_service(self):

        from backend.capabilities.vision.service import (
            VisionService,
        )

        return VisionService()