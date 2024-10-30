// notifications.js

document.addEventListener('DOMContentLoaded', function() {
    const notificationsContainer = document.querySelector('#notifications');

    function fetchNotifications() {
        fetch('/api/notifications')
            .then(response => response.json())
            .then(data => {
                notificationsContainer.innerHTML = data.notifications.map(notification => `
                    <div class="notification">
                        <p><strong>${notification.title}</strong>: ${notification.message}</p>
                    </div>
                `).join('');
            })
            .catch(error => console.error('Error fetching notifications:', error));
    }

    // Fetch notifications every 30 seconds
    setInterval(fetchNotifications, 30000);
    fetchNotifications();
});
