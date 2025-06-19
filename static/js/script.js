document.addEventListener('DOMContentLoaded', function () {
    const imageInput = document.getElementById('image-input');
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
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const file = imageInput.files[0];
        if (!file) {
            alert('Please upload an image first.');
            return;
        }

        const formData = new FormData();
        formData.append('image', file);

        // Example: replace with your backend endpoint
        fetch('/predict', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                resultContainer.innerHTML = `<p><strong>Prediction:</strong> ${data.prediction}</p>`;
            })
            .catch(error => {
                console.error('Error:', error);
                resultContainer.innerHTML = `<p style="color:red;">Prediction failed. Try again.</p>`;
            });
    });
});
