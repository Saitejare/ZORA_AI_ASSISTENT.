from pathlib import Path

VOICE = "af_heart"
LANGUAGE = "en-us"
SPEED = 1.0

BASE_DIR = Path(__file__).resolve().parent

MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_AUDIO = OUTPUT_DIR / "speech.wav"