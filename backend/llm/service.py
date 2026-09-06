import json
import logging
from .client import GroqClient
from .config import GROQ_MODEL
from .command_prompt import SYSTEM_PROMPT
from .chat_prompt import CHAT_PROMPT

logger = logging.getLogger(__name__)


class LLMService:

    def __init__(self):

        self.client = GroqClient()

        # Planner / Command prompt
        self.command_messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

        # Conversation prompt
        self.chat_messages = [
            {
                "role": "system",
                "content": CHAT_PROMPT,
            }
        ]

    # ==========================================================
    # Generic one-shot generation
    # Used for intent classification
    # ==========================================================

    def generate(self, prompt: str) -> str:

        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]

        return self.client.chat(
            messages,
            GROQ_MODEL,
        ).strip()

    # ==========================================================
    # Natural Conversation
    # ==========================================================

    def chat(
        self,
        user_input: str,
        memory_context: str = "",
    ) -> str:

        messages = list(self.chat_messages)

        if memory_context:

            messages.append(
                {
                    "role": "system",
                    "content": (
                        "Relevant User Memory:\n"
                        f"{memory_context}"
                    ),
                }
            )

        messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        response = self.client.chat(
            messages,
            GROQ_MODEL,
        ).strip()

        # Save conversation history

        self.chat_messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        self.chat_messages.append(
            {
                "role": "assistant",
                "content": response,
            }
        )

        logger.info("Generated conversational response")

        return response

    # ==========================================================
    # Command Generation
    # ==========================================================

    def generate_command(
        self,
        user_input: str,
        memory_context: str = "",
    ):

        messages = list(self.command_messages)

        if memory_context:

            messages.append(
                {
                    "role": "system",
                    "content": (
                        "Relevant User Memory:\n"
                        f"{memory_context}"
                    ),
                }
            )

        messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        response = self.client.chat(
            messages,
            GROQ_MODEL,
        ).strip()

        # Remove markdown code blocks

        if response.startswith("```json"):

            response = (
                response
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

        elif response.startswith("```"):

            response = (
                response
                .replace("```", "")
                .strip()
            )

        command = json.loads(response)

        logger.info("Generated command from LLM")

        return command

    # ==========================================================
    # Reset Chat History
    # ==========================================================

    def reset(self):

        self.command_messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

        self.chat_messages = [
            {
                "role": "system",
                "content": CHAT_PROMPT,
            }
        ]

    # ==========================================================
    # Legacy One Shot
    # ==========================================================

    def one_shot(self, prompt: str):

        messages = [
            {
                "role": "system",
                "content": CHAT_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]

        return self.client.chat(
            messages,
            GROQ_MODEL,
        )