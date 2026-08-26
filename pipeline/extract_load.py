import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "moviedb")



DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def load_staging_data():
    engine = create_engine(DATABASE_URL)

    # 1. execute DDL to create staging tables
    print("Creating staging tables in PostgreSQL...")
    with open("sql/1_create_staging_tables.sql", "r") as f:
        sql_ddl = f.read()

    with engine.connect() as connection:
        connection.execute(text(sql_ddl))
        connection.commit()

    # 2. charge tmdb_5000_movies.csv
    print("charging raw_movies...")
    df_movies = pd.read_csv("data/raw/tmdb_5000_movies.csv")
    df_movies.to_sql("raw_movies", engine, if_exists="append", index=False)
    print(f"  raw_movies charged with {len(df_movies)} records.")

    # 3. charge tmdb_5000_credits.csv
    print("charging raw_credits...")
    df_credits = pd.read_csv("data/raw/tmdb_5000_credits.csv")
    df_credits.to_sql("raw_credits", engine, if_exists="append", index=False)
    print(f"  raw_credits charged with {len(df_credits)} records.")

if __name__ == "__main__":
    load_staging_data()