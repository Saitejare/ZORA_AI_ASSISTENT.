import json
import re

from backend.planner.models import (
    ExecutionPlan,
    PlanStep,
)


class PlanParser:

    def _extract_json(self, response: str) -> str:
        text = response.strip()

        if text.startswith("```json"):
            text = text.removeprefix("```json").strip()

        if text.startswith("```"):
            text = text.removeprefix("```").strip()

        if text.endswith("```"):
            text = text.removesuffix("```").strip()

        if text.startswith("{"):
            return text

        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            return match.group(0)

        return text

    def parse(self, response: str) -> ExecutionPlan:

        payload = self._extract_json(response)

        try:
            data = json.loads(payload)
        except json.JSONDecodeError as exc:
            snippet = response.strip().replace("\n", " ")[:160]
            raise ValueError(
                f"Planner returned invalid JSON: {snippet}"
            ) from exc

        plan = ExecutionPlan()

        steps = data.get("steps")

        if not isinstance(steps, list):
            raise ValueError(
                "Planner response did not include a valid steps list."
            )

        for step in steps:

            plan.add_step(
                PlanStep(
                    capability=step["capability"],
                    action=step["action"],
                    parameters=step.get(
                        "parameters",
                        {},
                    ),
                )
            )

        return plan
