from dataclasses import dataclass
from typing import Optional
import sqlite3
import os

@dataclass
class IndexRef:
    name: str
    provider_id: str
    db: object  # FAISSAdapter

class IndexManager:
    def __init__(self):
        self.active: Optional[IndexRef] = None
        self.candidate: Optional[IndexRef] = None

    def set_active(self, idxref: IndexRef):
        self.active = idxref

    def set_candidate(self, idxref: IndexRef):
        self.candidate = idxref

    def promote(self):
        if not self.candidate:
            raise RuntimeError("No candidate to promote")
        # swap: candidate -> active; archive old active if needed
        self.active = self.candidate
        self.candidate = None

    def rollback(self):
        # drop candidate
        self.candidate = None

    def get_by_name(self, which: str):
        if which == "active":
            return self.active
        if which == "candidate":
            return self.candidate
        raise KeyError(which)
