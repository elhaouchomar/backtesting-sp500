# Backtesting S&P 500 – Momentum Strategy

## 📌 Overview

This project implements a quantitative **momentum-based stock-picking strategy** using historical S&P 500 constituent data. As a quantitative analyst at a hedge fund, you will:

- Clean and preprocess messy financial time series
- Optimize memory usage for large datasets
- Develop a stock selection signal based on 1-year average returns
- Backtest the strategy against the S&P 500 benchmark
- Generate performance reports and visualizations

The goal is to **outperform the market** using a simple yet robust momentum strategy.

---

## 👥 Group Setup

- **Team size**: 1–3 members
- All code must be collaboratively developed and submitted via Git
- Repository: `https://learn.zone01oujda.ma/git/oelhaouc/backtesting-sp500`

---
## 📂 Project Structure
```
backtesting-sp500/
│
├── README.md
├── requirements.txt
│
├── data/
│ ├── sp500.csv
│ └── stock_prices.csv
│
├── notebook/
│ └── analysis.ipynb
│
├── scripts/
│ ├── memory_reducer.py
│ ├── preprocessing.py
│ ├── create_signal.py
│ ├── backtester.py
│ └── main.py
│
└── results/
├── plots/
│ ├── avg_price_over_time.png
│ └── cumulative_performance.png
├── results.txt
└── outliers.txt
```


---

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://learn.zone01oujda.ma/git/oelhaouc/backtesting-sp500.git
cd backtesting-sp500
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
### Run the full pipeline
```bash
python3 scripts/main.py
```
This will execute:

- Memory optimization of input data
- Data preprocessing and EDA
- Signal generation
- Backtesting against S&P 500
- Saving results and plots

## Data Description

| File               | Description                                                      |
|--------------------|------------------------------------------------------------------|
| sp500.csv          | S&P 500 index historical data (adjusted close)                   |
| stock_prices.csv   | Monthly close prices for all current/past S&P 500 constituents   |

 **Note:** The dataset contains intentional issues:

 - Missing values  
 - Price spikes and errors  
 - Stock splits and dividend adjustments  
 - Changing S&P 500 composition over time  

##  Strategy Logic

### 🔹 Signal Construction

- Compute monthly past returns for each company  
- Calculate average return over the previous 12 months (1-year momentum)  
- Select top 20 companies by average return each month  
- Signal = `True` for selected stocks, `False` otherwise  

###  Benchmark

- S&P 500 index  
- Fixed monthly investment of $20 (equal to the number of selected stocks)  

---

##  Performance Metrics

The backtest computes:

- **Profit & Loss (PnL)** = Signal × Future Returns  
- **Strategy Return** = PnL / Number of selected stocks (20)  
- **Cumulative PnL** over the entire backtest period  
- Comparison chart vs. S&P 500 benchmark  

## ⚙️ Module Specifications

### 1. 📦 `memory_reducer.py`

```python
def optimize_memory(df: pd.DataFrame) -> pd.DataFrame
```
- Downcasts numeric columns to smallest possible dtype (`float32` minimum for floats)

- Ensures:
  - `stock_prices.csv` < 8MB  
  - `sp500.csv` < 0.15MB  

---

## 🧹 preprocessing.py + 📓 analysis.ipynb

- Missing values analysis  
- Outlier detection (IQR and Z-score methods)  
- Price outlier filtering: `0.1 < price < 10,000`  
- Monthly resampling (last value of month)  
- Monthly return calculation (historical & future)  
- Return outlier capping (`-0.5` to `1.0`, except 2008–2009)  
- Forward fill of missing values per company  

## 📋 EDA Requirements (`analysis.ipynb`)

The notebook must include:

- Missing values analysis – per variable and per year  
- Outliers analysis – using IQR or Z-score  

- Plot:
  - Average price over time **OR**
  - Price consistency across companies  

- 5 outliers identified – including:
  - Ticker  
  - Date  
  - Price  
  - External source verification (e.g., stock splits, earnings events)  

- Outliers saved to `results/outliers.txt`  

---

## 📊 Plot Requirements

All plots must:

- Be saved in `results/plots/`  
- Accept a `plot=False` parameter (no display by default)  
- Contain titles and axis labels  

## ⚠️ Important Notes

- The data is intentionally imperfect – your preprocessing should handle major issues without overfitting  
- 2008–2009 financial crisis returns are **exempt** from outlier capping  
- Use **vectorized operations** (no loops) for backtesting  
- Do **not** introduce look-ahead bias (future returns must be computed separately)  
- The final PnL should be reasonable (< $75) – if higher, outliers remain  