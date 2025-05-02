---
layout: default
---

# Amazon Sales & Reviews Analysis  
[![Download Report](https://img.shields.io/badge/Report-DOCX-blue)](https://github.com/Rolando-Villca/Rolando-Villca-DSPP/raw/main/final_report.docx) [![Notebook](https://img.shields.io/badge/Notebook-Jupyter-orange)](./analysis_notebook.ipynb)

> Turning Amazon data into strategic e-commerce insights.

---

## 📋 Table of Contents

1. [🔍 Research Question](#research-question)  
2. [🚀 Executive Summary](#executive-summary)  
3. [🛠️ Methodology](#methodology)  
4. [📈 Key Findings](#key-findings)  
5. [📂 Data Description](#data-description)  
6. [🎯 Conclusion](#conclusion)  
7. [📚 References](#references)  
8. [📝 Final Report](#final-report)  

---

## 🔍 Research Question

**How can Amazon sales and review data be analyzed to extract meaningful business insights?**  
We explore whether structured product metadata—review counts, star ratings, price, category, bestseller status—can predict sales performance and guide e-commerce strategy.

---

## 🚀 Executive Summary

We analyzed **2.2 million Amazon UK product records** in Python notebooks. After data cleaning and feature engineering, we trained:

- **Linear Regression** (baseline)  
- **Random Forest Regression**

🔹 **Random Forest** achieved **MAE: 11.38** and **RMSE: 59.66**, vs. linear’s MAE: 11.56 & RMSE: 87.13.  
🔹 **Top predictors**: review volume and bestseller status.

> These insights help sellers optimize inventory, pricing, and promotions.

---

## 🛠️ Methodology

1. **Data Collection**  
   - **Sales** (`data/sales.csv`): daily units sold, revenue, price (2020–2024)  
   - **Reviews** (`data/reviews.csv`): review text, star rating, date  
   - **Metadata** (`data/products.csv`): ASIN, category, launch date, bestseller flag  

2. **Data Cleaning**  
   - Removed outliers via IQR filtering  
   - Imputed missing values  

3. **Feature Engineering**  
   ```python
   df['reviews_per_star']   = df['reviews'] / (df['stars'] + 1)
   df['price_per_star']     = df['price']   / (df['stars'] + 1)
   df['review_intensity']   = df['reviews'] / (df['price'] + 1)
