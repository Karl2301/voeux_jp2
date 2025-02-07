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



  var userTableBody_banned = document.getElementById('user_banned');

  socket.on('update_data', function(data) {
    console.log(data);
      var banned_users_list = data.banned_users_list;

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
        email.style.color = "white";
        row.appendChild(email);

        var username = document.createElement('td');
        username.classList.add('min-width');
        username.textContent = `${user.username}`;
        username.style.color = "white";
        row.appendChild(username);

        var reason = document.createElement('td');
        reason.classList.add('min-width');
        reason.innerHTML = `${user.reason}`;
        reason.style.color = "white";
        row.appendChild(reason);

        var account = document.createElement('td');
        account.classList.add('min-width');
        account.innerHTML = `
            <div class="action justify-center">
              <form action="/unban_user/${user.id}" method="post">
                <button type="submit" class="edit" style="color: black;">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="#36ab50" xmlns="http://www.w3.org/2000/svg" transform="rotate(0 0 0)">
                  <path d="M19.2803 6.76264C19.5732 7.05553 19.5732 7.53041 19.2803 7.8233L9.86348 17.2402C9.57058 17.533 9.09571 17.533 8.80282 17.2402L4.71967 13.157C4.42678 12.8641 4.42678 12.3892 4.71967 12.0963C5.01256 11.8035 5.48744 11.8035 5.78033 12.0963L9.33315 15.6492L18.2197 6.76264C18.5126 6.46975 18.9874 6.46975 19.2803 6.76264Z" fill="#36ab50"/>
                  </svg>



                </button>
              </form>
            </div>`;
        row.appendChild(account);

        userTableBody_banned.appendChild(row);
    });

  });
});
