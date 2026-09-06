from pathlib import Path
import os


AUDIO_FILE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "response.wav"
)


SPEECH_LANGUAGE = os.getenv(
    "SPEECH_LANGUAGE",
    "auto",
)


WHISPER_MODEL = os.getenv(
    "WHISPER_MODEL",
    "base",
)


DEVICE = os.getenv(
    "WHISPER_DEVICE",
    "cpu",
)


COMPUTE_TYPE = os.getenv(
    "WHISPER_COMPUTE_TYPE",
    "int8",
)