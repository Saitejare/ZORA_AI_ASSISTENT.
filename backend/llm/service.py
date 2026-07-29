import json

from .client import GroqClient
from .config import GROQ_MODEL
from .prompts import SYSTEM_PROMPT


class LLMService:

    def __init__(self):

        self.client = GroqClient()

        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

    def chat(self, user_message: str, memory_context: str = "") -> str:

        if memory_context:

            self.messages.append(
                {
                    "role": "system",
                    "content": f"Relevant User Memory:\n{memory_context}",
                }
            )

        self.messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        response = self.client.chat(
            self.messages,
            GROQ_MODEL,
        )

        self.messages.append(
            {
                "role": "assistant",
                "content": response,
            }
        )

        return response

    def generate_command(self, user_input: str):

        response = self.chat(user_input).strip()

        if response.startswith("```json"):
            response = (
                response.replace("```json", "")
                .replace("```", "")
                .strip()
            )

        elif response.startswith("```"):
            response = (
                response.replace("```", "")
                .strip()
            )

        try:

            command = json.loads(response)

            print("\n========== LLM COMMAND ==========")
            print(command)
            print("=================================\n")

            return command

        except json.JSONDecodeError:

            raise Exception(
                f"LLM returned invalid JSON:\n{response}"
            )

    def reset(self):

        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]