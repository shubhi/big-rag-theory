// Replace with your API Gateway endpoints
const FILE_UPLOAD_API_URL = 'https://du47kunqgk.execute-api.us-east-1.amazonaws.com/prod/upload';
const QUERY_API_URL = 'https://du47kunqgk.execute-api.us-east-1.amazonaws.com/prod/query';

/**
 * Upload PDF File to API Gateway
 * @param {File} file - The PDF file to be uploaded
 * @returns {Promise<Object>} - Response from the API
 */
async function uploadFileToAPI(file) {
    const filename = encodeURIComponent(file.name); // Encode filename to avoid special character issues
  
    // Validate file type
    if (!file.type || file.type !== 'application/pdf') {
      throw new Error('Only PDF files are allowed.');
    }
  
    // Send the PDF file content and filename to the API
    const response = await fetch(`${FILE_UPLOAD_API_URL}?filename=${filename}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/pdf', // Ensure content type is set for PDF
      },
      body: file, // The raw file data
    });
  
    // Check if the response is successful
    if (!response.ok) {
      throw new Error(`File upload failed with status: ${response.status}`);
    }
  
    return await response.json(); // Parse and return the JSON response
  }
  
  /**
   * Send Query to API Gateway
   * @param {string} query - The user query
   * @returns {Promise<Object>} - Response from the API
   */
  async function sendQueryToAPI(query) {
    // Send the query as a JSON payload to the API
    const response = await fetch(QUERY_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // Specify that we're sending JSON
      },
      body: JSON.stringify({ query }), // Include the query in the request body
    });
  
    // Check if the response is successful
    if (!response.ok) {
      throw new Error(`Query failed with status: ${response.status}`);
    }
  
    return await response.json(); // Parse and return the JSON response
  }