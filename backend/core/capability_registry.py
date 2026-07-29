from backend.capabilities.application.service import ApplicationService
from backend.capabilities.browser.service import BrowserService
from backend.capabilities.filesystem.service import FileSystemService
from backend.capabilities.desktop.service import DesktopService
from backend.capabilities.system.service import SystemService
from backend.capabilities.vision.service import VisionService
class CapabilityRegistry:

    def __init__(self):

        self.capabilities = {}

        self.register(
            "application",
            ApplicationService()
        )

        self.register(
            "browser",
            BrowserService()
        )

        self.register(
            "filesystem",
            FileSystemService()
        )

        self.register(
            "desktop",
            DesktopService()
        )

        self.register("system",SystemService())
        self.register("vision",VisionService())
    def register(
        self,
        name,
        capability
    ):

        self.capabilities[name.lower()] = capability

    def unregister(
        self,
        name
    ):

        self.capabilities.pop(
            name.lower(),
            None
        )

    def exists(
        self,
        name
    ):

        return name.lower() in self.capabilities

    def get(
        self,
        name
    ):

        capability = self.capabilities.get(
            name.lower()
        )

        if capability is None:
            raise Exception(
                f"Capability '{name}' not registered."
            )

        return capability

    def execute(
        self,
        capability,
        action,
        parameters
    ):

        service = self.get(capability)

        return service.execute(
            action,
            parameters
        )

    def list_capabilities(self):

        return list(
            self.capabilities.keys()
        )