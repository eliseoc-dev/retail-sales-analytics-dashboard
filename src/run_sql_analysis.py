from pathlib import Path
import sqlite3


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DB_PATH = (
    PROJECT_ROOT
    / "data"
    / "retail_sales.db"
)


QUERIES = {
    "Business KPIs": """
        SELECT
            COUNT(*) AS total_orders,
            ROUND(SUM(net_sales), 2) AS total_revenue,
            ROUND(AVG(net_sales), 2) AS average_order_value,
            SUM(quantity) AS total_units
        FROM sales;
    """,

    "Revenue by country": """
        SELECT
            country,
            ROUND(SUM(net_sales), 2) AS revenue
        FROM sales
        GROUP BY country
        ORDER BY revenue DESC;
    """,

    "Top products": """
        SELECT
            product,
            SUM(quantity) AS units_sold,
            ROUND(SUM(net_sales), 2) AS revenue
        FROM sales
        GROUP BY product
        ORDER BY revenue DESC
        LIMIT 10;
    """,

    "Return rate": """
        SELECT
            ROUND(
                100.0 *
                SUM(
                    CASE
                        WHEN returned = 'Yes'
                        THEN 1
                        ELSE 0
                    END
                )
                / COUNT(*),
                2
            ) AS return_rate_percent
        FROM sales;
    """,
}


def run_analysis() -> None:
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        for title, query in QUERIES.items():
            print()
            print("=" * 60)
            print(title.upper())
            print("=" * 60)

            cursor.execute(query)

            columns = [
                description[0]
                for description
                in cursor.description
            ]

            rows = cursor.fetchall()

            print(columns)

            for row in rows:
                print(row)


if __name__ == "__main__":
    run_analysis()