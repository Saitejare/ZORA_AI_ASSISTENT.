from pathlib import Path

from PyInstaller.utils.hooks import collect_all


PROJECT_ROOT = Path.cwd()


datas = []
binaries = []
hiddenimports = []


# =========================================================
# ENVIRONMENT FILE
# =========================================================

env_file = PROJECT_ROOT / ".env"

if env_file.exists():
    datas.append(
        (
            str(env_file),
            ".",
        )
    )


# =========================================================
# BACKEND PACKAGE
# =========================================================

datas.append(
    (
        str(PROJECT_ROOT / "backend"),
        "backend",
    )
)


# =========================================================
# BACKEND DATA
# =========================================================

backend_data = PROJECT_ROOT / "backend" / "data"

if backend_data.exists():
    datas.append(
        (
            str(backend_data),
            "backend/data",
        )
    )


# =========================================================
# COLLECT IMPORTANT PACKAGES
# =========================================================

for package_name in [
    "faster_whisper",
    "ctranslate2",
    "speech_recognition",

    # IMPORTANT:
    # SpeechRecognition.Microphone() requires PyAudio.
    "pyaudio",

    "edge_tts",
    "torch",
    "scipy",
    "numpy",
    "pydantic",
    "fastapi",
    "uvicorn",
    "httpx",
    "groq",
]:

    try:

        package_datas, package_binaries, package_hiddenimports = (
            collect_all(package_name)
        )

        datas += package_datas
        binaries += package_binaries
        hiddenimports += package_hiddenimports

    except Exception as exc:

        print(
            f"Warning: could not collect {package_name}: {exc}"
        )


# =========================================================
# HIDDEN IMPORTS
# =========================================================

hiddenimports += [
    # -----------------------------------------------------
    # BACKEND
    # -----------------------------------------------------

    "backend",
    "backend.main",
    "backend.application",

    # -----------------------------------------------------
    # API
    # -----------------------------------------------------

    "backend.api",
    "backend.api.routes",
    "backend.api.models",

    # -----------------------------------------------------
    # AGENT
    # -----------------------------------------------------

    "backend.agent",
    "backend.agent.orchestrator",

    # -----------------------------------------------------
    # PLANNER
    # -----------------------------------------------------

    "backend.planner",
    "backend.planner.planner",

    # -----------------------------------------------------
    # LLM
    # -----------------------------------------------------

    "backend.llm",
    "backend.llm.client",
    "backend.llm.config",
    "backend.llm.service",

    # -----------------------------------------------------
    # SPEECH
    # -----------------------------------------------------

    "backend.speech",
    "backend.speech.record",
    "backend.speech.transcribe",

    # -----------------------------------------------------
    # MICROPHONE
    # -----------------------------------------------------

    "speech_recognition",
    "pyaudio",

    # -----------------------------------------------------
    # TTS
    # -----------------------------------------------------

    "backend.tts",
    "backend.tts.synthesizer",

    # -----------------------------------------------------
    # MULTIPART
    # -----------------------------------------------------

    "multipart",
    "python_multipart",

    # -----------------------------------------------------
    # UVICORN
    # -----------------------------------------------------

    "uvicorn",
    "uvicorn.logging",
    "uvicorn.loops",
    "uvicorn.loops.auto",
    "uvicorn.protocols",
    "uvicorn.protocols.http",
    "uvicorn.protocols.http.auto",
    "uvicorn.protocols.websockets",
    "uvicorn.protocols.websockets.auto",
    "uvicorn.lifespan",
    "uvicorn.lifespan.on",
]


# =========================================================
# ANALYSIS
# =========================================================

a = Analysis(
    [
        str(
            PROJECT_ROOT
            / "backend"
            / "main.py"
        ),
    ],

    pathex=[
        str(PROJECT_ROOT),
    ],

    binaries=binaries,

    datas=datas,

    hiddenimports=hiddenimports,

    hookspath=[],

    hooksconfig={},

    runtime_hooks=[],

    excludes=[],

    noarchive=False,
)


# =========================================================
# PYZ
# =========================================================

pyz = PYZ(
    a.pure,
)


# =========================================================
# EXE
# =========================================================

exe = EXE(
    pyz,

    a.scripts,

    a.binaries,

    a.datas,

    [],

    name="ZORA-backend",

    debug=False,

    bootloader_ignore_signals=False,

    strip=False,

    upx=False,

    console=True,

    disable_windowed_traceback=False,

    argv_emulation=False,

    target_arch=None,

    codesign_identity=None,

    entitlements_file=None,
)