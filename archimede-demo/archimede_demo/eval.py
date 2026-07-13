"""Evaluation utilities (skeleton)."""
import time
import json

def evaluate_model(model, env, n_steps=1000):
    metrics = {
        "cost": 0.0,
        "energy_not_served": 0.0,
        "violations": 0,
        "steps": 0,
        "time_per_step": 0.0
    }
    start = time.time()
    obs = env.reset()
    for t in range(n_steps):
        action = model.act(obs)
        obs, reward, done, info = env.step(action)
        # TODO: accumulate real metrics from info
        metrics["steps"] += 1
        if done:
            break
    total_time = time.time() - start
    metrics["time_per_step"] = total_time / max(1, metrics["steps"])
    return metrics

def save_metrics(metrics, path):
    with open(path, "w") as f:
        json.dump(metrics, f, indent=2)
