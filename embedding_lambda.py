import boto3
import json

# Initialize Bedrock client
bedrock = boto3.client('bedrock-runtime')

def generate_embeddings(text):
    try:
        # Log the input text
        # print(f"Generating embeddings for text: {text}")

        # Invoke the Bedrock model
        try:
            response = bedrock.invoke_model(
                modelId="amazon.titan-embed-text-v1",
                contentType="application/json",
                accept="application/json",
                body=json.dumps({"inputText": text})
            )
        except Exception as e:
            print(f"Error while invoking the Bedrock model: {e}")
            raise
        
        # Read and decode the response
        response_body = response['body'].read().decode('utf-8')
        # print(f"Raw response from Bedrock: {response_body}")  # Debugging raw response

        # Parse the JSON response
        result = json.loads(response_body)
        # print(f"Parsed JSON response: {result}")  # Debugging parsed JSON
        
        # Extract embeddings
        embeddings = result.get('embedding')
        if embeddings is None:
            raise ValueError("Embeddings field is missing or null in the response.")
        
        return embeddings
    except Exception as e:
        print(f"Error while generating embeddings: {e}")
        raise


# Lambda handler
def lambda_handler(event, context):
    try:
        # Extract S3 bucket and file details from the event
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']
        print(f"Processing file: s3://{bucket_name}/{object_key}")

        # Download the file from S3
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        text_content = response['Body'].read().decode('utf-8')

        # Generate embeddings
        embeddings = generate_embeddings(text_content)
        print("successful!", embeddings)
        # Return embeddings
        return {
            "statusCode": 200,
            "body": json.dumps({"embeddings": embeddings})
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
