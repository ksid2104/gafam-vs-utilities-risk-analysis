# 📊 Sector Analysis: GAFAM vs Utilities – Performance & Risk

This project aims to compare two sectors – Big Tech (GAFAM) and Utilities – through a quantitative approach.

> 🎯 Objectives :
> - Download **market data** using yfinance and manipulate it (pandas, numpy)
> - Calculate **statistical indicators**: return, volatility, skewness, kurtosis, Value at Risk (VaR)
> - Compare sectors using **visualizations** (matplotlib) and **statistical tools** (scipy.stats) relevant to financial markets

---

## 📁 Repository Content

- `gafam-vs-utilities-risk-analysis.py`  
  → Detailed and documented Python script, structured in pedagogical steps:
  - Data download
  - Analysis of main statistical indicators (mean, std, skewness, and kurtosis)
  - VaR calculation (historical vs normal)
  - Confidence intervals
  - Professional-grade visualizations using matplotlib


- `gafam-vs-utilities-risk-analysis_app.py`  
  → **Interactive** version of the project using **Streamlit**, allowing for a more dynamic exploration.
  > ℹ️ *Personal note 1* : I am still discovering Streamlit, and this interface was co-designed with the help of an AI to structure the user experience. The focus is on the analysis, not the technical design of the app.



## 🔍 Methodology & Indicators

| Metric        | Description                                                                 |
|-----------------|-------------------------------------------------------------------------------|
| `Mean`          | Average log return per stock / per sector                        |
| `Standard Deviation` | Daily volatility                                                    |
| `Skewness`      | Measure of distribution asymmetry                                      |
| `Kurtosis`      | Measure of flatness / tail thickness                                        |
| `VaR`           | Value at Risk at 95% and 99% – using **normal distribution** and **historical** methods            |
| `Confidence Interval` | Probable range of the mean with 95% certainty                      |

---

## 📈 Integrated Visualizations

- Histograms + Normal PDF
- Cumulative Distribution Functions (CDF) + VaR lines (historical and normal)
- Direct comparison between the two sectors (GAFAM vs Utilities)
---
## ▶️ Running the Streamlit App

```bash
streamlit run risk_app.py

---
## What This Project Says About Me: 
This project is more than just a technical exercise: it reflects my ability to apply data skills to real-world financial problems. Here’s what it will tell you about me:

🎯 Structured analytical mindset: each step in the code is designed as a rigorous, reproducible, and interpretable analysis process.

📊 Solid understanding of financial risk: strong command of key indicators (volatility, VaR, return distribution), relevant for risk-sensitive sectors.

🧠 Autonomy & curiosity: I developed this project independently, consolidating my knowledge in quantitative finance and Python through external resources.

💡 Ability to communicate technical results clearly: visualizations and comments are decision-oriented, as expected in a company or consulting environment.

⚙️ Willingness to upskill quickly: although I’m new to Streamlit, I managed to build an interactive app by leveraging AI intelligently, showcasing adaptability.

📌 If you're looking for a hybrid finance-data profile with an entrepreneurial mindset: this project is a good reflection of it.

