document.addEventListener("DOMContentLoaded", function () {
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