from src.extract.api_extractor import fetch_jobs
from src.transform.cleaner import transform_jobs
from src.load.db_loader import load_to_db
import pandas as pd


def run_pipeline():
    # 🔹 Extract
    raw_jobs = fetch_jobs()

    if not raw_jobs:
        print("❌ No data fetched from API.")
        return

    # 🔹 Transform
    cleaned_jobs = transform_jobs(raw_jobs)

    if not cleaned_jobs:
        print("❌ No data after transformation.")
        return

    # 🔹 Convert to DataFrame
    df = pd.DataFrame(cleaned_jobs)

    if df.empty:
        print("❌ DataFrame is empty.")
        return

    # 🔹 Safe date conversion
    if "posted_date" in df.columns:
        df["posted_date"] = pd.to_datetime(df["posted_date"], errors="coerce")

    print(df.head())

    # 🔹 Load
    load_to_db(df)


if __name__ == "__main__":
    run_pipeline()