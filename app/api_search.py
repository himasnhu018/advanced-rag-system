from fastapi import APIRouter, Query, Depends, WebSocket
from fastapi.responses import JSONResponse
from .core.router import ABRouter
from .core.index_manager import IndexManager
from .embeddings.base import EmbeddingProvider

router = APIRouter()

# to be injected by main
ROUTER: ABRouter = None
INDEX_MGR: IndexManager = None
EMBEDDERS: dict = {}

def _search(index_ref, embedder: EmbeddingProvider, q: str, k: int):
    qv = embedder.embed([q])[0]
    hits = index_ref.db.query(qv, k=k)
    return [{"id": hid, "score": score, "meta": meta} for hid, score, meta in hits]

@router.get("/api/search")
def search(q: str = Query(...), k: int = 5):
    route = ROUTER.route()
    target_idx = INDEX_MGR.candidate if route == "candidate" and INDEX_MGR.candidate else INDEX_MGR.active
    if not target_idx:
        return JSONResponse({"error":"no index ready"}, status_code=503)
    embedder = EMBEDDERS[target_idx.provider_id]
    results = _search(target_idx, embedder, q, k)
    return {"routed_to": route, "results": results}
