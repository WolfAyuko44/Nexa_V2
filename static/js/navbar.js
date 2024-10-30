// navbar.js

document.addEventListener("DOMContentLoaded", function () {
    // Sélectionner les éléments
    const navbarToggle = document.querySelector(".navbar-toggle");
    const navbarMenu = document.querySelector(".navbar-menu");
    const dropdownToggles = document.querySelectorAll(".dropdown-toggle");

    // Gestion du toggle pour le menu mobile
    if (navbarToggle) {
        navbarToggle.addEventListener("click", function () {
            navbarMenu.classList.toggle("open");
        });
    }

    // Gestion des dropdowns dans le menu
    dropdownToggles.forEach(function (toggle) {
        toggle.addEventListener("click", function (event) {
            event.preventDefault();
            const dropdown = this.nextElementSibling;
            dropdown.classList.toggle("show");

            // Fermer les autres dropdowns s'ils sont ouverts
            dropdownToggles.forEach(function (otherToggle) {
                if (otherToggle !== toggle) {
                    otherToggle.nextElementSibling.classList.remove("show");
                }
            });
        });
    });

    // Fermer le menu dropdown si on clique en dehors
    document.addEventListener("click", function (event) {
        if (!event.target.closest(".dropdown")) {
            dropdownToggles.forEach(function (toggle) {
                toggle.nextElementSibling.classList.remove("show");
            });
        }
    });
});
