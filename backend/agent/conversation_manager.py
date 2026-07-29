from collections import deque
from typing import Dict, List


class ConversationManager:
    """
    Maintains short-term conversation history for the AI assistant.
    """

    def __init__(self, max_history: int = 20):

        self.max_history = max_history

        self.history = deque(maxlen=max_history)

    def add_user_message(self, message: str):

        self.history.append(
            {
                "role": "user",
                "content": message,
            }
        )

    def add_assistant_message(self, message: str):

        self.history.append(
            {
                "role": "assistant",
                "content": message,
            }
        )

    def add_system_message(self, message: str):

        self.history.append(
            {
                "role": "system",
                "content": message,
            }
        )

    def get_history(self) -> List[Dict]:

        return list(self.history)

    def clear(self):

        self.history.clear()

    def last_message(self):

        if not self.history:
            return None

        return self.history[-1]

    def message_count(self):

        return len(self.history)

    def build_prompt(self) -> str:

        prompt = ""

        for message in self.history:

            prompt += (
                f"{message['role'].upper()}: "
                f"{message['content']}\n"
            )

        return prompt