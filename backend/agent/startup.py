from backend.llm.service import LLMService


class StartupAgent:

    def __init__(self):
        self.llm = LLMService()

    def greet(self, synthesizer, player):

        greeting = self.generate()

        print(f"\n🤖 ZORA : {greeting}")

        audio, sample_rate = synthesizer.synthesize(greeting)

        player.play(audio, sample_rate)
    def generate(self):

        prompt = """
You are ZORA, an intelligent AI desktop assistant.

The assistant has just started.

Generate exactly ONE natural greeting.

Rules:
- Maximum 20 words.
- Friendly and warm.
- Mention the user's name if known.
- Do not introduce yourself every time.
- Do not use emojis.
- Do not use quotation marks.
- Do not explain anything.
- Return ONLY the greeting.
"""
        return self.llm.one_shot(prompt).strip()