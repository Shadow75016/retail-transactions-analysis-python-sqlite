import sqlite3
import pandas as pd
from pathlib import Path

CLEAN_FILE = Path("data/cleaned/transactions_clean.csv")
CANCEL_FILE = Path("data/cleaned/cancellations.csv")
ANOMALY_FILE = Path("data/cleaned/anomalies_non_sales.csv")
DB_FILE = Path("database/online_retail_analysis.db")

def main():
    if not CLEAN_FILE.exists():
        raise FileNotFoundError(f"Fichier introuvable : {CLEAN_FILE}")

    DB_FILE.parent.mkdir(parents=True, exist_ok=True)

    csv_dtypes = {
    "invoice_no": "string",
    "stock_code": "string",
    "description": "string",
    "customer_id": "string",
    "country": "string",
    "source_sheet": "string",
    "invoice_year_month": "string",}

    transactions = pd.read_csv(CLEAN_FILE, dtype=csv_dtypes, low_memory=False)
    cancellations = pd.read_csv(CANCEL_FILE, dtype=csv_dtypes, low_memory=False) if CANCEL_FILE.exists() else pd.DataFrame()
    anomalies = pd.read_csv(ANOMALY_FILE, dtype=csv_dtypes, low_memory=False) if ANOMALY_FILE.exists() else pd.DataFrame()

    with sqlite3.connect(DB_FILE) as conn:
        transactions.to_sql("transactions_clean", conn, if_exists="replace", index=False)

        if not cancellations.empty:
            cancellations.to_sql("cancellations", conn, if_exists="replace", index=False)

        if not anomalies.empty:
            anomalies.to_sql("anomalies_non_sales", conn, if_exists="replace", index=False)

        conn.execute("""
        CREATE VIEW IF NOT EXISTS monthly_sales AS
        SELECT
            invoice_year_month,
            SUM(line_revenue) AS total_revenue
        FROM transactions_clean
        GROUP BY invoice_year_month
        ORDER BY invoice_year_month;
        """)

    print(f"Base SQLite créée : {DB_FILE}")
    print(f"Table transactions_clean : {len(transactions)} lignes")
    print(f"Table cancellations : {len(cancellations)} lignes")
    print(f"Table anomalies_non_sales : {len(anomalies)} lignes")

if __name__ == "__main__":
    main()