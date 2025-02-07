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


    const switchElement = document.getElementById('switch-theme');

    switchElement.addEventListener('change', function () {
        const state = this.checked; // Nouvel état du switch

        fetch('/update_settings', {
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