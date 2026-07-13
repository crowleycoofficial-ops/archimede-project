from abc import ABC, abstractmethod

class BaseModel(ABC):
    """Abstract base class for models used in the demo."""

    @abstractmethod
    def act(self, obs):
        """Return an action given an observation."""
        pass

    @abstractmethod
    def train(self, env, n_episodes: int = 1):
        pass

    @abstractmethod
    def save(self, path):
        pass

    @classmethod
    @abstractmethod
    def load(cls, path):
        pass
