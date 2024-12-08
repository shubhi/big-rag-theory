Big RAG Theory
==============

Welcome to **Big RAG Theory**, a Scalable Software Architecture project aimed at creating a Retrieval-Augmented Generation (RAG) system for querying scientific documents and images. The system leverages AWS services to store, process, and query user-uploaded documents such as PDFs and text files. By combining document processing, vector search, and language models, BIG RAG THEORY provides a seamless way for users to query and retrieve insights from scientific documents.

Table of Contents
-----------------

*   [Overview](#overview)
    
*   [Architecture](#architecture)
    
*   [Features](#features)
    
*   [Tech Stack](#tech-stack)
    
*   [How It Works](#how-it-works)
    
*   [Steps to Run the App](#steps-to-run-the-app)
    
*   [Contributing](#contributing)
    
*   [License](#license)
    

Overview
--------

**BIG RAG THEORY** is a serverless, scalable system built on AWS that enables users to upload scientific documents (PDFs, text files, and images) and query them for insights. The RAG system combines:

1.  **Document Storage and Processing**: Storing uploaded files in S3 and extracting meaningful text using AWS Textract.
    
2.  **Vectorization**: Converting text into embeddings using Amazon Titan G1 Text Embedding and storing them in a vector database for efficient semantic search.
    
3.  **Querying**: Utilizing Amazon Titan Text Express (amazon.titan-text-express-v1) for generating responses to user queries, enhanced by context retrieved from OpenSearch.
    

Architecture
------------

The architecture is fully serverless, leveraging AWS services for scalability and reliability.

### Workflow Diagram

1.  **Document Upload**:
    
    *   User uploads PDFs, text files, or images to an S3 bucket.
        
    *   A Lambda function is triggered to process the file with AWS Textract.
        
2.  **Text Processing**:
    
    *   Extracted text is converted to embeddings using **Amazon Titan G1 Text Embedding**.
        
    *   Embeddings are stored in a vector database.
        
3.  **Querying**:
    
    *   User submits a query.
        
    *   A Lambda function is triggered to:
        
        *   Search embeddings using OpenSearch.
            
        *   Generate responses using **Amazon Titan Text Express**.
            
    *   Combine results to return a contextually accurate response.
        

Features
--------

*   **Efficient Document Upload**: Supports PDFs, text files, and images.
    
*   **Scalable Text Extraction**: Automated extraction using AWS Textract.
    
*   **Semantic Search**: Embedding-based search for contextual relevance using Amazon Titan G1 Text Embedding.
    
*   **AI-Powered Querying**: Generates responses with Amazon Titan Text Express.
    
*   **Scalability**: Fully serverless architecture leveraging Lambda functions, S3, and other AWS services.
    

Tech Stack
----------

*   **AWS Services**:
    
    *   S3: File storage.
        
    *   Lambda: Serverless compute for triggers.
        
    *   Textract: Text extraction from documents.
        
    *   OpenSearch: Semantic search and indexing.
        
    *   Amazon Titan G1 Text Embedding: Text vectorization.
        
    *   Amazon Titan Text Express: Text generation.
        
*   **Vector Database**: Pinecone or similar for embedding storage.
    
*   **Programming Languages**: Python for Lambda functions.
    
*   **Frameworks**: AWS SDK (Boto3), LangChain for RAG orchestration, Flask, HTML, CSS.
    

How It Works
------------

1.  **Upload Phase**:
    
    *   Users upload documents via an API or web interface.
        
    *   S3 triggers a Lambda function to process the uploaded file.
        
2.  **Processing Phase**:
    
    *   AWS Textract extracts text from documents.
        
    *   The extracted text is sent to **Amazon Titan G1 Text Embedding**, which generates high-dimensional vector representations of the text.
        
    *   Vectorized data is stored in a vector database (e.g., OpenSearch or a compatible alternative).
        
3.  **Query Phase**:
    
    *   Users input queries via an API or web interface.
        
    *   The query is also converted into embeddings using **Amazon Titan G1 Text Embedding** for vector space matching.
        
    *   A Lambda function searches the vector database for relevant context.
        
    *   Context is sent to **Amazon Titan Text Express** for answer generation.
        
    *   Results are merged and returned to the user.

Steps to Run the App
--------------------

Follow these steps to run the application locally:

1. Open the project directory in a terminal and install the required libraries (requests and flask)

```bash
   pip install -r requirements.txt
```
2.  Move to the app directory

```bash
    cd app
```

3. Run the app.py
```bash
    python app.py
```
    
4.  **Access the Application**:Open the link provided in the terminal (usually http://127.0.0.1:5000) in a web browser.
    
5.  **Use the Application**:
    
    *   Use the **Upload** button to upload a file (test files included in test_files directory).
        
    *   Enter a query in the search bar to retrieve insights from the uploaded document.    


Contributing
------------

Contributions are welcome! Please follow these steps:

1.  Fork this repository.
    
2.  Create a feature branch: git checkout -b feature/your-feature.
    
3.  Commit your changes: git commit -m 'Add your feature'.
    
4.  Push to the branch: git push origin feature/your-feature.
    
5.  Open a pull request.
    

License
-------

This project is licensed under the MIT License. See the LICENSE file for more details.

Feel free to reach out with questions or suggestions. We hope you enjoy using **BIG RAG THEORY**! 🎉
