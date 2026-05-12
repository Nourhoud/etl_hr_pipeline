"""
generate_data.py
----------------
Generates a realistic fake HR dataset and saves it as a CSV file.
This simulates the raw data that would come from an HR system.
"""

import pandas as pd
from faker import Faker
import random
from pathlib import Path

# Initialize Faker for realistic fake data generation
fake = Faker("fr_FR")  # French locale for realistic HR data
random.seed(42)         # Seed for reproducibility

# ── Constants ────────────────────────────────────────────────────────────────
NUM_EMPLOYEES = 200

DEPARTMENTS = ["Engineering", "Marketing", "HR", "Finance", "Sales", "Operations"]
POSITIONS    = ["Analyst", "Manager", "Director", "Engineer", "Coordinator", "Intern"]
STATUSES     = ["Active", "Inactive", "On Leave"]

# ── Data Generation ───────────────────────────────────────────────────────────
def generate_hr_data(n: int) -> pd.DataFrame:
    """
    Generate n fake employee records.

    Args:
        n (int): Number of employee records to generate.

    Returns:
        pd.DataFrame: DataFrame containing fake HR data.
    """
    records = []

    for i in range(1, n + 1):
        record = {
            "employee_id"   : i,
            "first_name"    : fake.first_name(),
            "last_name"     : fake.last_name(),
            "email"         : fake.email(),
            "phone"         : fake.phone_number(),
            "department"    : random.choice(DEPARTMENTS),
            "position"      : random.choice(POSITIONS),
            "salary"        : round(random.uniform(30000, 120000), 2),
            "hire_date"     : fake.date_between(start_date="-10y", end_date="today"),
            "status"        : random.choice(STATUSES),
            "city"          : fake.city(),
            "country"       : "France",
        }
        records.append(record)

    return pd.DataFrame(records)


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Generate the dataset
    df = generate_hr_data(NUM_EMPLOYEES)

    # Save to CSV in the data/ folder
    output_path = Path("data/hr_raw.csv")
    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Dataset generated: {NUM_EMPLOYEES} employees saved to '{output_path}'")
    print(df.head())
