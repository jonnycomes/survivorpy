import os
import json
import boto3
from appdirs import user_cache_dir

_CACHE_DIR = user_cache_dir("survivorpy", "jonnycomes")
_CACHE_PATH = os.path.join(_CACHE_DIR, "table_names.json")
_S3_BUCKET = "survivorpy-data"
_S3_KEY = "metadata/table_names.json"

def _fetch_table_names_from_s3():
    """Download the table_names.json file from S3 to the local cache path."""
    s3 = boto3.client("s3")
    s3.download_file(_S3_BUCKET, _S3_KEY, _CACHE_PATH)

def _load_table_names(refresh=False):
    """
    Load the list of available Survivor data tables.

    Args:
        refresh (bool): If True, fetch a fresh copy from S3 even if cached.

    Returns:
        list[str]: Table names (or an empty list on failure).
    """
    if refresh or not os.path.exists(_CACHE_PATH) or os.stat(_CACHE_PATH).st_size == 0:
        try:
            os.makedirs(os.path.dirname(_CACHE_PATH), exist_ok=True)
            _fetch_table_names_from_s3()
        except Exception as e:
            print(f"Warning: Could not refresh table names from S3: {e}")
            return []

    try:
        with open(_CACHE_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Failed to load cached table names: {e}")
        return []
