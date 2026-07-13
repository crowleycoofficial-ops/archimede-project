"""Train a small ResNet policy as demo weights.

This script trains a tiny ResNet on random data or on the tiny fallback env to
produce a .pt file suitable for the demo. It is intentionally lightweight so
that users can generate demo weights quickly (CPU-friendly).

Usage:
  python3 archimede-demo/train_resnet.py --out archimede-demo/weights/pretrained_resnet_demo.pt --epochs 5

If you have GPU, pass --device cuda to speed up training.
"""
import argparse
import os
import numpy as np

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
except Exception:
    torch = None

from archimede_demo.envs.grid2op_env import Grid2OpEnv


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
    def __init__(self, input_dim, hidden_dim=64, n_blocks=3, output_dim=16):
        super().__init__()
        self.input = nn.Linear(input_dim, hidden_dim)
        self.blocks = nn.Sequential(*[ResidualBlock(hidden_dim) for _ in range(n_blocks)])
        self.output = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = torch.relu(self.input(x))
        x = self.blocks(x)
        return self.output(x)


def collect_random_batch(obs_dim, batch_size=64):
    X = np.random.randn(batch_size, obs_dim).astype(np.float32)
    y = np.zeros((batch_size, 16), dtype=np.float32)
    return X, y


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="archimede-demo/weights/pretrained_resnet_demo.pt")
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--tiny", action="store_true", help="Use tiny fallback environment for obs dim")
    args = parser.parse_args()

    if torch is None:
        print("PyTorch not available. Install torch to run training: pip install torch")
        return

    # instantiate environment to get obs dim; use tiny fallback for quick runs
    env = Grid2OpEnv(tiny=args.tiny)
    obs_dim = env.get_obs_dim() or 32
    print(f"Using obs_dim={obs_dim}")

    device = torch.device(args.device if torch.cuda.is_available() or args.device == 'cpu' else 'cpu')

    model = ResNetPolicy(input_dim=obs_dim, hidden_dim=64, n_blocks=3, output_dim=16).to(device)
    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    loss_fn = nn.MSELoss()

    for epoch in range(args.epochs):
        # simple random data training loop
        X, y = collect_random_batch(obs_dim, batch_size=args.batch_size)
        X_t = torch.from_numpy(X).to(device)
        y_t = torch.from_numpy(y).to(device)
        model.train()
        optimizer.zero_grad()
        out = model(X_t)
        loss = loss_fn(out, y_t)
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch+1}/{args.epochs} loss={loss.item():.6f}")

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    torch.save(model.state_dict(), args.out)
    print(f"Saved demo weights to {args.out}")


if __name__ == "__main__":
    main()
