from typing import List, Protocol

class EmbeddingProvider(Protocol):
    model_id: str
    def embed(self, texts: List[str]) -> List[List[float]]: ...
