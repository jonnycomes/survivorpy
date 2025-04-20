import os
import json
import boto3

_CACHE_PATH = os.path.join(os.path.dirname(__file__), "_cache", "table_names.json")
_S3_BUCKET = "survivorpy-data"
_S3_KEY = "metadata/table_names.json"

def _fetch_table_names_from_s3():
    s3 = boto3.client("s3")
    s3.download_file(_S3_BUCKET, _S3_KEY, _CACHE_PATH)

def _load_table_names(refresh=False):
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
