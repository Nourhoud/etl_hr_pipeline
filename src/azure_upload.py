"""
azure_upload.py
---------------
Handles uploading cleaned HR data to Azure Blob Storage.
This centralizes data storage in the cloud for easy access and archiving.
"""

import pandas as pd
import logging
import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from io import StringIO

# -- Load Environment Variables ------------------------------------------------
load_dotenv()

# -- Logging Configuration -----------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def upload_to_azure(df: pd.DataFrame, filename: str = "hr_cleaned.csv") -> None:
    """
    Upload a cleaned HR DataFrame to Azure Blob Storage as a CSV file.

    Args:
        df (pd.DataFrame): Cleaned HR data to upload.
        filename (str): Name of the file in Azure Blob Storage.
    """
    # -- Get credentials from .env ---------------------------------------------
    connection_string = os.getenv("AZURE_CONNECTION_STRING")
    container_name    = os.getenv("AZURE_CONTAINER_NAME")

    if not connection_string or not container_name:
        raise ValueError("Azure credentials not found in .env file!")

    # -- Connect to Azure Blob Storage -----------------------------------------
    logger.info("Connecting to Azure Blob Storage...")
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=filename
    )

    # -- Convert DataFrame to CSV in memory ------------------------------------
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, encoding="utf-8")
    csv_data = csv_buffer.getvalue()

    # -- Upload to Azure -------------------------------------------------------
    logger.info(f"Uploading '{filename}' to Azure container '{container_name}'...")
    blob_client.upload_blob(csv_data, overwrite=True, encoding="utf-8")

    logger.info(f"Successfully uploaded '{filename}' to Azure Blob Storage!")
    logger.info(f"Blob URL: {blob_client.url}")


# -- Main ----------------------------------------------------------------------
if __name__ == "__main__":
    from extract import extract_data
    from transform import transform_data

    raw_df   = extract_data("data/hr_raw.csv")
    clean_df = transform_data(raw_df)
    upload_to_azure(clean_df)
