// add hovered class to selected list item
let list = document.querySelectorAll(".navigation li");

function activeLink() {
  list.forEach((item) => {
    item.classList.remove("hovered");
  });
  this.classList.add("hovered");
}

list.forEach((item) => item.addEventListener("mouseover", activeLink));

// Menu Toggle
let toggle = document.querySelector(".toggle");
let navigation = document.querySelector(".navigation");
let main = document.querySelector(".main");

toggle.onclick = function () {
  navigation.classList.toggle("active");
  main.classList.toggle("active");
};

function getUpdatedData() {
    // Récupérer les données mises à jour depuis le DOM
    const rows = document.querySelectorAll('#sortable tr');
    const updatedData = [];
    rows.forEach(row => {
        const rowNumber = row.querySelector('td:nth-child(1)').textContent;
        const school = row.querySelector('td:nth-child(2)').textContent;
        const city = row.querySelector('td:nth-child(3)').textContent;
        const degree = row.querySelector('td:nth-child(4)').textContent;
        const specialization = row.querySelector('td:nth-child(5)').textContent;
        updatedData.push({ row_number: parseInt(rowNumber), school, city, degree, specialization });
    });
    return updatedData;
}


async function fetchVoeux() {
    const response = await fetch('/get_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const data = await response.json();
    console.log(data)
    let voeux = data.voeux_etablissements;

    // Vérifier si l'utilisateur est un élève
    if (data.professeur) {
        // Cacher 
                
        const elevesNav = document.getElementById('eleves_nav');
        if (elevesNav) {
            elevesNav.style.display = 'block';
        }

        const notificationNav = document.getElementById('notification_nav');
        if (notificationNav) {
            notificationNav.style.display = 'block';
        }

    }

    if(!data.professeur) {
        console.log("Eleve")
    } else {
        console.log("Professeur")
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const body = document.body;
    const dashboardTheme = body.getAttribute("data-theme");

    if (dashboardTheme === "1") {
        body.classList.add("dark");  // Applique le mode sombre
    } else {
        body.classList.remove("dark");  // Applique le mode clair
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const body = document.body;
    const recentOrdersContainer = document.getElementById('recentOrdersContainer');
    fetch('/get_theme', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.darkTheme === true) {
            body.classList.add("dark");
            localStorage.setItem("dark-theme", "enabled");
            if (recentOrdersContainer) {
                recentOrdersContainer.style.backgroundColor = "#333333";
            }
            body.style.color = "white"; // Set text color to white
        } else {
            body.classList.remove("dark");
            localStorage.setItem("dark-theme", "disabled");
            if (recentOrdersContainer) {
                recentOrdersContainer.style.backgroundColor = "";
            }
            body.style.color = ""; // Reset text color
        }
    });
});

window.onload = fetchVoeux;