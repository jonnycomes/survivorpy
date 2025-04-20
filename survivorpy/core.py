import os
import boto3
import requests
import pandas as pd
from io import BytesIO
from pathlib import Path
from .table_names import _load_table_names

_LOCAL_DATA_DIR = Path(__file__).parent.parent / "data"

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

    local_path = os.path.join(_LOCAL_DATA_DIR, f"{table}.parquet")
    
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
        os.makedirs(_LOCAL_DATA_DIR, exist_ok=True)
        df.to_parquet(local_path)

        return df

    except Exception as e:
        print(f"Error loading {table}: {e}")
        return None

