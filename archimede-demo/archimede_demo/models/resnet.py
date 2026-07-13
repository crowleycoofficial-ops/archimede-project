"""ResNet model skeleton using PyTorch.
Input: flattened observation vector. Output: redispatching action vector.
"""
import torch
import torch.nn as nn
from .base import BaseModel

class ResidualBlock(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(dim, dim),
            nn.ReLU(),
            nn.Linear(dim, dim)
        )
        self.act = nn.ReLU()

    def forward(self, x):
        return self.act(x + self.fc(x))

class ResNetPolicy(nn.Module):
    def __init__(self, input_dim, hidden_dim=256, n_blocks=4, output_dim=None):
        super().__init__()
        self.input = nn.Linear(input_dim, hidden_dim)
        self.blocks = nn.Sequential(*[ResidualBlock(hidden_dim) for _ in range(n_blocks)])
        self.output = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = torch.relu(self.input(x))
        x = self.blocks(x)
        return self.output(x)

class ResNetModel(BaseModel):
    def __init__(self, model: ResNetPolicy):
        self.model = model

    def act(self, obs):
        # obs: numpy array
        import numpy as np
        x = torch.from_numpy(np.asarray(obs)).float().unsqueeze(0)
        with torch.no_grad():
            out = self.model(x).squeeze(0).numpy()
        # TODO: convert output vector to grid2op.Action
        return out

    def train(self, env, n_episodes: int = 1):
        raise NotImplementedError

    def save(self, path):
        torch.save(self.model.state_dict(), path)

    @classmethod
    def load(cls, path, input_dim=None, hidden_dim=256, n_blocks=4, output_dim=None):
        model = ResNetPolicy(input_dim, hidden_dim, n_blocks, output_dim)
        model.load_state_dict(torch.load(path, map_location="cpu"))
        return cls(model)
