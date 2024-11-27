# Imports
from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import NoCredentialsError
import configparser

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Extract AWS credentials
AWS_ACCESS_KEY = config['aws']['aws_access_key']
AWS_SECRET_KEY = config['aws']['aws_secret_key']
S3_BUCKET_NAME = config['aws']['s3_bucket_name']

app = Flask(__name__)

# Create s3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    try:
        # Upload file to S3
        s3_client.upload_fileobj(file, S3_BUCKET_NAME, file.filename)
        return jsonify({'message': f'File {file.filename} uploaded successfully to {S3_BUCKET_NAME}.'}), 200
    except NoCredentialsError:
        return jsonify({'error': 'Credentials not available'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)