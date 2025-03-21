// add hovered class to selected list item
let list = document.querySelectorAll(".navigation li");

const validateBtn = document.getElementById('validateBtn');


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

document.getElementById('modifyBtn').addEventListener('click', async function() {
    var el = document.getElementById('sortable');
    var modifyBtn = document.getElementById('modifyBtn');
    var container = document.getElementById('recentOrdersContainer');
    var editModeMessage = document.getElementById('editModeMessage');
    
    if (modifyBtn.textContent === "Modifier") {
        modifyBtn.textContent = "Enregistrer";
        modifyBtn.style.backgroundColor = "green";
        container.classList.add('edit-mode');
        editModeMessage.style.display = "block";
        var sortable = Sortable.create(el, {
            animation: 150,
            ghostClass: 'blue-background-class',
            onUpdate: function () {
                updateRowNumbers();
            }
        });
    } else {
        modifyBtn.textContent = "Modifier";
        modifyBtn.style.backgroundColor = "";
        container.classList.remove('edit-mode');
        editModeMessage.style.display = "none";
        Sortable.get(el).destroy();

        // Enregistrer les données mises à jour
        const updatedData = getUpdatedData();
        try {
            const response = await fetch('/update_data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(updatedData)
            });
            const result = await response.json();
            if (result.success) {
                console.log('Données mises à jour avec succès');
            } else {
                console.error('Erreur lors de la mise à jour des données:', result.message);
            }
        } catch (error) {
            console.error('Erreur lors de la requête de mise à jour:', error);
        }
    }
});

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

        validateBtn.style.display = "none";  // Cache le bouton immédiatement si validé

        console.log("Professeurrr");
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
                    <a href="/classe/${classe}" class="card-link" style="text-decoration: none;">
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

                // Insérer le conteneur de cartes juste après la barre séparatrice (<hr class="barre-separatrice">)
                const hr = document.querySelector('.barre-separatrice');
                if (hr) {
                    hr.insertAdjacentElement('afterend', cardContainer);
                } else {
                    console.error('La barre séparatrice n\'a pas été trouvée.');
                }
            } else {
                console.error('niveau_classe n\'est pas un tableau:', niveauClasseArray);
            }
        }

        // Mise à jour des statistiques pour le professeur
        const elevesConnectes = document.getElementById('elevesConnectes');
        const elevesValideVoeux = document.getElementById('elevesValideVoeux');
        const vosMessagesDemandes = document.getElementById('vosMessagesDemandes');
        const nombreClasses = document.getElementById('nombreClasses');

        if (elevesConnectes) {
            elevesConnectes.textContent = data.eleve_online;
        }
        if (elevesValideVoeux) {
            elevesValideVoeux.textContent = data.eleve_choix_validees;
        }
        if (vosMessagesDemandes) {
            vosMessagesDemandes.textContent = data.identifiant_perdus;
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
    const elevesConnectes = document.getElementById('elevesConnectes');
    const elevesValideVoeux = document.getElementById('elevesValideVoeux');
    const vosMessagesDemandes = document.getElementById('vosMessagesDemandes');
    const nombreClasses = document.getElementById('nombreClasses');

    // Récupérer le cookie session_cookie
    const sessionCookie = document.cookie
        .split('; ')
        .find(row => row.startsWith('session_cookie='))
        ?.split('=')[1];

    if (sessionCookie) {
        // Envoyer le cookie au serveur après connexion
        console.log('Envoi du cookie session_cookie au serveur WebSocket');
        socket.emit('join', { session_cookie: sessionCookie });
    } else {
        console.warn("Aucun cookie 'session_cookie' trouvé");
    }

    // Écouter les messages du serveur
    socket.on('message', function (data) {
        console.log('Message reçu:', data);
        if (data.total_online_students !== undefined) {
            console.log('Mise à jour du nombre d\'élèves connectés:', data.total_online_students);
            if (elevesConnectes) {
                elevesConnectes.textContent = data.total_online_students;
            } else {
                console.error('Élément avec l\'ID "elevesConnectes" non trouvé');
            }
        }
    });

    // Détecter la déconnexion
    socket.on('disconnect', function () {
        console.log('Déconnecté du serveur WebSocket');
    });

    // Optionnel : Détecter la fermeture de la fenêtre/navigateur
    window.addEventListener('beforeunload', function () {
        console.log('Fermeture de la fenêtre détectée, déconnexion...');
        socket.disconnect();
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


document.addEventListener("DOMContentLoaded", async function() {
    const modifyBtn = document.getElementById('modifyBtn');

    // Vérifier si les vœux sont validés depuis la base de données
    try {
        const response = await fetch('/get_voeux_status', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        const data = await response.json();
        console.log('Statut des vœux:', data);
        if (data.choix_validees) {
            modifyBtn.style.display = "none";  // Cache le bouton immédiatement si validé
            validateBtn.style.pointerEvents = "none"; // Désactive le bouton "Valider"
            validateBtn.style.opacity = "0.6"; // Rend le bouton "Valider" visuellement désactivé
        }
    } catch (error) {
        console.error("Erreur lors de la récupération du statut des vœux :", error);
    }

});

validateBtn.addEventListener('click', async function() {
    try {
        const response = await fetch('/validate_voeux', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ validate: true })
        });

        const data = await response.json();
        if (data.success) {
            alert('Vos vœux ont été validés avec succès.');
            validateBtn.style.pointerEvents = "none"; // Désactive le bouton "Valider"
            validateBtn.style.opacity = "0.6"; // Rend le bouton "Valider" visuellement désactivé
            modifyBtn.style.display = "none"; // Cache le bouton "Modifier"
        } else {
            console.error('Erreur lors de la validation des vœux:', data.message);
        }
    } catch (error) {
        console.error('Erreur lors de la requête de validation:', error);
    }
});