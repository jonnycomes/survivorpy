import boto3
import os
from datetime import datetime, timedelta

s3 = boto3.client('s3')
BUCKET = os.environ['S3_BUCKET']

def handler(event, context):
    ip_address = event['requestContext']['identity']['sourceIp']

    key = f"rate-limiting/{ip_address}.json"

    # Try to get the existing data
    try:
        response = s3.get_object(Bucket=BUCKET, Key=key)
        data = response['Body'].read().decode('utf-8')
        count = int(data)
    except s3.exceptions.NoSuchKey:
        count = 0

    # Simple rate limit: allow up to 5 pings
    if count >= 5:
        return {
            "statusCode": 429,
            "body": "Too Many Requests"
        }

    # Update the count in S3
    new_count = count + 1
    s3.put_object(Bucket=BUCKET, Key=key, Body=str(new_count))

    return {
        "statusCode": 200,
        "body": f"Hello from Lambda! Ping #{new_count} from {ip_address}"
    }
