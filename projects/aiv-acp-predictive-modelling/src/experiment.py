"""Synthetic 2022–2025 weekly AIV/ACP history and held-out Q1 2026 comparison.

The static method uses a 2025 flat-period sales/quantity ratio plus weekly
Finance-style inflation. The predictive method models nominal ratios directly
without an extra inflation input or uplift. Both use identical forecast sales,
fixed sector mix, and fictional task time standards to estimate task-hours.

This public teaching experiment does NOT use employer data.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

STORES = tuple(f"DEMO-STORE-{n:03d}" for n in range(1, 7))
SECTORS = ("CATEGORY-A", "CATEGORY-B", "CATEGORY-C", "CATEGORY-D")
FLAT_WEEKS = tuple(range(18, 31))
HOLDOUT_WEEKS = tuple(range(1, 14))
# 100% invented, NOT official inflation rates.
SYNTHETIC_INFLATION_ANNUAL = {
    2022: .075, 2023: .060, 2024: .032, 2025: .022, 2026: .022
}
FINANCE_2025_ANNUAL_ASSUMPTION = .026  # fictional
FINANCE_2026_ANNUAL_ASSUMPTION = .028  # fictional
CASE_SECTORS = frozenset(("CATEGORY-C", "CATEGORY-D"))
SECTOR_MIX = (.30, .25, .23, .22)
TASK_MINUTES = {
    "CATEGORY-A": .31, "CATEGORY-B": .28,
    "CATEGORY-C": 2.60, "CATEGORY-D": 2.35
}


def make_synthetic_history(seed=2026):
    """Generate invented weekly realised quantities and planning sales.

    The generated actual Q1 2026 quantities are used for scoring ONLY.
    They are not available to either forecasting method.
    """
    rng = np.random.default_rng(seed)
    rows = []
    base_aiv = [3.5, 7.2, 5.3, 9.7]
    pack_size = [8.0, 13.0, 10.0, 6.0]
    seasonal = [.125, -.11, .18, -.16]
    store_scale = rng.uniform(.90, 1.12, size=len(STORES))
    price_level = {2022: 1.0}
    for year in range(2023, 2027):
        price_level[year] = price_level[year-1] * (
            1 + SYNTHETIC_INFLATION_ANNUAL[year-1]
        )
    for store_num, store in enumerate(STORES):
        store_sales = rng.uniform(84000, 134000)
        for year in range(2022, 2027):
            for week in range(1, 53 if year < 2026 else 14):
                t = (year-2022)*52 + week-1
                year_growth = 1 + .037*(year-2022)
                demand_season = 1 + .09*np.cos(2*np.pi*(week-4)/52)
                actual_div_sales = max(
                    1000, store_sales*year_growth*demand_season*(
                        1+rng.normal(0,.028)))
                forecast_div_sales = max(
                    1000, actual_div_sales*(1+rng.normal(0,.024)))
                for idx,sector in enumerate(SECTORS):
                    mix = SECTOR_MIX[idx]
                    actual_sector_sales = actual_div_sales*mix
                    forecast_sector_sales = forecast_div_sales*mix
                    inflation_price = price_level[year]*(
                        1+SYNTHETIC_INFLATION_ANNUAL[year]
                    )**((week-1)/52)
                    seasonal_ratio = 1+seasonal[idx]*np.cos(
                        2*np.pi*(week-5)/52)
                    implied_aiv = (
                        base_aiv[idx]*store_scale[store_num]*
                        inflation_price*seasonal_ratio*
                        (1+rng.normal(0,.008))
                    )
                    actual_items = max(1,round(actual_sector_sales/implied_aiv))
                    ipc = pack_size[idx]*(1+.035*np.sin(
                        2*np.pi*(week+idx*3)/52))
                    actual_cases = actual_items/ipc
                    rows.append({
                        "year":year,"week":week,"week_index":t,
                        "store_id":store,"sector_id":sector,
                        "division_actual_sales":actual_div_sales,
                        "division_forecast_sales":forecast_div_sales,
                        "sector_mix":mix,
                        "sector_actual_sales":actual_sector_sales,
                        "sector_forecast_sales":forecast_sector_sales,
                        "items_actual":float(actual_items),
                        "cases_actual":float(actual_cases),
                        "AIV_actual":actual_sector_sales/actual_items,
                        "ACP_actual":actual_sector_sales/actual_cases,
                        "SMV_minutes_per_unit":TASK_MINUTES[sector],
                        "workload_unit":(
                            "case" if sector in CASE_SECTORS else "item"),
                    })
    return pd.DataFrame(rows)


def planning_features(frame):
    """Only fictional IDs and calendar variables known at forecast origin.

    No inflation feature, forecast sales, or realised 2026 quantities are used.
    """
    week=frame["week"].to_numpy(dtype=float)
    t=frame["week_index"].to_numpy(dtype=float)
    return pd.DataFrame({
        "series_id":(
            frame["store_id"].astype(str)+"::"+
            frame["sector_id"].astype(str)),
        "t_years":t/52,
        "sin_1":np.sin(2*np.pi*week/52),
        "cos_1":np.cos(2*np.pi*week/52),
        "sin_2":np.sin(4*np.pi*week/52),
        "cos_2":np.cos(4*np.pi*week/52),
    },index=frame.index)


def model_predictions(train,test,target):
    """Forecast the nominal ratio itself; do not apply inflation afterwards."""
    features=["t_years","sin_1","cos_1","sin_2","cos_2"]
    prep=ColumnTransformer([
        ("continuous",StandardScaler(),features),
        ("series",OneHotEncoder(handle_unknown="ignore"),["series_id"]),
    ])
    pipeline=Pipeline([
        ("prep",prep),("ridge",Ridge(alpha=12.0))
    ])
    pipeline.fit(planning_features(train),np.log(train[target].to_numpy()))
    return np.exp(pipeline.predict(planning_features(test)))


def static_predictions(train,test,target):
    """Weighted 2025 W18–W30 reference value + weekly fictional inflation."""
    reference=train.loc[
        (train.year==2025)&train.week.isin(FLAT_WEEKS)
    ].copy()
    denominator=("items_actual" if target=="AIV_actual" else "cases_actual")
    totals=reference.groupby(["store_id","sector_id"])[
        ["sector_actual_sales",denominator]
    ].sum()
    lookup=totals["sector_actual_sales"]/totals[denominator]
    base=test.set_index(["store_id","sector_id"]).index.map(
        lookup).to_numpy(dtype=float)
    # Use separate *invented* annual assumptions, converted to weekly
    # effective rates; W24 is the midpoint of the flat reference period.
    remaining_weeks_2025=52-24
    elapsed_2026=test["week"].to_numpy(dtype=float)-1
    return (base
        *(1+FINANCE_2025_ANNUAL_ASSUMPTION)**(remaining_weeks_2025/52)
        *(1+FINANCE_2026_ANNUAL_ASSUMPTION)**(elapsed_2026/52))


def scoring(actual,predicted):
    actual=np.asarray(actual,dtype=float)
    prediction=np.asarray(predicted,dtype=float)
    errors=prediction-actual
    return {
        "MAE":round(float(np.mean(np.abs(errors))),4),
        "RMSE":round(float(np.sqrt(np.mean(errors**2))),4),
        "WAPE_pct":round(float(
            100*np.abs(errors).sum()/max(actual.sum(),1e-12)),3),
        "bias":round(float(errors.mean()),4),
    }


def backtest(panel):
    """Preserve actual Q1 2026 strictly as an out-of-sample target."""
    train=panel.loc[panel.year<=2025].copy()
    test=panel.loc[
        (panel.year==2026)&panel.week.isin(HOLDOUT_WEEKS)
    ].copy()
    if train.empty or test.empty or train.year.max()>=test.year.min():
        raise ValueError("Training must end before Q1 2026")

    for target,short in (
        ("AIV_actual","AIV"),("ACP_actual","ACP")
    ):
        test[f"{short}_static"]=static_predictions(train,test,target)
        test[f"{short}_model"]=model_predictions(train,test,target)
        for method in ("static","model"):
            volume=("items" if short=="AIV" else "cases")
            test[f"{volume}_{method}"]=(
                test["sector_forecast_sales"]/test[f"{short}_{method}"]
            )

    for method in ("static","model"):
        test[f"task_units_{method}"]=np.where(
            test.workload_unit.eq("item"),
            test[f"items_{method}"],test[f"cases_{method}"])
        test[f"hours_{method}"]=(
            test[f"task_units_{method}"]*test.SMV_minutes_per_unit/60
        )
    test["actual_task_units"]=np.where(
        test.workload_unit.eq("item"),test.items_actual,test.cases_actual)
    test["hours_actual"]=(
        test.actual_task_units*test.SMV_minutes_per_unit/60
    )
    result={
        "scope":{
            "historical_years":"2022-2025","test_year":2026,
            "test_weeks":"01-13","stores":len(STORES),
            "sectors":len(SECTORS),"training_rows":len(train),
            "holdout_rows":len(test),"reference_weeks":"2025 W18-W30",
            "synthetic_finance_2025_annual_inflation_pct":2.6,
            "synthetic_finance_2026_annual_inflation_pct":2.8,
            "inflation_in_model_features":False,
        },
    }
    for target in ("AIV","ACP"):
        result[target]={
            method:scoring(test[f"{target}_actual"],
                           test[f"{target}_{method}"])
            for method in ("static","model")
        }
    for target in ("items","cases"):
        result[target]={
            method:scoring(test[f"{target}_actual"],
                           test[f"{target}_{method}"])
            for method in ("static","model")
        }
    result["task_hours"]={
        method:scoring(test.hours_actual,test[f"hours_{method}"])
        for method in ("static","model")
    }
    return test,result


def run(output_dir="outputs"):
    """Run the demonstration; created outputs are deliberately gitignored."""
    output=Path(output_dir)
    output.mkdir(parents=True,exist_ok=True)
    panel=make_synthetic_history()
    test,results=backtest(panel)
    (output/"synthetic_results.json").write_text(
        json.dumps(results,indent=2)+"\n",encoding="utf8")
    test.to_csv(output/"synthetic_holdout_predictions.csv",index=False)
    # On-demand SVG charts are created from the same generated output.
    from src.charts import create_charts
    create_charts(panel,test,output/"figures")
    return results


if __name__=="__main__":
    print(json.dumps(run(),indent=2))
