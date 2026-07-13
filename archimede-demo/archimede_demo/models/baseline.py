"""Baseline heuristic model: dispatch proportional to cost.

This baseline is intentionally simple and robust: it attempts to produce a
no-op or safe action when precise integration with the simulator is not
available. When the environment exposes helpers for building actions the
baseline will use them.
"""
from .base import BaseModel

class BaselineModel(BaseModel):
    def __init__(self, **kwargs):
        pass

    def act(self, obs, env=None):
        """Return an action given an observation.

        The baseline prefers to ask the environment for a safe no-op action if
        available. Otherwise it returns None which upstream code should handle
        (for example by skipping the action or converting to a simulator-specific
        no-op).
        """
        # If called with the Grid2OpEnv wrapper, use its noop helper
        if env is not None and hasattr(env, "noop_action"):
            try:
                a = env.noop_action()
                return a
            except Exception:
                pass
        # Fallback: return None (caller should handle this)
        return None

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
