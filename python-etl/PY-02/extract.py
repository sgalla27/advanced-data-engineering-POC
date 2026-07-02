import os
import psycopg2
import pandas as pd

from dotenv import load_dotenv
from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_fixed

from exceptions import DataQualityError

load_dotenv()


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(5)
)
def get_connection():

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def extract_data(config):

    conn = get_connection()

    policy_df = pd.read_sql(
        f"SELECT * FROM {config['source_tables']['policy']}",
        conn
    )

    claims_df = pd.read_sql(
        f"SELECT * FROM {config['source_tables']['claims']}",
        conn
    )

    conn.close()

    if len(policy_df) < 5:
        raise DataQualityError(
            "Policy table contains fewer than 5 rows"
        )

    if len(claims_df) < 5:
        raise DataQualityError(
            "Claims table contains fewer than 5 rows"
        )

    return policy_df, claims_df