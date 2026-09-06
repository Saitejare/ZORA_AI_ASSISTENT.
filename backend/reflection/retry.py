from backend.llm.service import LLMService


RETRY_PROMPT = """
You are ZORA's Retry Agent.

The previous command failed.

Your job is to repair the command.

Rules:

1. Return ONLY JSON.
2. Keep the same intent.
3. Fix missing parameters.
4. Fix wrong actions.
5. Never explain.

Return:

{
    "capability":"",
    "action":"",
    "parameters":{}
}
"""


class RetryAgent:

    def __init__(self):

        self.llm = LLMService()

    def repair(
        self,
        user_input,
        failed_command,
        error_message,
    ):

        prompt = f"""
{RETRY_PROMPT}

User Request:
{user_input}

Failed Command:
{failed_command}

Error:
{error_message}
"""

        return self.llm.generate_command(prompt)