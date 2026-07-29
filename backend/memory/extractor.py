from backend.llm.client import GroqClient
from backend.llm.config import GROQ_MODEL

from .prompts import EXTRACTOR_PROMPT


class MemoryExtractor:

    def __init__(self):

        self.client = GroqClient()

    def extract(self, text: str) -> str:

        response = self.client.chat(
            messages=[
                {
                    "role": "system",
                    "content": EXTRACTOR_PROMPT,
                },
                {
                    "role": "user",
                    "content": text,
                },
            ],
            model=GROQ_MODEL,
        )

        return response.strip()