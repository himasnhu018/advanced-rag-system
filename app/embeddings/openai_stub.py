# This is a stub simulating an OpenAI embedding provider for offline runs.
# Replace with real OpenAI calls in production.
from typing import List
import numpy as np
from .base import EmbeddingProvider

class OpenAIStub:
    def __init__(self):
        self.model_id = "openai-text-emb-stub"

    def embed(self, texts: List[str]) -> List[List[float]]:
        # deterministic pseudo-embeddings using hash -> vector (cheap)
        vecs = []
        for t in texts:
            h = abs(hash(t)) % (10**8)
            rnd = np.random.RandomState(h)
            v = rnd.normal(size=(384,))
            v = v / np.linalg.norm(v)
            vecs.append(v.tolist())
        return vecs