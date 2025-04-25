import os
import boto3
import json
import requests
import pandas as pd
from io import BytesIO
from appdirs import user_cache_dir
from .config import _CACHE_DIR, _CACHE_DATA_DIR, _CACHE_TABLE_NAME_PATH, _S3_BUCKET, _S3_KEY


def load(table: str, refresh: bool = False) -> pd.DataFrame:
    """
    Load a Survivor dataset from local storage, refreshing from the source if necessary.

    Parameters:
        table (str): The name of the table to load (e.g., "castaways").
        refresh (bool): If True, forces the dataset to be reloaded, bypassing the local cache.

    Returns:
        pd.DataFrame: The requested dataset.

    Raises:
        ValueError: If the provided table name is not recognized.
    """
    table_names_list = _load_table_names(refresh=refresh)
    if refresh:
        globals()["TABLE_NAMES"] = table_names_list

    if table not in table_names_list:
        raise ValueError(f"Unknown table: '{table}'. Choose from: {table_names_list}")

    local_path = os.path.join(_CACHE_DATA_DIR, f"{table}.parquet")
    
    # Use local data when appropriate
    if not refresh and os.path.exists(local_path):
        return pd.read_parquet(local_path)

    # Fetch the data from the remote source
    try:
        s3 = boto3.client('s3')
        s3_key = f"tables/{table}.parquet"
        response = s3.get_object(Bucket='survivorpy-data', Key=s3_key)
        
        # Read the data from the response
        parquet_data = response['Body'].read()
        df = pd.read_parquet(BytesIO(parquet_data))
        
        # Save the data locally for future use
        os.makedirs(_CACHE_DATA_DIR, exist_ok=True)
        df.to_parquet(local_path)

        return df

    except Exception as e:
        print(f"Error loading {table}: {e}")
        return None


def _fetch_table_names_from_s3():
    """Download the table_names.json file from S3 to the local cache path."""
    s3 = boto3.client("s3")
    s3.download_file(_S3_BUCKET, _S3_KEY, _CACHE_TABLE_NAME_PATH)

def _load_table_names(refresh=False):
    """
    Load the list of available Survivor data tables.

    Args:
        refresh (bool): If True, fetch a fresh copy from S3 even if cached.

    Returns:
        list[str]: Table names (or an empty list on failure).
    """
    if refresh or not os.path.exists(_CACHE_TABLE_NAME_PATH) or os.stat(_CACHE_TABLE_NAME_PATH).st_size == 0:
        try:
            os.makedirs(os.path.dirname(_CACHE_TABLE_NAME_PATH), exist_ok=True)
            _fetch_table_names_from_s3()
        except Exception as e:
            print(f"Warning: Could not refresh table names from S3: {e}")
            return []

    try:
        with open(_CACHE_TABLE_NAME_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Failed to load cached table names: {e}")
        return []
