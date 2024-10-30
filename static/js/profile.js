// profile-stats.js

document.addEventListener('DOMContentLoaded', function() {
    const userId = document.querySelector('body').dataset.userId;
    const statsContainer = document.querySelector('#user-stats');

    if (userId && statsContainer) {
        fetch(`/api/users/${userId}/stats`)
            .then(response => response.json())
            .then(data => {
                statsContainer.innerHTML = `
                    <p><strong>Score:</strong> ${data.score}</p>
                    <p><strong>Victoire Royale:</strong> ${data.victories}</p>
                    <p><strong>Matchs Joués:</strong> ${data.matches}</p>
                `;
            })
            .catch(error => console.error('Error fetching user stats:', error));
    }
});
