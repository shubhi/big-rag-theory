import json
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

# Bedrock Runtime client used to invoke and question the models
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime', 
    region_name='us-east-1'
)

# OpenSearch configuration
OPENSEARCH_ENDPOINT = ''
INDEX_NAME = 'research-index'

# Set up AWS authentication for OpenSearch
session = boto3.Session()
credentials = session.get_credentials()
region = 'us-east-1'
auth = AWSV4SignerAuth(credentials, region, 'aoss')

# Initialize OpenSearch client
os_client = OpenSearch(
    hosts=[{'host': OPENSEARCH_ENDPOINT.replace('https://', ''), 'port': 443}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

def generate_embeddings(text):
    """Generate embeddings using AWS Bedrock."""
    response = bedrock_runtime.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body=json.dumps({"inputText": text}),
        accept="application/json",
        contentType="application/json"
    )
    response_body = response['body'].read().decode('utf-8')  # Read and decode the StreamingBody
    result = json.loads(response_body)
    return result['embedding']

def retrieve_from_opensearch(embedding, k=5):
    """Retrieve top-k similar items from OpenSearch using OpenSearchPy."""
    payload = {
        "query": {
            "knn": {
                "text_embedding": {
                    "vector": embedding,
                    "k": k
                }
            }
        }
    }

    response = os_client.search(
        index=INDEX_NAME,
        body=payload
    )

    hits = response['hits']['hits']
    return [hit['_source'] for hit in hits]

def aggregate_chunks(chunks):
    """Aggregate relevant chunks into a single text block."""
    return "\n".join(chunk['text_content'] for chunk in chunks)

def lambda_handler(event, context):
    try:
        # Extract the query parameter from the event
        query = event.get('queryStringParameters', {}).get('query', '')

        # Log the incoming query for debugging
        print("Received query:", query)

        # Check if the query parameter exists
        if not query:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS, POST',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({'error': "Query parameter 'query' is missing"})
            }

        # Generate embeddings for the query
        embedding = generate_embeddings(query)

        # Retrieve similar items from OpenSearch
        retrieved_items = retrieve_from_opensearch(embedding, k=5)

        # Aggregate chunks into a context block
        context_text = aggregate_chunks(retrieved_items)

        # Construct the response for Bedrock model
        response = bedrock_runtime.invoke_model(
            modelId="amazon.titan-text-express-v1",
            body=json.dumps({
                "inputText": f"Context: {context_text}\n\nQuestion: {query}",
                "textGenerationConfig": {
                    "maxTokenCount": 4096,
                    "temperature": 0,
                    "topP": 1,
                    "stopSequences": ["User:"]
                }
            }),
            accept="application/json",
            contentType="application/json"
        )

        # Parse and return the model's response
        response_body = json.loads(response['body'].read())
        response_text = response_body.get('results', [{}])[0].get('outputText', '')

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS, POST',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'answer': response_text})
        }

    except Exception as e:
        # Log the error for debugging
        print("Error occurred:", str(e))

        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS, POST',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'error': 'An internal server error occurred', 'details': str(e)})
        }
