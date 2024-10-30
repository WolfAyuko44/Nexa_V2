// private-messaging.js

document.addEventListener('DOMContentLoaded', function() {
    const messageForm = document.querySelector('#message-form');
    const messagesContainer = document.querySelector('#messages');
    const userId = document.querySelector('body').dataset.userId;

    if (messageForm) {
        messageForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(messageForm);
            formData.append('user_id', userId);

            fetch('/api/messages', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCSRFToken()  // Adjust according to your setup
                }
            })
            .then(response => response.json())
            .then(data => {
                messagesContainer.innerHTML += `
                    <div class="message">
                        <p><strong>${data.username}</strong>: ${data.message}</p>
                    </div>
                `;
            })
            .catch(error => console.error('Error sending message:', error));
        });
    }

    function getCSRFToken() {
        const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        return token;
    }
});
