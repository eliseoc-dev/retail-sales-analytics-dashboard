from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "retail_sales_clean.csv"
)

REPORTS_PATH = (
    PROJECT_ROOT
    / "reports"
)

REPORTS_PATH.mkdir(
    parents=True,
    exist_ok=True,
)


df = pd.read_csv(DATA_PATH)


# 1. Monthly revenue

monthly_sales = (
    df.groupby("year_month")["net_sales"]
    .sum()
    .reset_index()
)

plt.figure(figsize=(12, 6))
plt.plot(
    monthly_sales["year_month"],
    monthly_sales["net_sales"],
    marker="o",
)
plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(
    REPORTS_PATH / "monthly_revenue.png"
)
plt.close()


# 2. Revenue by country

country_sales = (
    df.groupby("country")["net_sales"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))
country_sales.plot(kind="bar")
plt.title("Revenue by Country")
plt.xlabel("Country")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig(
    REPORTS_PATH / "revenue_by_country.png"
)
plt.close()


# 3. Revenue by category

category_sales = (
    df.groupby("category")["net_sales"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))
category_sales.plot(kind="bar")
plt.title("Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig(
    REPORTS_PATH / "revenue_by_category.png"
)
plt.close()


# 4. Top products

top_products = (
    df.groupby("product")["net_sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))
top_products.sort_values().plot(
    kind="barh"
)
plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig(
    REPORTS_PATH / "top_products.png"
)
plt.close()


# 5. Sales by channel

channel_sales = (
    df.groupby("sales_channel")["net_sales"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8, 6))
channel_sales.plot(kind="bar")
plt.title("Revenue by Sales Channel")
plt.xlabel("Channel")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig(
    REPORTS_PATH / "sales_by_channel.png"
)
plt.close()


# 6. Return distribution

return_counts = (
    df["returned"]
    .value_counts()
)

plt.figure(figsize=(7, 5))
return_counts.plot(kind="bar")
plt.title("Returned vs Non-Returned Orders")
plt.xlabel("Returned")
plt.ylabel("Orders")
plt.tight_layout()
plt.savefig(
    REPORTS_PATH / "returns_distribution.png"
)
plt.close()


print("=" * 60)
print("VISUALIZATIONS GENERATED")
print("=" * 60)

for file in REPORTS_PATH.glob("*.png"):
    print(file.name)