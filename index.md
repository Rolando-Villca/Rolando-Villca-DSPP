---
layout: default
title: "Amazon Sales & Reviews Analysis"
permalink: /Rolando-Villca-DSPP/
---
title: “Rolando Villca – Data Science Portfolio”
---

# Rolando Villca  
**Data Science Apprentice**  
_Python · pandas · scikit-learn · Jupyter · GitHub Pages_

---

## 🚀 Amazon Sales & Reviews Analysis
<div class="project-card">
  <img src="/assets/amazon-hexbin.png" alt="Hexbin: Price vs Sales" />
  <div class="project-summary">
    <p><strong>Dataset:</strong> 2.22 M UK listings</p>
    <p><strong>Tools:</strong> Python · pandas · scikit-learn · Jupyter</p>
    <p><strong>Model:</strong> Random Forest on log-scaled target</p>
    <p><strong>Performance:</strong> MAE 169 · R² 0.24</p>
    <a class="button primary" href="#data-description">Jump to Data Description</a>
  </div>
</div>

**Predicting monthly units sold on Amazon UK from product metadata**  
2.22 million listings · Random Forest on log-scaled target · MAE 169 · R² 0.24

<div style="display: flex; gap: 1rem; align-items: flex-start; margin: 1rem 0;">
  <!-- 1. Thumbnail you export from your notebook -->
  <img src="/assets/amazon-hexbin.png" alt="Hexbin: Price vs Sales" width="140" style="border-radius:8px;"/>
  <div>
    **Key Steps**  
    1. **Clean & Engineer**: dropped zero-sales, built `review_intensity`.  
    2. **EDA**: distribution & hexbin plots, correlation heatmap.  
    3. **Model**: Linear vs Random Forest vs RF+log target.  

    **Top Metrics**  
    - **MAE**: 169.4  
    - **R²**: 0.242  

    <a href="https://rolando-villca.github.io/Rolando-Villca-DSPP/" 
       style="display:inline-block;margin-top:0.5rem;padding:0.4rem 0.8rem;
              background:#0366d6;color:white;border-radius:4px;text-decoration:none;">
      🔎 View Full Analysis
    </a>  
    <a href="https://github.com/Rolando-Villca/Rolando-Villca-DSPP" 
       style="margin-left:0.5rem;">🐙 Source on GitHub</a>
  </div>
</div>

---

## 📓 Notebook Snippet

```python
# Feature engineering: reviews per pound
df_clean['review_intensity'] = df_clean['reviews'] / (df_clean['price'] + 1)

# Quick corr heatmap
import seaborn as sns
sns.heatmap(
    df_clean[['review_intensity','reviews','price','stars']].corr(),
    annot=True, cmap='coolwarm'
)
