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
    var userId = window.location.pathname.split('/').pop();
    const first_name = document.getElementById('first_name');
    const last_name = document.getElementById('last_name');
    const username = document.getElementById('username');
    const email = document.getElementById('email');
    const bio = document.getElementById('bio');
    const description = document.getElementById('description');
    const adminLevel = document.getElementById('admin_level');
    const admin = document.getElementById('toggleSwitch1');


    fetch(`/user_info_get/${userId}`, {
      method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        alert(data.error);
    } else {
      console.log(data);
      first_name.value = data.first_name;
      last_name.value = data.last_name;
      username.value = data.username; 
      email.value = data.email;
      bio.value = data.bio;
      description.value = data.description;
      adminLevel.value = data.admin_level;
      admin.checked = data.admin;

      if(data.requester_lvl_admin >= 1) {
        document.getElementById('sous_modo_display').style.display = "block";
      }
      if(data.requester_lvl_admin >= 2) {
        document.getElementById('modo_display').style.display = "block";
      }
      if(data.requester_lvl_admin >= 3) {
        document.getElementById('manager_display').style.display = "block";
      }
      if(data.requester_lvl_admin >= 4) {
        document.getElementById('chef_display').style.display = "block";
        document.getElementById('admin_display').style.display = "block";
      }
    }
    })
    .catch((error) => {
      console.error('Erreur:', error);
    });
});



function envoyerDonnees() {
  var userId = window.location.pathname.split('/').pop();
  const first_name = document.getElementById('first_name').value;
  const last_name = document.getElementById('last_name').value;
  const username = document.getElementById('username').value;
  const email = document.getElementById('email').value;
  const bio = document.getElementById('bio').value;
  const description = document.getElementById('description').value;
  const adminLevel = document.getElementById('admin_level').value;
  const admin = document.getElementById('toggleSwitch1').checked;
  var div_success = document.getElementById("success_div_update");
  var div_error = document.getElementById("error_div_update");

  const data = {
    first_name: first_name,
    last_name: last_name,
    username: username,
    email: email,
    bio: bio,
    description: description,
    admin_level: adminLevel,
    admin: admin
  };

  fetch(`/update_user_admin_info/${userId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
    if(data.success) {
      div_success.style.display = "block";
      div_error.style.display = "none";
    } else {
      div_success.style.display = "none";
      div_error.style.display = "block";
    }
  })
  .catch((error) => {
    div_success.style.display = "none";
    div_error.style.display = "block";
  });
}


