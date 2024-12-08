import json
import boto3
import os
import pathlib
import urllib.parse

# Initialize S3 and Textract clients
s3_client = boto3.client('s3')
textract_client = boto3.client('textract')

# Environment variable for bucket name
BUCKETNAME = os.environ.get('BUCKET_NAME')

def lambda_handler(event, context):
    try:
        print("**STARTING**")
        print("**lambda: textract**")
        
        # Get S3 object key from the event
        BUCKETKEY = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        print("bucketkey:", BUCKETKEY)
        
        # Validate file extension
        extension = pathlib.Path(BUCKETKEY).suffix.lower()
        if extension != ".pdf":
            raise Exception("Unsupported file format. Expecting a PDF document.")
        
        # Generate a result file name
        bucketkey_results_file = pathlib.Path(BUCKETKEY).stem + ".txt"
        print("bucketkey results file:", bucketkey_results_file)
        
        # Start text detection using Textract
        print("**Starting Textract job for '", BUCKETKEY, "'**")
        response = textract_client.start_document_text_detection(
            DocumentLocation={
                'S3Object': {
                    'Bucket': BUCKETNAME,
                    'Name': BUCKETKEY
                }
            }
        )
        
        # Retrieve the Job ID
        job_id = response['JobId']
        print("Textract JobId:", job_id)
        
        # Wait for the job to complete
        print("**Waiting for Textract job completion**")
        job_status = "IN_PROGRESS"
        while job_status == "IN_PROGRESS":
            response = textract_client.get_document_text_detection(JobId=job_id)
            job_status = response['JobStatus']
            print("Job Status:", job_status)
            if job_status == "IN_PROGRESS":
                import time
                time.sleep(5)
        
        if job_status != "SUCCEEDED":
            raise Exception("Textract job did not succeed. Status: " + job_status)
        
        # Extract text from the response
        detected_text = ''
        for block in response['Blocks']:
            if block['BlockType'] == 'LINE':
                detected_text += block['Text'] + '\n'
        
        # Write the detected text back to S3
        print("**Writing extracted text to S3**")
        result_file_path = os.path.splitext(BUCKETKEY)[0] + '.txt'
        s3_client.put_object(Body=detected_text, Bucket=BUCKETNAME, Key=result_file_path)
        print('Generated ' + result_file_path)
        
        print("**DONE, returning success**")
        return {
            'statusCode': 200,
            'body': json.dumps("success")
        }
    
    except Exception as err:
        # Log and return error
        print("**ERROR**")
        print(str(err))
        return {
            'statusCode': 500,
            'body': json.dumps(str(err))
        }
