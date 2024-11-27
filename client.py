import requests

# URL of the Flask server
FLASK_SERVER_URL = 'http://127.0.0.1:5000/upload'

# File to upload
FILE_PATH = './test_files/paper1.pdf'

# Open the file in binary mode and send it as part of the POST request
with open(FILE_PATH, 'rb') as file:
    files = {'file': file}
    response = requests.post(FLASK_SERVER_URL, files=files)

# Check the response from the server
if response.status_code == 200:
    print('Success:', response.json())
else:
    print('Error:', response.status_code, response.json())
