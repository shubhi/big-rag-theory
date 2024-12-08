import json
import boto3
import os
import base64

# Initialize S3 client
s3_client = boto3.client('s3')

# Environment variable for bucket name
BUCKET_NAME = os.environ.get('BUCKET_NAME')

def lambda_handler(event, context):
    try:
        # Debug: Log the event
        print("Event received:", json.dumps(event))

        # Check if the filename is provided
        if not event.get("queryStringParameters", {}).get("filename"):
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                },
                "body": json.dumps({"message": "Missing filename"})
            }

        # Extract filename and body
        filename = event["queryStringParameters"]["filename"]
        file_content = base64.b64decode(event["body"])  # Decode the base64-encoded body

        # Upload file to S3
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=file_content,
            ContentType="application/pdf"  # Explicitly set Content-Type
        )

        print(f"File '{filename}' uploaded successfully to '{BUCKET_NAME}'")
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"message": f"File '{filename}' uploaded successfully"})
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"message": str(e)})
        }
