"""Baseline heuristic model: dispatch proportional to cost.
This is a minimal deterministic policy used as a sanity-check baseline."""
from .base import BaseModel

class BaselineModel(BaseModel):
    def __init__(self, **kwargs):
        pass

    def act(self, obs):
        # TODO: implement simple proportional dispatch
        raise NotImplementedError

    def train(self, env, n_episodes: int = 1):
        # Baseline does not train
        return self

    def save(self, path):
        # No weights to save; create a marker file
        with open(path, "w") as f:
            f.write("baseline\n")

    @classmethod
    def load(cls, path):
        return cls()
