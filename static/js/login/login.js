var identifiantSave = "";

document.addEventListener("DOMContentLoaded", function() {
    const identifiantInput = document.getElementById("identifiant");
    const identifiantContainer = document.getElementById("identifiant-container");
    const passwordContainer = document.getElementById("password-container");
  
    // Variable pour sauvegarder la valeur de l'identifiant
    let savedIdentifiant = "";
  
    identifiantInput.addEventListener("input", function() {
      // Exemple de condition : si l'identifiant saisi est "admin" temporaire
      if (this.value.trim().toLowerCase() === "compteprof") {
        // Sauvegarde de la valeur de l'identifiant
        savedIdentifiant = this.value;
        // Cache le champ identifiant
        identifiantContainer.style.display = "none";
        // Affiche le champ mot de passe
        passwordContainer.style.display = "block";
        console.log("Identifiant sauvegardé :", savedIdentifiant);
      } else {
        // Si la condition n'est pas validée, afficher l'identifiant et masquer le mot de passe
        identifiantContainer.style.display = "block";
        passwordContainer.style.display = "none";
      }
    });
  });

function send_login_post_data(event) {
  event.preventDefault();  // Empêche le rechargement de la page

  const identifiant = document.getElementById("identifiant").value;
  const password = document.getElementById("password").value;
  const data = { "identifiant": identifiant, "password": password };

  fetch("/login", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
  })
  .then((response) => response.json())
  .then((data) => {
      if (data.success) {
          document.cookie = `session_cookie=${data.cookie}; path=/`;
          window.location.href = "/dashboard";
      } else {
          alert(data.message);
      }
  })
  .catch((error) => {
      console.error("Erreur lors de la requête de connexion:", error);
  });
}