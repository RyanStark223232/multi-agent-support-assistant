import sqlite3
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "support.db"
SCHEMA_PATH = BASE_DIR / "db" / "schema.sql"

def load_csv_to_table(cursor, csv_path, table_name, columns):
    """Generic CSV → SQL loader."""
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [tuple(row[col] for col in columns) for row in reader]

    placeholders = ",".join(["?"] * len(columns))
    cursor.executemany(
        f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})",
        rows,
    )

def main():
    # Remove old DB if it exists
    if DB_PATH.exists():
        DB_PATH.unlink()

    # Connect to SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Apply schema
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    # Load customers
    customers_csv = DATA_DIR / "customers.csv"
    load_csv_to_table(
        cursor,
        customers_csv,
        "customers",
        ["id", "name", "email", "segment", "created_at"],
    )

    # Load tickets
    tickets_csv = DATA_DIR / "tickets.csv"
    load_csv_to_table(
        cursor,
        tickets_csv,
        "tickets",
        ["id", "customer_id", "subject", "description", "status", "created_at", "resolved_at"],
    )

    conn.commit()
    conn.close()
    print(f"Database initialized at: {DB_PATH}")

if __name__ == "__main__":
    main()