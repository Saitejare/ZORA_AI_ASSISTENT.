"""ZORA backend entry point."""

from __future__ import annotations

import logging

import uvicorn

from backend.application import zora_application


logger = logging.getLogger(__name__)


app = zora_application.start()


if __name__ == "__main__":

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info",
    )