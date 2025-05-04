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
## Introduction  
<a name="introduction"></a>

In this analysis, we harness public Amazon UK product metadata—price, star ratings, review counts, bestseller status—to uncover the key drivers of monthly sales volume. By combining exploratory data analysis with machine-learning models, we translate raw data into actionable e-commerce insights.

## 📖 Research Question  
<a name="research-question"></a>

**How can Amazon sales and review data be analysed to extract meaningful business insights and predict monthly sales volume?**

## 🚀 Executive Summary  
<a name="executive-summary"></a>

We processed **2.22 million** listings, engineered domain-driven features such as `review_intensity`, and compared three regression approaches.  
- **RF + log target** was best: MAE 169.4 | R² 0.242 (–17 % error vs baseline).  
- Review-based metrics (engagement per £, total reviews) outperformed price and rating alone.  
- Findings guide sellers to prioritise review acquisition and visibility over pure price competition.
---

## Data Description  
<a name="data-description"></a>

Our raw dataset held **2 222 742** rows and 10 columns, with no missing values but extreme right skew. We:  
1. Dropped **18** products with zero/negative prices.  
2. Removed ~2.06 million entries with no sales, focusing on **161 315** active listings.  

| Column               | Description                         |
|----------------------|-------------------------------------|
| `stars`              | Avg. rating (0–5); 61 % unrated     |
| `reviews`            | Total review count                  |
| `price`              | £0.20–£100 000                      |
| `boughtInLastMonth`  | Units sold in last 30 days          |
| `isBestSeller`       | Bestseller badge (0 or 1)           |
| `categoryName`       | Product category                    |

---

## Exploratory Data Analysis  
<a name="exploratory-data-analysis"></a>

![Price Distribution]({{ site.baseurl }}/assets/price-histogram.png)  
- Prices cluster at £5–£50, with peaks at £9.99 & £19.99.

![Sales Distribution]({{ site.baseurl }}/assets/sales-histogram.png)  
- Top 10 % of products drive 75 % of monthly volume.

![Price vs Sales (hexbin)]({{ site.baseurl }}/assets/amazon-hexbin.png)  
- Log–log scaling shows a weak inverse slope; hotspots at ~£10–£20 & 100–500 units.
---

## Feature Engineering  
<a name="feature-engineering"></a>

python
df_clean['review_intensity'] = df_clean['reviews'] / (df_clean['price'] + 1)
df_clean['reviews_per_star']  = df_clean['reviews'] / (df_clean['stars'] + 1)
# 'price_per_star' dropped later to avoid collinearity
## Modelling & Evaluation  
<a name="modelling--evaluation"></a>

| Model               | MAE      | R²       | CV-RMSE ± SD |
|---------------------|----------|----------|--------------|
| Linear Regression   | 204.12   | 0.2177   | 567 ± 4      |
| Random Forest       | 202.73   | 0.2071   | 574 ± 6      |
| **RF + log target** | **169.42** | **0.2424** | **559 ± 5** |

- Applying `log1p` to the target stabilised variance and cut MAE by ~17 %.

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

- In future work, validate these importances with permutation-based methods or SHAP for deeper insight.  

---

## Discussion & Next Steps  
<a name="discussion--next-steps"></a>

Our best model explains ~24 % of variance; drivers such as seasonality, marketing spend, and brand loyalty remain unobserved.  
**Next steps:**  
1. Hyperparameter optimisation (e.g. RandomizedSearch)  
2. Experiment with XGBoost / LightGBM / CatBoost  
3. Incorporate temporal features to capture seasonality  
4. Apply NLP-based sentiment analysis  
5. Build category-specific models via clustering

---

## Conclusion  
<a name="conclusion"></a>

Review-centric features—especially `review_intensity`—are the dominant signals for monthly sales. RF + log target gave the best trade-off (MAE 169.4, R² 0.242), highlighting the importance of handling skew. Sellers should invest in review engagement and integrate temporal & marketing data to improve forecasting.

---

## Reflection  
<a name="reflection"></a>

> **📝 Reflection**  
> - Feature engineering cut MAE by ~10 %.  
> - Log-scaling resolved heteroscedastic errors.  
> - RF + log target outperformed both baselines.  
> - **Next:** integrate seasonality, sentiment analysis, and advanced hyperparameter tuning.

---

## Download Materials  
<a name="download-materials"></a>

[![Report-DOCX](https://img.shields.io/badge/Report-DOCX-blue)]({{ site.baseurl }}/assets/final_report.docx)  
[![Notebook-IPYNB](https://img.shields.io/badge/Notebook-IPYNB-orange)]({{ site.baseurl }}/analysis_notebook.ipynb)

</div> <!-- /.main-content -->

<aside class="sidebar">
  ## 📊 More Visualisations

  ![Price Distribution]({{ site.baseurl }}/assets/price-histogram.png)
  ![Sales Distribution]({{ site.baseurl }}/assets/sales-histogram.png)
  ![Price vs Sales (hexbin)]({{ site.baseurl }}/assets/amazon-hexbin.png)
  ![Correlation Matrix]({{ site.baseurl }}/assets/corr-heatmap.png)
</aside>
</div> <!-- /.page-layout -->
