import pandas as pd

def standardize_status(df):
    df = df.copy()

    df["status"] = (
        df["status"]
        .str.upper()
        .str.strip()
    )

    return df


def calculate_claim_ratio(df):
    df = df.copy()

    df["claim_ratio"] = df["amount"] / df["premium"]

    return df