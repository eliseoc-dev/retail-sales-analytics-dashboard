import pandas as pd


DATA_PATH = "data/raw/retail_sales_raw.csv"


df = pd.read_csv(DATA_PATH)


print("=" * 60)
print("DATASET OVERVIEW")
print("=" * 60)

print()
print("Shape:")
print(df.shape)


print()
print("Columns:")
print(df.columns.tolist())


print()
print("Data types:")
print(df.dtypes)


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
print("Duplicate rows:")
print(
    df.duplicated().sum()
)


print()
print("Numerical summary:")
print(
    df.describe()
)