import boto3
import json
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Initialize clients
bedrock = boto3.client('bedrock-runtime')
s3 = boto3.client('s3')

# OSS serverless config
host = ''
region = 'us-east-1'
service = 'aoss'
index_name = 'research-index'


# Initialize OpenSearch client
credentials = boto3.Session().get_credentials()
auth = AWSV4SignerAuth(credentials, region, service)
os_client = OpenSearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

def generate_embeddings(text):
    try:

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

def store_in_opensearch(text_chunk, embeddings, metadata):
    document = {
        'text_content': text_chunk,
        'text_embedding': embeddings,
        'metadata': metadata
    }
    os_client.index(index=index_name, body=document)

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

        # Splitting the text file
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            length_function=len
        )

        text_chunks = text_splitter.split_text(text_content)

        # Store in the OSS Serverless index
        for chunk in text_chunks:
            embeddings = generate_embeddings(chunk)
            metadata = {
                'source': f"s3://{bucket_name}/{object_key}",
                'chunk_size': len(chunk)
            }
            store_in_opensearch(chunk, embeddings, metadata)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"Successfully processed and stored {len(text_chunks)} chunks"})
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
