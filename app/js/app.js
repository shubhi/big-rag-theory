/**
 * Handle file upload
 */
function uploadFile() {
    const fileInput = document.getElementById('fileInput'); // Get the file input element
    const responseBox = document.getElementById('responseBox'); // Get the response box element
  
    // Check if a file is selected
    if (!fileInput.files.length) {
      responseBox.innerHTML = '<p style="color: red;">Please select a file to upload.</p>';
      return;
    }
  
    const file = fileInput.files[0]; // Get the first selected file
  
    // Validate file type
    if (file.type !== 'application/pdf') {
      responseBox.innerHTML = '<p style="color: red;">Only PDF files are allowed. Please try again.</p>';
      return;
    }
  
    setLoading('Uploading file...'); // Display a loading message
  
    // Call the API to upload the file
    uploadFileToAPI(file)
      .then((response) => {
        responseBox.innerHTML = `<p style="color: green;">${response.message || 'File uploaded successfully!'}</p>`;
      })
      .catch((error) => {
        console.error(error);
        responseBox.innerHTML = '<p style="color: red;">File upload failed. Please try again.</p>';
      })
      .finally(clearLoading); // Clear the loading message
  }
  
  /**
   * Handle query submission
   */
  async function sendQuery() {
  const queryInput = document.getElementById('userQuery');
  const responseBox = document.getElementById('responseBox');

  // Get the user's query
  const userQuery = queryInput.value.trim();
  if (!userQuery) {
    responseBox.innerHTML = '<p style="color: red;">Please enter a query.</p>';
    return;
  }

  try {
    // Send the query to the API
    const response = await sendQueryToAPI(userQuery);

    // Display the answer from the API
    if (response && response.answer) {
      responseBox.innerHTML = `<p style="color: green;">${response.answer}</p>`;
    } else {
      responseBox.innerHTML = '<p style="color: red;">No answer received from the API.</p>';
    }
  } catch (error) {
    console.error('Error in sendQuery:', error);
    responseBox.innerHTML = '<p style="color: red;">Failed to fetch the answer. Please try again.</p>';
  }
}

  
  /**
   * Helper function to show a loading message
   * @param {string} message - The loading message to display
   */
  function setLoading(message) {
    const responseBox = document.getElementById('responseBox'); // Get the response box element
    responseBox.innerHTML = `<p style="color: blue;">${message}</p>`;
  }
  
  /**
   * Helper function to clear the loading message
   */
  function clearLoading() {
    const responseBox = document.getElementById('responseBox'); // Get the response box element
    responseBox.innerHTML = ''; // Clear the content
  }
  