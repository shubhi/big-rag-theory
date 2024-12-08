from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# API Gateway Endpoints
UPLOAD_API_URL = 'Add Your End Points Here' 
QUERY_API_URL = 'Add Your End Points Here' 

@app.route('/', methods=['GET'])
def index():
    """Render the main HTML page."""
    return render_template('index.html', upload_response=None, query_response=None)


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads and call the Upload API."""
    file = request.files.get('file')  # Retrieve the file from the form
    if not file:
        return render_template('index.html', upload_response="No file provided.", query_response=None)

    try:
        response = requests.post(
            f"{UPLOAD_API_URL}?filename={file.filename}",  # Pass filename as query param
            headers={"Content-Type": "application/pdf"},  # API expects a PDF file
            data=file.read()  # Read and send the file content
        )
        if response.status_code == 200:
            upload_response = f"File '{file.filename}' uploaded successfully!"
        else:
            upload_response = f"Upload failed: {response.text}"
    except Exception as e:
        upload_response = f"An error occurred: {str(e)}"

    return render_template('index.html', upload_response=upload_response, query_response=None)


@app.route('/query', methods=['GET', 'POST'])
def send_query():
    """Handle queries and call the Query API."""
    query = request.form.get('query')  # Retrieve the query from the form
    if not query:
        return render_template('index.html', query_response="No query provided.", upload_response=None)

    try:
        response = requests.post(
            f"{QUERY_API_URL}?query={query}",  # Pass the query as a query param
            headers={"Content-Type": "application/json"}  # Set appropriate headers
        )
        if response.status_code == 200:
            query_response = response.json().get('answer', 'No answer provided.')
        else:
            query_response = f"Query failed: {response.text}"
    except Exception as e:
        query_response = f"An error occurred: {str(e)}"

    return render_template('index.html', upload_response=None, query_response=query_response)


if __name__ == '__main__':
    app.run(debug=True)
