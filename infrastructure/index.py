import boto3
import os
import time
import json

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("rate-limit")

DAILY_LIMIT = 10
SEC_PER_DAY = 60 * 60 * 24

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

        # If it's been more than 24 hours, reset count
        if last_reset is None or now - last_reset > SEC_PER_DAY:
            count = 0
            last_reset = now

        # Handle exceeding rate limit
        if count >= DAILY_LIMIT:
            return {
                "statusCode": 429,
                "body": json.dumps({"message": "Rate limit exceeded. Try again tomorrow."})
            }

        # Update count and reset
        table.put_item(Item={
            "ip_address": ip,
            "count": count + 1,
            "last_reset": last_reset
        })

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"Hello from Lambda! Ping #{count + 1} from {ip}"
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error", "error": str(e)})
        }
