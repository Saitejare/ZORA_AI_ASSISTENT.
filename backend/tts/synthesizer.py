"""ZORA text-to-speech synthesis."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from backend.tts.text_cleaner import clean_for_speech


logger = logging.getLogger(__name__)


class SpeechSynthesizer:

    def __init__(self) -> None:

        self.output_directory = (
            Path(__file__).resolve().parents[1]
            / "data"
        )

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.output_file = (
            self.output_directory
            / "response.mp3"
        )


    # =====================================================
    # SYNTHESIZE
    # =====================================================

    def synthesize(
        self,
        text: str,
    ) -> tuple[Path, int, str]:

        if not text or not text.strip():

            raise ValueError(
                "Cannot synthesize empty text."
            )


        # -------------------------------------------------
        # Clean ONLY the text sent to TTS.
        #
        # The original LLM response remains untouched
        # for the UI and conversation history.
        # -------------------------------------------------

        speech_text = clean_for_speech(
            text
        )


        if not speech_text:

            raise ValueError(
                "No speakable text remained after cleaning."
            )


        logger.info(
            "Preparing TTS text. Original chars=%d, speech chars=%d",
            len(text),
            len(speech_text),
        )

        logger.debug(
            "TTS speech text: %s",
            speech_text,
        )


        # -------------------------------------------------
        # Edge TTS
        # -------------------------------------------------

        try:

            from backend.config import (
                TTS_VOICE,
            )

        except ImportError:

            TTS_VOICE = (
                "en-IN-NeerjaNeural"
            )


        try:

            import asyncio
            import edge_tts


            async def generate() -> None:

                communicate = (
                    edge_tts.Communicate(
                        speech_text,
                        TTS_VOICE,
                    )
                )

                await communicate.save(
                    str(self.output_file)
                )


            asyncio.run(
                generate()
            )


            if not self.output_file.exists():

                raise RuntimeError(
                    "Edge TTS did not create the audio file."
                )


            file_size = (
                self.output_file.stat()
                .st_size
            )


            if file_size <= 0:

                raise RuntimeError(
                    "Generated TTS audio file is empty."
                )


            logger.info(
                "Edge TTS audio generated: %d bytes",
                file_size,
            )


            logger.info(
                "Edge TTS synthesis completed."
            )


            # Edge TTS MP3 sample rate is not directly
            # required by the browser audio player.
            #
            # Keep the existing API contract.
            sample_rate = 24000


            return (
                self.output_file,
                sample_rate,
                "audio/mpeg",
            )


        except Exception:

            logger.exception(
                "Edge TTS synthesis failed."
            )

            raise


    # =====================================================
    # OPTIONAL INSPECTION
    # =====================================================

    def prepare_text(
        self,
        text: str,
    ) -> str:
        """
        Return the exact cleaned text that will be spoken.
        """

        return clean_for_speech(
            text
        )