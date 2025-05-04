---
layout: default
title: "Amazon Sales & Reviews Analysis"
---

# Amazon Sales & Reviews Analysis

<div class="project-card">
  <img src="/assets/amazon-hexbin.png" alt="Hexbin: Price vs Sales" />
  <div class="project-summary">
    <p><strong>Dataset:</strong> 2.22 million UK listings</p>
    <p><strong>Tools:</strong> Python · pandas · scikit-learn · Jupyter</p>
    <p><strong>Model:</strong> Random Forest on log-scaled target</p>
    <p><strong>Performance:</strong> MAE 169.4 · R² 0.242</p>
    <a class="button primary" href="#data-description">Jump to Data Description</a>
  </div>
</div>

_Predicting monthly units sold on Amazon UK from product metadata_

---

## 📋 Table of Contents

1. [Data Description](#data-description)  
2. [Exploratory Data Analysis](#exploratory-data-analysis)  
3. [Feature Engineering](#feature-engineering)  
4. [Modelling & Evaluation](#modelling--evaluation)  
5. [Feature Importance](#feature-importance)  
6. [Discussion & Next Steps](#discussion--next-steps)  
7. [Conclusion](#conclusion)  
8. [Reflection](#reflection)  

---

## Data Description  
<a name="data-description"></a>

*Explain the raw dataset (2.22 million rows, 10 columns), no missing values, extreme skew.*  
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

```python
df_clean['review_intensity'] = df_clean['reviews'] / (df_clean['price'] + 1)
df_clean['reviews_per_star']   = df_clean['reviews'] / (df_clean['stars'] + 1)
# price_per_star dropped later for collinearity
