console.log('Script loaded successfully!');

// DOMContent Loaded Event means the HTML is fully loaded and parsed
// This is where we can safely manipulate the DOM and add event listeners
// DOM stands for Document Object Model, which is a representation of the HTML document
// Event listeners are functions that wait for a specific event to occur, like a button click or a form submission
// this script runs when the DOM is ready, ensuring all elements are available for manipulation and interaction

document.addEventListener('DOMContentLoaded', function () {
    const imageInput = document.getElementById('image-input');
    // preview is the image element where the uploaded image will be displayed
    // meaning of image emlement: it is an HTML element that displays images on a webpage, its type is <img>
    const preview = document.getElementById('image-preview');
    const form = document.getElementById('image-form');
    const resultContainer = document.getElementById('prediction-result');

    // Preview uploaded image
    imageInput.addEventListener('change', function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });

    // Handle form submission
    // below event listener is for the form submission, it prevents the default behavior of the form (which is to reload the page)
    // and instead sends the image to the server for prediction
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        // imageInput looks like <input type="file" id="image-input" accept="image/*">
        // why .files used with imageInput, its because .files is a property of the input element that contains the list of files selected by the user
        // but this list only contain images, because of the accept="image/*" attribute in the input element

        const file = imageInput.files[0];
        if (!file) {
            alert('Please upload an image first.');
            return;
        }

        // Create a FormData object to send the image file
        // FormData is a built-in JavaScript object that allows you to easily construct a set of key/value pairs representing form fields and their values, which can then be sent using the Fetch API or XMLHttpRequest
        // it is used to send files and other data to the server in a format that can be easily processed by the server
        // here we are appending the image file to the FormData object with the key 'image'
        // the key 'image' is used to identify the file on the server side, so the server knows what to do with the file when it receives it
        const formData = new FormData();
        formData.append("file", file);
        // formdata looks like this:
        // FormData { 'image': [file] }

        // Example: replace with your backend endpoint
        // Fetch API is used to send the image to the server for prediction
        // fetch is a built-in JavaScript function that allows you to make network requests to servers
        // it returns a Promise that resolves to the Response object representing the response to the request
        // the Response object contains the data returned by the server
        // so when we call fetch('/predict', { method: 'POST', body: formData }), we are sending a POST request to the '/predict' endpoint on the server with the image file in the body of the request
        // the server will then process the image and return a prediction, which we will display in the resultContainer
        fetch('http://localhost:8000/predict', {
            method: 'POST',
            body: formData
        })
        .then(async response => {
            if (!response.ok) {
                const text = await response.text();  // Read the HTML or error text
                throw new Error(`HTTP ${response.status}: ${text}`);
            }
            return response.json();
        })
        .then(data => {
            const pred = data.prediction;
            resultContainer.innerHTML = `
                <div class="result-box" style="border: 2px solid #4CAF50; padding: 10px 20px; margin-top: 20px; background-color: #f9f9f9;" align="left">
                    <h3 style="padding-top: 5px;">Prediction:</h3>
                    <ul style="padding-top: 15px">
                        <li><strong>Article Type:</strong> ${pred.articleType}</li>
                        <li><strong>Color:</strong> ${pred.baseColour}</li>
                        <li><strong>Season:</strong> ${pred.season}</li>
                        <li><strong>Gender:</strong> ${pred.gender}</li>
                    </ul>
                </div>
            `;
        })
        .catch(error => {
            console.error('Error:', error);
            resultContainer.innerHTML = `<p style="color:red;">Prediction failed. Try again.</p>`;
        });
    });
});
