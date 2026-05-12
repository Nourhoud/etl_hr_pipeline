# azure_upload.py
# Uploads the cleaned HR data to Azure Blob Storage as a CSV.
# Credentials are loaded from the .env file.

import pandas as pd
import logging
import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from io import StringIO

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def upload_to_azure(df: pd.DataFrame, filename: str = "hr_cleaned.csv") -> None:
    connection_string = os.getenv("AZURE_CONNECTION_STRING")
    container_name    = os.getenv("AZURE_CONTAINER_NAME")

    if not connection_string or not container_name:
        raise ValueError("Azure credentials not found in .env file")

    logger.info("Connecting to Azure Blob Storage...")
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=filename
    )

    # convert DataFrame to CSV in memory to avoid writing to disk
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, encoding="utf-8")

    logger.info(f"Uploading '{filename}' to container '{container_name}'...")
    blob_client.upload_blob(csv_buffer.getvalue(), overwrite=True, encoding="utf-8")

    logger.info(f"Upload complete - {blob_client.url}")


if __name__ == "__main__":
    from extract import extract_data
    from transform import transform_data
    raw_df = extract_data("data/hr_raw.csv")
    clean_df = transform_data(raw_df)
    upload_to_azure(clean_df)
