import pandas as pd
from pathlib import Path

RAW_FILE = Path("data/raw/online_retail_II.xlsx")
CLEAN_FILE = Path("data/cleaned/transactions_clean.csv")
CANCEL_FILE = Path("data/cleaned/cancellations.csv")
ANOMALY_FILE = Path("data/cleaned/anomalies_non_sales.csv")

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "Invoice": "invoice_no",
        "StockCode": "stock_code",
        "Description": "description",
        "Quantity": "quantity",
        "InvoiceDate": "invoice_date",
        "Price": "unit_price",
        "Customer ID": "customer_id",
        "CustomerID": "customer_id",
        "Country": "country",
    }
    df = df.rename(columns=rename_map)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

def main():
    if not RAW_FILE.exists():
        raise FileNotFoundError(f"Fichier introuvable : {RAW_FILE}")

    sheets = pd.read_excel(RAW_FILE, sheet_name=None)

    frames = []
    for sheet_name, frame in sheets.items():
        frame["source_sheet"] = sheet_name
        frames.append(frame)

    df = pd.concat(frames, ignore_index=True)
    df = standardize_columns(df)

    # Suppression des doublons exacts
    df = df.drop_duplicates().copy()

    # Types
    if "invoice_date" in df.columns:
        df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")

    for col in ["quantity", "unit_price", "customer_id"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Flags qualité
    df["is_cancellation"] = df["invoice_no"].astype(str).str.startswith("C", na=False)
    df["missing_description"] = df["description"].isna()
    df["missing_customer_id"] = df["customer_id"].isna()
    df["invalid_quantity"] = df["quantity"] <= 0
    df["invalid_unit_price"] = df["unit_price"] <= 0

    # Valeur de ligne
    df["line_revenue"] = df["quantity"] * df["unit_price"]

    # Colonnes temporelles
    df["invoice_year"] = df["invoice_date"].dt.year
    df["invoice_month"] = df["invoice_date"].dt.month
    df["invoice_year_month"] = df["invoice_date"].dt.to_period("M").astype(str)

    # Sous-ensembles
    cancellations = df[df["is_cancellation"]].copy()

    anomalies_non_sales = df[
        (~df["is_cancellation"]) &
        (
            df["invalid_quantity"] |
            df["invalid_unit_price"] |
            df["missing_description"]
        )
    ].copy()

    transactions_clean = df[
        (~df["is_cancellation"]) &
        (~df["invalid_quantity"]) &
        (~df["invalid_unit_price"]) &
        (~df["missing_description"])
    ].copy()

    # Exports
    CLEAN_FILE.parent.mkdir(parents=True, exist_ok=True)
    transactions_clean.to_csv(CLEAN_FILE, index=False)
    cancellations.to_csv(CANCEL_FILE, index=False)
    anomalies_non_sales.to_csv(ANOMALY_FILE, index=False)

    print(f"Transactions propres exportées vers : {CLEAN_FILE}")
    print(f"Annulations exportées vers : {CANCEL_FILE}")
    print(f"Anomalies non sales exportées vers : {ANOMALY_FILE}")
    print(f"Shape transactions_clean : {transactions_clean.shape}")
    print(f"Shape cancellations : {cancellations.shape}")
    print(f"Shape anomalies_non_sales : {anomalies_non_sales.shape}")

if __name__ == "__main__":
    main()