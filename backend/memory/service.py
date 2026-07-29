from .classifier import MemoryClassifier
from .extractor import MemoryExtractor
from .memory_manager import MemoryManager


class MemoryService:

    def __init__(self):

        self.manager = MemoryManager()
        self.classifier = MemoryClassifier()
        self.extractor = MemoryExtractor()

    def remember(self, text: str):

        if not self.classifier.should_remember(text):
            return

        fact = self.extractor.extract(text)

        self.manager.remember(fact)

    def recall(self, query: str):

        return self.manager.recall(query)