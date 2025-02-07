import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";

var url = window.location.pathname;
var partieApresDashboard = url.split("/dashboard/")[1];
console.log(partieApresDashboard)
if (partieApresDashboard != undefined) {
    var current_conv_with_user = partieApresDashboard.replace("/", "")
    console.log(current_conv_with_user)
}

document.addEventListener('DOMContentLoaded', function() {
    window.onbeforeunload = null;
    window.onunload = null;
    
    window.addEventListener('load', function() {
        window.print = function() {};
    });

    document.addEventListener('keydown', function(event) {
        if (event.key === 'p' && (event.ctrlKey || event.metaKey)) {
            event.preventDefault();
        }
    });

    // Autres scripts pour le dashboard
});

window.NewConvWithUser = function() {
    var username = document.getElementById('search-member-input').value;

    // Appel Ajax pour obtenir l'UUID du contact
    fetch('/search_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username })
    })
    .then(response => response.json())
    .then(data => {
        if (data.uuid) {
            // Redirection vers la page de conversation
            window.location.href = `/dashboard/${data.uuid}`;
            console.log(data.uuid);
        } else {
            alert('Utilisateur non trouvé');
        }
    })
    .catch((error) => {
        console.error('Erreur:', error);
    });
}




window.searchUsers = function() {

    var query = document.getElementById('search-input').value;

    fetch(`/search_users?query=${query}`)
        .then(response => response.json())
        .then(data => {
            var resultsContainer = document.getElementById('results');
            resultsContainer.innerHTML = '';

            if (data.length === 0) {
                resultsContainer.textContent = 'Aucun utilisateur avec ce nom d\'utilisateur existe';
                return;
            }

            data.forEach(function(user) {
                var li = document.createElement('li');
                li.className = 'card contact-item';
                li.innerHTML = `
                    <div class="card-body">
                        <div class="d-flex align-items-center">
                            <!-- Avatar -->
                            <div class="avatar me-4">
                                <img src="data:image/png;base64,${user.profile_image}" alt="${user.username}'s profile image" class="avatar-label bg-success text-white" style="border-radius: 50%;">
                            </div>
                            <!-- Avatar -->
                            <!-- Content -->
                            <div class="flex-grow-1 overflow-hidden">
                                <div class="d-flex align-items-center mb-1">
                                    <h5 class="text-truncate mb-0 me-auto">${user.first_name} ${user.last_name}</h5>
                                </div>
                                <div class="d-flex align-items-center">
                                    <div class="text-truncate me-auto">${user.username}</div>
                                </div>
                            </div>
                            <!-- Content -->
                            <!-- Dropdown -->
                            <div class="dropdown">
                                <button class="btn btn-icon btn-base btn-sm" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                    <i class="ri-more-fill"></i>
                                </button>
                                <ul class="dropdown-menu dropdown-menu-right">
                                    <li>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" onclick="sendFriendRequest('${user.id}')">Demander en amis<i class="ri-message-2-line"></i></a>
                                    </li>
                                    <li>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" onclick=" reportUser('${user.id}')">Signaler l'utilisateur<i class="ri-edit-line"></i></a>
                                    </li>
                                    <li>
                                        <div class="dropdown-divider"></div>
                                    </li>
                                    <li>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Bloquer l'utilisateur<i class="ri-forbid-line"></i></a>
                                    </li>
                                </ul>
                            </div>
                            <!-- Dropdown -->
                        </div>
                    </div>
                `;
                resultsContainer.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Erreur:', error);
        });
}
document.addEventListener('DOMContentLoaded', function() {
    fetch('/friend_requests')
        .then(response => response.json())
        .then(data => {
            var requestsContainer = document.getElementById('requestsFriendsRequest');
            requestsContainer.innerHTML = '';
            data.forEach(function(request) {
                var div = document.createElement('div');
                div.setAttribute('id', 'friends-request-'+request.id);
                div.className = 'card mb-3';
                div.innerHTML = `
                    <div class="card-body">
                        <div class="d-flex align-items-center">
                            <!-- Avatar -->
                            <div class="avatar me-4">
                                <img src="data:image/png;base64,${request.profile_image}" alt="${request.requester_first_name} ${request.requester_last_name}" class="avatar-label bg-soft-success text-success" style="border-radius: 50%; width: 50px; height: 50px;">
                            </div>
                            <!-- Avatar -->
                            <div class="flex-grow-1">
                                <div class="d-flex align-items-center overflow-hidden">
                                    <h5 class="me-auto text-break mb-0">${request.requester_first_name} ${request.requester_last_name}</h5>
                                    <span class="small text-muted text-nowrap ms-2">04:45 PM</span>
                                </div>
                                <div class="d-flex align-items-center">
                                    <div class="line-clamp me-auto">Vous a envoyé une demande d'ami</div>
                                    <div class="dropdown ms-5">
                                        <button class="btn btn-icon btn-base btn-sm" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                            <i class="ri-more-fill"></i>
                                        </button>
                                        <ul class="dropdown-menu">
                                            <li><a class="dropdown-item" href="#">See less often</a></li>
                                            <li><a class="dropdown-item" href="#">Hide</a></li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="card-footer">
                        <div class="row gx-4">
                            <div class="col">
                                <a href="#" onclick="rejectFriendRequest('${request.request_id}')" class="btn btn-secondary btn-sm w-100">Refuser</a>
                            </div>
                            <div class="col">
                                <button onclick="acceptFriendRequest('${request.request_id}')" class="btn btn-primary btn-sm w-100">Accepter</button>
                            </div>
                        </div>
                    </div>
                `;
                requestsContainer.appendChild(div);
            });
        })
        .catch(error => {
            console.error('Erreur:', error);
        });
});


window.sendFriendRequest = function(receiverId) {

    fetch('/send_friend_request', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ receiver_id: receiverId })
    })
    .then(response => response.json())
    .then(data => {
        ;   
    })
    .catch(error => {
        console.error('Erreur:', error);
    });
}


