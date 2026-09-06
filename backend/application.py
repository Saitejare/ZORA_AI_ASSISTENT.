"""Application lifecycle and dependency wiring for ZORA."""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import router
from backend.config import AppConfig, load_config


logger = logging.getLogger(__name__)


class ZoraApplication:
    """Coordinates startup, API, voice, AI, and shutdown flows."""

    def __init__(
        self,
        config: AppConfig | None = None,
    ) -> None:

        self.config = config or load_config()

        self.initialized = False

        self.started_at: float | None = None

        self.orchestrator: Any | None = None

        self._recorder: Any | None = None
        self._transcriber: Any | None = None
        self._synthesizer: Any | None = None

        self._logging_configured = False


    # =====================================================
    # INITIALIZE
    # =====================================================

    def initialize(self) -> None:
        """
        Initialize ZORA core services.

        Heavy microphone initialization is deliberately
        performed separately through initialize_microphone().
        """

        if self.initialized:
            return

        self._configure_logging()

        logger.info(
            "Initializing ZORA application..."
        )

        from backend.agent.orchestrator import Orchestrator

        self.orchestrator = Orchestrator()

        self.initialized = True

        self.started_at = time.time()

        logger.info(
            "ZORA application initialized."
        )


    # =====================================================
    # MICROPHONE INITIALIZATION
    # =====================================================

    def initialize_microphone(self) -> dict[str, Any]:
        """
        Initialize the microphone before the frontend
        starts the ZORA introduction.
        """

        self.initialize()

        if self._recorder is None:

            from backend.speech.record import SpeechRecorder

            self._recorder = SpeechRecorder()

        logger.info(
            "Preparing ZORA microphone..."
        )

        self._recorder.initialize()

        logger.info(
            "ZORA microphone is ready."
        )

        return {
            "ready": True,
            "microphone": True,
        }


    # =====================================================
    # FASTAPI
    # =====================================================

    def start(self) -> FastAPI:
        """Create and return the FastAPI application."""

        self._configure_logging()

        app = FastAPI(
            title="ZORA AI Assistant",
            version="1.0.0",
        )

        app.state.zora = self

        app.add_middleware(
            CORSMiddleware,
            allow_origins=list(
                self.config.server.cors_origins
            ),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        app.include_router(router)

        logger.info(
            "FastAPI application started"
        )

        return app


    # =====================================================
    # TEXT
    # =====================================================

    def process_text(
        self,
        text: str,
    ) -> str:

        if not text.strip():

            raise ValueError(
                "Message cannot be empty."
            )

        self.initialize()

        assert self.orchestrator is not None

        logger.info(
            "Processing text request"
        )

        return self.orchestrator.run(
            text.strip()
        )


    # =====================================================
    # VOICE
    # =====================================================

    def process_voice(
        self,
        audio_path: str | None = None,
    ) -> dict[str, Any]:
        """
        Complete voice pipeline.

        Microphone
            ↓
        Whisper
            ↓
        Transcript
            ↓
        ZORA
            ↓
        Edge TTS
        """

        self.initialize()

        # -------------------------------------------------
        # Recorder
        # -------------------------------------------------

        if self._recorder is None:

            from backend.speech.record import SpeechRecorder

            self._recorder = SpeechRecorder()

        # -------------------------------------------------
        # Transcriber
        # -------------------------------------------------

        if self._transcriber is None:

            from backend.speech.transcribe import SpeechTranscriber

            self._transcriber = SpeechTranscriber()

        # -------------------------------------------------
        # Ensure microphone is ready
        # -------------------------------------------------

        if not self._recorder.is_ready:

            logger.info(
                "Microphone was not ready. Initializing now."
            )

            self._recorder.initialize()

        # -------------------------------------------------
        # Record
        # -------------------------------------------------

        logger.info(
            "Starting microphone recording"
        )

        audio = self._recorder.record()

        # -------------------------------------------------
        # Language
        # -------------------------------------------------

        try:

            from backend.speech.config import SPEECH_LANGUAGE

        except ImportError:

            SPEECH_LANGUAGE = "auto"

        # -------------------------------------------------
        # Transcription
        # -------------------------------------------------

        logger.info(
            "Transcribing voice input."
        )

        transcript = self._transcriber.transcribe(
            audio,
            language=SPEECH_LANGUAGE,
        )

        if not transcript:

            raise ValueError(
                "No speech was detected."
            )

        logger.info(
            "Voice transcript: %s",
            transcript,
        )

        # -------------------------------------------------
        # AI
        # -------------------------------------------------

        response = self.process_text(
            transcript
        )

        # -------------------------------------------------
        # TTS
        # -------------------------------------------------

        try:

            audio_output = self._synthesize(
                response
            )

        except Exception:

            logger.exception(
                "TTS synthesis failed"
            )

            audio_output = {
                "sample_rate": 0,
                "audio_file": None,
                "error": (
                    "Speech output failed, "
                    "but the text response is available."
                ),
            }

        return {
            "transcript": transcript,
            "response": response,
            "audio": audio_output,
        }


    # =====================================================
    # DIRECT COMMAND
    # =====================================================

    def process_command(
        self,
        capability: str,
        action: str,
        parameters: dict[str, Any],
    ) -> Any:

        self.initialize()

        assert self.orchestrator is not None

        command = {
            "capability": capability,
            "action": action,
            "parameters": parameters,
        }

        validated = (
            self.orchestrator
            .executor
            .validator
            .validate(command)
        )

        result = (
            self.orchestrator
            .executor
            .executor
            .execute(validated)
        )

        return (
            result.model_dump()
            if hasattr(result, "model_dump")
            else result
        )


    # =====================================================
    # SHUTDOWN
    # =====================================================

    def shutdown(self) -> None:

        logger.info(
            "Shutting down ZORA application"
        )

        try:

            if self.orchestrator:

                self.orchestrator.shutdown()

        except Exception:

            logger.exception(
                "Orchestrator shutdown failed."
            )

        self.initialized = False


    # =====================================================
    # HEALTH
    # =====================================================

    def health(self) -> Any:

        from backend.api.models import HealthResponse

        return HealthResponse(
            status="ok",
            initialized=self.initialized,
            version="1.0.0",
        )


    # =====================================================
    # STATUS
    # =====================================================

    def status(self) -> dict[str, Any]:

        uptime = (
            None
            if self.started_at is None
            else round(
                time.time()
                - self.started_at,
                2,
            )
        )

        return {
            "initialized": self.initialized,
            "uptime_seconds": uptime,
            "speech_loaded": (
                self._transcriber is not None
            ),
            "microphone_ready": (
                self._recorder is not None
                and self._recorder.is_ready
            ),
            "tts_loaded": (
                self._synthesizer is not None
            ),
        }


    # =====================================================
    # CONVERSATION
    # =====================================================

    def conversation_history(
        self,
    ) -> list[dict[str, Any]]:

        if self.orchestrator is None:

            return []

        return (
            self.orchestrator
            .conversation
            .get_history()
        )


    # =====================================================
    # MEMORY
    # =====================================================

    def memory_snapshot(
        self,
    ) -> dict[str, Any]:

        if self.orchestrator is None:

            return {
                "enabled": self.config.memory.enabled,
                "items": [],
            }

        return {
            "enabled": self.config.memory.enabled,
            "items": (
                self.orchestrator
                .memory
                .recall(
                    "user preferences"
                )
            ),
        }


    # =====================================================
    # TEXT TO SPEECH
    # =====================================================

    def _synthesize(
        self,
        text: str,
    ) -> dict[str, Any]:

        if self._synthesizer is None:

            from backend.tts.synthesizer import SpeechSynthesizer

            self._synthesizer = SpeechSynthesizer()

        (
            audio_file,
            sample_rate,
            media_type,
        ) = self._synthesizer.synthesize(
            text
        )

        logger.info(
            "TTS generated successfully: %s",
            audio_file,
        )

        logger.info(
            "TTS media type: %s",
            media_type,
        )

        return {
            "sample_rate": sample_rate,
            "audio_file": str(audio_file),
            "media_type": media_type,
        }


    # =====================================================
    # LOGGING
    # =====================================================

    def _configure_logging(self) -> None:

        if self._logging_configured:
            return

        self.config.paths.logs_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        logging.basicConfig(
            level=logging.INFO,
            format=(
                "%(asctime)s "
                "%(levelname)s "
                "[%(name)s] "
                "%(message)s"
            ),
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(
                    self.config.paths.logs_dir
                    / "zora.log",
                    encoding="utf-8",
                ),
            ],
        )

        self._logging_configured = True


# =========================================================
# GLOBAL APPLICATION
# =========================================================

zora_application = ZoraApplication()

app = zora_application.start()