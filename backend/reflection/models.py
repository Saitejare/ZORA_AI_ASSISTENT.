from dataclasses import dataclass


@dataclass
class ReflectionResult:

    success: bool

    reason: str = ""

    retry: bool = False

    corrected_command: dict | None = None