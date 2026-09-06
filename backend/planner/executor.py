import logging

from backend.agent.validator import Validator
from backend.agent.executor import Executor
from backend.agent.response_generator import ResponseGenerator

from backend.reflection.reflector import Reflector
from backend.reflection.retry import RetryAgent

logger = logging.getLogger(__name__)


class PlanExecutor:

    def __init__(
        self,
        validator=None,
        executor=None,
        response_generator=None,
        reflector=None,
        retry=None,
    ):

        self.validator = validator or Validator()
        self.executor = executor or Executor()
        self.response_generator = (
            response_generator or ResponseGenerator()
        )

        self.reflector = reflector or Reflector()
        self.retry = retry or RetryAgent()

    def execute(
        self,
        plan,
        user_input,
    ):

        logger.info(
            "Executing plan with %d step(s)",
            len(plan.steps),
        )

        responses = []

        for index, step in enumerate(plan.steps, start=1):

            logger.info(
                "Executing step %d : %s/%s",
                index,
                step.capability,
                step.action,
            )

            command = {
                "capability": step.capability,
                "action": step.action,
                "parameters": step.parameters,
            }

            try:

                self.validator.validate(command)

                result = self.executor.execute(command)

                reflection = self.reflector.reflect(
                    command,
                    result,
                )

                if reflection.retry:

                    logger.info(
                        "Retrying step %d",
                        index,
                    )

                    repaired = self.retry.repair(
                        user_input=user_input,
                        failed_command=command,
                        error_message=reflection.reason,
                    )

                    self.validator.validate(repaired)

                    result = self.executor.execute(
                        repaired
                    )

                responses.append(
                    self.response_generator.generate(
                        result
                    )
                )

            except Exception as e:

                logger.exception(
                    "Step %d failed",
                    index,
                )

                responses.append(
                    f"I couldn't complete this step: {e}"
                )

        logger.info("Plan execution completed.")

        return responses

    def shutdown(self):

        logger.info("Shutting down PlanExecutor")

        try:

            self.executor.shutdown()

        except Exception:

            logger.exception(
                "Executor shutdown failed."
            )