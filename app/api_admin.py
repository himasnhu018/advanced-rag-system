from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
from .core.index_manager import IndexManager, IndexRef
from .embeddings.sbert_provider import SBERTProvider
from .embeddings.openai_stub import OpenAIStub
from .vectordb.faiss_adapter import FAISSAdapter
from .core.migrator import Migrator

router = APIRouter()

# globals from main
INDEX_MGR = None
ROUTER = None
EMBEDDERS = None
MIGRATOR_THREAD = None

class StartMigrationReq(BaseModel):
    new_model: str  # "sbert" or "openai_stub"

@router.post("/admin/migration/start")
def start_migration(req: StartMigrationReq, background_tasks: BackgroundTasks):
    global MIGRATOR_THREAD
    # build candidate index object
    if req.new_model == "sbert":
        emb = SBERTProvider()
    else:
        emb = OpenAIStub()
    EMBEDDERS[emb.model_id] = emb

    # candidate FAISS file path
    name = f"candidate_{emb.model_id.replace(':','_')}"
    idx_path = f"indexes/{name}.index"
    candidate_db = FAISSAdapter(dims=384, index_path=idx_path)
    candidate_ref = IndexRef(name=name, provider_id=emb.model_id, db=candidate_db)
    INDEX_MGR.set_candidate(candidate_ref)

    # prepare corpus
    import json, os
    with open("app/data/sample_corpus.json","r", encoding="utf8") as f:
        corpus = json.load(f)

    migrator = Migrator(corpus, emb, candidate_db, batch_size=64)
    # run background
    MIGRATOR_THREAD = migrator.run_background()
    return {"status":"migration_started","candidate":name}

@router.post("/admin/migration/shift")
def shift_traffic(percent: int):
    ROUTER.set_split(percent)
    return {"status":"ok","candidate_percent":percent}

@router.post("/admin/migration/promote")
def promote():
    # Basic gating: require candidate to exist and have docs
    if not INDEX_MGR.candidate:
        return {"error":"no candidate"}
    ccount = INDEX_MGR.candidate.db.count()
    if ccount < 1:
        return {"error":"candidate empty", "count": ccount}
    INDEX_MGR.promote()
    # set router to 0 candidate (candidate now None)
    ROUTER.set_split(0)
    return {"status":"promoted","active":INDEX_MGR.active.name}

@router.post("/admin/migration/rollback")
def rollback():
    INDEX_MGR.rollback()
    ROUTER.set_split(0)
    return {"status":"rolled_back"}
