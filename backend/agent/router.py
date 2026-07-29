from backend.llm.service import LLMService
from .models import RequestType


class Router:

    def __init__(self):
        self.llm = LLMService()

    def classify(self, text: str) -> RequestType:
        """
        Classify the user's request into one of the supported request types.
        """

        prompt = f"""
You are an intent classifier.

Return ONLY one word.

chat
capability
memory
system

Examples

Open Chrome
capability

Search YouTube
capability

Create Folder
capability

Delete File
capability

Remember my favourite language is Python
memory

What is my favourite language
memory

Who are you
chat

Explain Python decorators
chat

Shutdown computer
system

Restart computer
system

User:
{text}
"""

        response = self.llm.chat(prompt).strip().lower()

        if response == "capability":
            return RequestType.CAPABILITY

        if response == "memory":
            return RequestType.MEMORY

        if response == "system":
            return RequestType.SYSTEM

        return RequestType.CHAT

    def route(self, text: str) -> RequestType:
        """
        Backward-compatible alias for classify().
        """
        return self.classify(text)