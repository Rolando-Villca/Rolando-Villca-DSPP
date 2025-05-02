# Amazon Sales & Reviews Analysis  
[![Notebook](https://img.shields.io/badge/notebook-%F0%9F%9B%96-blue)](./analysis_notebook.ipynb) [![Report](https://img.shields.io/badge/report-pdf-red)](./report.md) [![License](https://img.shields.io/badge/license-MIT-green)]

## Overview
A data-driven deep dive into Amazon product performance and customer sentiment. Leveraging sales figures, review text, and pricing data to uncover actionable insights.

## Table of Contents
1. [Key Findings](#key-findings)  
2. [Data Description](#data-description)  
3. [Methodology](#methodology)  
4. [Results & Visualizations](#results--visualizations)  
5. [Usage](#usage)  
6. [License](#license)

## Key Findings
- **Demand & Pricing Trends**: Detected seasonal spikes in X category.  
- **Sentiment Analysis**: 75% of reviews are positive; spikes in negative sentiment correlate with price hikes.  
- **Sales vs. Rating**: Products with ≥4.5⭐ averages sell 30% more units.

## Data Description
- **Sales dataset**: daily units sold, revenue, price  
- **Reviews dataset**: review text, star rating, timestamp  
*(see `data/` folder for CSVs and schema)*

## Methodology
1. **Data Cleaning & ETL** (Pandas)  
2. **Exploratory Analysis** (Matplotlib & Seaborn)  
3. **Sentiment Scoring** (NLTK/VADER)  
4. **Correlation Analysis** (SciPy)

## Results & Visualizations
![Sales Over Time](./images/sales_trend.png)  
*Figure 1: Monthly revenue trend.*

![Sentiment Distribution](./images/sentiment_dist.png)  
*Figure 2: Review sentiment breakdown.*

## Usage
```bash
git clone https://github.com/Rolando-Villca/Rolando-Villca-DSPP.git
cd Rolando-Villca-DSPP
pip install -r requirements.txt
jupyter notebook analysis_notebook.ipynb

