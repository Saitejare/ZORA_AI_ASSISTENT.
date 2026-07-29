import pickle
from pathlib import Path

import faiss
import numpy as np

from .config import INDEX_PATH, METADATA_PATH, TOP_K


class VectorStore:

    def __init__(self):

        self.dimension = None
        self.index = None
        self.metadata = []

        self._load()

    def _create_index(self, dimension: int):

        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)

    def add(self, embedding: np.ndarray, text: str):

        embedding = embedding.reshape(1, -1).astype("float32")

        if self.index is None:
            self._create_index(embedding.shape[1])

        self.index.add(embedding)

        self.metadata.append(text)

    def search(self, embedding: np.ndarray, top_k: int = TOP_K):

        if self.index is None or self.index.ntotal == 0:
            return []

        embedding = embedding.reshape(1, -1).astype("float32")

        scores, indices = self.index.search(embedding, top_k)

        results = []

        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            results.append(
                {
                    "text": self.metadata[idx],
                    "score": float(score),
                }
            )

        return results

    def save(self):

        if self.index is not None:
            faiss.write_index(self.index, str(INDEX_PATH))

        with open(METADATA_PATH, "wb") as f:
            pickle.dump(self.metadata, f)

    def _load(self):

        if Path(INDEX_PATH).exists():
            self.index = faiss.read_index(str(INDEX_PATH))
            self.dimension = self.index.d

        if Path(METADATA_PATH).exists():
            with open(METADATA_PATH, "rb") as f:
                self.metadata = pickle.load(f)