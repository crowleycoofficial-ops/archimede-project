#!/usr/bin/env bash
set -euo pipefail

DEMO_DIR=$(cd "$(dirname "$0")" && pwd)
PYTHON=${PYTHON:-python3}

usage() {
  echo "Usage: $0 [--quick|--train]"
  echo "  --quick   : quick run (download dataset, load pretrained weights if available, evaluate and generate report)"
  echo "  --train   : train models locally (may be long), then evaluate and generate report"
  exit 1
}

MODE="quick"
if [ "$#" -gt 0 ]; then
  case "$1" in
    --train) MODE="train" ;;
    --quick) MODE="quick" ;;
    *) usage ;;
  esac
fi

$PYTHON -m pip install -r "$DEMO_DIR/requirements.txt"

if [ "$MODE" = "quick" ]; then
  echo "Running quick demo: download dataset, load pretrained weights if present, evaluate and generate report"
  $PYTHON -m archimede_demo.main --quick
else
  echo "Running full demo: will train models (this can take a long time)"
  $PYTHON -m archimede_demo.main --train
fi
