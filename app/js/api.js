// Replace with your API Gateway endpoints
const FILE_UPLOAD_API_URL = 'https://du47kunqgk.execute-api.us-east-1.amazonaws.com/prod/upload';
const QUERY_API_URL = 'https://du47kunqgk.execute-api.us-east-1.amazonaws.com/prod/query';

/**
 * Upload PDF File to API Gateway
 * @param {File} file - The PDF file to be uploaded
 * @returns {Promise<Object>} - Response from the API
 */
async function uploadFileToAPI(file) {
    const filename = encodeURIComponent(file.name);
    console.log('Uploading file:', filename);
  
    try {
      const response = await fetch(`${FILE_UPLOAD_API_URL}?filename=${filename}`, {
        method: 'POST',
        headers: {
          'Content-Type': file.type, // Ensure the MIME type matches the file
        },
        body: file, // Send the raw file data
      });
  
      if (!response.ok) {
        throw new Error(`Failed to upload file: ${response.status} ${response.statusText}`);
      }
  
      const jsonResponse = await response.json();
      console.log('Upload successful:', jsonResponse);
      return jsonResponse;
  
    } catch (error) {
      console.error('Error uploading file:', error);
      throw error;
    }
  }
  /**
 * Send Query to API Gateway
 * @param {string} query - The user query
 * @returns {Promise<Object>} - Response from the API
 */
async function sendQueryToAPI(query) {
    const encodedQuery = encodeURIComponent(query); // Encode the query to handle special characters
    const apiUrl = `${QUERY_API_URL}?query=${encodedQuery}`; // Add the query as a query string parameter
  
    console.log(`Sending query to API: ${apiUrl}`); // Log the full API URL for debugging
  
    const response = await fetch(apiUrl, {
      method: 'POST', // The API expects a POST request
      headers: {
        'Content-Type': 'application/json', // Specify JSON format for any additional headers
      },
    });
  
    // Check if the response is successful
    if (!response.ok) {
      throw new Error(`Query failed with status: ${response.status} - ${response.statusText}`);
    }
  
    return await response.json(); // Parse and return the JSON response
  }
  
  