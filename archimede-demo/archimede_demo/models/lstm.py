"""LSTM model skeleton for sequence-based policies."""
import torch
import torch.nn as nn
from .base import BaseModel

class LSTMModel(BaseModel):
    def __init__(self, input_dim, hidden_dim=128, n_layers=2, output_dim=None):
        self.lstm = nn.LSTM(input_dim, hidden_dim, n_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def act(self, obs):
        # obs: sequence of vectors
        raise NotImplementedError

    def train(self, env, n_episodes: int = 1):
        raise NotImplementedError

    def save(self, path):
        raise NotImplementedError

    @classmethod
    def load(cls, path):
        raise NotImplementedError
