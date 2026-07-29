from pathlib import Path

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

INDEX_PATH = DATA_DIR / "memory.index"

METADATA_PATH = DATA_DIR / "metadata.pkl"

TOP_K = 5
SIMILARITY_THRESHOLD = 0.75
