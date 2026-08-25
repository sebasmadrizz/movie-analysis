import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def test_connection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            port=os.getenv("POSTGRES_PORT", "5432"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        
        print(" Successfully connected to PostgreSQL!")
        print(f" Server version: {db_version[0]}")
        
        cursor.close()
        connection.close()
    except Exception as error:
        print(f" Error connecting to PostgreSQL: {error}")

if __name__ == "__main__":
    test_connection()