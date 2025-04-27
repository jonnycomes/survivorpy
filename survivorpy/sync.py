import boto3
import json
import pandas as pd
from io import BytesIO
from datetime import datetime
from .config import _CACHE_DATA_DIR, _CACHE_TABLE_NAMES_PATH, _CACHE_LAST_SYNCED_PATH, _S3_BUCKET, _S3_TABLE_NAMES_KEY

def _cache_data(tables):
    """
    Download datasets from the source and store them in the local cache.

    For each table name in the list, this function fetches the corresponding dataset 
    from the source and saves it as a Parquet file in the local cache directory. 
    Overwrites any existing files with the same name.

    Parameters:
        tables (list[str]): A list of table names to download.

    Raises:
        Exception: If any download or file operation fails.
    """
    _CACHE_DATA_DIR.mkdir(parents=True, exist_ok=True)

    for table in tables:
        local_path = _CACHE_DATA_DIR / f"{table}.parquet"
        s3 = boto3.client('s3')
        s3_key = f"tables/{table}.parquet"
        response = s3.get_object(Bucket=_S3_BUCKET, Key=s3_key)

        # Read the data from the response
        parquet_data = response['Body'].read()
        df = pd.read_parquet(BytesIO(parquet_data))

        # Save the data locally
        df.to_parquet(local_path)

def _cache_table_names():
    """
    Downloads the metadata file containing available table names from the source
    and stores it in the local cache. This function creates or overwrites a local 
    JSON file in the cache directory.

    This file is used to support the `TABLE_NAMES` attribute in the public API.
    """
    _CACHE_TABLE_NAMES_PATH.parent.mkdir(parents=True, exist_ok=True)
    s3 = boto3.client("s3")
    s3.download_file(_S3_BUCKET, _S3_TABLE_NAMES_KEY, _CACHE_TABLE_NAMES_PATH)

def _update_last_synced():
    """
    Record the current UTC time as the last successful data sync.

    This function creates or overwrites a local JSON file in the cache directory 
    with a timestamp indicating the most recent data refresh. The timestamp is 
    stored in ISO 8601 format.

    This file is used to support the `LAST_SYNCED` attribute in the public API.
    """
    _CACHE_LAST_SYNCED_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(_CACHE_LAST_SYNCED_PATH, "w") as f:
        json.dump({"timestamp": datetime.utcnow().isoformat()}, f)

