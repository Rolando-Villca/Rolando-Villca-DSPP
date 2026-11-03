# From Value Drivers to Workload — An Illustrative Calculation Guide

## The business connection

**Value forecasts → physical workload → task-level labour demand**.

Sales forecasts are measured in currency, but many store activities require handling items or cases. AIV and ACP are conversion factors that translate financial demand into an estimate of physical volume. Whether this improves *total* labour forecasts depends on the accuracy of sales, mix, the conversion driver, packaging assumptions, and task time standards.

This is a **simplified educational illustration**, not a description of confidential business rules or an operational wage engine. All numerical inputs are invented.

## Terms and units

| Symbol | Definition | Units |
| --- | --- | --- |
| `S` | Forecast division sales | £ |
| `m` | Sector share of division sales | Fraction, 0–1 |
| `AIV` | Average Item Value | £/item |
| `ACP` | Average Case Price | £/case |
| `IPC` | Items Per Case | items/case |
| `SMV` | Standard Minute Value for a specific task | min/case or min/item, as applicable |

Calculate **sector sales = S × m**.

- **Item-led calculation:** `items = sector_sales / AIV`; for case-based work, `cases = items / IPC`.
- **Case-led calculation:** `cases = sector_sales / ACP`.
- **Task hours:** `units × matching SMV / 60`, ensuring the unit type and SMV agree.

**Never double count** the item-led and case-led routes: they are alternatives for the same sales slice. A task with an item-specific standard should use item volume; a case-specific task should use cases. Fixed hours and other workload drivers are outside this miniature example.

### Invented worked example

| Step | Fictional input or calculation | Result |
| --- | --- | --- |
| Divisional sales | £120,000 | £120,000 |
| Sector sales mix | 25% | £30,000 sector sales |
| Item-based assumption | AIV £5 per item | 6,000 items |
| Packaging assumption | 12 items per case | 500 cases |
| **Alternative** case-based assumption | ACP £60 per case | 500 cases |
| Case-handling task standard | 2.4 minutes per case | **20 task-hours** |

An alternative true quarterly ACP of **£75** would give **400 cases** and **16 task-hours**. Holding a static £60 driver would then overstate this task's workload by **4 hours**. That does *not* mean four actual paid hours could be cut: operational timing, fixed time, other tasks, safe staffing and constraints would need separate examination.

## What counts as a successful predictive model?

The project should report performance at **three levels**, rather than focusing only on AIV/ACP MAE:

1. **Conversion-driver accuracy:** errors and directional bias for AIV/ACP.
2. **Derived volume accuracy:** errors for items and/or cases after forecast sales and mix are applied.
3. **Downstream sensitivity:** an illustrative difference in calculated task-hours under static versus quarterly assumptions.

No evaluation of actual company labour requirements is included in this public reconstruction.

## Quarter adjustment is an assumption unless validated

If a model predicts an annual value and applies quarter multipliers, `forecast_q = annual_forecast × quarterly_factor_q` is an **adjustment scenario**. It is not, by itself, an independently forecast seasonal effect.

Quarter factors would need evidence from prior history or separate validation. The synthetic illustration allows the mechanics to be explored without publishing internal seasonal coefficients.

## Weekly inflation adjustments and the labour-planning effect

**Operational planning:** Finance-provided, forward-looking inflation assumptions can adjust expected AIV/ACP **at weekly frequency** as the planning period approaches. The exact annual, quarterly, monthly or weekly input frequency must be known first; **an annual inflation rate is not a weekly rate**.

**External alternative:** published inflation or retail price indices can serve as **historical comparators**, scenario inputs, or explanatory features. The UK ONS publishes CPI/CPIH mainly as **monthly data with a publication lag**, not a ready-to-use weekly forecast ([ONS publication guidance](https://www.ons.gov.uk/economy/inflationandpriceindices/methodologies/howwepublishourconsumerpricesoutputs)). The [ONS retail sales methodology](https://www.ons.gov.uk/businessindustryandtrade/retailindustry/bulletins/retailsales/august2024) also distinguishes sales **value** from sales **volume** by accounting for price changes.

### Example: convert a fictional annual rate into weekly price assumptions

```text
annual_rate                 = 0.052   # illustrative 5.2% per year
weekly_rate                 = (1 + annual_rate) ** (1/52) - 1
AIV_at_week_t               = AIV_at_base_week × (1 + weekly_rate) ** t
ACP_at_week_t               = ACP_at_base_week × (1 + weekly_rate) ** t
items_at_week_t             = forecast_sector_sales_t / AIV_at_week_t
case_equivalents_at_week_t  = forecast_sector_sales_t / ACP_at_week_t
```

This interpolation assumes a **constant compounding path**, which is appropriate for a simple teaching scenario but should not replace known week-specific Finance assumptions. An **index-level ratio** `index_t / index_base` is generally preferable when a relevant observed price index is available.

In the worked example with `£30,000` of fictional weekly sector sales and `£60` ACP, a rising inflation-adjusted ACP leads to **lower forecast case equivalents at fixed nominal sales**, and therefore fewer case-task minutes. That is a mathematical **sensitivity**, not evidence that real demand, deliveries or actual labour needs have fallen.

### What to compare

| Scenario | Inflation source | Intended role |
| --- | --- | --- |
| Annual driver held constant | None | Baseline |
| Finance-inflated driver | Week-dated planning assumptions | Operational scenario |
| Observed-index adjustment | Published CPI / sector index **already available by forecast origin** | Historical benchmark or retrospective analysis |
| Modelled AIV/ACP | Historical ratio, price and mix drivers | Predictive challenger; avoid applying inflation twice |

**Key modelling safeguards:**
- Track *when* Finance supplied each rate and when external figures were published; using a future realised rate in an earlier forecast is information leakage.
- Inflation changes **price-related value**, while sector mix, promotions and packaging can change the AIV/ACP ratio separately.
- Annualised, monthly and weekly rates must be converted with explicit compounding rules; do **not** add a full 12-month CPI percentage every week.
- Keep both **sector sales and AIV/ACP on the same nominal price basis**. Do not separately inflation-uplift a predicted nominal AIV that already includes the same price effect.
- Evaluate **item/case error and task-hour bias**, not just improvement in AIV/ACP accuracy.

A runnable fictional weekly example is provided in [`src/inflation.py`](src/inflation.py). Published values are **not downloaded** by that script and must never be represented as forecasts known in advance.

## Confidentiality

The public case study uses no real store IDs, real product codes, internal labour standards, actual costs, employee information, source paths or protected data. All coefficients and worked examples are fictional.
