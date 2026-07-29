import numpy as np

from .config import SPEED, VOICE
from .model_manager import model_manager


class SpeechSynthesizer:

    def __init__(self):
        self.pipeline = model_manager.get_pipeline()

    def synthesize(self, text: str):

        generator = self.pipeline(
            text=text,
            voice=VOICE,
            speed=SPEED,
        )

        audio_chunks = []

        for _, _, samples in generator:
            audio_chunks.append(samples)

        audio = np.concatenate(audio_chunks)

        return audio, 24000