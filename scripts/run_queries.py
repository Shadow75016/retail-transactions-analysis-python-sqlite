import sqlite3
from pathlib import Path

DB_FILE = Path("database/online_retail_analysis.db")
SQL_FILE = Path("scripts/analysis_queries.sql")

def main():
    if not DB_FILE.exists():
        raise FileNotFoundError(f"Base introuvable : {DB_FILE}")
    if not SQL_FILE.exists():
        raise FileNotFoundError(f"Fichier SQL introuvable : {SQL_FILE}")

    sql_text = SQL_FILE.read_text(encoding="utf-8")
    queries = [q.strip() for q in sql_text.split(";") if q.strip()]

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        for i, query in enumerate(queries, start=1):
            print(f"\n=== REQUÊTE {i} ===")
            print(query)
            print("\n--- RÉSULTAT ---")

            cursor.execute(query)
            rows = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description] if cursor.description else []

            if col_names:
                print(" | ".join(col_names))
                print("-" * 80)

            for row in rows:
                print(" | ".join(str(x) for x in row))

if __name__ == "__main__":
    main()