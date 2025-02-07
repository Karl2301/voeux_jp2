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



  var userTableBody_most_active = document.getElementById('user_most_active');
  var userTableBody_recent = document.getElementById('user_recent');

  socket.on('update_data', function(data) {
    console.log(data);
      var users_most_active = data.most_active_users;
      var users_most_recent = data.recent_users;

      userTableBody_most_active.innerHTML = ''; // Clear the table body
      userTableBody_recent.innerHTML = ''; // Clear the table body
      console.log(data)
      var message_today = document.getElementById('message_today');
      var online_users = document.getElementById('online_users');
      var report_count = document.getElementById('report_count');
      var total_users = document.getElementById('total_users');
      var amis_per_user = document.getElementById('friends_per_user');
      var message_per_user = document.getElementById('messages_per_user');
      var bannissement = document.getElementById('bannissements');
      var unread_messages = document.getElementById('unread_messages');

      message_today.innerHTML = data.messages_today;
      online_users.innerHTML= data.active_users;
      report_count.innerHTML = data.total_reports;
      total_users.innerHTML = data.total_users;
      amis_per_user.innerHTML = data.avg_friends_per_user.toFixed(5);;
      message_per_user.innerHTML= data.avg_messages_per_user.toFixed(5);;
      bannissement.innerHTML = data.banned_users;
      unread_messages.innerHTML = data.unread_messages;

      users_most_active.forEach(function(user) {
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
          email.innerHTML = `<p><a href="mailto:${user.email}" style="color: white;">${user.email}</a></p>`;
          email.style.color = "white"; // Ajoute la couleur blanche
          row.appendChild(email);


          var username = document.createElement('td');
          username.classList.add('min-width');
          username.textContent = `${user.username}`; // Placeholder phone number
          username.style.color = "white";
          row.appendChild(username);

          var online = document.createElement('td');
          online.classList.add('min-width');
          if (user.online == true) {
            online.innerHTML = `<span class="status-btn success-btn">En Ligne</span>`;
          }else {
            online.innerHTML = `<span class="status-btn close-btn">Hors Ligne</span>`;
          } // Placeholder company name
          row.appendChild(online);

          var messages = document.createElement('td');
          messages.textContent = user.message_count;
          messages.style.color = "white"; // Ajoute la couleur blanche
          row.appendChild(messages);

          userTableBody_most_active.appendChild(row);
      });

      
      users_most_recent.forEach(function(user) {
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
        email.style.color = "white"; // Ajoute la couleur blanche
        row.appendChild(email);

        var phone = document.createElement('td');
        phone.classList.add('min-width');
        phone.textContent = `${user.username}`; // Placeholder phone number
        phone.style.color = "white"; // Ajoute la couleur blanche
        row.appendChild(phone);

        var online = document.createElement('td');
        online.classList.add('min-width');
        if (user.online == true) {
          online.innerHTML = `<span class="status-btn success-btn">En Ligne</span>`;
        }else {
          online.innerHTML = `<span class="status-btn close-btn">Hors Ligne</span>`;
        } // Placeholder company name
        row.appendChild(online);

        var account = document.createElement('td');
        account.classList.add('min-width');
        if (user.verified_email == true) {
          account.innerHTML = `<span class="status-btn success-btn">Vérifié</span>`;
        }else {
          account.innerHTML = `<span class="status-btn close-btn">Non Vérifié</span>`;
        } // Placeholder company name
        row.appendChild(account);

        var date = document.createElement('td');
        var options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
        var formattedDate = new Date(user.created_at).toLocaleDateString('fr-FR', options);
        date.textContent = formattedDate;
        date.style.color = "white";
        row.appendChild(date);

        userTableBody_recent.appendChild(row);
    });

  });
});
