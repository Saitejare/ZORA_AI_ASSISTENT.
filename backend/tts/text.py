"""Text preparation helpers for speech synthesis."""

from __future__ import annotations

import re


def sanitize_for_tts(text: str) -> str:
    """Remove common display formatting while preserving natural speech text."""

    cleaned = text.strip()

    cleaned = re.sub(r"```(?:\w+)?\s*([\s\S]*?)```", r"\1", cleaned)
    cleaned = re.sub(r"`([^`]*)`", r"\1", cleaned)
    cleaned = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", cleaned)
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    cleaned = re.sub(r"^\s{0,3}#{1,6}\s*", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^\s*[-*+]\s+", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^\s*\d+\.\s+", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"(\*\*|__)(.*?)\1", r"\2", cleaned)
    cleaned = re.sub(r"(\*|_)(.*?)\1", r"\2", cleaned)
    cleaned = cleaned.replace("`", "")
    cleaned = cleaned.replace("*", "")
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(r"([!?.,]){3,}", r"\1\1", cleaned)
    cleaned = re.sub(r"\s+([!?.,;:])", r"\1", cleaned)

    return cleaned.strip()
