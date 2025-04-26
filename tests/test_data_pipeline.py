import boto3
import pytest
from survivorpy.config import _S3_BUCKET, _S3_TABLE_NAMES_KEY


s3 = boto3.client("s3")

def test_survivor_data_in_s3():
    expected_table_name = "castaways"
    key = f"tables/{expected_table_name}.parquet"
    try:
        s3.head_object(Bucket=_S3_BUCKET, Key=key)
    except s3.exceptions.ClientError as e:
        pytest.fail(f"{key} not found in bucket")

def test_table_names_json_in_s3():
    try:
        response = s3.get_object(Bucket=_S3_BUCKET, Key=_S3_TABLE_NAMES_KEY)
        body = response["Body"].read().decode("utf-8")
        import json
        tables = json.loads(body)
        assert isinstance(tables, list)
        assert all(isinstance(t, str) for t in tables)
    except s3.exceptions.ClientError:
        pytest.fail(f"{_S3_TABLE_NAMES_KEY} not found in bucket")
