from backend.llm.client import GroqClient
from backend.llm.config import GROQ_MODEL

from .prompts import CLASSIFIER_PROMPT


class MemoryClassifier:

    def __init__(self):

        self.client = GroqClient()

    def should_remember(self, text: str) -> bool:

        response = self.client.chat(
            messages=[
                {
                    "role": "system",
                    "content": CLASSIFIER_PROMPT,
                },
                {
                    "role": "user",
                    "content": text,
                },
            ],
            model=GROQ_MODEL,
        )

        return response.strip().upper() == "YES"