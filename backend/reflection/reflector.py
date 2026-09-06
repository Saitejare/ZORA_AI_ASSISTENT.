from backend.reflection.models import ReflectionResult
from backend.reflection.verifier import Verifier


class Reflector:

    def __init__(self):

        self.verifier = Verifier()

    def reflect(
        self,
        command,
        execution_result,
    ):

        # ----------------------------------
        # Execution Failed
        # ----------------------------------

        if execution_result.status.name != "SUCCESS":

            return ReflectionResult(
                success=False,
                reason=execution_result.message,
                retry=True,
            )

        # ----------------------------------
        # Verify the Result
        # ----------------------------------

        verified = self.verifier.verify(
            command,
            execution_result,
        )

        if verified:

            return ReflectionResult(
                success=True,
                reason="Task verified successfully.",
                retry=False,
            )

        # ----------------------------------
        # Verification Failed
        # ----------------------------------

        return ReflectionResult(
            success=False,
            reason="Execution completed but verification failed.",
            retry=True,
        )