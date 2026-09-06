from pathlib import Path
import logging

import speech_recognition as sr


logger = logging.getLogger(__name__)


class SpeechTranscriber:

    def __init__(self) -> None:

        self.recognizer = sr.Recognizer()


    # =========================================================
    # WHISPER TRANSCRIPTION
    # =========================================================

    def _transcribe_whisper(
        self,
        audio: sr.AudioData,
        language: str = "auto",
    ) -> str:

        from backend.speech.models import model_manager


        # -----------------------------------------------------
        # Temporary audio directory
        # -----------------------------------------------------

        audio_dir = (
            Path(__file__).resolve().parent
            / "temp"
        )

        audio_dir.mkdir(
            parents=True,
            exist_ok=True,
        )


        # -----------------------------------------------------
        # Save recording
        # -----------------------------------------------------

        audio_file = (
            audio_dir
            / "recording.wav"
        )

        audio_file.write_bytes(
            audio.get_wav_data()
        )


        # -----------------------------------------------------
        # Determine language
        # -----------------------------------------------------

        whisper_language = None

        normalized_language = (
            language or "auto"
        ).strip().lower()


        if normalized_language not in {
            "auto",
            "multilingual",
            "",
        }:

            whisper_language = (
                normalized_language
            )


        # -----------------------------------------------------
        # Logging
        # -----------------------------------------------------

        logger.info(
            "Starting Whisper transcription: model=%s language=%s",
            getattr(
                model_manager,
                "model_name",
                "configured",
            ),
            whisper_language or "auto",
        )


        # -----------------------------------------------------
        # Whisper transcription
        # -----------------------------------------------------

        segments, info = (
            model_manager
            .get_model()
            .transcribe(
                str(audio_file),

                language=whisper_language,

                vad_filter=True,

                beam_size=5,

                temperature=0.0,

                condition_on_previous_text=False,
            )
        )


        # -----------------------------------------------------
        # Build transcript
        # -----------------------------------------------------

        text_parts = []


        for segment in segments:

            segment_text = (
                segment.text
                .strip()
            )

            if segment_text:

                text_parts.append(
                    segment_text
                )


        text = " ".join(
            text_parts
        ).strip()


        # -----------------------------------------------------
        # Language information
        # -----------------------------------------------------

        detected_language = getattr(
            info,
            "language",
            None,
        )

        language_probability = getattr(
            info,
            "language_probability",
            None,
        )


        logger.info(
            "Whisper detected language=%s probability=%s",
            detected_language,
            language_probability,
        )


        logger.info(
            "Whisper transcript: %s",
            text,
        )


        return text


    # =========================================================
    # PUBLIC TRANSCRIBE METHOD
    # =========================================================

    def transcribe(
        self,
        audio: sr.AudioData,
        language: str = "auto",
    ) -> str:

        try:

            print(
                "Recognizing..."
            )


            normalized_language = (
                language or "auto"
            ).strip().lower()


            # -------------------------------------------------
            # Whisper for automatic/multilingual recognition
            # -------------------------------------------------

            if normalized_language in {
                "auto",
                "multilingual",
                "",
            }:

                text = (
                    self._transcribe_whisper(
                        audio,
                        language="auto",
                    )
                )


            # -------------------------------------------------
            # Telugu / English / explicit language
            # -------------------------------------------------

            else:

                text = (
                    self._transcribe_whisper(
                        audio,
                        language=normalized_language,
                    )
                )


            # -------------------------------------------------
            # Result
            # -------------------------------------------------

            text = (
                text
                .strip()
            )


            if text:

                print(
                    f"User said: {text}"
                )

            else:

                print(
                    "Speech could not be understood."
                )


            return text


        # -----------------------------------------------------
        # SpeechRecognition errors
        # -----------------------------------------------------

        except sr.UnknownValueError:

            print(
                "Speech could not be understood."
            )

            return ""


        except sr.RequestError as exc:

            print(
                "Speech recognition service error: "
                f"{exc}"
            )

            raise RuntimeError(
                "Speech recognition service is unavailable."
            ) from exc


        except Exception:

            logger.exception(
                "Whisper transcription failed."
            )

            raise