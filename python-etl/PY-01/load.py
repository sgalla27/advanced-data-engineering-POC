import os

def load_data(df):

    os.makedirs("output", exist_ok=True)

    output_path = "output/claims_enriched.parquet"

    df.to_parquet(
        output_path,
        index=False
    )

    return output_path