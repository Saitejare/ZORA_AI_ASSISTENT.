from __future__ import annotations

import logging
import threading

import speech_recognition as sr


logger = logging.getLogger(__name__)


class SpeechRecorder:
    """
    Production microphone recorder for ZORA.

    The microphone is initialized once and reused.
    Ambient-noise calibration is performed only once,
    which avoids the delay before every request.
    """

    def __init__(self) -> None:

        self.recognizer = sr.Recognizer()

        self.recognizer.pause_threshold = 0.8
        self.recognizer.non_speaking_duration = 0.3
        self.recognizer.phrase_threshold = 0.2

        self._microphone: sr.Microphone | None = None
        self._microphone_ready = False

        self._lock = threading.Lock()


    # =====================================================
    # MICROPHONE INITIALIZATION
    # =====================================================

    def initialize(self) -> None:
        """
        Initialize the microphone once.

        This should happen before ZORA introduces herself.
        """

        with self._lock:

            if self._microphone_ready:
                return

            logger.info(
                "Initializing ZORA microphone..."
            )

            microphone = sr.Microphone()

            with microphone as source:

                logger.info(
                    "Calibrating microphone for ambient noise..."
                )

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5,
                )

            self._microphone = microphone
            self._microphone_ready = True

            logger.info(
                "ZORA microphone ready."
            )


    # =====================================================
    # RECORD
    # =====================================================

    def record(self) -> sr.AudioData:
        """
        Record one user utterance.

        The microphone must already be initialized.
        """

        if not self._microphone_ready:

            self.initialize()

        if self._microphone is None:

            raise RuntimeError(
                "ZORA microphone is not initialized."
            )

        logger.info(
            "Microphone ready. Listening for user speech."
        )

        print("Listening...")

        with self._microphone as source:

            audio = self.recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=10,
            )

        logger.info(
            "Recording finished."
        )

        print(
            "Recording finished"
        )

        return audio


    # =====================================================
    # STATUS
    # =====================================================

    @property
    def is_ready(self) -> bool:

        return self._microphone_ready