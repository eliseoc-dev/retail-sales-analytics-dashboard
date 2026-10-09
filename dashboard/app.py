from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "retail_sales_clean.csv"
)


st.set_page_config(
    page_title="Retail Sales Analytics",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)

    df["order_date"] = pd.to_datetime(
        df["order_date"]
    )

    return df


df = load_data()


st.title("📊 Retail Sales Analytics Dashboard")

st.caption(
    "Interactive analysis of retail sales, customers, products and business performance."
)


# Sidebar filters

st.sidebar.header("Filters")


countries = sorted(
    df["country"]
    .dropna()
    .unique()
    .tolist()
)

categories = sorted(
    df["category"]
    .dropna()
    .unique()
    .tolist()
)

channels = sorted(
    df["sales_channel"]
    .dropna()
    .unique()
    .tolist()
)


selected_countries = st.sidebar.multiselect(
    "Country",
    options=countries,
    default=countries,
)

selected_categories = st.sidebar.multiselect(
    "Category",
    options=categories,
    default=categories,
)

selected_channels = st.sidebar.multiselect(
    "Sales Channel",
    options=channels,
    default=channels,
)


min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()


selected_dates = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)


filtered_df = df[
    df["country"].isin(selected_countries)
    & df["category"].isin(selected_categories)
    & df["sales_channel"].isin(selected_channels)
].copy()


if len(selected_dates) == 2:
    start_date = pd.Timestamp(selected_dates[0])
    end_date = pd.Timestamp(selected_dates[1])

    filtered_df = filtered_df[
        (filtered_df["order_date"] >= start_date)
        & (filtered_df["order_date"] <= end_date)
    ]


# KPIs

total_revenue = filtered_df["net_sales"].sum()
total_orders = len(filtered_df)
total_units = filtered_df["quantity"].sum()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)

return_rate = (
    filtered_df["returned"]
    .eq("Yes")
    .mean()
    * 100
    if total_orders > 0
    else 0
)


col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Revenue",
    f"${total_revenue:,.2f}",
)

col2.metric(
    "Orders",
    f"{total_orders:,}",
)

col3.metric(
    "Units Sold",
    f"{total_units:,}",
)

col4.metric(
    "Avg Order Value",
    f"${average_order_value:,.2f}",
)

col5.metric(
    "Return Rate",
    f"{return_rate:.2f}%",
)


st.divider()


# Monthly revenue

st.subheader("Revenue Trend")

monthly_sales = (
    filtered_df
    .groupby("year_month")["net_sales"]
    .sum()
    .reset_index()
)

st.line_chart(
    monthly_sales,
    x="year_month",
    y="net_sales",
)


# Country and category

left, right = st.columns(2)


with left:
    st.subheader("Revenue by Country")

    country_sales = (
        filtered_df
        .groupby("country")["net_sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(country_sales)


with right:
    st.subheader("Revenue by Category")

    category_sales = (
        filtered_df
        .groupby("category")["net_sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_sales)


st.divider()


# Top products

st.subheader("Top Products")

top_products = (
    filtered_df
    .groupby("product")
    .agg(
        units_sold=("quantity", "sum"),
        revenue=("net_sales", "sum"),
    )
    .sort_values(
        "revenue",
        ascending=False,
    )
    .head(10)
    .reset_index()
)

st.dataframe(
    top_products,
    use_container_width=True,
)


# Sales channels

st.subheader("Sales Channels")

channel_sales = (
    filtered_df
    .groupby("sales_channel")
    .agg(
        orders=("order_id", "count"),
        revenue=("net_sales", "sum"),
    )
    .sort_values(
        "revenue",
        ascending=False,
    )
)

st.bar_chart(
    channel_sales["revenue"]
)


# Raw/filtered data

st.divider()

st.subheader("Top Customers")

top_customers = (
    filtered_df
    .groupby("customer_id")
    .agg(
        orders=("order_id", "count"),
        revenue=("net_sales", "sum"),
    )
    .sort_values(
        "revenue",
        ascending=False,
    )
    .head(10)
    .reset_index()
)

st.subheader("Customer Ratings")

rating_distribution = (
    filtered_df["customer_rating"]
    .dropna()
    .value_counts()
    .sort_index()
)

st.bar_chart(
    rating_distribution
)

st.dataframe(
    top_customers,
    use_container_width=True,
)

st.subheader("Return Rate by Category")

return_by_category = (
    filtered_df
    .assign(
        returned_flag=(
            filtered_df["returned"] == "Yes"
        ).astype(int)
    )
    .groupby("category")[
        "returned_flag"
    ]
    .mean()
    .mul(100)
    .sort_values(
        ascending=False
    )
)

st.subheader("Return Rate by Category")

return_by_category = (
    filtered_df
    .assign(
        returned_flag=(
            filtered_df["returned"] == "Yes"
        ).astype(int)
    )
    .groupby("category")[
        "returned_flag"
    ]
    .mean()
    .mul(100)
    .sort_values(
        ascending=False
    )
)

st.bar_chart(
    return_by_category
)

st.bar_chart(
    return_by_category
)


with st.expander("View filtered dataset"):
    st.dataframe(
        filtered_df,
        use_container_width=True,
    )