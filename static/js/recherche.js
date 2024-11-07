// recherche.js

document.getElementById('search-input').addEventListener('input', function() {
    const query = this.value;
    const resultsContainer = document.getElementById('results-container');
    const resultsList = document.getElementById('results-list');
    resultsList.innerHTML = '';  // Réinitialise les résultats

    if (query.length > 0) {
        fetch(`{% url 'recherche:recherche_utilisateur' %}?q=${query}`)
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newResultsList = doc.getElementById('results-list');
                resultsList.innerHTML = newResultsList.innerHTML;

                if (resultsList.children.length === 0) {
                    resultsList.innerHTML = '<p class="no-results">Aucun utilisateur trouvé.</p>';
                }
            })
            .catch(error => console.error('Erreur lors de la recherche:', error));
    } else {
        resultsList.innerHTML = ''; // Efface les résultats si la barre de recherche est vide
    }
});
