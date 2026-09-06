from backend.llm.service import LLMService


class Planner:

    def __init__(self):

        self.llm = LLMService()

    def plan(self, user_input: str):

        return self.llm.generate_command(user_input)