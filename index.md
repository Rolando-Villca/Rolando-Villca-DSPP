---
layout: default
title: "Amazon Sales & Reviews Analysis"
permalink: /
---

# Amazon Sales & Reviews Analysis

<div class="project-card">
  <img src="{{ site.baseurl }}/assets/amazon-hexbin.png" alt="Hexbin: Price vs Sales" />
  <div class="project-summary">
    <p><strong>Dataset:</strong> 2.22 million UK listings</p>
    <p><strong>Tools:</strong> Python · pandas · scikit-learn · Jupyter</p>
    <p><strong>Model:</strong> Random Forest on log-transformed target</p>
    <p><strong>Performance:</strong> MAE 169.4 · R² 0.242</p>
  </div>
</div>

--- 

## Introduction  
In this analysis, we harness public Amazon UK product metadata—price, star ratings, review counts, bestseller status—to uncover the key drivers of monthly sales volume. By combining exploratory data analysis with machine-learning models, we translate raw data into actionable e-commerce insights.

--- 

## 📖 Research Question  
**How can Amazon sales and review data be analysed to extract meaningful business insights and predict monthly sales volume?**

--- 

## 🚀 Executive Summary  
We processed **2.22 million** listings, engineered domain-driven features such as `review_intensity`, and compared three regression approaches:  
- **RF + log target** was best (MAE 169.4, R² 0.242; −17 % error vs baseline).  
- Review-based metrics outperformed price and ratings alone.  
- Sellers should prioritise review acquisition and visibility to boost sales.
  
--- 

## 1️⃣ Data Description  
Our raw dataset held **2 222 742** rows and 10 columns, with no missing values but extreme right skew. We:  
1. Dropped **18** products with zero/negative prices.  
2. Removed ~2.06 million listings with no sales, leaving **161 315** active items.  

| Column               | Description                       |
|----------------------|-----------------------------------|
| `stars`              | Avg. rating (0–5); 61 % unrated   |
| `reviews`            | Total review count                |
| `price`              | £0.20–£100 000                    |
| `boughtInLastMonth`  | Units sold in last 30 days        |
| `isBestSeller`       | Bestseller badge (0 or 1)         |
| `categoryName`       | Product category                  |

---

## 2️⃣ Exploratory Data Analysis  
![Price Distribution]({{ site.baseurl }}/assets/price-histogram.png)  
- Prices cluster at £5–£50, with peaks at £9.99 & £19.99.

![Sales Distribution]({{ site.baseurl }}/assets/sales-histogram.png)  
- Top 10 % of products drive 75 % of monthly volume.

![Price vs Sales (hexbin)]({{ site.baseurl }}/assets/amazon-hexbin.png)  
- Log–log scaling reveals a weak inverse slope; hotspots around £10–20 & 100–500 units.

---

## 3️⃣ Feature Engineering  

``python
df_clean['review_intensity']  = df_clean['reviews'] / (df_clean['price']   + 1)
df_clean['reviews_per_star']  = df_clean['reviews'] / (df_clean['stars']   + 1)
###'price_per_star' was dropped later to avoid collinearity

## 4️⃣ Modelling & Metrics Summary  

| Model                 | MAE        | RMSE       | R²         |
|-----------------------|------------|------------|------------|
| `Linear Regression`   | 204.12     | 568.80     | 0.2177     |
| `Random Forest`       | 202.73     | 572.64     | 0.2071     |
| `RF + log target`     | 169.42     | 559.74     | 0.2424     |

> *Applied `log1p` to stabilise variance, reducing MAE by ~17 %.*

---

## 5️⃣ Feature Importance  

| Rank | Feature            | Importance |
|------|--------------------|------------|
| 1    | `review_intensity` | 0.32       |
| 2    | `reviews`          | 0.26       |
| 3    | `price`            | 0.18       |
| 4    | `stars`            | 0.08       |
| 5    | `isBestSeller`     | 0.05       |
| 6    | `Category dummies` | 0.11       |

![Feature Importance]({{ site.baseurl }}/assets/feature-importance.png)

---

## 6️⃣ Discussion & Next Steps  
Our best model explains ~24 % of variance; external factors such as seasonality and marketing spend remain unobserved.  
**Next steps:**  
1. Hyperparameter tuning (RandomizedSearch)  
2. Test XGBoost / LightGBM / CatBoost  
3. Incorporate temporal features (seasonality)  
4. Apply sentiment analysis on review text  
5. Build category-specific models via clustering

---

## 7️⃣ Conclusion  
Review-centric features—especially `review_intensity`—are the strongest signals for monthly sales. RF + log target delivers the best trade-off (MAE 169.4, R² 0.242). Sellers should focus on review engagement and integrate temporal and marketing data to improve forecasts.

---

## 📝 Reflection  
> - Feature engineering improved MAE by ~10 %.  
> - Log-scale resolved heteroscedasticity.  
> - RF + log target outperformed baselines.  
> - **Next:** explore seasonality, sentiment analysis, advanced tuning.

---

## 📄 Download Materials  
[![Report-DOCX](https://img.shields.io/badge/Report-DOCX-blue)]({{ site.baseurl }}/assets/final_report.docx)  
[![Notebook-IPYNB](https://img.shields.io/badge/Notebook-IPYNB-orange)]({{ site.baseurl }}/analysis_notebook.ipynb)


---

## More Data Science Portfolio Projects

### Retail Item Demand Forecasting (Synthetic Demonstration)

[**Explore the case study: forecasting charts, findings and conclusions**]({{ site.baseurl }}/projects/retail-item-demand-forecasting/)

![Synthetic demand forecast error comparison]({{ site.baseurl }}/projects/retail-item-demand-forecasting/docs/figures/synthetic-error-metrics.svg)

A reproducible seven-day-ahead seasonal-naive versus Gradient Boosting comparison using **only fictional data**. Includes three charts, a results table, methodology, limitations, Python code and tests. The statistics describe a public simulation, not measured business performance.
