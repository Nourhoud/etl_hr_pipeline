# main.py
# Entry point for the ETL pipeline.
# Runs all 4 steps in order: extract, transform, load, upload to Azure.

import logging
import time
from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data
from src.azure_upload import upload_to_azure

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/pipeline.log")
    ]
)
logger = logging.getLogger(__name__)


def run_pipeline():
    logger.info("=" * 50)
    logger.info("HR ETL PIPELINE - STARTING")
    logger.info("=" * 50)

    start_time = time.time()

    logger.info("STEP 1 - Extract")
    raw_df = extract_data("data/hr_raw.csv")

    logger.info("STEP 2 - Transform")
    clean_df = transform_data(raw_df)

    logger.info("STEP 3 - Load")
    load_data(clean_df)

    logger.info("STEP 4 - Upload to Azure")
    upload_to_azure(clean_df)

    elapsed = round(time.time() - start_time, 2)
    logger.info("=" * 50)
    logger.info(f"PIPELINE COMPLETE - {elapsed}s")
    logger.info("=" * 50)


if __name__ == "__main__":
    run_pipeline()
