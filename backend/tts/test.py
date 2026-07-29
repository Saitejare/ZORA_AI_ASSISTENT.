import time

from .synthesizer import SpeechSynthesizer

tts = SpeechSynthesizer()

start = time.perf_counter()

tts.synthesize("Hello, I am ZORA. How can I help you today?")

print(f"TTS Time: {time.perf_counter() - start:.2f} seconds")