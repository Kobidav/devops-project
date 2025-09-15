from dotenv import dotenv_values, load_dotenv 
import os

def import_envs_and_create_db_config():
    load_dotenv()
    DB_CONFIG = {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "dbname": os.getenv("DB_NAME"),
    }
    return DB_CONFIG


print(import_envs_and_create_db_config())