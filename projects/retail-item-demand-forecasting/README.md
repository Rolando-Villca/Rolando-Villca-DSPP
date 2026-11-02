# Retail Item Demand Forecasting — Public Portfolio Demonstration

**Skills:** Python, pandas, NumPy, scikit-learn, time-series feature engineering, chronological validation, data governance

## Business question
Could forecasts of item quantities provide a useful input to future workload planning, compared with a simple seasonal-naive rule? The project investigates **demand forecasting**, not direct prediction of employee hours or a replacement for an operational labour model.

## Provenance: original project versus this public reconstruction
This is an **independent, reproducible reconstruction** of a previously completed academic proof of concept. It retains the broad analytical approach: daily store–item demand, a seven-day-ahead forecast, a seasonal-naive baseline, a gradient-boosted challenger and a held-out chronological test period.

**All data in this repository are newly generated and fictional.** IDs are invented, figures and dates are simulated, and any metrics produced by the code describe **this demo only**. They are **not** the results or data of the original organisational analysis. The original project used large-scale data preparation upstream; this public demo deliberately runs locally and does not claim to reproduce enterprise-scale distributed ingestion.

## How the public version works
1. Generate synthetic item demand with weekly seasonality and different fictional stores and products.
2. Create demand features at lags of 7, 14 and 28 days, plus the mean of the most recent **fully observable** seven-day window (days t−13 through t−7).
3. Use the final 42 days for a chronological test; never shuffle the time series.
4. Compare **Seasonal Naive** (demand seven days ago) with **Histogram Gradient Boosting**.
5. Measure MAE, RMSE, WAPE and signed bias. Save test-set forecasts and a chart to a local `outputs/` directory.

No future observed demand is supplied to the challenger: every historical demand feature is at least seven days old relative to its forecasted date. This design supports a rolling seven-day-ahead interpretation, not a forecast that has seen transactions inside the horizon.

## Run locally

```bash
python -m pip install -r requirements.txt
python -m src.forecast
python -m unittest discover -s tests -v
```

Running the script generates files under `outputs/`, which is ignored by Git. You do not need internal data, a Databricks account, or a company network.

## Interpreting results and next steps
- Improvement over a naive forecast on synthetic data is **not** evidence of actual business savings.
- A dense set of fictional items does not establish performance for intermittent demand, seasonal peaks, promotions or new products.
- A true weekly planning experiment should fix a common forecast origin and use only the data available at that origin; this demo uses a rolling per-target-date seven-day horizon.
- Item forecasts would require further validation against cases, deliveries, work standards, and task-level requirements before being used for staffing.
- Future work: rolling-origin backtests, calibrated uncertainty, promotion calendars, hierarchical aggregation, and separately validated mapping to workload.

## Publication and confidentiality
No real store numbers, customer records, transaction tables, operational paths, internal documentation, credentials or proprietary screenshots are included. Do not add any non-public source data. See [PRIVACY.md](PRIVACY.md).

> Portfolio disclosure: the code in this public reconstruction was prepared with AI assistance and should be reviewed, understood, tested and adapted by the repository owner before describing it as independently implemented software.
