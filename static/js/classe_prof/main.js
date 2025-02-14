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


document.getElementById('siteStatusCard').addEventListener('click', function() {
  var statusElement = document.getElementById('siteStatus');
  if (statusElement.textContent === "Ouvert") {
      statusElement.textContent = "Fermé";
      statusElement.style.color = "red";
  } else {
      statusElement.textContent = "Ouvert";
      statusElement.style.color = "green";
  }
});



async function fetchVoeux() {
    const response = await fetch('/get_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const data = await response.json();
    console.log(data);
    let voeux = data.voeux_etablissements;

    if (data.professeur) {
        // Affichage des éléments spécifiques au professeur
        const cards = document.querySelectorAll('.cardBox');
        cards.forEach(card => {
            card.style.display = 'grid';
        });

        const elevesNav = document.getElementById('eleves_nav');
        if (elevesNav) {
            elevesNav.style.display = 'block';
        }
        const notificationNav = document.getElementById('notification_nav');
        if (notificationNav) {
            notificationNav.style.display = 'block';
        }

        // --- Création d'un conteneur en ligne pour afficher chaque classe ---
        if (data.niveau_classe) {
            let niveauClasseArray = data.niveau_classe;
            // Si la donnée est une chaîne JSON, la convertir en tableau
            if (typeof niveauClasseArray === 'string') {
                try {
                    niveauClasseArray = JSON.parse(niveauClasseArray);
                } catch (error) {
                    console.error('Erreur lors de la conversion de niveau_classe en tableau:', error);
                    return;
                }
            }
            if (Array.isArray(niveauClasseArray)) {
                // Créer un conteneur pour les cartes (classes) qui s'afficheront en ligne
                const cardContainer = document.createElement('div');
                cardContainer.classList.add('cardContainer'); // Ce conteneur sera mis en forme en ligne via le CSS

                // Pour chaque valeur de niveau_classe, créer une carte
                niveauClasseArray.forEach(classe => {
                    const card = document.createElement('div');
                    card.classList.add('cardBox'); 
                    card.innerHTML = `
                        <a href="/classes/${classe}" class="card-link" style="text-decoration: none;">
                            <div class="card">
                                <div>
                                    <div class="numbers">${classe}</div>
                                    <div class="cardName">Classe</div>
                                </div>
                                <div class="iconBx">
                                    <!-- inutile je pense -->
                                </div>
                            </div>
                        </a>
                    `;
                    cardContainer.appendChild(card);
                });
            } else {
                console.error('niveau_classe n\'est pas un tableau:', niveauClasseArray);
            }
        }

        // Mise à jour des statistiques pour le professeur
        const elevesConnectes = document.getElementById('elevesConnectes');
        const elevesValideVoeux = document.getElementById('elevesValideVoeux');
        const nombreClasses = document.getElementById('nombreClasses');

        if (elevesConnectes) {
            elevesConnectes.textContent = data.eleve_online;
        }
        if (elevesValideVoeux) {
            elevesValideVoeux.textContent = data.eleve_choix_validees;
        }
        if (nombreClasses) {
            nombreClasses.textContent = data.classes;
        }
        console.log("Professeur");
    } else {
        // Pour l'élève : afficher le tableau des vœux
        const tableVoeux = document.querySelectorAll('.details');
        tableVoeux.forEach(table => {
            table.style.display = 'block';
        });

        console.log("Elève");
        console.log('Type of voeux:', typeof voeux);
        console.log('Content of voeux:', voeux);

        // Convertir la chaîne JSON en tableau si nécessaire
        if (typeof voeux === 'string') {
            try {
                voeux = JSON.parse(voeux);
            } catch (error) {
                console.error('Erreur lors de la conversion de voeux en tableau:', error);
                return;
            }
        }

        if (Array.isArray(voeux)) {
            const tbody = document.getElementById('sortable');
            if (!tbody) {
                console.error('Element with id "sortable" not found.');
                return;
            }
            voeux.forEach((item, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td class="row-number">${index + 1}</td>
                    <td>${item.school}</td>
                    <td>${item.city}</td>
                    <td>${item.degree}</td>
                    <td>${item.specialization}</td>
                `;
                tbody.appendChild(row);
            });
            updateRowNumbers(); // Mise à jour des numéros de ligne
        } else {
            console.error('voeux_etablissements is not an array:', voeux);
        }
    }
}





document.addEventListener('DOMContentLoaded', function () {
    var protocol = location.protocol === 'https:' ? 'wss://' : 'ws://';
    var socket = io.connect(protocol + document.domain + ':' + location.port);

    // Récupérer le cookie session_cookie
    const sessionCookie = document.cookie
        .split('; ')
        .find(row => row.startsWith('session_cookie='))
        ?.split('=')[1];

    if (sessionCookie) {
        // Envoyer le cookie au serveur après connexion
        socket.emit('join', { session_cookie: sessionCookie });
    } else {
        console.warn("Aucun cookie 'session_cookie' trouvé");
    }

    // Écouter les messages du serveur
    socket.on('message', function (data) {
        console.log('Message reçu:', data);
    });

    // Détecter la déconnexion
    window.addEventListener('beforeunload', function () {
        socket.emit('disconnect_user', { session_cookie: sessionCookie });
    });
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
window.onload = async function() {
    await fetchVoeux();
}
