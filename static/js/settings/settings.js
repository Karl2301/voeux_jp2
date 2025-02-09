document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("theme-toggle");
    const body = document.body;
    const siteToggle = document.getElementById("site-toggle");
    
    if (localStorage.getItem("dark-theme") === "enabled") {
        body.classList.add("dark-theme");
        themeToggle.textContent = "☀️";
    }

    themeToggle.addEventListener("click", function () {
        body.classList.toggle("dark-theme");
        if (body.classList.contains("dark-theme")) {
            localStorage.setItem("dark-theme", "enabled");
            themeToggle.textContent = "☀️";
        } else {
            localStorage.setItem("dark-theme", "disabled");
            themeToggle.textContent = "🌙";
        }
    });

    siteToggle.addEventListener("click", function () {
        if (siteToggle.textContent === "Ouvert") {
            siteToggle.textContent = "Fermé";
            siteToggle.style.backgroundColor = "red";
        } else {
            siteToggle.textContent = "Ouvert";
            siteToggle.style.backgroundColor = "green";
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("theme-toggle");
    const body = document.body;

    function updateTheme() {
        if (localStorage.getItem("dark-theme") === "enabled") {
            body.style.backgroundColor = "#2e2e2e"; // Gris foncé élégant
            themeToggle.textContent = "Désactiver";
        } else {
            body.style.backgroundColor = "#f4f4f4"; // Gris clair agréable
            themeToggle.textContent = "Activer";
        }
    }

    themeToggle.addEventListener("click", function () {
        if (localStorage.getItem("dark-theme") === "enabled") {
            localStorage.setItem("dark-theme", "disabled");
        } else {
            localStorage.setItem("dark-theme", "enabled");
        }
        updateTheme();
    });

    updateTheme(); // Appliquer le thème au chargement
});

