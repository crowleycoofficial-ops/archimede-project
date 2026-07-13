"""GNN model skeleton (PyTorch Geometric could be used in full impl).
This file provides a placeholder GNN model using networkx for topology handling.
"""
import torch
import torch.nn as nn
from .base import BaseModel

class GNNModel(BaseModel):
    def __init__(self, **kwargs):
        # Placeholder: in a full impl use torch_geometric or DGL
        pass

    def act(self, obs):
        # TODO: convert graph observation to tensor and run GNN
        raise NotImplementedError

    def train(self, env, n_episodes: int = 1):
        raise NotImplementedError

    def save(self, path):
        raise NotImplementedError

    @classmethod
    def load(cls, path):
        raise NotImplementedError
