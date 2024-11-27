import json
import base64
import boto3
import os

# Initialize S3 client
s3_client = boto3.client('s3')

# Environment variable for bucket name
BUCKET_NAME = os.environ.get('BUCKET_NAME')

def lambda_handler(event, context):
    try:
        # Check if the body and filename are provided
        if not event.get("body") or not event.get("queryStringParameters", {}).get("filename"):
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Missing file content or filename"})
            }
        # Get the file content and decode it from base64
        file_content = base64.b64decode(event["body"])
        
        # Extract filename from query parameters
        filename = event["queryStringParameters"]["filename"]

        # Upload file to S3
        s3_client.put_object(Bucket=BUCKET_NAME, Key=filename, Body=file_content)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"File '{filename}' uploaded successfully to '{BUCKET_NAME}'"})
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }