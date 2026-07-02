import argparse
import csv
import logging
import time

from datetime import datetime

from config import load_config
from extract import extract_data
from transform import transform_data
from load import load_data


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("etl.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def write_run_history(
    rows_extracted,
    rows_written,
    status,
    duration
):

    with open(
        "run_history.csv",
        "a",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            datetime.now(),
            rows_extracted,
            rows_written,
            status,
            duration
        ])


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dry-run",
        action="store_true"
    )

    args = parser.parse_args()

    start_time = time.time()

    status = "SUCCESS"

    try:

        config = load_config()

        logger.info("Starting extraction")

        policy_df, claims_df = extract_data(
            config
        )

        logger.info("Starting transformation")

        enriched_df = transform_data(
            policy_df,
            claims_df
        )

        rows_written = len(enriched_df)

        if args.dry_run:

            logger.info(
                f"DRY RUN: Would write {rows_written} rows to "
                f"{config['output_path']}"
            )

        else:

            load_data(
                enriched_df,
                config["output_path"]
            )

            logger.info(
                f"File written to {config['output_path']}"
            )

        duration = round(
            time.time() - start_time,
            2
        )

        write_run_history(
            rows_extracted=len(claims_df),
            rows_written=rows_written,
            status=status,
            duration=duration
        )

    except Exception as e:

        status = "FAILED"

        logger.exception("Pipeline failed")

        duration = round(
            time.time() - start_time,
            2
        )

        write_run_history(
            rows_extracted=0,
            rows_written=0,
            status=status,
            duration=duration
        )


if __name__ == "__main__":
    main()