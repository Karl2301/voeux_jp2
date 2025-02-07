document.addEventListener('DOMContentLoaded', function() {
    const socket = io.connect('https://' + document.domain + ':' + location.port);
    console.log("WebSocket connecté !");

    const div1 = document.getElementById('websites_designed');
    const div2 = document.getElementById('apps_developed');

    socket.on('update_data_about_us', function(data) {
            div1.innerHTML = data.total_users;
            div2.innerHTML = data.online_users;
    });
});
