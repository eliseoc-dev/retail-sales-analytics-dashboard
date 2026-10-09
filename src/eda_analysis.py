import pandas as pd


DATA_PATH = (
    "data/processed/"
    "retail_sales_clean.csv"
)


df = pd.read_csv(DATA_PATH)


print("=" * 60)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 60)


print()
print("TOP 5 COUNTRIES BY REVENUE")

country_revenue = (
    df.groupby("country")["net_sales"]
    .sum()
    .sort_values(ascending=False)
    .head()
)

print(country_revenue)


print()
print("TOP 5 PRODUCTS BY REVENUE")

product_revenue = (
    df.groupby("product")["net_sales"]
    .sum()
    .sort_values(ascending=False)
    .head()
)

print(product_revenue)


print()
print("TOP CATEGORIES")

category_revenue = (
    df.groupby("category")["net_sales"]
    .sum()
    .sort_values(ascending=False)
)

print(category_revenue)


print()
print("BEST SALES CHANNEL")

channel_revenue = (
    df.groupby("sales_channel")["net_sales"]
    .sum()
    .sort_values(ascending=False)
)

print(channel_revenue)


print()
print("RETURN RATE BY CATEGORY")

return_rate_by_category = (
    df.assign(
        returned_flag=(
            df["returned"] == "Yes"
        ).astype(int)
    )
    .groupby("category")["returned_flag"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)

print(
    return_rate_by_category.round(2)
)


print()
print("AVERAGE RATING BY CATEGORY")

rating_by_category = (
    df.groupby("category")[
        "customer_rating"
    ]
    .mean()
    .sort_values(ascending=False)
)

print(
    rating_by_category.round(2)
)


print()
print("BEST MONTH")

monthly_revenue = (
    df.groupby("year_month")["net_sales"]
    .sum()
    .sort_values(ascending=False)
)

print(
    monthly_revenue.head(5)
)