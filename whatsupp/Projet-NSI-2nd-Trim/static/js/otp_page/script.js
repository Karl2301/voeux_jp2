document.getElementById('reset-password-button').addEventListener('click', function(event) {
    event.preventDefault(); // Empêche toute action par défaut

    // Récupère les valeurs des inputs
    var newPassword = document.getElementById('new-password').value;
    var confirmPassword = document.getElementById('confirm-password').value;

    // Vérifie que les nouveaux mots de passe correspondent
    if (newPassword !== confirmPassword) {
        alert('Les nouveaux mots de passe ne correspondent pas.');
        return;
    }

    // Récupère le reset_id depuis l'URL
    var url = window.location.pathname;
    var partieApresDashboard = url.split("/new_password/")[1];
    console.log(partieApresDashboard)
    if (partieApresDashboard != undefined) {
        var token = partieApresDashboard.replace("/", "")
        console.log(token)
        resetPassword(token, newPassword, confirmPassword);
    }

    // Appelle la fonction pour réinitialiser le mot de passe
});

function resetPassword(resetId, newPassword, confirmPassword) {
    fetch(`/new_password/${resetId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password: newPassword, confirm_password: confirmPassword }),
    })
    .then(response => {
        return response.json().then(data => ({ status: response.status, body: data }));
    })
    .then(data => {
        if (data.status === 400) {
            alert(data.body.error); // Afficher le message d'erreur
        } else if (data.body.success) {
            window.location.href = '/login';
            // Réinitialiser les champs d'entrée
            document.getElementById('new-password').value = '';
            document.getElementById('confirm-password').value = '';
        } else {
            alert('Erreur lors de la réinitialisation du mot de passe.');
        }
    });
}
