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

  var usersTable = document.getElementById('usersTable');

  socket.on('update_data', function(data) {
      var users_list = data.total_users_info;

      usersTable.innerHTML = ''; // Clear the table body
      console.log(data)
      var verified_user = document.getElementById('verified_user');
      var online_users = document.getElementById('online_users');
      var report_count = document.getElementById('report_count');
      var total_users = document.getElementById('total_users');


      verified_user.innerHTML = data.verified_users;
      online_users.innerHTML = data.active_users;
      report_count.innerHTML = data.total_reports;
      total_users.innerHTML = data.total_users;

      users_list.forEach(function(user) {
          var row = document.createElement('tr');

          var leadInfo = document.createElement('td');
          leadInfo.classList.add('min-width');
          var leadDiv = document.createElement('div');
          leadDiv.classList.add('lead');
          var leadText = document.createElement('div');
          leadText.classList.add('lead-text');
          leadText.textContent = user.first_name + " " + user.last_name;
          leadDiv.appendChild(leadText);
          leadInfo.appendChild(leadDiv);
          row.appendChild(leadInfo);

          var email = document.createElement('td');
          email.classList.add('min-width');
          email.innerHTML = `<p><a style="color: white;" href="mailto:${user.email}">${user.email}</a></p>`;
          row.appendChild(email);

          var username = document.createElement('td');
          username.classList.add('min-width');
          username.textContent = `${user.username}`;
          username.style.color = "white";
          row.appendChild(username);

          var online = document.createElement('td');
          online.classList.add('min-width');
          if (user.online == true) {
            online.innerHTML = `<span class="status-btn success-btn">En Ligne</span>`;
          } else {
            online.innerHTML = `<span class="status-btn close-btn">Hors Ligne</span>`;
          }
          row.appendChild(online);

          // Ajouter la partie HTML spécifiée après la colonne "online"
          var action = document.createElement('td');
          action.classList.add('min-width');
          action.innerHTML = `
            <div class="action justify-center">
              <form action="/user_info/${user.id}" method="get">
                <button type="submit" class="edit" style="color: black;">
                  <i style="color: white;" class="lni lni-pencil"></i>
                </button>
              </form>
              <form action="/delete_user/${user.id}" method="post">
                <button type="submit" class="text-danger">
                  <i class="lni lni-trash-can"></i>
                </button>
              </form>
            </div>`;
          row.appendChild(action);

          usersTable.appendChild(row);
      });
  });
});
