document.querySelector('.cta-button').addEventListener('click', function() {
    const message = currentLanguage === 'English' ? 
        'Welcome to Nexa! Our registration process is coming soon...' :
        'Bienvenue sur Nexa ! Notre processus d\'inscription arrive bientôt...';
    alert(message);
});

const languageToggle = document.getElementById('languageToggle');
let currentLanguage = 'English';

function updateLanguage(lang) {
    document.querySelectorAll('[data-en]').forEach(elem => {
        elem.textContent = elem.getAttribute(`data-${lang.toLowerCase()}`);
    });
}

languageToggle.addEventListener('click', function() {
    if (currentLanguage === 'English') {
        currentLanguage = 'Français';
        this.textContent = 'Français';
        updateLanguage('fr');
    } else {
        currentLanguage = 'English';
        this.textContent = 'English';
        updateLanguage('en');
    }
});

function isElementInViewport(el) {
    var rect = el.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

function animateOnScroll() {
    var items = document.querySelectorAll('.feature-item, .functionality-item, .hero h1, .hero p, .hero .cta-button');
    items.forEach(item => {
        if (isElementInViewport(item)) {
            item.classList.add('fade-in-up');
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    animateOnScroll();
});

window.addEventListener('scroll', animateOnScroll);
window.addEventListener('load', animateOnScroll);

const notificationSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/notifications/'
);

notificationSocket.onmessage = function(e) {
       const data = JSON.parse(e.data);
    alert('Nouvelle notification : ' + data.message);
};

notificationSocket.onclose = function(e) {
    console.error('Socket fermé de façon inattendue');
};

