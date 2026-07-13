from abc import ABC, abstractmethod

class Environment(ABC):
    """Abstract environment interface to wrap different power system simulators."""

    @abstractmethod
    def reset(self):
        """Reset the environment and return the initial observation."""
        pass

    @abstractmethod
    def step(self, action):
        """Apply action, return (obs, reward, done, info)."""
        pass

    @abstractmethod
    def get_topology(self):
        """Return network topology as a graph object."""
        pass

    @abstractmethod
    def get_observation_space(self):
        pass

    @abstractmethod
    def get_action_space(self):
        pass
