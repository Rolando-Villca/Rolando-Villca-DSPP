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

## Confidentiality

The public case study uses no real store IDs, real product codes, internal labour standards, actual costs, employee information, source paths or protected data. All coefficients and worked examples are fictional.
