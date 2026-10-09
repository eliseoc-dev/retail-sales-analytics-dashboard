import pandas as pd


DATA_PATH = (
    "data/processed/"
    "retail_sales_clean.csv"
)


def load_data():
    return pd.read_csv(DATA_PATH)


def test_no_duplicates():
    df = load_data()

    assert df.duplicated().sum() == 0


def test_positive_quantities():
    df = load_data()

    assert (df["quantity"] > 0).all()


def test_positive_prices():
    df = load_data()

    assert (df["unit_price"] > 0).all()


def test_valid_discounts():
    df = load_data()

    assert (
        (df["discount"] >= 0)
        & (df["discount"] <= 1)
    ).all()


def test_net_sales_not_negative():
    df = load_data()

    assert (
        df["net_sales"] >= 0
    ).all()


def test_required_columns_exist():
    df = load_data()

    required_columns = {
        "gross_sales",
        "discount_amount",
        "net_sales",
        "year",
        "month",
        "year_month",
    }

    assert required_columns.issubset(
        df.columns
    )