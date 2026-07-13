"""PyPSA environment adapter (skeleton).

Implements Environment interface and adapts PyPSA to the same API.
"""
from .base import Environment

class PyPSAEnv(Environment):
    def __init__(self, case_name: str = None):
        self.case_name = case_name
        self.net = None

    def reset(self):
        raise NotImplementedError

    def step(self, action):
        raise NotImplementedError

    def get_topology(self):
        raise NotImplementedError

    def get_observation_space(self):
        raise NotImplementedError

    def get_action_space(self):
        raise NotImplementedError
