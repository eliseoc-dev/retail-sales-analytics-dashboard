from pathlib import Path

import numpy as np
import pandas as pd


RANDOM_SEED = 42
ROW_COUNT = 50000

np.random.seed(RANDOM_SEED)


OUTPUT_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "raw"
    / "retail_sales_raw.csv"
)


countries = {
    "Ecuador": [
        "Guayaquil",
        "Quito",
        "Cuenca",
    ],
    "Colombia": [
        "Bogotá",
        "Medellín",
        "Cali",
    ],
    "Peru": [
        "Lima",
        "Arequipa",
        "Cusco",
    ],
    "Mexico": [
        "Mexico City",
        "Guadalajara",
        "Monterrey",
    ],
    "United States": [
        "Miami",
        "New York",
        "Houston",
    ],
}


products = {
    "Electronics": [
        ("Wireless Headphones", 85.00),
        ("Mechanical Keyboard", 70.00),
        ("Wireless Mouse", 35.00),
        ("Webcam", 55.00),
        ("USB Hub", 25.00),
    ],
    "Computers": [
        ("Laptop Stand", 40.00),
        ("SSD 1TB", 95.00),
        ("RAM 16GB", 65.00),
        ("External HDD", 80.00),
    ],
    "Office": [
        ("Office Chair", 180.00),
        ("Desk Lamp", 30.00),
        ("Notebook Pack", 15.00),
        ("Desk Organizer", 20.00),
    ],
    "Gaming": [
        ("Gaming Mouse", 60.00),
        ("Gaming Headset", 90.00),
        ("Controller", 65.00),
        ("RGB Mouse Pad", 25.00),
    ],
    "Accessories": [
        ("USB-C Cable", 12.00),
        ("Phone Stand", 18.00),
        ("Power Bank", 45.00),
        ("Bluetooth Speaker", 55.00),
    ],
}


payment_methods = [
    "Credit Card",
    "Debit Card",
    "PayPal",
    "Bank Transfer",
    "Cash",
]


sales_channels = [
    "Online",
    "Store",
    "Mobile App",
]


rows = []


for index in range(ROW_COUNT):
    order_id = f"ORD-{index + 1:06d}"

    date = pd.Timestamp("2024-01-01") + pd.to_timedelta(
        np.random.randint(0, 730),
        unit="D",
    )

    customer_id = f"CUST-{np.random.randint(1, 4001):05d}"

    country = np.random.choice(
        list(countries.keys())
    )

    city = np.random.choice(
        countries[country]
    )

    category = np.random.choice(
        list(products.keys())
    )

    product_name, base_price = products[
        category
    ][
        np.random.randint(
            len(products[category])
        )
    ]

    quantity = np.random.randint(1, 6)

    price_variation = np.random.uniform(
        0.90,
        1.10,
    )

    unit_price = round(
        base_price * price_variation,
        2,
    )

    discount = np.random.choice(
        [
            0,
            0,
            0,
            0.05,
            0.10,
            0.15,
            0.20,
        ]
    )

    payment_method = np.random.choice(
        payment_methods
    )

    sales_channel = np.random.choice(
        sales_channels,
        p=[
            0.55,
            0.25,
            0.20,
        ],
    )

    returned = np.random.choice(
        [
            "No",
            "Yes",
        ],
        p=[
            0.92,
            0.08,
        ],
    )

    customer_rating = np.random.choice(
        [
            1,
            2,
            3,
            4,
            5,
            np.nan,
        ],
        p=[
            0.03,
            0.07,
            0.15,
            0.30,
            0.35,
            0.10,
        ],
    )

    rows.append(
        {
            "order_id": order_id,
            "order_date": date.date(),
            "customer_id": customer_id,
            "country": country,
            "city": city,
            "category": category,
            "product": product_name,
            "quantity": quantity,
            "unit_price": unit_price,
            "discount": discount,
            "payment_method": payment_method,
            "sales_channel": sales_channel,
            "returned": returned,
            "customer_rating": customer_rating,
        }
    )


df = pd.DataFrame(rows)


# Introduce intentional data quality issues

missing_supplier_rows = np.random.choice(
    df.index,
    size=150,
    replace=False,
)

df.loc[
    missing_supplier_rows,
    "payment_method",
] = np.nan


messy_category_rows = np.random.choice(
    df.index,
    size=120,
    replace=False,
)

df.loc[
    messy_category_rows,
    "category",
] = (
    df.loc[
        messy_category_rows,
        "category",
    ]
    .str.lower()
    .str.strip()
)


messy_city_rows = np.random.choice(
    df.index,
    size=100,
    replace=False,
)

df.loc[
    messy_city_rows,
    "city",
] = (
    " "
    + df.loc[
        messy_city_rows,
        "city",
    ]
    + " "
)


duplicate_rows = df.sample(
    75,
    random_state=RANDOM_SEED,
)

df = pd.concat(
    [
        df,
        duplicate_rows,
    ],
    ignore_index=True,
)


OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

df.to_csv(
    OUTPUT_PATH,
    index=False,
)


print("=" * 60)
print("RETAIL SALES DATASET GENERATED")
print("=" * 60)
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"Output: {OUTPUT_PATH}")