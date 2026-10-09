import pandas as pd


DATA_PATH = (
    "data/processed/"
    "retail_sales_clean.csv"
)


df = pd.read_csv(DATA_PATH)


print("=" * 60)
print("DATA QUALITY REPORT")
print("=" * 60)

print()
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")

print()
print("Duplicate rows:")
print(df.duplicated().sum())

print()
print("Missing values:")
print(
    df.isna()
    .sum()
    .sort_values(
        ascending=False
    )
)

print()
print("Categories:")
print(
    df["category"]
    .value_counts()
)

print()
print("Countries:")
print(
    df["country"]
    .value_counts()
)

print()
print("Date range:")
print(
    df["order_date"].min(),
    "→",
    df["order_date"].max(),
)