document.getElementById('save-password-button').addEventListener('click', function(event) {
    event.preventDefault(); // Empêche toute action par défaut

    // Récupère les valeurs des inputs
    var currentPassword = document.getElementById('current-password').value;
    var newPassword = document.getElementById('new-password').value;
    var confirmPassword = document.getElementById('confirm-password').value;

    // Vérifie que les nouveaux mots de passe correspondent
    if (newPassword !== confirmPassword) {
        alert('Les nouveaux mots de passe ne correspondent pas.');
        return;
    }

    // Appelle la fonction pour changer le mot de passe
    changePassword(currentPassword, newPassword);
});

function changePassword(currentPassword, newPassword) {
    fetch('/change_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ current_password: currentPassword, new_password: newPassword }),
    })
    .then(response => {
        return response.json().then(data => ({ status: response.status, body: data }));
    })
    .then(data => {
        if (data.status === 400) {
            alert(data.body.error); // Afficher le message d'erreur
        } else if (data.body.success) {
            alert('Mot de passe mis à jour avec succès.');
            // Réinitialiser les champs d'entrée
            document.getElementById('current-password').value = '';
            document.getElementById('new-password').value = '';
            document.getElementById('confirm-password').value = '';
        } else {
            alert('Erreur lors de la mise à jour du mot de passe.');
        }
    });
}



document.getElementById('save-button').addEventListener('click', function(event) {
    event.preventDefault(); // Empêche toute action par défaut

    // Récupère les valeurs des inputs
    var username = document.getElementById('username-input').value;
    var email = document.getElementById('email-input').value;
    var bio = document.getElementById('bio-input').value;
    var description = document.getElementById('description-input').value;

    // Appelle la fonction pour mettre à jour les informations de l'utilisateur
    updateUserInfo(username, email, bio, description);

});

