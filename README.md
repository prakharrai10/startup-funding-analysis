# Startup Funding Analysis (Pandas + Streamlit)

A case study on Indian startup funding data. The raw CSV is cleaned with pandas
and explored through an interactive Streamlit dashboard.

**Live app:** https://prakharrai10-startup-funding-analysis-app-xcuup8.streamlit.app/

## Features
- **Overall Analysis:** total, max and average funding, number of funded startups, and a month-on-month trend (total or count)
- **StartUp view:** industry, city, funding rounds, funding over time, and similar startups
- **Investor view:** recent investments, biggest investments, a sector pie chart, and a year-on-year investment graph

## Data cleaning (`clean_data.py`)
1. Dropped the `Remarks` column
2. Set `Sr No` as the index (`sno`)
3. Renamed columns to `date, startup, vertical, subvertical, city, investors, round, amount`
4. Converted amount from USD to INR crores (assumed rate: 1 USD = 83 INR)
5. Dropped rows with missing values

I also fixed messy amounts (`undisclosed`, stray characters), malformed dates, and stray quotes in investor names.

## Project structure
```
.
├── app.py                 # Streamlit dashboard
├── clean_data.py          # data cleaning script
├── startup_funding.csv    # raw data
├── startup_cleaned.csv    # cleaned data
├── requirements.txt
└── README.md
```

## Run locally
```bash
pip install -r requirements.txt
python clean_data.py        # optional: regenerates startup_cleaned.csv
streamlit run app.py
```

## Tech stack
Python, pandas, matplotlib, Streamlit

## What I learned
- Cleaning real-world data: inconsistent formats, missing values and bad dates
- Grouping and aggregating with pandas (`groupby`, `agg`, `nunique`)
- Building an interactive multi-page dashboard with Streamlit
- Using Git and GitHub to publish a project