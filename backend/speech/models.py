from threading import Lock

from faster_whisper import WhisperModel

from .config import (
    COMPUTE_TYPE,
    DEVICE,
    WHISPER_MODEL,
)


class ModelManager:

    _instance = None
    _lock = Lock()

    def __new__(cls):

        if cls._instance is None:

            with cls._lock:

                if cls._instance is None:

                    cls._instance = super().__new__(
                        cls
                    )

                    print(
                        f"Loading Whisper model: {WHISPER_MODEL}"
                    )

                    print(
                        f"Device: {DEVICE}"
                    )

                    print(
                        f"Compute type: {COMPUTE_TYPE}"
                    )

                    cls._instance.model = WhisperModel(
                        model_size_or_path=WHISPER_MODEL,
                        device=DEVICE,
                        compute_type=COMPUTE_TYPE,
                    )

                    print(
                        "Whisper model loaded successfully."
                    )

        return cls._instance

    def get_model(self) -> WhisperModel:

        return self.model


model_manager = ModelManager()