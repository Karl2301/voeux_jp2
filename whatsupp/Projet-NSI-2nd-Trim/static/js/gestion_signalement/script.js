function banUser(user_id, ban_id) {
    fetch('/ban-user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: user_id, ban_id: ban_id })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Erreur:', error);
    });
}


document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.ban').forEach(button => {
        button.addEventListener('click', function() {
            handleReport(this.dataset.id, 'ban');
        });
    });

    document.querySelectorAll('.refuse').forEach(button => {
        button.addEventListener('click', function() {
            handleReport(this.dataset.id, 'refuse');
        });
    });

    document.querySelectorAll('.warn').forEach(button => {
        button.addEventListener('click', function() {
            handleReport(this.dataset.id, 'warn');
        });
    });
});

function handleReport(reportId, action) {
    console.log("reportId: "+reportId)
    console.log("action: "+action)
    fetch('/handle_report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ report_id: reportId, action: action }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Action effectuée avec succès.');
            location.reload(); // Recharger la page après l'action
        } else {
            alert('Erreur : ' + data.error);
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        alert('Erreur lors du traitement de la requête.');
    });
}


