"""Central runtime configuration for the ZORA backend."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent


@dataclass(frozen=True)
class ServerConfig:
    """HTTP server settings used by FastAPI and local launch scripts."""

    host: str = os.getenv("ZORA_HOST", "127.0.0.1")
    port: int = int(os.getenv("ZORA_PORT", "8000"))
    cors_origins: tuple[str, ...] = tuple(
        origin.strip()
        for origin in os.getenv(
            "ZORA_CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        ).split(",")
        if origin.strip()
    )


@dataclass(frozen=True)
class PathConfig:
    """Filesystem paths shared by application services."""

    base_dir: Path = BASE_DIR
    project_dir: Path = PROJECT_DIR
    logs_dir: Path = BASE_DIR / "logs"
    browser_profile_dir: Path = BASE_DIR / "browser_profile"


@dataclass(frozen=True)
class SpeechConfig:
    """Speech recognition and synthesis defaults."""

    enabled: bool = os.getenv("ZORA_SPEECH_ENABLED", "1") == "1"
    voice: str = os.getenv("ZORA_TTS_VOICE", "default")
    timeout_seconds: float = float(os.getenv("ZORA_SPEECH_TIMEOUT", "30"))


@dataclass(frozen=True)
class LLMConfig:
    """LLM defaults and API key locations."""

    groq_api_key: str | None = os.getenv("GROQ_API_KEY")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")


@dataclass(frozen=True)
class MemoryConfig:
    """Memory subsystem settings."""

    enabled: bool = os.getenv("ZORA_MEMORY_ENABLED", "1") == "1"


@dataclass(frozen=True)
class BrowserConfig:
    """Browser automation settings."""

    lazy_load: bool = True
    headless: bool = os.getenv("ZORA_BROWSER_HEADLESS", "0") == "1"


@dataclass(frozen=True)
class AppConfig:
    """Top-level application configuration."""

    server: ServerConfig = ServerConfig()
    paths: PathConfig = PathConfig()
    speech: SpeechConfig = SpeechConfig()
    llm: LLMConfig = LLMConfig()
    memory: MemoryConfig = MemoryConfig()
    browser: BrowserConfig = BrowserConfig()


def load_config() -> AppConfig:
    """Load configuration from environment variables."""

    return AppConfig()
