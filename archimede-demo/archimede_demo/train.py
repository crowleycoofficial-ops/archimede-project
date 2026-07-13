"""Training utilities (skeleton)."""

def train_model(model, env, n_episodes=10):
    """Train model on env for n_episodes. This is a simplified placeholder."""
    for ep in range(n_episodes):
        obs = env.reset()
        done = False
        while not done:
            action = model.act(obs)
            obs, reward, done, info = env.step(action)
    return model
