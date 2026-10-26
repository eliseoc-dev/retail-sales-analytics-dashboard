from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

PROCESSED_DIR = BASE_DIR / "data" / "processed"
EXCEL_DIR = BASE_DIR / "excel"
POWERBI_DIR = BASE_DIR / "powerbi"


def find_processed_csv() -> Path:
    csv_files = list(
        PROCESSED_DIR.glob("*.csv")
    )

    if not csv_files:
        raise FileNotFoundError(
            "No processed CSV file found."
        )

    return csv_files[0]


def export_for_bi() -> None:
    source_file = find_processed_csv()

    print(
        f"Loading processed data from: "
        f"{source_file.name}"
    )

    df = pd.read_csv(source_file)

    EXCEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    POWERBI_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    excel_path = (
        EXCEL_DIR
        / "retail_sales_analysis.xlsx"
    )

    powerbi_path = (
        POWERBI_DIR
        / "retail_sales_bi.csv"
    )

    with pd.ExcelWriter(
        excel_path,
        engine="openpyxl",
    ) as writer:

        df.to_excel(
            writer,
            sheet_name="SalesData",
            index=False,
        )

        summary = pd.DataFrame(
            {
                "Metric": [
                    "Rows",
                    "Revenue",
                    "Units",
                    "Average Order Value",
                ],
                "Value": [
                    len(df),
                    df["net_sales"].sum(),
                    df["quantity"].sum(),
                    df["net_sales"].mean(),
                ],
            }
        )

        summary.to_excel(
            writer,
            sheet_name="Summary",
            index=False,
        )

    df.to_csv(
        powerbi_path,
        index=False,
    )

    print()
    print("BI exports created:")
    print(excel_path)
    print(powerbi_path)


if __name__ == "__main__":
    export_for_bi()