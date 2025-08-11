from dotenv import dotenv_values

def import_envs_and_create_db_config(env_file_path=".env"):
    envs = dotenv_values(env_file_path)
    DB_CONFIG = {
        "host": envs.get("DB_HOST"),
        "port": envs.get("DB_PORT"),
        "user": envs.get("DB_USER"),
        "password": envs.get("DB_PASSWORD"),
        "dbname": envs.get("DB_NAME"),
    }
    return DB_CONFIG
