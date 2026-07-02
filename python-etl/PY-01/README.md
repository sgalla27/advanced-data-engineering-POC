List of Files


.env --> Stores NeonDB credentials to keep sensitive information out of code.
<br/><br/>
.env.example --> Template showing what environmental variables are required.
<br/><br/>
requirements.txt --> Lists the Python packages needed to run the project.
<br/><br/>
extract.py --> Connects to NeonDB, reads policy and claims table and loads both into Pandas DataFrames
<br/><br/>
transform.py --> Joins policy_df and claims_df and calculates claim_ratio (amount/premium) and outputs as enriched_df
<br/><br/>
test_transform.py --> verifies transform works before entire pipeline is ran
<br/><br/>
load.py --> Creates output directory and writes the transformed data (from dataframe to file)
<br/><br/>
main.py --> goes through pipeline of extract --> transform --> load
<br/><br/>
output/claims_enriched.parquet --> final result of ETL process
<br/><br/>
<br/><br/>
show contents:

python

import pandas as pd

df = pd.read_parquet("output/claims_enriched.parquet")

print(df)
