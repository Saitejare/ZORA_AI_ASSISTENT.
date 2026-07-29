from threading import Lock

from kokoro import KPipeline

from .config import LANGUAGE


class ModelManager:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.pipeline = KPipeline(
                        lang_code=LANGUAGE
                    )
        return cls._instance

    def get_pipeline(self) -> KPipeline:
        return self.pipeline


model_manager = ModelManager()