function updateUserInfo(username, email, bio, description) {
    fetch('/update_user_info', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username, email: email, bio: bio, description: description }),
    })
    .then(response => {
        return response.json().then(data => ({ status: response.status, body: data }));
    })
    .then(data => {
        if (data.status === 409) {
            alert(data.body.error); // Afficher le message d'erreur
        } else if (data.body.success) {
            alert('Informations mises à jour avec succès.');
            document.getElementById('username').value = '';
            document.getElementById('email').value = '';
            document.getElementById('bio').value = '';
            document.getElementById('description').value = '';
        } else {
            alert('Erreur lors de la mise à jour des informations.');
        }
    });
}



document.addEventListener('DOMContentLoaded', function() {
    // Récupérer l'ID de l'utilisateur courant
    fetch('/get_user_id')
    .then(response => response.json())
    .then(data => {
        var socket = io.connect('https://' + document.domain + ':' + location.port);
        var userId = data.user_id;

        socket.on('connect', function() {
            socket.emit('join', { user_id: userId });
        });


        socket.on('friend_online', function(data) {
            updateStatus(data.user_id, 'online');
            console.log("friend_online: " + data.user_id)
        }); // Écouter l'événement de déconnexion d'un ami

        socket.on('friend_offline', function(data) {
            updateStatus(data.user_id, 'offline');
            console.log("friend_offline: " + data.user_id)
        });


        socket.on('receive_message', function(data) {
            console.log("message reçu")
            console.log(data)
            if (data.to === userId) {
                addMessageToDOM(data);
                console.log("message reçu")
                var audioPlayer = document.getElementById('audioPlayerReceive');
                audioPlayer.play()
            }
        });
        
        socket.on('update_unread_message', function(data) {
            updateUnreadMessage(data.contact_id, data.unread_messages)
        });


        socket.on('connect', function() {
            console.log('Connected to WebSocket');
        });

        socket.on('friend_request', function(data) {
            addFriendRequestToDOM(data);
        });

        socket.on('update_unread_counter', function(data) {
            updateUnreadCounter(data.contact_id, data.unread_messages);
        });

        socket.on('add_friend_request', function(data) {
            if(data.status == true) {
                var audioPlayer = document.getElementById('audioPlayerAccepted');
                audioPlayer.play()
                location.reload();
            }
        });

        // Ecouter l'événement 'message_deleted'
        socket.on('message_deleted', (data) => {
            const messageElement = document.getElementById(`div-${data.message_id}`);
            if (messageElement) {
                messageElement.remove();
            }
        });

        socket.on('update_contacts', function(data) {
            var hasContactsElement = document.getElementById('has_contacts');
            if (hasContactsElement) {
                console.log(hasContactsElement.value)
                hasContactsElement.value = data.has_contacts;
                console.log(hasContactsElement.value)
                // Optionnel : Mettre à jour d'autres parties de l'interface utilisateur en conséquence
            }
        });
        socket.on('remove_friend_request', function(data){
            console.log(data)
        });

        socket.on('typing', function(data) {
            if (data.from === contactId) {
                document.getElementById('typing-notification').style.display = 'block';
                var element = document.getElementById("autoscroll");
                element.scrollTop = element.scrollHeight;
            }
        });

        socket.on('stop_typing', function(data) {
            if (data.from === contactId) {
                document.getElementById('typing-notification').style.display = 'none';
                var element = document.getElementById("autoscroll");
                element.scrollTop = element.scrollHeight;
            }
        });

        var messageInput = document.getElementById('message_input');
        var typingTimeout;
        var contactId = current_conv_with_user;  // Remplace par l'ID réel du contact
         

        messageInput.addEventListener('keypress', function(event) {
            if (event.key !== 'Enter') {
                socket.emit('typing', { from: userId, to: contactId });
                console.log("est en train d'écrire")
                clearTimeout(typingTimeout);
                typingTimeout = setTimeout(function() {
                    socket.emit('stop_typing', { from: userId, to: contactId });
                }, 2000);
            }else {
                socket.emit('stop_typing', { from: userId, to: contactId });
            }
        });
        
        messageInput.addEventListener('blur', function() {
            console.log("n'est pas en train d'écrire")
            socket.emit('stop_typing', { from: userId, to: contactId });
        });

        function updateUnreadCounter(contactId, increment) {
            var counter = document.getElementById(`unread-counter-${contactId}`);
            if (counter) {
                var count = parseInt(counter.textContent) + increment;
                counter.textContent = count;
                console.log("nouveau print: " + count)
            }
        }

        function updateStatus(userId, status) {
            const friendElement = document.getElementById(`user-status-contact-${userId}`);
            if (friendElement) {
                friendElement.classList.remove('avatar-online', 'avatar-busy');
                switch (status) {
                    case 'online':
                        friendElement.classList.add('avatar-online');
                        break;
                    case 'offline':
                        friendElement.classList.add('avatar-busy');
                        break;
                }
            }
        }



        function updateUnreadMessage(contactId, message) {
            console.log("contact : " + contactId)
            console.log("increment : " + message)
            var newMessage = document.getElementById(`unread-message-${contactId}`);
            if (newMessage) {
                var msg = message;
                newMessage.textContent = msg;
                console.log("nouveau message: " + msg)
            }
        }
    

        // Ajouter le message au DOM
        function addMessageToDOM(message) {
            var conversationsContainer = document.getElementById('conversation_user');
            var senderInfo = message.sender_id === userId ? 'self' : 'other';
            console.log("message id: ", message);
            console.log("message content: ", String(message.message));
            
            // Détecter et rendre le Markdown entre les délimiteurs (md_start) et (md_end)
            const mdStart = '(md_start)';
            const mdEnd = '(md_end)';
            const mdStartIndex = message.message.indexOf(mdStart);
            const mdEndIndex = message.message.indexOf(mdEnd);
        
            let messageText = message.message;
        
            if (mdStartIndex !== -1 && mdEndIndex !== -1 && mdEndIndex > mdStartIndex) {
                const mdContent = message.message.substring(mdStartIndex + mdStart.length, mdEndIndex);
                const renderedMarkdown = marked(mdContent);
                messageText = message.message.substring(0, mdStartIndex) + `<div class="markdown-content">${renderedMarkdown}</div>` + message.message.substring(mdEndIndex + mdEnd.length);
            } else {
                // Remplacer les sauts de ligne par des balises <br> si ce n'est pas du Markdown
                messageText = messageText.replace(/\n/g, '<br>');
            }
        
            var div = document.createElement('div');
            div.setAttribute('id', 'div-' + message.id);
            div.className = `message ${senderInfo === 'self' ? 'self' : ''}`;
            div.innerHTML = `
            <div class="message-wrap">
                <div class="message-item">
                <div class="message-content">
                    ${message.type === 'image' ? 
                    `<img src="data:image/png;base64,${messageText}" alt="Image" style="max-width: 100%; height: auto;" />` : 
                    `<span id="message-${ message.id }">${messageText || 'Aucun message'}</span>`
                    }
                </div>
                ${senderInfo === 'self' ? `
                <div class="dropdown align-self-center">
                    <button class="btn btn-icon btn-base btn-sm" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                    <i class="ri-more-2-fill"></i>
                    </button>
                    <ul class="dropdown-menu ${senderInfo === 'self' ? 'dropdown-menu-end' : ''}">
                    <li>
                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Modifier
                        <i class="ri-edit-line"></i>
                        </a>
                    </li>
                    <li>
                        <a onclick="deleteMessage('${ message.id }')" class="dropdown-item d-flex align-items-center justify-content-between" href="#">Supprimer
                        <i class="ri-delete-bin-line"></i>
                        </a>
                    </li>
                    </ul>
                </div>` : ''}
                </div>
            </div>
            `;
            conversationsContainer.appendChild(div);
            var element = document.getElementById("autoscroll");
            element.scrollTop = element.scrollHeight;
        }


        // Fonction pour envoyer un message
        var messageInput = document.getElementById('message_input');
        var sendButton = document.getElementById('send-button');
        sendButton.addEventListener('click', function() { 
            var message = messageInput.value;
            if (message.trim() !== '') {
                var message = messageInput.value;
                let myuuid = crypto.randomUUID();
                console.log(myuuid)
                var audioPlayer = document.getElementById('audioPlayerSend');
                audioPlayer.volume = 1;
                audioPlayer.play()
                fetch('/send_message', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        id: myuuid,
                        message_type: "message",
                        contact_id: contactId,
                        message: message
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        messageInput.value = '';
                        // Ajouter le message au DOM
                        addMessageToDOM({
                            id: myuuid,
                            sender_id: userId,
                            message: message,
                            send_time: new Date().toISOString(),
                        });
                        // Envoyer le message via WebSocket
                        socket.emit('send_message', {
                            contact_id: contactId,
                            sender_id: userId,
                            message: message,
                            send_time: new Date().toISOString()
                        });
                    } else {
                        console.error('Erreur:', data.error);
                    }
                })
                .catch(error => {
                    console.error('Erreur:', error);
                }); 
            }
        });
        messageInput.addEventListener('keypress', function(event) {
            var message = messageInput.value;
            if (event.key === 'Enter' && message.trim() !== '') {
                event.preventDefault();
                var audioPlayer = document.getElementById('audioPlayerSend');
                audioPlayer.play()
                let myuuid = crypto.randomUUID();
                console.log(myuuid)
                fetch('/send_message', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        id: myuuid,
                        message_type: "message",
                        contact_id: contactId,
                        message: message
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        messageInput.value = '';
                        // Ajouter le message au DOM
                        addMessageToDOM({
                            id: myuuid,
                            sender_id: userId,
                            message: message,
                            send_time: new Date().toISOString(),
                        });
                        // Envoyer le message via WebSocket
                        socket.emit('send_message', {
                            contact_id: contactId,
                            sender_id: userId,
                            message: message,
                            send_time: new Date().toISOString()
                        });
                    } else {
                        console.error('Erreur:', data.error);
                    }
                })
                .catch(error => {
                    console.error('Erreur:', error);
                });
            }
        });

        document.getElementById('image-input').addEventListener('change', function(event) {
            var file = event.target.files[0];
            if (file) {
                var reader = new FileReader();
                reader.onloadend = function() {
                    var base64String = reader.result.replace('data:', '').replace(/^.+,/, '');
                    console.log(base64String)
                    var messageId = crypto.randomUUID();
                    fetch('/send_message', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ 
                            id: messageId,
                            contact_id: current_conv_with_user,
                            message: base64String,
                            message_type: "image"
                        }),
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            console.log('Image envoyée avec succès');
                            var message = {id: messageId,sender_id: userId,message: base64String,type: "image",send_time: new Date().toISOString()}
                            console.log(message)

                            addMessageToDOM(message);
                        } else {
                            console.error('Erreur:', data.error);
                        }
                    })
                    .catch(error => {
                        console.error('Erreur:', error);
                    });
                };
                reader.readAsDataURL(file);
            }
        });

        // Initialiser les messages existants
        fetch(`/get_messages/${contactId}`)
        .then(response => response.json())
        .then(data => {
            data.messages.forEach(message => addMessageToDOM(message));
        })
        .catch(error => {
            console.error('Erreur:', error);
        });
    })
    .catch(error => {
        console.error('Erreur:', error);
    });
    

    function addFriendRequestToDOM(request) {
        var requestsContainer = document.getElementById('requestsFriendsRequest');

        var div = document.createElement('div');
        div.setAttribute('name', request.request_id);
        console.log(request.request_id)
        div.className = 'card mb-3';
        div.setAttribute('id', 'friends-request-'+request.request_id);
        div.innerHTML = `
            <div class="card-body">
                <div class="d-flex align-items-center">
                    <div class="avatar me-4">
                        <img src="data:image/png;base64,${request.profile_image || ''}" alt="${request.requester_first_name || ''} ${request.requester_last_name || ''}" class="avatar-label bg-soft-success text-success" style="border-radius: 50%; width: 50px; height: 50px;">
                    </div>
                    <div class="flex-grow-1">
                        <div class="d-flex align-items-center overflow-hidden">
                            <h5 class="me-auto text-break mb-0">${request.requester_first_name || 'N/A'} ${request.requester_last_name || 'N/A'}</h5>
                            <span class="small text-muted text-nowrap ms-2">04:45 PM</span>
                        </div>
                        <div class="d-flex align-items-center">
                            <div class="line-clamp me-auto">Vous a envoyé une demande d'ami</div>
                            <div class="dropdown ms-5">
                                <button class="btn btn-icon btn-base btn-sm" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                    <i class="ri-more-fill"></i>
                                </button>
                                <ul class="dropdown-menu">
                                    <li><a class="dropdown-item" href="#">See less often</a></li>
                                    <li><a class="dropdown-item" href="#">Hide</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="card-footer">
                <div class="row gx-4">
                    <div class="col">
                        <a href="#" onclick="rejectFriendRequest('${request.request_id}')" class="btn btn-secondary btn-sm w-100">Refuser</a>
                    </div>
                    <div class="col">
                        <button onclick="acceptFriendRequest('${request.request_id}')" class="btn btn-primary btn-sm w-100">Accepter</button>
                    </div>
                </div>
            </div>
        `;
        requestsContainer.appendChild(div);
    }

    

    fetch('/friend_requests')
    .then(response => response.json())
    .then(data => {
        var requestsContainer = document.getElementById('requestsFriendsRequest');
        requestsContainer.innerHTML = '';

        if (data.length === 0) {
            requestsContainer.textContent = 'Aucune demande d\'ami reçue.';
            return;
        }
        console.log(data);

        data.forEach(function(request) {
            addFriendRequestToDOM(request);
        });
    })
    .catch(error => {
        console.error('Erreur:', error);
    });
    document.getElementById('typing-notification').style.display = 'none';
});

