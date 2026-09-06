from backend.agent.models import (
    ExecutionResult,
    ExecutionStatus,
)


class ResponseGenerator:
    """
    Converts the execution result into a natural language response.
    """

    def generate(self, result):

        if result.status == ExecutionStatus.SUCCESS:

            if result.data:

                return str(result.data)

            return "Task completed successfully."

        return f"I couldn't complete that: {result.message}"
