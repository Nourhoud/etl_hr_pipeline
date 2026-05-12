# extract.py
# Reads the raw HR CSV and returns it as a DataFrame.
# First step of the ETL pipeline.

import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def extract_data(filepath: str) -> pd.DataFrame:
    path = Path(filepath)

    if not path.exists():
        logger.error(f"File not found: {filepath}")
        raise FileNotFoundError(f"No file found at: {filepath}")

    logger.info(f"Extracting data from: {filepath}")
    df = pd.read_csv(path, encoding="utf-8")
    logger.info(f"Extraction complete — {len(df)} rows, {len(df.columns)} columns")
    return df


if __name__ == "__main__":
    df = extract_data("data/hr_raw.csv")
    print(df.head())
    print(f"\nShape: {df.shape}")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nData types:\n{df.dtypes}")
