from pathlib import Path


class Verifier:

    def verify(self, command, result):

        capability = command["capability"]
        action = command["action"]
        parameters = command.get("parameters", {})

        # -------------------------------------
        # Filesystem Verification
        # -------------------------------------

        if capability == "filesystem":

            if action == "create_file":

                return Path(
                    parameters["path"]
                ).exists()

            elif action == "create_folder":

                return Path(
                    parameters["path"]
                ).exists()

            elif action == "delete_file":

                return not Path(
                    parameters["path"]
                ).exists()

            elif action == "write_file":

                path = Path(parameters["path"])

                if not path.exists():
                    return False

                return (
                    path.read_text(
                        encoding="utf-8"
                    ) == parameters["content"]
                )

        # -------------------------------------
        # Browser
        # -------------------------------------

        if capability == "browser":

            return result.status.name == "SUCCESS"

        # -------------------------------------
        # Application
        # -------------------------------------

        if capability == "application":

            return result.status.name == "SUCCESS"

        # -------------------------------------
        # Desktop
        # -------------------------------------

        if capability == "desktop":

            return result.status.name == "SUCCESS"

        # -------------------------------------
        # Vision
        # -------------------------------------

        if capability == "vision":

            return result.status.name == "SUCCESS"

        # -------------------------------------
        # System
        # -------------------------------------

        if capability == "system":

            return result.status.name == "SUCCESS"

        return False