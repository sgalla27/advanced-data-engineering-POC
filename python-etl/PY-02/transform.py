def transform_data(policy_df, claims_df):

    enriched_df = claims_df.merge(
        policy_df,
        on="policy_id",
        how="left"
    )

    enriched_df["claim_ratio"] = (
        enriched_df["amount"] /
        enriched_df["premium"]
    )

    return enriched_df