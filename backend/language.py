"""Small language helpers for routing STT/TTS behavior."""

from __future__ import annotations


def detect_language_code(text: str, default: str = "en") -> str:
    """Detect languages needed by local routing without changing the text."""

    for char in text:
        codepoint = ord(char)

        if 0x0C00 <= codepoint <= 0x0C7F:
            return "te"

    return default
