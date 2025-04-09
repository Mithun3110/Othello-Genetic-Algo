import random

class Genome:
    def __init__(self, initialize=True):
        self.genes = {
            "corners": random.uniform(-1, 1) if initialize else 0.0,
            "edges": random.uniform(-1, 1) if initialize else 0.0,
            "centres": random.uniform(-1, 1) if initialize else 0.0,
            "diagonals": random.uniform(-1, 1) if initialize else 0.0,
            "stability": random.uniform(-1, 1) if initialize else 0.0,
            "coin_diff": random.uniform(-1, 1) if initialize else 0.0
        }
        self.fitness = 0

    @classmethod
    def empty(cls):
        return cls(initialize=False)
