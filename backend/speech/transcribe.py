from pathlib import Path

from .models import model_manager


class SpeechTranscriber:
    def __init__(self) -> None:
        self.model = model_manager.get_model()

    def transcribe(self, audio_path: Path) -> str:
        segments, info = self.model.transcribe(
            str(audio_path),beam_size=10,best_of=5,temperature=0.0,language="en",vad_filter=True,word_timestamps=False,)

        text = "".join(segment.text for segment in segments).strip()

        return text