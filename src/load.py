"""
load.py
-------
Handles the load phase of the ETL pipeline.
Connects to PostgreSQL and loads the cleaned HR data into a table.
"""

import pandas as pd
import logging
from sqlalchemy import create_engine, text

# -- Logging Configuration -----------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# -- Database Connection -------------------------------------------------------
CONNECTION_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/hr_database"


def load_data(df: pd.DataFrame, table_name: str = "employees") -> None:
    """
    Load the cleaned DataFrame into a PostgreSQL table.

    Args:
        df (pd.DataFrame): Cleaned HR data to load.
        table_name (str): Target table name in PostgreSQL.
    """
    engine = create_engine(CONNECTION_URL)
    logger.info(f"Loading {len(df)} rows into table '{table_name}'...")

    # Convert hire_date to string format for PostgreSQL
    df["hire_date"] = pd.to_datetime(df["hire_date"], errors="coerce").dt.strftime("%Y-%m-%d")

    with engine.begin() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
        conn.execute(text(f"""
            CREATE TABLE {table_name} (
                employee_id INTEGER,
                first_name  VARCHAR(100),
                last_name   VARCHAR(100),
                email       VARCHAR(200),
                phone       VARCHAR(50),
                department  VARCHAR(100),
                position    VARCHAR(100),
                salary      FLOAT,
                hire_date   DATE,
                status      VARCHAR(50),
                city        VARCHAR(100),
                country     VARCHAR(100)
            )
        """))

        records = df.to_dict(orient="records")
        for record in records:
            conn.execute(text("""
                INSERT INTO employees
                (employee_id, first_name, last_name, email, phone, department,
                 position, salary, hire_date, status, city, country)
                VALUES
                (:employee_id, :first_name, :last_name, :email, :phone, :department,
                 :position, :salary, :hire_date, :status, :city, :country)
            """), record)

    logger.info(f"Data successfully loaded into '{table_name}'")

    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        count = result.scalar()
        logger.info(f"Verification - rows in '{table_name}': {count}")


if __name__ == "__main__":
    from extract import extract_data
    from transform import transform_data
    raw_df = extract_data("data/hr_raw.csv")
    clean_df = transform_data(raw_df)
    load_data(clean_df)
