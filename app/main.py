from fastapi import FastAPI
from app import api_search, api_admin
from app.core.router import ABRouter
from app.core.index_manager import IndexManager
from app.embeddings.sbert_provider import SBERTProvider
from app.vectordb.faiss_adapter import FAISSAdapter
from app.core.index_manager import IndexRef
import os, json

app = FastAPI(title="Advanced RAG with Hot-Swap")

# --- Create real instances ---
ROUTER = ABRouter(split_candidate=0)   # load balancing router
INDEX_MGR = IndexManager()
EMBEDDERS = {}

# --- Inject into api_search and api_admin ---
api_search.ROUTER = ROUTER
api_search.INDEX_MGR = INDEX_MGR
api_search.EMBEDDERS = EMBEDDERS

api_admin.ROUTER = ROUTER
api_admin.INDEX_MGR = INDEX_MGR
api_admin.EMBEDDERS = EMBEDDERS

# --- Bootstrap default index ---
def bootstrap():
    os.makedirs("indexes", exist_ok=True)

    emb = SBERTProvider()
    EMBEDDERS[emb.model_id] = emb

    db = FAISSAdapter(dims=384, index_path="indexes/active_sbert.index")

    # load some sample docs
    with open("app/data/sample_corpus.json", "r", encoding="utf-8") as f:
        corpus = json.load(f)

    ids = [d["id"] for d in corpus]
    texts = [d["text"] for d in corpus]
    metas = [{"title": d.get("title", "")} for d in corpus]
    vecs = emb.embed(texts)
    db.upsert(ids, vecs, metas)

    INDEX_MGR.set_active(IndexRef(name="active_sbert", provider_id=emb.model_id, db=db))

bootstrap()

# --- Register routes ---
app.include_router(api_search.router)
app.include_router(api_admin.router)

@app.get("/")
def root():
    return {"status": "ok"}
