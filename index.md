---
layout: default
title: "Amazon Sales & Reviews Analysis"
permalink: /Rolando-Villca-DSPP/
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

Your narrative here: explain the 2.22 million rows, the 10 columns, zero-value filtering (18 price errors, ~2.06 M zero-sales), and the 161,315 active listings. You can present a markdown table of column names and definitions.

---

## Exploratory Data Analysis  
<a name="exploratory-data-analysis"></a>

Embed your histograms and hexbin plots:

```markdown
![Price Distribution](/assets/price-histogram.png)
![Sales Distribution](/assets/sales-histogram.png)
![Price vs Sales (hexbin)](/assets/amazon-hexbin.png)
