import pandas as pd


DATA_PATH = (
    "data/processed/"
    "retail_sales_clean.csv"
)


df = pd.read_csv(DATA_PATH)


total_revenue = df["net_sales"].sum()
total_orders = len(df)
total_units = df["quantity"].sum()

average_order_value = (
    total_revenue / total_orders
)

return_rate = (
    df["returned"]
    .eq("Yes")
    .mean()
    * 100
)

average_rating = (
    df["customer_rating"]
    .mean()
)


print("=" * 60)
print("BUSINESS KPIs")
print("=" * 60)

print(
    f"Total revenue: "
    f"${total_revenue:,.2f}"
)

print(
    f"Orders: "
    f"{total_orders:,}"
)

print(
    f"Units sold: "
    f"{total_units:,}"
)

print(
    f"Average order value: "
    f"${average_order_value:,.2f}"
)

print(
    f"Return rate: "
    f"{return_rate:.2f}%"
)

print(
    f"Average rating: "
    f"{average_rating:.2f}"
)