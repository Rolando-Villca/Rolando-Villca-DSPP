---
layout: default
title: "Amazon Sales & Reviews Analysis"
---

## :rocket: Executive Summary  
<a name="executive-summary"></a>

In this project we analysed **2.22 million** Amazon UK listings to predict monthly sales volume (`boughtInLastMonth`) from product metadata.  
Key highlights:

- **Skewed distributions** in price and sales required log-scaling and careful filtering.  
- **Feature engineering** (e.g. `review_intensity`) boosted signal beyond raw counts.  
- Compared **three models**: Linear Regression, Random Forest, and Random Forest with `log1p` target.  
- **Best model** (RF + log target) achieved **MAE 169.4** and **R² 0.242**, cutting error by ~17 %.  
- **Review-based metrics** (engagement per £, total reviews) proved more predictive than price alone.

---

# Amazon Sales & Reviews Analysis

<div class="project-card">
  <img src="assets/amazon-hexbin.png" alt="Hexbin: Price vs Sales" />
    <p><strong>Dataset:</strong> 2.22 million UK listings</p>
    <p><strong>Tools:</strong> Python · pandas · scikit-learn · Jupyter</p>
    <p><strong>Model:</strong> Random Forest on log-scaled target</p>
    <p><strong>Performance:</strong> MAE 169.4 · R² 0.242</p>
    <a class="button primary" href="#data-description">Jump to Data Description</a>
  </div>
---

## Data Description  
<a name="data-description"></a>

*Explain the raw dataset (2.22 M rows, 10 columns), no missing values, extreme skew.*  
*Detail filtering: dropped 18 price errors, ~2.06 M zero-sales, leaving 161 315 active listings.*

| Column            | Description                  |
| ----------------- | ---------------------------- |
| `stars`           | Avg. rating (0–5), 61 % blank |
| `reviews`         | Total review count           |
| `price`           | £0.20–£100 000               |
| `boughtInLastMonth` | Units sold last 30 days    |
| `isBestSeller`    | Bestseller badge flag        |
| `categoryName`    | Product category             |

---

## Exploratory Data Analysis  
<a name="exploratory-data-analysis"></a>

![Price Distribution](/assets/price-histogram.png)  
_Bullet: Most prices £5–£50, peaks at £9.99 & £19.99._

![Sales Distribution](/assets/sales-histogram.png)  
_Bullet: Top decile drives 75 % of volume._

![Price vs Sales (hexbin)](/assets/amazon-hexbin.png)  
_Bullet: Log–log reveals weak inverse relationship; hot-spots at £10–20 & 100–500 units._

---

## Feature Engineering  
<a name="feature-engineering"></a>


python
df_clean['review_intensity'] = df_clean['reviews'] / (df_clean['price'] + 1)
df_clean['reviews_per_star']   = df_clean['reviews'] / (df_clean['stars'] + 1)
# price_per_star dropped later for collinearity


---

## Modelling & Evaluation  
<a name="modelling--evaluation"></a>

| Model               | MAE    | R²     | CV-RMSE ± SD |
|---------------------|--------|--------|--------------|
| Linear Regression   | 204.12 | 0.2177 | 567 ± 4      |
| Random Forest       | 202.73 | 0.2071 | 574 ± 6      |
| **RF + log target** | **169.42** | **0.2424** | **559 ± 5** |

- Note: `log1p` transform stabilized variance, reducing MAE by 17 %.

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

![Feature Importance](/assets/feature-importance.png)

*Mention validating with permutation importance or SHAP in future work.*

---

## Discussion & Next Steps  
<a name="discussion--next-steps"></a>

Despite improvements, models explain ~24 % variance—seasonality, marketing, brand effects missing.  
**Next:** hyperparameter tuning, test XGBoost/CatBoost, add temporal features, sentiment analysis, segment-specific models.

---

## Conclusion  
<a name="conclusion"></a>

Review-centric metrics (especially `review_intensity`) are the strongest sales predictors. RF + log delivered the best trade-off. Merchants should prioritize review engagement, and future models should include seasonality and marketing data.

---

## Reflection  
<a name="reflection"></a>

> **📝 Reflection**  
> - Feature engineering delivered ~10 % MAE improvement.  
> - Log-scaling fixed heteroscedasticity.  
> - RF + log target outperformed baselines.  
> - Upcoming: integrate seasonality, sentiment, and advanced tuning.

---

*All visuals and full code are available in the [analysis notebook](analysis_notebook.ipynb).*  
