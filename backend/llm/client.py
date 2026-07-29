from groq import Groq

from .config import GROQ_API_KEY


class GroqClient:

    def __init__(self):
        self.client = Groq(
            api_key=GROQ_API_KEY
        )

    def chat(self, messages, model):

        response = self.client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=0.5,
    max_completion_tokens=120,
)

        return response.choices[0].message.content