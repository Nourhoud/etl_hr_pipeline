"""
transform.py
------------
Handles the transformation phase of the ETL pipeline.
Cleans, validates, and standardizes the raw HR data.
"""

import pandas as pd
import logging

# ── Logging Configuration ─────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)
logger = logging.getLogger(__name__)


# ── Transform Functions ───────────────────────────────────────────────────────
def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate rows from the DataFrame."""
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    logger.info(f"Duplicates removed: {removed}")
    return df


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names to lowercase with underscores."""
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    logger.info("Column names standardized")
    return df


def clean_text_fields(df: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace and capitalize text fields."""
    text_cols = ["first_name", "last_name", "department", "position", "city", "country", "status"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].str.strip().str.title()
    logger.info("Text fields cleaned")
    return df


def validate_email(df: pd.DataFrame) -> pd.DataFrame:
    """Flag rows with invalid email format."""
    invalid_mask = ~df["email"].str.contains(r"^[\w\.-]+@[\w\.-]+\.\w+$", regex=True, na=False)
    invalid_count = invalid_mask.sum()
    if invalid_count > 0:
        logger.warning(f"Invalid emails found: {invalid_count} — rows will be dropped")
        df = df[~invalid_mask]
    else:
        logger.info("All emails are valid")
    return df


def validate_salary(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with negative or missing salary values."""
    before = len(df)
    df = df[df["salary"] > 0].dropna(subset=["salary"])
    removed = before - len(df)
    logger.info(f"Invalid salary rows removed: {removed}")
    return df


def convert_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Convert hire_date column to datetime format."""
    df["hire_date"] = pd.to_datetime(df["hire_date"], errors="coerce")
    invalid_dates = df["hire_date"].isna().sum()
    if invalid_dates > 0:
        logger.warning(f"Invalid dates coerced to NaT: {invalid_dates}")
    else:
        logger.info("All dates converted successfully")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows where critical fields are missing."""
    critical_cols = ["employee_id", "first_name", "last_name", "email", "department"]
    before = len(df)
    df = df.dropna(subset=critical_cols)
    removed = before - len(df)
    logger.info(f"Rows with missing critical values removed: {removed}")
    return df

def normalize_phone(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize phone numbers to a consistent format: +33XXXXXXXXX
    Handles formats like: 0327013079, +33 3 24 18 06 66, +33 (0)6 67 64 62 15
    """
    def clean_phone(phone):
        if pd.isna(phone):
            return None
        # Remove all spaces, dashes, dots and parentheses
        phone = str(phone).replace(" ", "").replace("-", "").replace(".", "").replace("(", "").replace(")", "")
        # Remove +33 or 0033 prefix and replace with 0
        if phone.startswith("+33"):
            phone = "0" + phone[3:]
        elif phone.startswith("0033"):
            phone = "0" + phone[4:]
        # Keep only digits
        phone = ''.join(filter(str.isdigit, phone))
        # Format as 0X XX XX XX XX
        if len(phone) == 10:
            return f"{phone[0:2]} {phone[2:4]} {phone[4:6]} {phone[6:8]} {phone[8:10]}"
        return None  # Invalid phone number

    before = len(df)
    df["phone"] = df["phone"].apply(clean_phone)
    invalid = df["phone"].isna().sum()
    if invalid > 0:
        logger.warning(f"Invalid phone numbers set to NULL: {invalid}")
    logger.info("Phone numbers normalized")
    return df

# ── Main Transform Pipeline ───────────────────────────────────────────────────
def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply all transformation steps to the raw HR DataFrame.

    Args:
        df (pd.DataFrame): Raw HR data.

    Returns:
        pd.DataFrame: Cleaned and validated HR data.
    """
    logger.info("Starting transformation pipeline...")

    df = clean_column_names(df)
    df = remove_duplicates(df)
    df = clean_text_fields(df)
    df = validate_email(df)
    df = validate_salary(df)
    df = convert_dates(df)
    df = handle_missing_values(df)
    df = normalize_phone(df)

    logger.info(f"Transformation complete — {len(df)} rows remaining")
    return df


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    from extract import extract_data

    raw_df = extract_data("data/hr_raw.csv")
    clean_df = transform_data(raw_df)

    print(clean_df.head())
    print(f"\nShape after transformation: {clean_df.shape}")
    print(f"\nMissing values:\n{clean_df.isnull().sum()}")
