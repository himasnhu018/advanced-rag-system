import threading
from typing import Iterable, Dict
import time

class Migrator:
    def __init__(self, corpus: Iterable[Dict], embedder, candidate_db, batch_size=64):
        self.corpus = list(corpus)
        self.embedder = embedder
        self.db = candidate_db
        self.batch_size = batch_size
        self._stop = False

    def run_background(self, on_progress=None):
        t = threading.Thread(target=self.run, daemon=True)
        t.start()
        return t

    def run(self):
        batch_ids, batch_texts, batch_metas = [], [], []
        for doc in self.corpus:
            if self._stop:
                break
            batch_ids.append(doc["id"])
            batch_texts.append(doc["text"])
            batch_metas.append({"title": doc.get("title","")})
            if len(batch_ids) >= self.batch_size:
                vecs = self.embedder.embed(batch_texts)
                self.db.upsert(batch_ids, vecs, batch_metas)
                batch_ids, batch_texts, batch_metas = [], [], []
        if batch_ids:
            vecs = self.embedder.embed(batch_texts)
            self.db.upsert(batch_ids, vecs, batch_metas)

    def stop(self):
        self._stop = True
