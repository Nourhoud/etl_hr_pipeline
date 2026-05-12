"""
main.py
-------
Entry point for the HR ETL pipeline.
Orchestrates the full Extract → Transform → Load process.
"""

import logging
import time
from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data

# ── Logging Configuration ─────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
    handlers=[
        logging.StreamHandler(),                              # Log to console
        logging.FileHandler("logs/pipeline.log")             # Log to file
    ]
)
logger = logging.getLogger(__name__)

# ── Pipeline ──────────────────────────────────────────────────────────────────
def run_pipeline():
    """
    Run the full ETL pipeline:
    1. Extract raw HR data from CSV
    2. Transform and clean the data
    3. Load the cleaned data into PostgreSQL
    """
    logger.info("=" * 50)
    logger.info("   HR ETL PIPELINE — STARTING")
    logger.info("=" * 50)

    start_time = time.time()

    # ── Step 1: Extract ───────────────────────────────────────────────────────
    logger.info("STEP 1 — Extract")
    raw_df = extract_data("data/hr_raw.csv")

    # ── Step 2: Transform ─────────────────────────────────────────────────────
    logger.info("STEP 2 — Transform")
    clean_df = transform_data(raw_df)

    # ── Step 3: Load ──────────────────────────────────────────────────────────
    logger.info("STEP 3 — Load")
    load_data(clean_df)

    # ── Summary ───────────────────────────────────────────────────────────────
    elapsed = round(time.time() - start_time, 2)
    logger.info("=" * 50)
    logger.info(f"   PIPELINE COMPLETE — {elapsed}s")
    logger.info("=" * 50)


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_pipeline()
