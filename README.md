# 🏗️ ETL Pipeline – HR Data

## 📋 Overview
Automated ETL pipeline to ingest, clean, and centralize HR data into PostgreSQL.
Built with Python, SQL, Airflow, PostgreSQL, and Azure.

## 🛠️ Technologies
- **Python 3.12** — Core language
- **Pandas** — Data manipulation and cleaning
- **SQLAlchemy + psycopg2** — PostgreSQL connection
- **PostgreSQL 18** — Local data storage
- **Apache Airflow** — Pipeline scheduling *(coming soon)*
- **Azure** — Cloud storage *(coming soon)*

## 🗂️ Project Structure
etl_hr_pipeline/
│
├── main.py                  # Pipeline entry point
├── .env                     # Credentials (not pushed to GitHub)
├── .gitignore               # Git ignore rules
├── README.md                # Project documentation
│
├── src/
│   ├── generate_data.py     # Generate fake HR dataset
│   ├── extract.py           # Extract data from CSV
│   ├── transform.py         # Clean and validate data
│   └── load.py              # Load data into PostgreSQL
│
├── data/                    # Raw data files
└── logs/                    # Pipeline execution logs

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/etl_hr_pipeline.git
cd etl_hr_pipeline
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file at the root:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=hr_database
DB_USER=postgres
DB_PASSWORD=postgres
```

### 5. Run the pipeline
```bash
python main.py
```

## 📊 Pipeline Phases
| Phase | Description |
|-------|-------------|
| **Extract** | Reads raw HR data from CSV |
| **Transform** | Cleans, validates and standardizes data |
| **Load** | Loads cleaned data into PostgreSQL |

## 👤 Author
Nour-El Houda Guendoula — [GitHub]: (https://github.com/Nourhoud) — [LinkedIn](https://www.linkedin.com/in/nourguendoula/ )
