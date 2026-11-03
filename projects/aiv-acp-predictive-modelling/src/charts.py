"""Charts for the synthetic Q1 2026 AIV/ACP forecasting experiment."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["svg.fonttype"] = "none"
COLOURS={"static":"#e09d48","model":"#168c86","actual":"#223a61"}


def create_charts(panel,test,output_dir="outputs/figures"):
    output=Path(output_dir)
    output.mkdir(parents=True,exist_ok=True)
    saved=[]

    # History: real calculation of synthetic weekly AIV, not a sketch.
    sample=panel.loc[
        (panel.sector_id=="CATEGORY-A")&(panel.year<=2025)
    ].groupby(["year","week"])["AIV_actual"].mean().unstack(0)
    fig,ax=plt.subplots(figsize=(9.5,4.6))
    for year in (2022,2023,2024,2025):
        ax.plot(sample.index,sample[year],label=str(year),linewidth=2)
    ax.set(title="Fictional weekly AIV | Category A | 2022–2025",
           xlabel="Week of year",ylabel="AIV (£ per item)",xlim=(1,52))
    ax.legend(ncol=4);ax.grid(alpha=.2);fig.tight_layout()
    file=output/"historical-weekly-aiv.svg"
    fig.savefig(file);plt.close(fig);saved.append(file)

    for ratio,filename in (
        ("AIV","q1-aiv-forecast.svg"),("ACP","q1-acp-forecast.svg")
    ):
        weekly=test.loc[test.sector_id=="CATEGORY-A"].groupby("week")[
            [f"{ratio}_actual",f"{ratio}_static",f"{ratio}_model"]
        ].mean()
        fig,ax=plt.subplots(figsize=(9.5,4.6))
        for key,name,method in (
            ("actual","Simulated actual","actual"),
            ("static","2025 reference + weekly inflation","static"),
            ("model","Predicted directly, no extra inflation","model"),
        ):
            ax.plot(weekly.index,weekly[f"{ratio}_{key}"],
                    label=name,color=COLOURS[method],linewidth=2.5,
                    marker="o",markersize=3)
        unit="£ per item" if ratio=="AIV" else "£ per case"
        ax.set(title=f"Q1 2026: {ratio} out-of-sample comparison (synthetic)",
               xlabel="Week of 2026",ylabel=unit,
               xticks=[1,3,5,7,9,11,13])
        ax.legend();ax.grid(alpha=.2);fig.tight_layout()
        file=output/filename
        fig.savefig(file);plt.close(fig);saved.append(file)

    weekly=test.groupby("week")[[
        "hours_actual","hours_static","hours_model"
    ]].sum()
    fig,ax=plt.subplots(figsize=(9.5,4.6))
    for key,name,method in (
        ("actual","Simulated actual task-hours","actual"),
        ("static","Static + weekly inflation","static"),
        ("model","Predictive AIV/ACP","model"),
    ):
        ax.plot(weekly.index,weekly[f"hours_{key}"],
                label=name,color=COLOURS[method],marker="o",linewidth=2.5)
    ax.set(title="Q1 2026: estimated task-hours by week (synthetic)",
           xlabel="Week of 2026",ylabel="Illustrative task-hours",
           xticks=[1,3,5,7,9,11,13])
    ax.legend();ax.grid(alpha=.2);fig.tight_layout()
    file=output/"q1-weekly-task-hours.svg"
    fig.savefig(file);plt.close(fig);saved.append(file)

    names=("Items","Cases","Task-hours")
    observed=(test.items_actual,test.cases_actual,test.hours_actual)
    static=(test.items_static,test.cases_static,test.hours_static)
    model=(test.items_model,test.cases_model,test.hours_model)
    def wape(actual,pred):
        return 100*abs(pred-actual).sum()/actual.sum()
    static_err=[wape(a,b) for a,b in zip(observed,static)]
    model_err=[wape(a,b) for a,b in zip(observed,model)]
    fig,ax=plt.subplots(figsize=(9.5,4.6))
    xs=np.arange(len(names))
    bars_a=ax.bar(xs-.19,static_err,width=.38,color=COLOURS["static"],
                  label="Static + weekly inflation")
    bars_b=ax.bar(xs+.19,model_err,width=.38,color=COLOURS["model"],
                  label="Predictive AIV/ACP")
    ax.bar_label(bars_a,fmt="%.1f%%",padding=3)
    ax.bar_label(bars_b,fmt="%.1f%%",padding=3)
    ax.set(xticks=xs,xticklabels=names,
           title="Downstream forecasting errors | Q1 2026 synthetic holdout",
           ylabel="WAPE (%) — lower is better",
           ylim=(0,max(static_err+model_err)*1.35))
    ax.legend();fig.tight_layout()
    file=output/"downstream-wape.svg"
    fig.savefig(file);plt.close(fig);saved.append(file)
    return saved
