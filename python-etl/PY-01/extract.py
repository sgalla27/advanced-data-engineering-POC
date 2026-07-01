import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def extract_data():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    policy_df = pd.read_sql(
        "SELECT * FROM policy",
        conn
    )

    claims_df = pd.read_sql(
        "SELECT * FROM claims",
        conn
    )

    conn.close()

    return policy_df, claims_df

if __name__ == "__main__":
    policy_df, claims_df = extract_data()

    print(policy_df.head())
    print(claims_df.head())