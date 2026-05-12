# ETL Pipeline – HR Data

An automated ETL pipeline I built to practice data engineering with real tools.
It pulls HR data, cleans it, loads it into PostgreSQL, and pushes it to Azure Blob Storage.
Scheduled daily with Apache Airflow.

## Technologies
Python, Pandas, SQLAlchemy, PostgreSQL, Apache Airflow, Azure Blob Storage, Git

## What it does

1. **Extract** – reads raw HR data from a CSV file
2. **Transform** – cleans and validates the data (emails, phone numbers, dates, duplicates, missing values)
3. **Load** – inserts the cleaned data into a PostgreSQL database
4. **Upload** – pushes the cleaned CSV to Azure Blob Storage

## Project Structure

etl_hr_pipeline/
├── main.py                  # runs the full pipeline
├── src/
│   ├── generate_data.py     # generates fake HR data for testing
│   ├── extract.py           # reads the CSV
│   ├── transform.py         # cleans and validates the data
│   ├── load.py              # loads into PostgreSQL
│   └── azure_upload.py      # uploads to Azure
├── .env                     # credentials (not committed)
└── requirements.txt

## How to run

```bash
# clone and install
git clone https://github.com/Nourhoud/etl_hr_pipeline.git
cd etl_hr_pipeline
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# set up your .env file
DB_HOST=localhost
DB_PORT=5432
DB_NAME=hr_database
DB_USER=postgres
DB_PASSWORD=your_password
AZURE_CONNECTION_STRING=your_connection_string
AZURE_CONTAINER_NAME=hr-data

# generate data and run
python src/generate_data.py
python main.py
```

## Airflow

The pipeline runs as a DAG in Apache Airflow on WSL, scheduled `@daily`.
Each step (extract, transform, load) is an independent task.

## Author
 Nour — [GitHub](https://github.com/Nourhoud)
