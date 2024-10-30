// footer.js

document.addEventListener('DOMContentLoaded', function() {
    // Fonction pour afficher un message de confirmation lors du clic sur un lien de politique de confidentialité
    const privacyLinks = document.querySelectorAll('.footer-section.links a[href*="privacy_policy"]');
    privacyLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            if (!confirm('Êtes-vous sûr de vouloir lire notre politique de confidentialité ?')) {
                event.preventDefault(); // Annule le lien si l'utilisateur annule
            }
        });
    });

    // Fonction pour afficher une notification simple lors du clic sur des icônes de réseaux sociaux
    const socialLinks = document.querySelectorAll('.social-links a');
    socialLinks.forEach(link => {
        link.addEventListener('click', function() {
            alert('Merci de nous suivre sur les réseaux sociaux !');
        });
    });
});
