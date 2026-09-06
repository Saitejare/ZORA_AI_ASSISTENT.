from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class PlanStep:

    capability: str

    action: str

    parameters: Dict


@dataclass
class ExecutionPlan:

    steps: List[PlanStep] = field(default_factory=list)

    def add_step(self, step: PlanStep):

        self.steps.append(step)

    def empty(self):

        return len(self.steps) == 0