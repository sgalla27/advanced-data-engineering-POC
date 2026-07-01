from extract import extract_data
from transform import transform_data
from load import load_data

def main():

    print("Starting extraction...")

    policy_df, claims_df = extract_data()

    print("Starting transformation...")

    enriched_df = transform_data(
        policy_df,
        claims_df
    )

    print("Writing parquet file...")

    output_path = load_data(enriched_df)

    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    main()