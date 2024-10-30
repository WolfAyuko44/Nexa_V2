// content-sharing.js

document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.querySelector('#upload-form');
    const contentList = document.querySelector('#content-list');

    if (uploadForm) {
        uploadForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(uploadForm);

            fetch('/api/upload', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCSRFToken()  // Adjust according to your setup
                }
            })
            .then(response => response.json())
            .then(data => {
                contentList.innerHTML += `
                    <div class="content-item">
                        <p><strong>${data.username}</strong></p>
                        <img src="${data.url}" alt="Shared content">
                    </div>
                `;
            })
            .catch(error => console.error('Error uploading content:', error));
        });
    }

    function getCSRFToken() {
        const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        return token;
    }
});
