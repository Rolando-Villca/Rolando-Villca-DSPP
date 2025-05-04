# Amazon Sales & Reviews Analysis

*Data Science Portfolio Project*

## 🎯 Research Question

**How can Amazon sales and review data be analysed to extract meaningful business insights?**
This project explores how product metadata and review information can be used to predict sales volume on Amazon UK.

---

## 🔍 Objective

Build a predictive model to estimate **`boughtInLastMonth`** (monthly sales) based on product features.

---

## 🧪 Approach

1.  **Data Inspection**: Load the dataset, review structure, check for nulls and types.
2.  **Exploratory Data Analysis (EDA)**: Understand distributions, relationships, and key trends using visualisations and descriptive statistics.
3.  **Feature Engineering**: Create meaningful variables that might improve model performance.
4.  **Baseline Modelling**: Train a simple Linear Regression model and evaluate its performance.
5.  **Advanced Modelling**: Use Random Forest to capture non-linear relationships and compare results.
6.  **Insights & Recommendations**: Summarise findings and their potential business implications.

---

## 📋 Table of Contents

1.  [Data Description](#data-description)
2.  [Exploratory Data Analysis](#exploratory-data-analysis)
3.  [Feature Engineering](#feature-engineering)
4.  [Modelling & Evaluation](#modelling--evaluation)
5.  [Feature Importance](#feature-importance)
6.  [Discussion & Next Steps](#discussion--next-steps)
7.  [Conclusion](#conclusion)
8.  [Reflection](#reflection)

---

## Data Description <a name="data-description"></a>

The raw dataset contains 2.22 million rows and 10 columns. There were no missing values.  Key characteristics include heavily skewed distributions for sales volume (`boughtInLastMonth`) and predictor variables like `price` and `reviews`.

After filtering, we dropped 18 price errors and ~2.06 million zero-sales listings, resulting in 161,315 active listings for analysis.

| Column                | Description                                    |
| --------------------- | ---------------------------------------------- |
| `stars`               | Avg. rating (0–5), 61% blank                   |
| `reviews`             | Total review count                             |
| `price`               | £0.20–£100,000                                 |
| `boughtInLastMonth`   | Units sold last 30 days                         |
| `isBestSeller`        | Bestseller badge flag                          |
| `categoryName`          | Product category                               |

---

## Exploratory Data Analysis <a name="exploratory-data-analysis"></a>

### Price and Sales Distributions

* Most products are priced below £50.
* A small proportion of items generate very high sales.

### Price vs. Sales

* A weak inverse relationship exists between price and sales.
* Sales hotspots are observed for products priced between £10-£20 and £100-£500.

---
## Feature Engineering <a name="feature-engineering"></a>

New features were engineered to capture potential non-linear relationships:

```python
df_clean['review_intensity'] = df_clean['reviews'] / (df_clean['price'] + 1)
df_clean['reviews_per_star']  = df_clean['reviews'] / (df_clean['stars'] + 1)
# price_per_star dropped later for collinearity
```

* `review_intensity`:  Reviews per unit price.

* `reviews_per_star`: Reviews per star rating.

---

## Modelling & Evaluation <a name="modelling--evaluation"></a>

### Linear Regression (Baseline)

A baseline linear regression model showed limited explanatory power due to the non-linear relationships in the data.

### Random Forest (Advanced)

A Random Forest model with log-transformed target variable was trained, achieving improved performance.

* **Key Metrics:**

    * MAE: 169.4

    * R²: 0.2424

---

## Feature Importance <a name="feature-importance"></a>

The Random Forest model identified the following as the most important features:

* `reviews`

* `price`

* `review_intensity`

* `stars`

* `isBestSeller`

---

## Discussion & Next Steps <a name="discussion--next-steps"></a>

Product metadata can provide some predictive power for sales.  Review-related features are particularly important.

Next steps could include:

* Expanding the dataset with more features.

* Exploring other non-linear models.

* Analyzing the impact of seasonality.

---

## Conclusion <a name="conclusion"></a>

This project explores the relationship between Amazon UK product features and monthly sales volume. The analysis provides insights into the factors that influence sales, highlighting the importance of reviews, price, and bestseller status.

---

## Reflection <a name="reflection"></a>

This project improved my skills in data analysis, feature engineering, and machine learning.  Key challenges included dealing with skewed data and selecting appropriate models.