window.reportUser = function(reportedUserId) {
    const reason = prompt("Pourquoi voulez-vous signaler cet utilisateur ?");
        if (!reason) {
            return;
        }

        fetch('/report_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ reported_user_id: reportedUserId, reason: reason })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            console.error('Erreur:', error);
        });
}

window.acceptFriendRequest = function(requestId) {

    fetch('/accept_friend_request', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ request_id: requestId })
    })
    .then(response => response.json())
    .then(data => {
        // Retirer la demande d'ami de la liste
        const messageElement = document.getElementById(`friends-request-`+requestId);
            if (messageElement) {
                messageElement.remove();
                var audioPlayer = document.getElementById('audioPlayerAccepted');
                audioPlayer.play()
            }
    })
    .catch(error => {
        console.error('Erreur:', error);
    });
}

window.rejectFriendRequest = function(requestId) {

    fetch('/reject_friend_request', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ request_id: requestId })
    })
    .then(response => response.json())
    .then(data => {
        // Retirer la demande d'ami de la liste
        const messageElement = document.getElementById(`friends-request-`+requestId);
            if (messageElement) {
                messageElement.remove();
            }
    })
    .catch(error => {
        console.error('Erreur:', error);
    });
}

// Fonction pour supprimer un message

window.deleteMessage = function(messageId) {
    fetch('/delete_message', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message_id: messageId }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Retirer le message de l'interface utilisateur
            const messageElement = document.getElementById(`div-${messageId}`);
            if (messageElement) {
                messageElement.remove();
            }
        } else {
            alert('Erreur lors de la suppression du message');
        }
    });
}





