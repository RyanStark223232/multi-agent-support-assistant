import sqlite3
from pathlib import Path
import pytest

# Path helpers
BASE_DIR = Path(__file__).resolve().parents[1] / "app"
DB_PATH = BASE_DIR / "support.db"
INIT_DB_SCRIPT = BASE_DIR / "db" / "init_db.py"


@pytest.fixture(scope="module", autouse=True)
def run_init_db():
    """
    Automatically run init_db.py before tests.
    Ensures a fresh database for each test session.
    """
    import runpy
    runpy.run_path(str(INIT_DB_SCRIPT))
    yield


def test_database_file_created():
    assert DB_PATH.exists(), "support.db should be created by init_db.py"


def test_tables_exist():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cursor.fetchall()}

    assert "customers" in tables, "customers table should exist"
    assert "tickets" in tables, "tickets table should exist"

    conn.close()


def test_customers_data_loaded():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM customers")
    count = cursor.fetchone()[0]

    assert count > 0, "customers table should contain rows from CSV"

    conn.close()


def test_tickets_data_loaded():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tickets")
    count = cursor.fetchone()[0]

    assert count > 0, "tickets table should contain rows from CSV"

    conn.close()


def test_foreign_key_relationship():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT tickets.customer_id
        FROM tickets
        LEFT JOIN customers ON tickets.customer_id = customers.id
        WHERE customers.id IS NULL
    """)

    missing_fk = cursor.fetchall()

    assert len(missing_fk) == 0, "All tickets.customer_id values should reference valid customers.id"

    conn.close()