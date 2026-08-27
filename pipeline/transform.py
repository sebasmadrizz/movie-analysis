import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "movie_analysis")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def run_transformation():
    """Reads and executes the analytics transformation SQL script."""
    engine = create_engine(DATABASE_URL)
    sql_file_path = "sql/2_create_analytics_tables.sql"
    
    print("Executing analytics schema transformation and JSON parsing...")
    
    with open(sql_file_path, "r", encoding="utf-8") as file:
        sql_script = file.read()

    # Execute SQL script inside a single transaction
    with engine.begin() as connection:
        connection.execute(text(sql_script))
        
    print("Analytics layer created and populated successfully.")

if __name__ == "__main__":
    run_transformation()