from pathlib import Path
import sqlite3

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "retail_sales_clean.csv"
)

DB_PATH = (
    PROJECT_ROOT
    / "data"
    / "retail_sales.db"
)


def load_data_to_sqlite() -> None:
    df = pd.read_csv(CSV_PATH)

    with sqlite3.connect(DB_PATH) as connection:
        df.to_sql(
            "sales",
            connection,
            if_exists="replace",
            index=False,
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_sales_order_date
            ON sales(order_date)
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_sales_category
            ON sales(category)
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_sales_country
            ON sales(country)
            """
        )

        connection.commit()

    print("=" * 60)
    print("DATA LOADED INTO SQLITE")
    print("=" * 60)
    print(f"Rows loaded: {len(df):,}")
    print(f"Database: {DB_PATH}")


if __name__ == "__main__":
    load_data_to_sqlite()