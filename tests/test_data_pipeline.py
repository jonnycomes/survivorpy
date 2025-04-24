import boto3
import pytest

s3 = boto3.client("s3")
bucket = "survivorpy-data"

def test_survivor_data_in_s3():
    expected_table_name = "castaways"
    key = f"tables/{expected_table_name}.parquet"
    try:
        s3.head_object(Bucket=bucket, Key=key)
    except s3.exceptions.ClientError as e:
        pytest.fail(f"{key} not found in bucket")

def test_table_names_json_in_s3():
    key = "metadata/table_names.json"
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode("utf-8")
        import json
        tables = json.loads(body)
        assert isinstance(tables, list)
        assert all(isinstance(t, str) for t in tables)
    except s3.exceptions.ClientError:
        pytest.fail(f"{key} not found in bucket")
