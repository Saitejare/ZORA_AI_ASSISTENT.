from .embeddings import EmbeddingModel
from .vector_store import VectorStore


class MemoryManager:

    def __init__(self):

        self.embedder = EmbeddingModel()
        self.store = VectorStore()

    def remember(self, text: str):

        embedding = self.embedder.encode(text)

        self.store.add(
            embedding,
            text,
        )

        self.store.save()

    def recall(self, query: str):

        embedding = self.embedder.encode(query)

        return self.store.search(embedding)