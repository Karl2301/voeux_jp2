const uname = document.getElementById('username');
const pass = document.getElementById('password');
const form = document.querySelector('login-form');

function getClientInfo() {
    var clientInfo = {
        userAgent: navigator.userAgent,
        platform: navigator.platform,
        appVersion: navigator.appVersion,
        appName: navigator.appName,
        appCodeName: navigator.appCodeName,
        language: navigator.language,
        languages: navigator.languages,
        cookiesEnabled: navigator.cookieEnabled,
        online: navigator.onLine,
        screenWidth: screen.width,
        screenHeight: screen.height,
        windowWidth: window.innerWidth,
        windowHeight: window.innerHeight
    };

    document.getElementById('client_info').value = JSON.stringify(clientInfo);
    console.log(clientInfo);
}

document.getElementById('login-form').addEventListener('submit', function(event) {
    getClientInfo();
});


