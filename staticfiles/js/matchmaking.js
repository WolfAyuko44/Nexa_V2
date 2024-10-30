// matchmaking.js

document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.querySelector('#filter-form');
    const resultsContainer = document.querySelector('#results');

    if (filterForm) {
        filterForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(filterForm);
            const params = new URLSearchParams(formData).toString();

            fetch(`/api/matchmaking?${params}`)
                .then(response => response.json())
                .then(data => {
                    resultsContainer.innerHTML = data.players.map(player => `
                        <div class="player">
                            <p><strong>${player.username}</strong></p>
                            <p>Rank: ${player.rank}</p>
                            <p>Region: ${player.region}</p>
                        </div>
                    `).join('');
                })
                .catch(error => console.error('Error fetching players:', error));
        });
    }
});
