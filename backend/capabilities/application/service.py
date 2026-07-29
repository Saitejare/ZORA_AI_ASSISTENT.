from .scanner import ApplicationScanner
from .matcher import ApplicationMatcher
from .launcher import ApplicationLauncher
from .process_manager import ProcessManager
from .window_manager import WindowManager


class ApplicationService:
    """
    Handles all application-related operations.

    Supported actions:
        - launch
        - terminate
        - is_running
        - activate
        - minimize
        - maximize
        - close_window
        - refresh
    """

    def __init__(self):

        self.scanner = ApplicationScanner()
        self.matcher = ApplicationMatcher()
        self.launcher = ApplicationLauncher()

        self.process_manager = ProcessManager()
        self.window_manager = WindowManager()

        self.refresh()

    def refresh(self):
        """
        Refresh the application cache.
        """
        self.applications = self.scanner.scan()

    def _find_application(self, target: str):

        application = self.matcher.match(
            target,
            self.applications
        )

        if application is None:
            raise Exception(f"Application '{target}' not found.")

        return application

    def execute(self, action, parameters):

        if action == "refresh":
            self.refresh()
            return "Application cache refreshed."

        target = parameters.get("target")

        if not target:
            raise Exception("Missing application target.")

        # ----------------------------------------------------
        # Launch Application
        # ----------------------------------------------------
        if action == "launch":

            application = self._find_application(target)

            return self.launcher.launch(application)

        # ----------------------------------------------------
        # Terminate Process
        # ----------------------------------------------------
        elif action == "terminate":

            count = self.process_manager.terminate(target)

            if count == 0:
                return f"No running process found for '{target}'."

            return f"Terminated {count} process(es)."

        # ----------------------------------------------------
        # Check Running Status
        # ----------------------------------------------------
        elif action == "is_running":

            running = self.process_manager.is_running(target)

            if running:
                return f"{target} is running."

            return f"{target} is not running."

        # ----------------------------------------------------
        # Bring Window to Front
        # ----------------------------------------------------
        elif action == "activate":

            success = self.window_manager.activate(target)

            if success:
                return f"Activated {target}."

            return f"Window not found for '{target}'."

        # ----------------------------------------------------
        # Minimize Window
        # ----------------------------------------------------
        elif action == "minimize":

            success = self.window_manager.minimize(target)

            if success:
                return f"Minimized {target}."

            return f"Window not found for '{target}'."

        # ----------------------------------------------------
        # Maximize Window
        # ----------------------------------------------------
        elif action == "maximize":

            success = self.window_manager.maximize(target)

            if success:
                return f"Maximized {target}."

            return f"Window not found for '{target}'."

        # ----------------------------------------------------
        # Close Window
        # ----------------------------------------------------
        elif action == "close_window":

            success = self.window_manager.close(target)

            if success:
                return f"Closed window for {target}."

            return f"Window not found for '{target}'."

        # ----------------------------------------------------
        # Unsupported Action
        # ----------------------------------------------------
        else:

            raise Exception(f"Unsupported action: {action}")