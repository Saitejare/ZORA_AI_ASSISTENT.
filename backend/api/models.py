"""Typed API request and response models."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request body for text chat."""

    message: str = Field(min_length=1)


class VoiceRequest(BaseModel):
    """Request body for voice processing.

    If ``audio_path`` is omitted, the backend records from the configured
    microphone before transcribing.
    """

    audio_path: str | None = None


class CommandRequest(BaseModel):
    """Request body for direct capability execution."""

    capability: str = Field(min_length=1)
    action: str = Field(min_length=1)
    parameters: dict[str, Any] = Field(default_factory=dict)


class ZoraResponse(BaseModel):
    """Standard API response."""

    success: bool
    message: str
    data: Any = None


class HealthResponse(BaseModel):
    """Health response returned by ``GET /health``."""

    status: str
    initialized: bool
    version: str
