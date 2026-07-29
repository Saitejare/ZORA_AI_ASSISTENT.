from backend.core.capability_registry import CapabilityRegistry
from backend.agent.models import (
    ExecutionResult,
    ExecutionStatus,
)


class Executor:

    def __init__(self):
        self.registry = CapabilityRegistry()

    def execute(self, command: dict) -> ExecutionResult:
        """
        Execute a single command returned by the LLM.
        """

        try:

            result = self.registry.execute(
                capability=command["capability"],
                action=command["action"],
                parameters=command.get("parameters", {}),
            )

            return ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                message="Execution completed successfully.",
                data=result,
            )

        except Exception as e:

            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message=str(e),
                data=None,
            )