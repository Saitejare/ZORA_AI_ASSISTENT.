from __future__ import annotations

import logging
from typing import Any

from groq import Groq

from .config import GROQ_API_KEY


logger = logging.getLogger(__name__)


class GroqClient:

    def __init__(self) -> None:

        if not GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        self.client = Groq(
            api_key=GROQ_API_KEY
        )


    # =====================================================
    # CHAT COMPLETION
    # =====================================================

    def chat(
        self,
        messages: list[dict[str, Any]],
        model: str,
        *,
        temperature: float = 0.3,
        max_completion_tokens: int = 1024,
    ) -> str:

        logger.info(
            "Sending request to Groq model: %s",
            model,
        )

        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_completion_tokens=max_completion_tokens,
        )


        # -------------------------------------------------
        # Validate response
        # -------------------------------------------------

        if not response.choices:

            raise RuntimeError(
                "Groq returned no choices."
            )


        message = response.choices[0].message

        content = message.content


        # -------------------------------------------------
        # Handle empty content
        # -------------------------------------------------

        if content is None:

            logger.error(
                "Groq returned empty message content."
            )

            raise RuntimeError(
                "Groq returned an empty response."
            )


        content = content.strip()


        if not content:

            logger.error(
                "Groq returned an empty text response."
            )

            raise RuntimeError(
                "Groq returned an empty text response."
            )


        logger.info(
            "Groq response received successfully."
        )


        return content