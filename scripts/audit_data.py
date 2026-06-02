import pandas as pd
from pathlib import Path

RAW_FILE = Path("data/raw/online_retail_II.xlsx")

def main():
    if not RAW_FILE.exists():
        raise FileNotFoundError(f"Fichier introuvable : {RAW_FILE}")

    # Adapter sheet_name si nécessaire après ouverture du fichier
    sheets = pd.read_excel(RAW_FILE, sheet_name=None)

    frames = []
    for sheet_name, frame in sheets.items():
        frame["source_sheet"] = sheet_name
        frames.append(frame)

    df = pd.concat(frames, ignore_index=True)

    print("\n=== APERÇU ===")
    print(df.head())

    print("\n=== SHAPE ===")
    print(df.shape)

    print("\n=== TYPES ===")
    print(df.dtypes)

    print("\n=== VALEURS MANQUANTES ===")
    print(df.isna().sum().sort_values(ascending=False))

    print("\n=== DOUBLONS EXACTS ===")
    print(df.duplicated().sum())

    if "Invoice" in df.columns:
        cancel_mask = df["Invoice"].astype(str).str.startswith("C", na=False)
        print("\n=== ANNULATIONS (Invoice commence par C) ===")
        print(cancel_mask.sum())

    for col in ["Quantity", "Price"]:
        if col in df.columns:
            print(f"\n=== STATS {col.upper()} ===")
            print(df[col].describe())

    cancel_mask = df["Invoice"].astype(str).str.startswith("C", na=False)

    print("\n=== CUSTOMER ID MANQUANT (%) ===")
    print(round(df["Customer ID"].isna().mean() * 100, 2))

    print("\n=== QUANTITY <= 0 ===")
    print((df["Quantity"] <= 0).sum())

    print("\n=== PRICE <= 0 ===")
    print((df["Price"] <= 0).sum())

    print("\n=== QUANTITY <= 0 ET ANNULATION ? ===")
    print(pd.crosstab(cancel_mask, df["Quantity"] <= 0, rownames=["is_cancellation"], colnames=["quantity_le_0"]))

    print("\n=== PRICE <= 0 ET ANNULATION ? ===")
    print(pd.crosstab(cancel_mask, df["Price"] <= 0, rownames=["is_cancellation"], colnames=["price_le_0"]))

    print("\n=== EXEMPLES PRICE <= 0 HORS ANNULATIONS ===")
    print(df[(df["Price"] <= 0) & (~cancel_mask)].head(10))

    print("\n=== EXEMPLES QUANTITY <= 0 HORS ANNULATIONS ===")
    print(df[(df["Quantity"] <= 0) & (~cancel_mask)].head(10))
    
if __name__ == "__main__":
    main()
