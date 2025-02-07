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
    let voeux = data.voeux_etablissements;

    console.log('Type of voeux:', typeof voeux);
    console.log('Content of voeux:', voeux);

    // Convertir la chaîne JSON en tableau
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
        updateRowNumbers(); // Appeler updateRowNumbers après avoir ajouté les lignes
    } else {
        console.error('voeux_etablissements is not an array:', voeux);
    }
}

window.onload = fetchVoeux;