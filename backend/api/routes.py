"""FastAPI route definitions for the ZORA assistant."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse

from backend.api.models import (
    ChatRequest,
    CommandRequest,
    HealthResponse,
    VoiceRequest,
    ZoraResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter()


# =====================================================
# APPLICATION
# =====================================================

def _app(request: Request) -> Any:

    application = getattr(
        request.app.state,
        "zora",
        None,
    )

    if application is None:

        raise HTTPException(
            status_code=503,
            detail="ZORA application is not initialized.",
        )

    return application


# =====================================================
# AUDIO
# =====================================================

AUDIO_DIRECTORY = (
    Path(__file__).resolve().parents[1]
    / "data"
)

MP3_AUDIO_FILE = (
    AUDIO_DIRECTORY
    / "response.mp3"
)

WAV_AUDIO_FILE = (
    AUDIO_DIRECTORY
    / "response.wav"
)


# =====================================================
# AUDIO LATEST
# =====================================================

@router.get("/audio/latest")
def latest_audio():

    candidates = []

    if MP3_AUDIO_FILE.exists():
        candidates.append(
            MP3_AUDIO_FILE
        )

    if WAV_AUDIO_FILE.exists():
        candidates.append(
            WAV_AUDIO_FILE
        )

    if not candidates:

        raise HTTPException(
            status_code=404,
            detail="No audio available.",
        )

    audio_file = max(
        candidates,
        key=lambda path: path.stat().st_mtime,
    )

    if audio_file.suffix.lower() == ".mp3":

        media_type = "audio/mpeg"

    elif audio_file.suffix.lower() == ".wav":

        media_type = "audio/wav"

    else:

        raise HTTPException(
            status_code=500,
            detail="Unsupported audio format.",
        )

    logger.info(
        "Serving latest TTS audio: %s",
        audio_file,
    )

    return FileResponse(
        path=audio_file,
        media_type=media_type,
        filename=audio_file.name,
        headers={
            "Cache-Control": (
                "no-store, no-cache, "
                "must-revalidate, max-age=0"
            ),
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )


# =====================================================
# ROOT
# =====================================================

@router.get("/")
def root():

    return {
        "name": "ZORA AI Assistant",
        "status": "Running",
        "version": "1.0.0",
    }


# =====================================================
# HEALTH
# =====================================================

@router.get(
    "/health",
    response_model=HealthResponse,
)
def health(
    request: Request,
):

    return _app(
        request
    ).health()


# =====================================================
# READY
# =====================================================

@router.get(
    "/ready",
    response_model=ZoraResponse,
)
def ready(
    request: Request,
):

    application = _app(
        request
    )

    if not application.initialized:

        return ZoraResponse(
            success=False,
            message="ZORA is initializing.",
            data={
                "ready": False,
            },
        )

    return ZoraResponse(
        success=True,
        message="ZORA is ready.",
        data={
            "ready": True,
        },
    )


# =====================================================
# MICROPHONE READY
# =====================================================

@router.post(
    "/microphone/initialize",
    response_model=ZoraResponse,
)
def initialize_microphone(
    request: Request,
):

    try:

        result = (
            _app(
                request
            )
            .initialize_microphone()
        )

        return ZoraResponse(
            success=True,
            message="Microphone ready.",
            data=result,
        )

    except Exception as exc:

        logger.exception(
            "Microphone initialization failed."
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "ZORA microphone could not "
                "be initialized."
            ),
        ) from exc


# =====================================================
# STATUS
# =====================================================

@router.get(
    "/status",
    response_model=ZoraResponse,
)
def status(
    request: Request,
):

    return ZoraResponse(
        success=True,
        message="Success",
        data=_app(
            request
        ).status(),
    )


# =====================================================
# CONVERSATION
# =====================================================

@router.get(
    "/conversation",
    response_model=ZoraResponse,
)
def conversation(
    request: Request,
):

    return ZoraResponse(
        success=True,
        message="Success",
        data=_app(
            request
        ).conversation_history(),
    )


# =====================================================
# MEMORY
# =====================================================

@router.get(
    "/memory",
    response_model=ZoraResponse,
)
def memory(
    request: Request,
):

    return ZoraResponse(
        success=True,
        message="Success",
        data=_app(
            request
        ).memory_snapshot(),
    )


# =====================================================
# CHAT
# =====================================================

@router.post(
    "/chat",
    response_model=ZoraResponse,
)
def chat(
    payload: ChatRequest,
    request: Request,
):

    try:

        response = (
            _app(
                request
            )
            .process_text(
                payload.message
            )
        )

        return ZoraResponse(
            success=True,
            message="Success",
            data={
                "response": response,
            },
        )

    except Exception as exc:

        logger.exception(
            "Chat request failed"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "ZORA could not process "
                "that message. Please try again."
            ),
        ) from exc


# =====================================================
# VOICE
# =====================================================

@router.post(
    "/voice",
    response_model=ZoraResponse,
)
def voice(
    request: Request,
    payload: VoiceRequest | None = None,
):

    try:

        logger.info(
            "Voice request received."
        )

        audio_path = None

        if payload is not None:

            audio_path = (
                payload.audio_path
            )

        result = (
            _app(
                request
            )
            .process_voice(
                audio_path
            )
        )

        logger.info(
            "Voice request completed successfully."
        )

        return ZoraResponse(
            success=True,
            message="Success",
            data=result,
        )

    except Exception as exc:

        logger.exception(
            "Voice request failed"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "ZORA could not process "
                "voice input. Please try again."
            ),
        ) from exc


# =====================================================
# DIRECT COMMAND
# =====================================================

@router.post(
    "/command",
    response_model=ZoraResponse,
)
def command(
    payload: CommandRequest,
    request: Request,
):

    try:

        result = (
            _app(
                request
            )
            .process_command(
                capability=payload.capability,
                action=payload.action,
                parameters=payload.parameters,
            )
        )

        return ZoraResponse(
            success=True,
            message="Success",
            data=result,
        )

    except Exception as exc:

        logger.exception(
            "Command request failed"
        )

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc