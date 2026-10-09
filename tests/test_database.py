from pathlib import Path
import sqlite3


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DB_PATH = (
    PROJECT_ROOT
    / "data"
    / "retail_sales.db"
)


def test_database_exists():
    assert DB_PATH.exists()


def test_sales_table_exists():
    with sqlite3.connect(DB_PATH) as connection:
        result = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name = 'sales'
            """
        ).fetchone()

    assert result is not None


def test_sales_table_has_rows():
    with sqlite3.connect(DB_PATH) as connection:
        count = connection.execute(
            """
            SELECT COUNT(*)
            FROM sales
            """
        ).fetchone()[0]

    assert count > 0