from backend.llm.service import LLMService


class IntentClassifier:

    def __init__(self):
        self.llm = LLMService()

    def classify(self, text: str) -> str:

        prompt = f"""
You are an intent classifier.

Classify the user's request into ONLY ONE category.

Categories:

COMMAND
- Open applications
- Create files
- Delete files
- Browser operations
- Desktop control
- System control

CHAT
- General questions
- Greetings
- Conversation
- Explanations
- Jokes
- Opinions

Return ONLY one word.

COMMAND
or
CHAT

User:
{text}
"""

        result = self.llm.chat(prompt).strip().upper()

        if "COMMAND" in result:
            return "COMMAND"

        return "CHAT"