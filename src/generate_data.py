# generate_data.py
# Generates a fake HR dataset using Faker and saves it as a CSV.
# Used to simulate raw data coming from an HR system.

import pandas as pd
from faker import Faker
import random
from pathlib import Path

fake = Faker("fr_FR")
random.seed(42)

NUM_EMPLOYEES = 200
DEPARTMENTS = ["Engineering", "Marketing", "HR", "Finance", "Sales", "Operations"]
POSITIONS   = ["Analyst", "Manager", "Director", "Engineer", "Coordinator", "Intern"]
STATUSES    = ["Active", "Inactive", "On Leave"]


def generate_hr_data(n: int) -> pd.DataFrame:
    records = []
    for i in range(1, n + 1):
        records.append({
            "employee_id" : i,
            "first_name"  : fake.first_name(),
            "last_name"   : fake.last_name(),
            "email"       : fake.email(),
            "phone"       : fake.phone_number(),
            "department"  : random.choice(DEPARTMENTS),
            "position"    : random.choice(POSITIONS),
            "salary"      : round(random.uniform(30000, 120000), 2),
            "hire_date"   : fake.date_between(start_date="-10y", end_date="today"),
            "status"      : random.choice(STATUSES),
            "city"        : fake.city(),
            "country"     : "France",
        })
    return pd.DataFrame(records)


if __name__ == "__main__":
    df = generate_hr_data(NUM_EMPLOYEES)
    output_path = Path("data/hr_raw.csv")
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Generated {NUM_EMPLOYEES} employee records → {output_path}")
    print(df.head())
