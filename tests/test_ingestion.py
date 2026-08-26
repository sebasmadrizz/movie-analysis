import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def test_staging_row_counts():
    DB_USER = os.getenv("POSTGRES_USER", "postgres")
    DB_PASS = os.getenv("POSTGRES_PASSWORD")
    DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
    DB_PORT = os.getenv("POSTGRES_PORT", "5432")
    DB_NAME = os.getenv("POSTGRES_DB", "moviedb")

    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

    df_movies_csv = pd.read_csv("data/raw/tmdb_5000_movies.csv")
    df_credits_csv = pd.read_csv("data/raw/tmdb_5000_credits.csv")

    with engine.connect() as conn:
        db_movies_count = conn.execute(text("SELECT COUNT(*) FROM raw_movies;")).scalar()
        db_credits_count = conn.execute(text("SELECT COUNT(*) FROM raw_credits;")).scalar()

    print(f"Movies  - CSV: {len(df_movies_csv)} | DB Staging: {db_movies_count}")
    print(f"Credits - CSV: {len(df_credits_csv)} | DB Staging: {db_credits_count}")

    assert db_movies_count == len(df_movies_csv), "the count of raw_movies does not match the CSV"
    assert db_credits_count == len(df_credits_csv), "the count of raw_credits does not match the CSV"
    print(" Verification successful: All records were inserted correctly.")

if __name__ == "__main__":
    test_staging_row_counts()