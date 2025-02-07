document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('forgot-password-button').addEventListener('click', function(event) {
        event.preventDefault(); // Empêche toute action par défaut

        // Récupère l'email
        var email = document.getElementById('forgot-password-email').value;

        // Appelle la fonction pour envoyer le lien de réinitialisation du mot de passe
        requestPasswordReset(email);
    });
});

function requestPasswordReset(email) {
    fetch('/reset_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email }),
    })
    .then(response => {
        return response.json().then(data => ({ status: response.status, body: data }));
    })
    .then(data => {
        if (data.status === 404) {
            alert(data.body.error); // Afficher le message d'erreur
        } else if (data.body.success) {
            window.location.href = '/email_sent';
            document.getElementById('forgot-password-email').value = '';
        } else {
            alert('Une demande de réinitialisation de mot de passe a déjà été envoyée pour cet email. Ou cette email n\'existe pas.');
        }
    });
}
