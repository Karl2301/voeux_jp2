
document.addEventListener("DOMContentLoaded", function () {
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

    

    const checkbox = document.getElementById("checkbox");
    const body = document.body;

    function updateTheme() {
        if (localStorage.getItem("dark-theme") === "enabled") {
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
        }
        updateTheme();
    });

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
        } else {
            body.classList.remove("dark");
            localStorage.setItem("dark-theme", "disabled");
        }
    });
  }
);  




window.onload = fetchVoeux;