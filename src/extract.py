"""
extract.py
----------
Handles the extraction phase of the ETL pipeline.
Reads the raw HR data from a CSV file and returns it as a DataFrame.
"""

import pandas as pd
from pathlib import Path
import logging

# ── Logging Configuration ─────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)
logger = logging.getLogger(__name__)


# ── Extract Function ──────────────────────────────────────────────────────────
def extract_data(filepath: str) -> pd.DataFrame:
    """
    Read raw HR data from a CSV file.

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Raw HR data as a DataFrame.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
    """
    path = Path(filepath)

    if not path.exists():
        logger.error(f"File not found: {filepath}")
        raise FileNotFoundError(f"No file found at: {filepath}")

    logger.info(f"Extracting data from: {filepath}")
    df = pd.read_csv(path, encoding="utf-8")

    logger.info(f"Extraction complete — {len(df)} rows, {len(df.columns)} columns")
    return df


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = extract_data("data/hr_raw.csv")
    print(df.head())
    print(f"\nShape: {df.shape}")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nData types:\n{df.dtypes}")
