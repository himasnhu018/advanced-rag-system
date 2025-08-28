import random
from threading import Lock

class ABRouter:
    def __init__(self, split_candidate: int = 0):
        self.lock = Lock()
        self.split_candidate = split_candidate  # 0..100

    def route(self) -> str:
        with self.lock:
            r = random.randint(1,100)
            return "candidate" if r <= self.split_candidate else "active"

    def set_split(self, candidate_percent: int):
        with self.lock:
            self.split_candidate = max(0, min(100, int(candidate_percent)))
