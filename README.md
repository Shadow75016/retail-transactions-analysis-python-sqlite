# Retail Transactions Analysis with Python and SQLite

## Overview
This project focuses on building a complete data preparation and analysis pipeline from the **Online Retail II** dataset.

The goal is not only to run SQL queries on a raw file, but to:
- audit data quality issues
- define consistent cleaning rules
- separate valid sales from cancellations and anomalies
- load the cleaned data into SQLite
- extract business insights through SQL analysis

This project was designed to demonstrate practical skills in:
- **data cleaning with Python**
- **data manipulation with pandas**
- **database loading with SQLite**
- **SQL analysis**
- **documentation of cleaning and analysis choices**

---

## Project Objectives
The main objectives of this project were:

- import and merge the two Excel sheets of the original dataset
- identify the main data quality issues
- clean and standardize the data
- build a reliable table of valid transactions
- separate cancellations from non-sales anomalies
- load the cleaned outputs into a SQLite database
- answer business questions using SQL queries

---

## Dataset
The project uses the **Online Retail II** dataset, provided as an Excel file with two sheets:

- `Year 2009-2010`
- `Year 2010-2011`

### Main columns used
- `Invoice`
- `StockCode`
- `Description`
- `Quantity`
- `InvoiceDate`
- `Price`
- `Customer ID`
- `Country`

This dataset is interesting because it is **large enough to be realistic** and contains **several quality issues** that require actual cleaning decisions rather than simple formatting.

---

## Tools Used
- **Python**
- **pandas**
- **SQLite**
- **SQL**
- **Excel**

---

## Project Structure
```text
Retail Transactions Analysis with Python and SQLite/
├── data/
│   ├── raw/
│   │   └── online_retail_II.xlsx
│   └── cleaned/
│       ├── transactions_clean.csv
│       ├── cancellations.csv
│       └── anomalies_non_sales.csv
│
├── scripts/
│   ├── audit_data.py
│   ├── clean_data.py
│   ├── load_to_sqlite.py
│   ├── run_queries.py
│   └── analysis_queries.sql
│
├── database/
│   └── online_retail_analysis.db
│
└── README.md