# Amazon Sales & Reviews Analysis

> Turning 2.2 million Amazon UK listings into actionable e-commerce insights.

🔗 **Live report & portfolio**: [View on GitHub Pages](https://rolando-villca.github.io/Rolando-Villca-DSPP/)

## 📋 Project Overview

This project explores how structured product metadata (price, star ratings, review counts, bestseller status and category) can be used to predict **monthly units sold** on Amazon UK. Through exploratory data analysis, feature engineering, and regression models, we identify the key drivers of sales volume and provide sellers with strategic recommendations.

## 🚀 Key Highlights

- **Dataset:** 2 222 742 UK product listings  
- **Models compared:**  
  - Linear Regression (baseline)  
  - Random Forest  
  - Random Forest on log-transformed target  
- **Top performance:** RF + log target → MAE 169.4 | RMSE 559.7 | R² 0.242  
- **Top predictors:**  
  1. **Review intensity** (reviews per £)  
  2. **Total reviews**  
  3. **Price**  

## 📈 What You’ll Find

- **Interactive notebook** with all code and visualisations  
- **Cleaned & engineered dataset** (161 315 active listings)  
- **EDA visuals:** histograms, scatter & hexbin plots, correlation heatmap  
- **Model evaluation:** performance tables & actual vs. predicted plots  
- **Feature importance analysis** & business implications  
- **Discussion & next steps** for further improvement  
- **Reflection** on lessons learned and future skill development  

## 🛠️ Tech Stack

- **Data manipulation:** Python, pandas  
- **Visualisation:** Matplotlib, seaborn  
- **Modelling:** scikit-learn  
- **Documentation & hosting:** Jupyter Notebook, GitHub Pages (Jekyll)  

## 🚀 Getting Started

1. **Clone this repo:**  
   ```bash
   git clone https://github.com/Rolando-Villca/Rolando-Villca-DSPP.git
   ```
2. **Open the index page** in your browser:  
   https://rolando-villca.github.io/Rolando-Villca-DSPP/
3. **View or run** the Jupyter notebook:  
   ```bash
   cd Rolando-Villca-DSPP
   jupyter notebook analysis_notebook.ipynb
   ```
4. **Inspect the code, rerun cells,** and review exported assets under `assets/`.

---

_For detailed methodology, results, and full discussion, see the [live index page](https://rolando-villca.github.io/Rolando-Villca-DSPP/)
