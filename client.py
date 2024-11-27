import requests
import base64

# URL of the Lambda function
LAMBDA_SERVER_URL = 'https://du4h657am6lbmobtw3amspowqa0eotqz.lambda-url.us-east-1.on.aws/'

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
