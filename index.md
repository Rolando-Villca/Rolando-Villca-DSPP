---
layout: default
title: "Amazon Sales & Reviews Analysis"
---

# Amazon Sales & Reviews Analysis

<div class="project-card">
  <div class="project-summary">
    <p><strong>Dataset:</strong> 2.22 million UK listings</p>
    <p><strong>Tools:</strong> Python · pandas · scikit-learn · Jupyter</p>
    <p><strong>Model:</strong> Random Forest on log-transformed target</p>
    <p><strong>Performance:</strong> MAE 169.4 · R² 0.242</p>
  </div>
</div>

## 🚀 Executive Summary
<a name="executive-summary"></a>

In this project, we analysed **2.22 million** Amazon UK product listings to predict **monthly sales volume** using structured metadata.  
**Key highlights:**  
- Skewed price and sales distributions required log-scaling and focused filtering  
- Domain-driven feature engineering (e.g. `review_intensity`) enhanced predictive signal  
- Compared three models: Linear Regression, Random Forest, and Random Forest on a `log1p` target  
- The best model (RF + log target) achieved **MAE 169.4** and **R² 0.242**, reducing error by ~17 %  
- Review-based metrics outperformed price and ratings alone, guiding strategic engagement

---
## Data Description  
<a name="data-description"></a>

*Explain the raw dataset (2.22 million rows, 10 columns), no missing values, extreme skew.*  
*Filtering: dropped 18 price errors, ~2.06 million zero-sales, leaving 161 315 active listings.*

| Column                | Description                        |
|-----------------------|------------------------------------|
| `stars`               | Avg. rating (0–5); 61 % unrated    |
| `reviews`             | Total review count                 |
| `price`               | £0.20–£100 000                     |
| `boughtInLastMonth`   | Units sold in last 30 days         |
| `isBestSeller`        | Bestseller badge flag (0 or 1)     |
| `categoryName`        | Product category                   |

---

## Exploratory Data Analysis  
<a name="exploratory-data-analysis"></a>

![Price Distribution]({{ site.baseurl }}/assets/price-histogram.png)

- Most product prices fall between £5–£50, with peaks at £9.99 and £19.99.

![Sales Distribution]({{ site.baseurl }}/assets/sales-histogram.png)

- The top decile of products drives 75 % of total sales volume.

![Price vs Sales (hexbin)]({{ site.baseurl }}/assets/amazon-hexbin.png)

- Log–log scaling reveals a weak inverse relationship, with hotspots at £10–20 and 100–500 units.

---

## Feature Engineering  
<a name="feature-engineering"></a>

python
df_clean['review_intensity'] = df_clean['reviews'] / (df_clean['price'] + 1)
df_clean['reviews_per_star']  = df_clean['reviews'] / (df_clean['stars'] + 1)
# 'price_per_star' dropped later to avoid collinearity

---

### Part 2 (Modelling → Reflection)

## Modelling & Evaluation  
<a name="modelling--evaluation"></a>

| Model               | MAE      | R²       | CV-RMSE ± SD |
|---------------------|----------|----------|--------------|
| Linear Regression   | 204.12   | 0.2177   | 567 ± 4      |
| Random Forest       | 202.73   | 0.2071   | 574 ± 6      |
| **RF + log target** | **169.42** | **0.2424** | **559 ± 5** |

- Applying `log1p` stabilized variance, reducing MAE by ~17 %.

---

## Feature Importance  
<a name="feature-importance"></a>

| Rank | Feature            | Importance |
|------|--------------------|------------|
| 1    | `review_intensity` | 0.32       |
| 2    | `reviews`          | 0.26       |
| 3    | `price`            | 0.18       |
| 4    | `stars`            | 0.08       |
| 5    | `isBestSeller`     | 0.05       |
| 6    | Category dummies   | 0.11       |

![Feature Importance]({{ site.baseurl }}/assets/feature-importance.png)

- Future work: validate importances with permutation importance or SHAP.

---

## Discussion & Next Steps  
<a name="discussion--next-steps"></a>

Our best model explains ~24 % of variance; missing factors such as seasonality, marketing spend, and brand loyalty remain unobserved.  
**Next steps:**  
1. Hyperparameter optimization (e.g., RandomizedSearch)  
2. Explore gradient boosting (XGBoost, LightGBM, CatBoost)  
3. Incorporate temporal features to capture seasonality  
4. Apply sentiment analysis to review text  
5. Build category-specific models via clustering

---

## Conclusion  
<a name="conclusion"></a>

Review-centric metrics—particularly `review_intensity`—are the strongest signals for monthly sales volume on Amazon UK. A Random Forest on a log-transformed target produced the best performance (MAE 169.4, R² 0.242), underscoring the importance of handling skewed data. Sellers should prioritize review acquisition and engagement, and future work will benefit from integrating temporal and contextual marketing data.

---

## Reflection  
<a name="reflection"></a>

> **📝 Reflection**  
> - Feature engineering cut MAE by ~10 %.  
> - Log-scaling resolved heteroscedastic errors.  
> - RF + log target outperformed the baselines.  
> - Next: integrate seasonality, sentiment analysis, and advanced hyperparameter tuning.

---

*Full code and visuals are available in the [analysis notebook](analysis_notebook.ipynb).*

