import faiss
import numpy as np
import os
from typing import List, Tuple

class FAISSAdapter:
    def __init__(self, dims=384, index_path=None):
        self.d = dims
        self.index_path = index_path or "indexes/faiss.index"
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            self.id_map = self._load_id_map()
        else:
            self.index = faiss.IndexFlatIP(self.d)  # inner-product on normalized vectors
            self.id_map = []  # parallel list of doc ids

    def upsert(self, ids: List[str], vectors: List[List[float]], metas: List[dict] = None):
        arr = np.array(vectors).astype("float32")
        # normalize for cosine (if not already)
        norms = np.linalg.norm(arr, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        arr = arr / norms
        self.index.add(arr)
        self.id_map.extend(ids)
        self._persist()

    def query(self, vector: List[float], k: int = 5) -> List[Tuple[str, float, dict]]:
        v = np.array(vector).astype("float32").reshape(1, -1)
        v = v / (np.linalg.norm(v) + 1e-12)
        D, I = self.index.search(v, k)
        res = []
        for score, idx in zip(D[0].tolist(), I[0].tolist()):
            if idx < 0 or idx >= len(self.id_map):
                continue
            res.append((self.id_map[idx], float(score), {}))
        return res

    def count(self):
        return self.index.ntotal

    def save(self):
        faiss.write_index(self.index, self.index_path)
        self._persist_id_map()

    def _persist(self):
        self.save()

    def _persist_id_map(self):
        with open(self.index_path + ".ids", "w", encoding="utf8") as f:
            f.write("\n".join(self.id_map))

    def _load_id_map(self):
        p = self.index_path + ".ids"
        if not os.path.exists(p):
            return []
        with open(p, "r", encoding="utf8") as f:
            return [l.strip() for l in f.readlines()]
