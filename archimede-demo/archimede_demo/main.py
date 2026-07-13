"""Small enhancements to the main entrypoint: support --quick download of weights and a --tiny mode."""
import argparse
import os
from archimede_demo.envs.grid2op_env import Grid2OpEnv
from archimede_demo.models.baseline import BaselineModel
from archimede_demo.eval import evaluate_model, save_metrics
from archimede_demo.report import generate_report
from archimede_demo.utils import ensure_weights

WEIGHTS_URL = os.environ.get("ARCHIMEDE_DEMO_WEIGHTS_URL", "")
WEIGHTS_PATH = "archimede-demo/weights/pretrained_baseline.pt"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="Quick run: use pretrained weights if present")
    parser.add_argument("--train", action="store_true", help="Train models before evaluation")
    parser.add_argument("--tiny", action="store_true", help="Use tiny fallback environment for local testing")
    args = parser.parse_args()

    # Create results dir if missing
    os.makedirs("results", exist_ok=True)

    # If quick and weights URL provided, ensure weights are downloaded
    if args.quick and WEIGHTS_URL:
        try:
            ensure_weights(WEIGHTS_URL, WEIGHTS_PATH)
        except Exception as e:
            print(f"Warning: failed to download weights: {e}")

    env = Grid2OpEnv(tiny=args.tiny)
    model = BaselineModel()

    # Evaluate
    metrics = evaluate_model(model, env, n_steps=100)
    save_metrics(metrics, "results/metrics.json")
    generate_report("results/report.pdf", metrics)

if __name__ == "__main__":
    main()
