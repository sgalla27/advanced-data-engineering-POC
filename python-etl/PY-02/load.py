import os

def load_data(df, output_path):

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    df.to_parquet(
        output_path,
        index=False
    )

    return output_path