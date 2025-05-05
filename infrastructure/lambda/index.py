import boto3
import os
import time
import json
import base64

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("rate-limit")
s3 = boto3.client("s3")

DAILY_LIMIT = 10
SEC_PER_DAY = 60 * 60 * 24
BUCKET = "survivorpy-data"
ZIP_KEY = "survivor_data.zip"

def handler(event, context):
    try:
        ip = event["requestContext"]["identity"]["sourceIp"]
    except KeyError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "sourceIp not found in request"})
        }

    now = int(time.time())

    try:
        response = table.get_item(Key={"ip_address": ip})
        item = response.get("Item", {})

        count = item.get("count", 0)
        last_reset = item.get("last_reset")

        # Reset count if it's been more than 24 hours
        if last_reset is None or now - last_reset > SEC_PER_DAY:
            count = 0
            last_reset = now

        # Enforce rate limit
        if count >= DAILY_LIMIT:
            seconds_remaining = (last_reset + SEC_PER_DAY) - now
            hours = seconds_remaining // 3600
            minutes = (seconds_remaining % 3600) // 60

            return {
                "statusCode": 429,
                "body": json.dumps({"message": f"You have reached the daily limit of {DAILY_LIMIT} data refreshes. You can try again in {hours} hour{'s' if hours != 1 else ''} and {minutes} minute{'s' if minutes != 1 else ''}."})
            }

        # Update usage in DynamoDB
        table.put_item(Item={
            "ip_address": ip,
            "count": count + 1,
            "last_reset": last_reset
        })

        # Fetch the zip file from S3
        zip_obj = s3.get_object(Bucket=BUCKET, Key=ZIP_KEY)
        zip_content = zip_obj["Body"].read()
        zip_b64 = base64.b64encode(zip_content).decode("utf-8")

        return {
            "statusCode": 200,
            "body": zip_b64
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error", "error": str(e)})
        }
