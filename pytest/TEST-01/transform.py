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


def add_high_risk_flag(df):
    df = df.copy()

    df["is_high_risk"] = df["claim_ratio"] >= 0.8

    return df


def drop_null_policy_id(df):
    df = df.copy()

    return df.dropna(subset=["policy_id"])