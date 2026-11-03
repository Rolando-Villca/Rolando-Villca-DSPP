---
layout: default
title: "Predicting AIV and ACP for Retail Labour Planning"
permalink: /projects/aiv-acp-predictive-modelling/
---

# Predicting AIV and ACP to Improve Retail Labour Requirements

**Comparing the traditional sales-and-inflation method with predictive modelling, using four years of weekly history and a held-out quarter.**

> **Synthetic demonstration — not original company results.** Every store ID, category, sales amount, average value, inflation rate, SMV and result is fictional. This is an AI-assisted public reconstruction of an analytical research idea. No genuine company data or identifiers are included.

## 1. Why predict AIV and ACP?

A sales forecast expresses expected demand in **pounds (£)**, but a store's physical workload is often driven by the **items and cases** its colleagues must handle. That is why value-to-volume conversion drivers exist.

**Average Item Value (AIV)** is historical sector sales divided by items sold. **Average Case Price (ACP)** is historical sector sales divided by case equivalents. Given forecast sales, these relationships can be reversed to obtain estimates of future item or case volumes.

| Historical ratio | Definition | Forecast quantity |
| --- | --- | --- |
| **AIV (£/item)** | Historical sales ÷ actual items | **Forecast sales ÷ forecast AIV = items** |
| **ACP (£/case)** | Historical sales ÷ actual case equivalents | **Forecast sales ÷ forecast ACP = cases** |

The arithmetic is defensible: **sales value = quantity × average value per unit**. The uncertainty lies in the *future* sales figure and *future* AIV/ACP assumption. Estimated case equivalents associated with sales are not automatically the same as delivered, stored or replenished cases.

For this experiment, we first apply the **sector share of division sales**, then derive items or cases, and apply a corresponding **Standard Minute Value (SMV)** to obtain illustrative variable task-hours.

![Illustrative flow from forecast sales through item and case volumes to labour task-hours](assets/demand-to-hours.svg)

## 2. What is wrong with leaving AIV/ACP static?

In the existing-method reconstruction, AIV and ACP are averaged from a relatively flat trading period in the **previous year**, then adjusted **week by week using Finance-style inflation assumptions**. Once the sector mix is fixed, the estimated weekly items and cases change through **forecast sales and inflation-adjusted AIV/ACP**.

But real averages can vary with the prices and mix of products purchased in different weeks, promotions and seasonal purchasing patterns. The question is whether those historical weekly patterns can be modelled more accurately than using an annual reference plus inflation alone.

> **Research question:** Will directly forecasting weekly AIV and ACP improve forecast items, case equivalents and calculated task-hours compared with the static previous-year method?

## 3. Experimental design: Q1 2026

Both methods receive the **same fictional forecast division sales, the same fixed sector mix and the same task SMVs**. Neither receives the held-out actual Q1 2026 item/case values.

| | **Method A — Static + inflation** | **Method B — Predictive challenger** |
| --- | --- | --- |
| Data source | Historical **2025 weeks 18–30** ratios | Weekly observations from **2022–2025** |
| How the drivers are forecast | Average sales ÷ actual item/case volume from the relatively flat reference period | Separate Ridge regressions on log AIV and log ACP, using calendar trend, seasonality and fictional series identity |
| Price changes | Fictional Finance-style **weekly inflation adjustments**: 2.6% annual assumption for remaining 2025, 2.8% for 2026 | **No separate inflation feature or uplift** (nominal history can still reflect past price changes) |
| Sales and workload inputs | Same forecast sales, fixed sector mix, and synthetic task SMVs | **Exactly the same** sales, sector mix, and task SMVs |
| End result | Forecast items/cases → calculated task-hours | Forecast items/cases → calculated task-hours |

**Scale of this public simulation:** 6 fictional stores × 4 fictional sectors × 208 historical weeks = **4,992 training observations**. The entire first **13 weeks of 2026**, or **312 observations**, were held out for evaluation.

## 4. Results: what the synthetic data show

### Historical weekly AIV patterns

![Fictional weekly AIV from the first quarter of 2022 through 2025](assets/historical-q1-aiv.svg)

The simulated AIV has recurring week-of-year variation and increasing nominal price levels across years. A constant previous-year flat-period value does not represent all of those effects.

### Forecast AIV for Q1 2026

![Fictional Q1 2026 AIV: simulated actual versus static and predictive forecasts](assets/q1-aiv-forecast.svg)

### Forecast ACP for Q1 2026

![Fictional Q1 2026 ACP: simulated actual versus static and predictive forecasts](assets/q1-acp-forecast.svg)

### How this flows into labour requirements

The model comparison is **not finished at AIV or ACP**. Forecast sector sales are divided by each method's ratio to get item or case forecasts, and these are multiplied by the matching synthetic task SMV.

![Fictional Q1 weekly task-hours from both methods compared with simulated actual hours](assets/q1-weekly-task-hours.svg)

### The key results: accuracy after converting into physical workload

![Comparison of synthetic Q1 2026 WAPE for predicted items, cases and task-hours](assets/downstream-wape.svg)

| Held-out Q1 2026 accuracy | Static + inflation WAPE | Predictive WAPE |
| --- | ---: | ---: |
| **AIV** | 21.998% | **12.116%** |
| **ACP** | 19.416% | **11.546%** |
| **Items** | 20.834% | **9.193%** |
| **Case equivalents** | 21.682% | **8.924%** |
| **Calculated task-hours** | 20.929% | **9.702%** |

**Finding:** task-hour forecast error decreased by **11.227 percentage points**, a **53.6% relative reduction** in this *synthetic scenario*. The direct method also reduced item and case errors. This is an experiment in forecasting methodology, **not evidence of real staffing savings**.

## 5. Interpretation and limitations

The simulated histories were **deliberately constructed with seasonality and inflation-like changes**. Therefore, a calendar-based model has an opportunity to improve on a ratio taken from a static period. Real data could produce a very different result.

The predictive model receives **no separate inflation feature or post-prediction uplift**. Its nominal AIV/ACP forecasts can nevertheless reflect price growth inferred from historical observations. Adding Finance inflation again could **double-count** the effect.

Both methods use the same forecast sales, but actual Q1 sales differ slightly from the shared forecast. This reflects a source of error common to both methods. The synthetic “actual” task-hours are calculated using invented time standards and physical quantities; they are **not real scheduled or paid hours**.

The next genuine validation would need authorised historical item/case volumes, strict forecast-origin timing for inflation assumptions and published indices, multiple out-of-time quarters, and a demonstrated relationship between sales-derived case equivalents and actual task workload.

**Conclusion:** the experiment shows how to test whether smarter AIV/ACP forecasting produces a better labour demand estimate. It does not show that the approach has already succeeded in a production wage model.

---

[**Read detailed findings and limitations**](FINDINGS.md) · [**View reproducible Python code and methodology**](README.md) · [**Explore the conversion and inflation logic**](WORKLOAD_LOGIC.md)

*The public code and documentation were prepared with AI assistance. This case study is a synthetic reconstruction; it does not publish original retailer data or original project measured outcomes.*
