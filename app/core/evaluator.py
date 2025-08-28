# Simple online evaluator using shadow queries and a small offline goldset.
import time
from typing import List, Dict

class Evaluator:
    def __init__(self, goldset: List[Dict]=None):
        self.goldset = goldset or []

    def score_pair(self, gold_answer: str, candidate_answer: str) -> float:
        # naive metric: token overlap ratio (placeholder)
        g = set(gold_answer.lower().split())
        c = set(candidate_answer.lower().split())
        if not g: return 0.0
        return len(g & c) / len(g)

    def evaluate_offline(self, index_active, index_candidate, embedder_active, embedder_candidate):
        # compute score averages on goldset (if present)
        scores = {"active":0.0, "candidate":0.0}
        if not self.goldset: 
            return scores
        for q in self.goldset:
            qv_a = embedder_active.embed([q["q"]])[0]
            a_hits = index_active.db.query(qv_a, k=1)
            a_ans = a_hits[0][2].get("title","") if a_hits else ""
            s_a = self.score_pair(q["a"], a_ans)

            qv_c = embedder_candidate.embed([q["q"]])[0]
            c_hits = index_candidate.db.query(qv_c, k=1)
            c_ans = c_hits[0][2].get("title","") if c_hits else ""
            s_c = self.score_pair(q["a"], c_ans)

            scores["active"] += s_a
            scores["candidate"] += s_c
        n = len(self.goldset)
        scores["active"] /= n
        scores["candidate"] /= n
        return scores
