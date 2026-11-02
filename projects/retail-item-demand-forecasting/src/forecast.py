"""Seven-day-ahead synthetic-demand forecasting with a naive benchmark."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

from src.synthetic_data import generate_synthetic_demand


FEATURES = [
    "store_id", "item_id", "day_of_week", "month",
    "lag_7", "lag_14", "lag_28", "prior_week_mean",
]


def engineer_features(panel: pd.DataFrame) -> pd.DataFrame:
    """Construct features available at least seven days before each target."""
    ordered = panel.sort_values(["store_id", "item_id", "date"]).copy()
    ordered["date"] = pd.to_datetime(ordered["date"])
    group = ordered.groupby(["store_id", "item_id"], sort=False)["units"]

    for lag in (7, 14, 28):
        ordered[f"lag_{lag}"] = group.shift(lag)

    # At target t, this window contains only t-13 ... t-7.
    ordered["prior_week_mean"] = group.transform(
        lambda series: series.shift(7).rolling(window=7, min_periods=7).mean()
    )
    ordered["day_of_week"] = ordered["date"].dt.dayofweek
    ordered["month"] = ordered["date"].dt.month
    return ordered.dropna(subset=["lag_7", "lag_14", "lag_28", "prior_week_mean"]).reset_index(drop=True)


def chronological_split(
    frame: pd.DataFrame, test_days: int = 42
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Hold out the last test_days, across all series."""
    if test_days < 1:
        raise ValueError("test_days must be positive")
    first_test_date = frame["date"].max() - pd.Timedelta(days=test_days - 1)
    train = frame.loc[frame["date"] < first_test_date].copy()
    test = frame.loc[frame["date"] >= first_test_date].copy()
    if train.empty or test.empty:
        raise ValueError("Need historical rows and a later holdout period")
    return train, test


def metrics(actual: np.ndarray, predicted: np.ndarray) -> dict[str, float]:
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    abs_error = np.abs(actual - predicted)
    return {
        "MAE": round(float(mean_absolute_error(actual, predicted)), 3),
        "RMSE": round(float(np.sqrt(mean_squared_error(actual, predicted))), 3),
        "WAPE_pct": round(float(100 * abs_error.sum() / max(actual.sum(), 1.0)), 3),
        "bias": round(float(np.mean(predicted - actual)), 3),
    }


def run_demo(output_dir: str | Path = "outputs") -> dict[str, dict[str, float]]:
    """Train locally; only synthetic data is used."""
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    panel = generate_synthetic_demand()
    frame = engineer_features(panel)
    train, test = chronological_split(frame)

    # Encode fictional store/item categories without using target observations.
    all_x = pd.get_dummies(frame[FEATURES], columns=["store_id", "item_id"], dtype=float)
    x_train = all_x.loc[train.index].to_numpy(dtype=float)
    x_test = all_x.loc[test.index].to_numpy(dtype=float)

    model = HistGradientBoostingRegressor(
        max_iter=90, max_leaf_nodes=15, learning_rate=0.08,
        l2_regularization=1.0, random_state=2026,
    )
    model.fit(x_train, train["units"].to_numpy())
    prediction = np.maximum(0.0, model.predict(x_test))
    naive = test["lag_7"].to_numpy(dtype=float)
    actual = test["units"].to_numpy(dtype=float)

    scores = {
        "seasonal_naive": metrics(actual, naive),
        "gradient_boosting": metrics(actual, prediction),
    }
    (output / "metrics.json").write_text(json.dumps(scores, indent=2) + "\n", encoding="utf-8")

    results = test[["date", "store_id", "item_id", "units"]].copy()
    results["seasonal_naive"] = naive
    results["gradient_boosting"] = prediction
    # All IDs in this CSV are invented. Outputs are still intentionally gitignored.
    results.to_csv(output / "synthetic_test_forecasts.csv", index=False)

    daily = results.groupby("date")[["units", "seasonal_naive", "gradient_boosting"]].sum()
    ax = daily.plot(figsize=(10, 5), title="Synthetic daily demand: final 42 days")
    ax.set_ylabel("Fictional units per day")
    ax.set_xlabel("Date")
    plt.tight_layout()
    plt.savefig(output / "synthetic_forecast_comparison.png", dpi=140)
    plt.close()
    return scores


if __name__ == "__main__":
    print(json.dumps(run_demo(), indent=2))
