from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv


# =========================================================
# APPLICATION DIRECTORY
# =========================================================

if getattr(sys, "frozen", False):

    # Running as PyInstaller EXE
    APPLICATION_DIRECTORY = (
        Path(sys.executable).resolve().parent
    )

else:

    # Running normally from source
    APPLICATION_DIRECTORY = (
        Path(__file__).resolve().parents[2]
    )


# =========================================================
# ENVIRONMENT FILE
# =========================================================

if getattr(sys, "frozen", False):

    # -----------------------------------------------------
    # Development PyInstaller EXE
    #
    # Example:
    # dist/
    #   .env
    #   ZORA-backend.exe
    # -----------------------------------------------------

    ENV_FILE = (
        APPLICATION_DIRECTORY
        / ".env"
    )

    # -----------------------------------------------------
    # Installed Electron application
    #
    # Example:
    # resources/
    #   .env
    #   backend/
    #       ZORA-backend.exe
    # -----------------------------------------------------

    if not ENV_FILE.exists():

        ENV_FILE = (
            APPLICATION_DIRECTORY.parent
            / ".env"
        )

else:

    # Running normally from source
    ENV_FILE = (
        APPLICATION_DIRECTORY
        / ".env"
    )


# =========================================================
# LOAD ENVIRONMENT
# =========================================================

load_dotenv(
    ENV_FILE
)


# =========================================================
# GROQ CONFIGURATION
# =========================================================

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b",
)


# =========================================================
# VALIDATION
# =========================================================

if not GROQ_API_KEY:

    raise ValueError(
        "GROQ_API_KEY not found.\n"
        f"Expected .env file at:\n{ENV_FILE}"
    )