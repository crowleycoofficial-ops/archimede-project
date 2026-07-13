"""Grid2Op environment adapter (skeleton).

Implements Environment interface defined in envs/base.py.
"""
from .base import Environment

# Note: This file is a skeleton. Implementation will import grid2op and adapt observations/actions.

class Grid2OpEnv(Environment):
    def __init__(self, env_name: str = "l2rpn_neurips_2020"):
        self.env_name = env_name
        self.env = None

    def reset(self):
        # TODO: instantiate grid2op.Environment and call reset
        raise NotImplementedError

    def step(self, action):
        raise NotImplementedError

    def get_topology(self):
        raise NotImplementedError

    def get_observation_space(self):
        raise NotImplementedError

    def get_action_space(self):
        raise NotImplementedError