document.addEventListener('DOMContentLoaded', function() {
fetch('/user_contacts')
    .then(response => response.json())
    .then(data => {
        var contactsContainer = document.getElementById('list-contacts');
        contactsContainer.innerHTML = '';

        if (data.length === 0) {
            contactsContainer.textContent = 'Aucun contact trouvé.';
            return;
        }

        data.forEach(function(contact) {
            console.log(contact);
            var li = document.createElement('li');
            li.className = 'card contact-item mb-3';
            console.log(contact.contact_id)
            if (contact.contact_id == current_conv_with_user) {
                li.className += ' active';
                console.log("active pour", current_conv_with_user)
            }

            li.innerHTML = `
                <a href="/dashboard/${contact.contact_id}" class="contact-link"></a>
                <div class="card-body">
                    <div class="d-flex align-items-center">
                        <!-- Avatar -->
                        <div id="user-status-contact-${contact.contact_id}" class="avatar me-4">
                            <span class="avatar-label bg-soft-primary text-primary">${contact.first_name[0]}${contact.last_name[0]}</span>
                        </div>
                        <!-- Avatar -->

                        <!-- Content -->
                        <div class="flex-grow-1 overflow-hidden">
                            <div class="d-flex align-items-center mb-1">
                                <h5 class="text-truncate mb-0 me-auto">${contact.first_name || 'N/A'} ${contact.last_name || 'N/A'}</h5>
                                <p class="small text-muted text-nowrap ms-4 mb-0">8:12 AM</p>
                            </div>
                            <div class="d-flex align-items-center">
                                <div class="line-clamp me-auto" id="unread-message-${contact.contact_id}">${contact.last_message || 'Aucun message'}</div>
                                <span class="badge rounded-pill bg-primary ms-2" id="unread-counter-${contact.contact_id}">${contact.unread_messages_count || 0}</span>
                            </div>
                        </div>
                        <!-- Content -->
                    </div>
                </div>
            `;
            contactsContainer.appendChild(li);
        });
    })
    .catch(error => {
        console.error('Erreur:', error);
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var logoutButton = document.getElementById('logout_button');
    console.log("CLICKE")
    logoutButton.addEventListener('click', function() {
        fetch('/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            }
        })
        .catch(error => {
            console.error('Erreur:', error);
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var logoutButton = document.getElementById('logout_button2');
    console.log("CLICKE")
    logoutButton.addEventListener('click', function() {
        fetch('/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            }
        })
        .catch(error => {
            console.error('Erreur:', error);
        });
    });
});

window.deleteUser = function() {
    const contactId = current_conv_with_user;

    fetch('/remove_friend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ contact_id: contactId }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            window.location.href = '/dashboard';
        } else {
            alert('Erreur : ' + data.error);
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        alert('Erreur lors du traitement de la requête.');
    });
}





document.addEventListener('DOMContentLoaded', function () {
    const switchElement = document.getElementById('switch-theme');

    switchElement.addEventListener('change', function () {
        const state = this.checked; // Nouvel état du switch

        fetch('/update-dashboard-theme', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                state: state,
            }),
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                } else {
                    window.location.reload();
                }
            })
            .catch(error => console.error('Error:', error));
    });
});

document.getElementById('message_input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter' && event.shiftKey) {
        // Empêcher l'envoi du formulaire
        event.preventDefault();
        // Ajouter une nouvelle ligne dans le textarea
        const cursorPosition = this.selectionStart;
        this.value = this.value.substring(0, cursorPosition) + '\n' + this.value.substring(cursorPosition);
        // Repositionner le curseur après le saut de ligne
        this.selectionEnd = cursorPosition + 1;
        // Faire défiler la zone de texte vers le bas
        this.scrollTop = this.scrollHeight;
    }
});