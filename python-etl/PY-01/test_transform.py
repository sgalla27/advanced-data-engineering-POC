from extract import extract_data
from transform import transform_data

policy_df, claims_df = extract_data()

result = transform_data(
    policy_df,
    claims_df
)

print(result)