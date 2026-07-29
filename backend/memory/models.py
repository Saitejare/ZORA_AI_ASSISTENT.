from dataclasses import dataclass
from datetime import datetime


@dataclass
class MemoryItem:
    id: int
    text: str
    created_at: datetime