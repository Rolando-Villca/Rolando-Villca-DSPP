"""Legacy entry point, now runs the revised Q1 2026 backtest.

The former exploratory prototype was superseded: see src.experiment.
"""
import json
from src.experiment import run


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
