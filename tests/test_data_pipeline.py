import boto3
import pytest
import json
from survivorpy.config import _S3_BUCKET, _S3_TABLE_NAMES_KEY

s3 = boto3.client("s3")

def test_survivor_data_in_s3():
    key = "tables/castaways.parquet"
    try:
        s3.head_object(Bucket=_S3_BUCKET, Key=key)
    except s3.exceptions.ClientError:
        pytest.fail(f"{key} not found in bucket")

def test_table_names_json_in_s3():
    try:
        response = s3.get_object(Bucket=_S3_BUCKET, Key=_S3_TABLE_NAMES_KEY)
        tables = json.loads(response["Body"].read().decode("utf-8"))
        assert isinstance(tables, list)
        assert all(isinstance(t, str) for t in tables)
    except s3.exceptions.ClientError:
        pytest.fail(f"{_S3_TABLE_NAMES_KEY} not found in bucket")
