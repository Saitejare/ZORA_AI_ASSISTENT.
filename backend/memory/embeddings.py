from sentence_transformers import SentenceTransformer

from .config import EMBEDDING_MODEL


class EmbeddingModel:

    def __init__(self):
        self.model = SentenceTransformer(
            EMBEDDING_MODEL
        )

    def encode(self, text: str):

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.astype("float32")