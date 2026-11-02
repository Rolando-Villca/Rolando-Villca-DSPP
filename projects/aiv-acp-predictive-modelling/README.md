# Quarterly AIV and ACP Predictive Modelling — Synthetic Portfolio Reconstruction

**Status:** Initial reproducible reconstruction; original model metrics have not been verified.

## Question
Can historical Average Item Value (AIV) and Average Case Price (ACP) patterns inform quarterly planning assumptions instead of applying one static annual assumption?

This is a **separate project from item-level demand forecasting**. The objective is to explore the behaviour of value-per-item and price-per-case proxies, not to claim that labour hours can be predicted directly.

## What is included
- Fictional historical records across multiple years, store-like identifiers and retail categories.
- Exploratory charts for yearly patterns, quarterly profiles and AIV/ACP relationships.
- An explicit distinction between **illustrative seasonality** and observed historical seasonality.
- A chronological holdout demonstration comparing a historical baseline against a regularised regression model.

## Data protection and provenance
**Every number is generated from scratch.** No original files, store identifiers, category codes, transaction records, colleague information or operational figures are included. Fictional categories are labelled `CATEGORY-A` through `CATEGORY-E`. All published figures and model scores are synthetic and must not be represented as measured business performance.

The original work explored historical AIV and ACP patterns and quarterly assumptions. This public code is an **AI-assisted reconstruction**, not a copy of an internal notebook. Model results and precise methods of the original analysis have not yet been independently checked against its source notebooks.

## Run
```bash
python -m pip install -r requirements.txt
python -m src.analysis
python -m unittest discover -s tests -v
```

Generated figures and scores are saved to the gitignored `outputs/` directory.

## Next review
After running the reconstruction, add the synthetic results and figures to a full case-study page. Before describing any original research outcomes, validate them against the original project material and confirm they are suitable for public disclosure.
