from sentence_transformers import SentenceTransformer
from typing import List
from .base import EmbeddingProvider

class SBERTProvider:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model_id = f"sbert:{model_name}"
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts, show_progress_bar=False, convert_to_numpy=True).tolist()
