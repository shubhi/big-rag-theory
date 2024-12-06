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
  function sendQuery() {
    const queryInput = document.getElementById('userQuery').value.trim(); // Get the query input value
    const responseBox = document.getElementById('responseBox'); // Get the response box element
  
    // Check if a query is entered
    if (!queryInput) {
      responseBox.innerHTML = '<p style="color: red;">Please enter a query.</p>';
      return;
    }
  
    setLoading('Processing query...'); // Display a loading message
  
    // Call the API to process the query
    sendQueryToAPI(queryInput)
      .then((response) => {
        responseBox.innerHTML = `<p style="color: green;">${response.answer || 'Response received!'}</p>`;
      })
      .catch((error) => {
        console.error(error);
        responseBox.innerHTML = '<p style="color: red;">Query failed. Please try again.</p>';
      })
      .finally(clearLoading); // Clear the loading message
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
  