"""Synthetic quarterly AIV/ACP exploration; never reads employer data."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error


def synthetic_panel(seed=2026):
    rng = np.random.default_rng(seed)
    records = []
    for store in range(1, 13):
        for category in "ABCDE":
            base_aiv = rng.uniform(2.5, 12)
            base_acp = rng.uniform(15, 65)
            for year in range(2016, 2026):
                for quarter in range(1, 5):
                    season = [0.95, 1.04, 0.99, 1.12][quarter - 1]
                    trend = 1 + 0.014 * (year - 2016)
                    aiv = max(0.1, base_aiv * season * trend + rng.normal(0, 0.28))
                    acp = max(0.1, base_acp * season * trend + rng.normal(0, 2.4))
                    records.append((f"DEMO-STORE-{store:03d}", f"CATEGORY-{category}",
                                    year, quarter, aiv, acp))
    return pd.DataFrame(records, columns=["store_id", "category", "year", "quarter", "AIV", "ACP"])


def evaluate(df, target):
    # Forecast 2025 from 2016-2024. The baseline is a category/quarter
    # historical average; the model also uses a trend in calendar year.
    train = df[df.year < 2025].copy()
    test = df[df.year == 2025].copy()
    features = ["store_id", "category", "quarter", "year"]
    x_train = pd.get_dummies(train[features].astype(str), dtype=float)
    x_test = pd.get_dummies(test[features].astype(str), dtype=float).reindex(
        columns=x_train.columns, fill_value=0)
    model = Ridge(alpha=8)
    model.fit(x_train, train[target])
    predicted = model.predict(x_test)
    historical = train.groupby(["store_id", "category", "quarter"])[target].mean()
    baseline = test.set_index(["store_id", "category", "quarter"]).index.map(historical).to_numpy()
    return {"historical_baseline_MAE": round(float(mean_absolute_error(test[target], baseline)), 3),
            "ridge_MAE": round(float(mean_absolute_error(test[target], predicted)), 3)}


def main(output_dir="outputs"):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    df = synthetic_panel()
    scores = {target: evaluate(df, target) for target in ("AIV", "ACP")}
    (output / "synthetic_metrics.json").write_text(json.dumps(scores, indent=2) + "\n")
    for target in ("AIV", "ACP"):
        fig, ax = plt.subplots(figsize=(9, 4.5))
        df.groupby(["year", "quarter"])[target].mean().unstack().plot(ax=ax, marker="o")
        ax.set(title=f"Synthetic {target} by year and quarter", ylabel=f"Fictional {target} value",
               xlabel="Year")
        fig.tight_layout()
        fig.savefig(output / f"synthetic_{target.lower()}_quarterly.svg")
        plt.close(fig)
    return scores


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
