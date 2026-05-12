# load.py
# Loads the cleaned HR data into PostgreSQL.
# Drops and recreates the table on each run to keep data fresh.

import pandas as pd
import logging
from sqlalchemy import create_engine, text

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

CONNECTION_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/hr_database"


def load_data(df: pd.DataFrame, table_name: str = "employees") -> None:
    engine = create_engine(CONNECTION_URL)
    logger.info(f"Loading {len(df)} rows into table '{table_name}'...")

    # hire_date comes in as datetime, PostgreSQL needs a string
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

    # quick sanity check
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        count = result.scalar()
        logger.info(f"Verification - {count} rows in '{table_name}'")


if __name__ == "__main__":
    from extract import extract_data
    from transform import transform_data
    raw_df = extract_data("data/hr_raw.csv")
    clean_df = transform_data(raw_df)
    load_data(clean_df)
