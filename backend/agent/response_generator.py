from backend.agent.models import (
    ExecutionResult,
    ExecutionStatus,
)


class ResponseGenerator:
    """
    Converts the execution result into a natural language response.
    """

    def generate(self, result: ExecutionResult) -> str:

        if result.status == ExecutionStatus.SUCCESS:

            if result.data is not None:
                return str(result.data)

            return "Done."

        return f"Failed: {result.message}"