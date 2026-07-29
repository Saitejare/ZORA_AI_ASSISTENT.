from pathlib import Path

WHISPER_MODEL = "medium"
DEVICE = "cpu"
COMPUTE_TYPE = "int8"

SAMPLE_RATE = 16000
CHANNELS = 1
DTYPE = "float32"

FRAME_DURATION_MS = 30
VAD_AGGRESSIVENESS = 2
SILENCE_DURATION = 1.0
PRE_SPEECH_DURATION = 0.3
BASE_DIR = Path(__file__).resolve().parent

TEMP_DIR = BASE_DIR / "temp"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

AUDIO_FILE = TEMP_DIR / "recording.wav"