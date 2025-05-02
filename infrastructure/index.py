import boto3
import os
import time

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("rate-limit")

DAILY_LIMIT = 10  # or 20

def handler(event, context):
    ip = event["requestContext"]["identity"]["sourceIp"]
    now = int(time.time())

    response = table.get_item(Key={"ip_address": ip})
    item = response.get("Item", {})

    count = item.get("count", 0)
    last_reset = item.get("last_reset", now)

    # If it's been more than 24 hours, reset count
    if now - last_reset > 86400:
        count = 0
        last_reset = now

    if count >= DAILY_LIMIT:
        return {
            "statusCode": 429,
            "body": "Rate limit exceeded. Try again tomorrow."
        }

    # Update count
    table.put_item(Item={
        "ip_address": ip,
        "count": count + 1,
        "last_reset": last_reset
    })

    return {
        "statusCode": 200,
        "body": f"Hello from Lambda! Ping #{count + 1} from {ip}"
    }
