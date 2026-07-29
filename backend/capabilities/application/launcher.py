import os
import subprocess


class ApplicationLauncher:
    """
    Launches Windows applications from Start Menu shortcut paths.
    """

    def launch(self, application: dict):

        if application is None:
            raise Exception("Application not found.")

        shortcut = application["path"]

        if not os.path.exists(shortcut):
            raise Exception(f"Shortcut does not exist: {shortcut}")

        try:
            os.startfile(shortcut)

            return f"Opening {application['name'].title()}"

        except Exception:
            try:
                subprocess.Popen(shortcut, shell=True)

                return f"Opening {application['name'].title()}"

            except Exception as e:
                raise Exception(f"Failed to launch application: {e}")