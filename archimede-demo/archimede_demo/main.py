"""Command-line entrypoint for the demo."""
import argparse
from archimede_demo.envs.grid2op_env import Grid2OpEnv
from archimede_demo.models.baseline import BaselineModel
from archimede_demo.eval import evaluate_model, save_metrics
from archimede_demo.report import generate_report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="Quick run: use pretrained weights if present")
    parser.add_argument("--train", action="store_true", help="Train models before evaluation")
    args = parser.parse_args()

    env = Grid2OpEnv()
    model = BaselineModel()

    metrics = evaluate_model(model, env, n_steps=100)
    save_metrics(metrics, "results/metrics.json")
    generate_report("results/report.pdf", metrics)

if __name__ == "__main__":
    main()
