import psycopg2
from datetime import date
import requests
import time
from create_envs import import_envs_and_create_db_config

# Database connection parameters
DB_CONFIG = import_envs_and_create_db_config()

def ensure_table_exists():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS data (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        date DATE NOT NULL
                    )
                """)
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        conn.close()
ensure_table_exists()

def create_row(name: str, date_value: date):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO data (name, date) VALUES (%s, %s)",
                    (name, date_value)
                )
                print("Row created:", name, date_value)
    except Exception as e:
        print(f"Error creating row: {e}")
    finally:
        conn.close()

def fetch_joke():
    try:
        resp = requests.get("https://geek-jokes.sameerkumar.website/api?format=json", timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("joke", "")
    except Exception as e:
        return f"Error fetching joke: {e}"

if __name__ == "__main__":
    while True:
        joke = fetch_joke()
        if joke:
            create_row(joke, date.today())
        time.sleep(30)