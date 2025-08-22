import json

def handler(event, context):
    for record in event["Records"]:
        message = record["Sns"]["Message"]
        print(f"Processing SNS message: {message}")
    return {"statusCode": 200}
