from pathlib import Path

import pandas as pd


RAW_DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "raw"
    / "retail_sales_raw.csv"
)

PROCESSED_DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "processed"
    / "retail_sales_clean.csv"
)


def clean_sales_data() -> pd.DataFrame:
    df = pd.read_csv(RAW_DATA_PATH)

    print("=" * 60)
    print("DATA CLEANING")
    print("=" * 60)

    print(f"Initial rows: {len(df):,}")

    # Remove exact duplicates
    duplicate_count = df.duplicated().sum()

    print(f"Duplicate rows found: {duplicate_count}")

    df = df.drop_duplicates().copy()

    # Clean text columns
    text_columns = [
        "country",
        "city",
        "category",
        "product",
        "payment_method",
        "sales_channel",
        "returned",
    ]

    for column in text_columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    # Normalize categories
    df["category"] = (
        df["category"]
        .str.title()
    )

    # Normalize returned values
    df["returned"] = (
        df["returned"]
        .str.title()
    )

    # Fill missing payment methods
    df["payment_method"] = (
        df["payment_method"]
        .fillna("Unknown")
    )

    # Convert dates
    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce",
    )

    # Numeric conversion
    numeric_columns = [
        "quantity",
        "unit_price",
        "discount",
        "customer_rating",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    # Remove impossible/invalid rows
    df = df[
        (df["quantity"] > 0)
        & (df["unit_price"] > 0)
        & (df["discount"] >= 0)
        & (df["discount"] <= 1)
    ].copy()

    # Business metrics
    df["gross_sales"] = (
        df["quantity"]
        * df["unit_price"]
    )

    df["discount_amount"] = (
        df["gross_sales"]
        * df["discount"]
    )

    df["net_sales"] = (
        df["gross_sales"]
        - df["discount_amount"]
    )

    # Time dimensions
    df["year"] = (
        df["order_date"]
        .dt.year
    )

    df["month"] = (
        df["order_date"]
        .dt.month
    )

    df["month_name"] = (
        df["order_date"]
        .dt.month_name()
    )

    df["year_month"] = (
        df["order_date"]
        .dt.to_period("M")
        .astype(str)
    )

    # Round monetary columns
    money_columns = [
        "unit_price",
        "gross_sales",
        "discount_amount",
        "net_sales",
    ]

    df[money_columns] = (
        df[money_columns]
        .round(2)
    )

    # Sort chronologically
    df = df.sort_values(
        by=[
            "order_date",
            "order_id",
        ]
    ).reset_index(drop=True)

    print(f"Final rows: {len(df):,}")

    print()
    print("Missing values after cleaning:")
    print(df.isna().sum())

    PROCESSED_DATA_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        PROCESSED_DATA_PATH,
        index=False,
    )

    print()
    print(
        f"Clean dataset saved to: "
        f"{PROCESSED_DATA_PATH}"
    )

    return df


if __name__ == "__main__":
    clean_sales_data()