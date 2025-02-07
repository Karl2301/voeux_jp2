(function () {
  /* ========= Preloader ======== */
  const preloader = document.querySelectorAll('#preloader')

  window.addEventListener('load', function () {
    if (preloader.length) {
      this.document.getElementById('preloader').style.display = 'none'
    }
  })

  /* ========= Add Box Shadow in Header on Scroll ======== */
  window.addEventListener('scroll', function () {
    const header = document.querySelector('.header')
    if (window.scrollY > 0) {
      header.style.boxShadow = '0px 0px 30px 0px rgba(200, 208, 216, 0.30)'
    } else {
      header.style.boxShadow = 'none'
    }
  })

  /* ========= sidebar toggle ======== */
  const sidebarNavWrapper = document.querySelector(".sidebar-nav-wrapper");
  const mainWrapper = document.querySelector(".main-wrapper");
  const menuToggleButton = document.querySelector("#menu-toggle");
  const menuToggleButtonIcon = document.querySelector("#menu-toggle i");
  const overlay = document.querySelector(".overlay");

  menuToggleButton.addEventListener("click", () => {
    sidebarNavWrapper.classList.toggle("active");
    overlay.classList.add("active");
    mainWrapper.classList.toggle("active");

    if (document.body.clientWidth > 1200) {
      if (menuToggleButtonIcon.classList.contains("lni-chevron-left")) {
        menuToggleButtonIcon.classList.remove("lni-chevron-left");
        menuToggleButtonIcon.classList.add("lni-menu");
      } else {
        menuToggleButtonIcon.classList.remove("lni-menu");
        menuToggleButtonIcon.classList.add("lni-chevron-left");
      }
    } else {
      if (menuToggleButtonIcon.classList.contains("lni-chevron-left")) {
        menuToggleButtonIcon.classList.remove("lni-chevron-left");
        menuToggleButtonIcon.classList.add("lni-menu");
      }
    }
  });
  overlay.addEventListener("click", () => {
    sidebarNavWrapper.classList.remove("active");
    overlay.classList.remove("active");
    mainWrapper.classList.remove("active");
  });
})();




document.addEventListener('DOMContentLoaded', function() {
  const socket = io.connect('https://' + document.domain + ':' + location.port);
  console.log("WebSocket connecté !");


    // Récupérer l'ID de l'utilisateur courant
    fetch('/get_user_id')
    .then(response => response.json())
    .then(data => {
        var userId = data.user_id;
        console.log(userId);
        socket.on('connect', function() {
            socket.emit('join', { user_id: userId });
        });
    });



  var userTableBody_banned = document.getElementById('user_report');

  socket.on('update_data', function(data) {
    console.log(data);
      var banned_users_list = data.report_users_list
      ;

      userTableBody_banned.innerHTML = ''; // Clear the table body
      console.log(data)
      var online_users = document.getElementById('online_users');
      var report_count = document.getElementById('report_count');
      var total_users = document.getElementById('total_users');
      var bannissement = document.getElementById('bannissements');

      online_users.innerHTML= data.active_users;
      report_count.innerHTML = data.total_reports;
      total_users.innerHTML = data.total_users;
      bannissement.innerHTML = data.banned_users;

      
      banned_users_list.forEach(function(user) {
        var row = document.createElement('tr');

        var id = document.createElement('td');
        id.classList.add('min-width');
        id.textContent = `${user.report_id}`;
        id.style.color = "white";
        row.appendChild(id);

        var id = document.createElement('td');
        id.classList.add('min-width');
        id.textContent = `${user.reported_user.username}`;
        id.style.color = "white";
        row.appendChild(id);

        var id = document.createElement('td');
        id.classList.add('min-width');
        id.textContent = `${user.reporter_user.username}`;
        id.style.color = "white";
        row.appendChild(id);

        var reason = document.createElement('td');
        reason.classList.add('min-width');
        reason.innerHTML = `${user.reason}`;
        reason.style.color = "white";
        row.appendChild(reason);

        var account = document.createElement('td');
        account.classList.add('min-width');
        account.innerHTML = `
            <div class="action justify-center">
                <button onClick="handleReport(${ user.report_id }, 'refuse')" class="edit" style="color: black;">
                  <svg width="40" height="40" viewBox="0 0 24 24" fill="#36ab50" xmlns="http://www.w3.org/2000/svg" transform="rotate(0 0 0)">
                  <path d="M19.2803 6.76264C19.5732 7.05553 19.5732 7.53041 19.2803 7.8233L9.86348 17.2402C9.57058 17.533 9.09571 17.533 8.80282 17.2402L4.71967 13.157C4.42678 12.8641 4.42678 12.3892 4.71967 12.0963C5.01256 11.8035 5.48744 11.8035 5.78033 12.0963L9.33315 15.6492L18.2197 6.76264C18.5126 6.46975 18.9874 6.46975 19.2803 6.76264Z" fill="#36ab50"/>
                  </svg>
                </button>
                <button onClick="handleReport(${ user.report_id }, 'warn')" class="edit" style="color: black;">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <circle cx="12" cy="17" r="1" fill="#f3ab12"></circle> <path d="M12 10L12 14" stroke="#f3ab12" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> <path d="M3.44722 18.1056L10.2111 4.57771C10.9482 3.10361 13.0518 3.10362 13.7889 4.57771L20.5528 18.1056C21.2177 19.4354 20.2507 21 18.7639 21H5.23607C3.7493 21 2.78231 19.4354 3.44722 18.1056Z" stroke="#f3ab12" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>
                </button>
                <button onClick="handleReport(${ user.report_id }, 'ban')" class="edit" style="color: black;">
                  <svg height="28" width="28" version="1.1" id="_x32_" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" xml:space="preserve" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <style type="text/css"> .st0{fill:#db0f0f;} </style> <g> <path class="st0" d="M387.317,0.005H284.666h-57.332h-102.65L0,124.688v102.67v57.294v102.67l124.684,124.674h102.65h57.332 h102.651L512,387.321v-102.67v-57.294v-102.67L387.317,0.005z M255.45,411.299c-19.082,0-34.53-15.467-34.53-34.549 c0-19.053,15.447-34.52,34.53-34.52c19.082,0,34.53,15.467,34.53,34.52C289.98,395.832,274.532,411.299,255.45,411.299z M283.414,278.692c0,15.448-12.516,27.964-27.964,27.964c-15.458,0-27.964-12.516-27.964-27.964l-6.566-135.368 c0-19.072,15.447-34.54,34.53-34.54c19.082,0,34.53,15.467,34.53,34.54L283.414,278.692z"></path> </g> </g></svg>
                </button>
            </div>`;
        row.appendChild(account);

        userTableBody_banned.appendChild(row);
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

      } else {
          alert('Erreur : ' + data.error);
      }
  })
  .catch(error => {
      console.error('Erreur:', error);
      alert('Erreur lors du traitement de la requête.');
  });
}
