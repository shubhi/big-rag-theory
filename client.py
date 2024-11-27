import requests
import base64
import configparser

# Load the config file
config = configparser.ConfigParser()
config.read('config.ini')

# URL of the Lambda function
LAMBDA_SERVER_URL = config['aws']['upload_url']
LAMBDA_RAG_URL = config['aws']['rag_url']

choice = int(input("Enter a Number> \n"))

if choice == 1: 
    # File to upload
    FILE_PATH = './test_files/paper1.pdf'
    FILENAME = 'paper1.pdf'

    # Open the file and encode it in Base64
    with open(FILE_PATH, 'rb') as file:
        file_content = base64.b64encode(file.read()).decode('utf-8')

    # Send the POST request to the Lambda function
    response = requests.post(
        LAMBDA_SERVER_URL,
        params={'filename': FILENAME},  # Add the filename as a query string parameter
        data=file_content,  # Base64-encoded file content
        headers={'Content-Type': 'application/json'}  # Set content type
    )

    # Check the response from the Lambda function
    if response.status_code == 200:
        print('Success:', response.json())
    else:
        print('Error:', response.status_code, response.json())

if choice == 2:
    print("Performing RAG")
    user_query = "Hello!"
    response = requests.get(
        LAMBDA_RAG_URL, 
        params={'query': user_query}
    )
    if response.status_code == 200:
        print("Response received:")
        print(response.json())  # Parse and print the JSON response
    else:
        print(f"Error: Received status code {response.status_code}")
        print(response.json())
