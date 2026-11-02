"""Generate fictional store–item–day demand. No source data are read."""
from __future__ import annotations

import numpy as np
import pandas as pd


def generate_synthetic_demand(
    n_stores: int = 8,
    n_items: int = 18,
    n_days: int = 252,
    seed: int = 2026,
) -> pd.DataFrame:
    """Return synthetic demand with no real or derived store/product IDs."""
    if min(n_stores, n_items) < 1 or n_days < 35:
        raise ValueError("Use positive store/item counts and at least 35 days.")
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2024-01-01", periods=n_days, freq="D")
    weekday = dates.dayofweek.to_numpy()
    weekend = np.where(weekday >= 5, 1.18, 1.0)
    t = np.arange(n_days)
    seasonal = 1.0 + 0.10 * np.sin(2 * np.pi * t / 56)
    results = []

    for store in range(1, n_stores + 1):
        store_effect = rng.uniform(0.75, 1.30)
        for item in range(1, n_items + 1):
            item_effect = rng.uniform(5, 32)
            weekly = 1.0 + rng.uniform(0.02, 0.20) * np.cos(
                2 * np.pi * (weekday + item % 7) / 7
            )
            mean = np.maximum(0.5, store_effect * item_effect * weekend * weekly * seasonal)
            units = rng.poisson(mean)
            results.append(
                pd.DataFrame({
                    "date": dates,
                    "store_id": f"DEMO-STORE-{store:03d}",
                    "item_id": f"DEMO-ITEM-{item:03d}",
                    "units": units.astype(int),
                })
            )

    return pd.concat(results, ignore_index=True)
