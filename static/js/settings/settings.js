document.addEventListener("DOMContentLoaded", function () {
<<<<<<< HEAD
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
=======
    const checkbox = document.getElementById("checkbox");
>>>>>>> ff0dfbf (update project)
    const body = document.body;

    function updateTheme() {
        if (localStorage.getItem("dark-theme") === "enabled") {
<<<<<<< HEAD
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
=======
            body.classList.add("dark");
            checkbox.checked = true;
        } else {
            body.classList.remove("dark");
            checkbox.checked = false;
        }

        fetch('/update-theme', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify({ darkTheme: checkbox.checked })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }


    checkbox.addEventListener("change", function () {
        if (checkbox.checked) {
            localStorage.setItem("dark-theme", "enabled");
        } else {
            localStorage.setItem("dark-theme", "disabled");
>>>>>>> ff0dfbf (update project)
        }
        updateTheme();
    });

<<<<<<< HEAD
    updateTheme(); // Appliquer le thème au chargement
});

=======
    updateTheme();
});

// Menu Toggle
let toggle = document.querySelector(".toggle");
let navigation = document.querySelector(".navigation");
let main = document.querySelector(".main");

toggle.onclick = function () {
  navigation.classList.toggle("active");
  main.classList.toggle("active");
};

function updateRowNumbers() {
  const rows = document.querySelectorAll('#sortable tr');
  rows.forEach((row, index) => {
    const rowNumberElement = row.querySelector('.row-number');
    if (rowNumberElement) {
      rowNumberElement.textContent = index + 1;
    } else {
      console.error('Element with class "row-number" not found in row:', row);
    }
  });
}
>>>>>>> ff0dfbf (update project)
