var support_dropdown = document.getElementById("Support_dropdown");
var support_btn = document.getElementById("dropbtn-Support");
var solutions_dropdown = document.getElementById("Solutions_dropdown");
var solutions_btn = document.getElementById("dropbtn-Solutions");

function clickDropdown(inp) {
    if(inp == "Support") {
      support_dropdown.classList.toggle("show");
      support_btn.classList.toggle("opened");
      solutions_dropdown.classList.remove("show");
      solutions_btn.classList.remove("opened");
    } else if (inp = "Solutions"){
      solutions_dropdown.classList.toggle("show");
      solutions_btn.classList.toggle("opened");
      support_dropdown.classList.remove("show");
      support_btn.classList.remove("opened");
    }
  }

  window.addEventListener("click", function(event) {
    if (!event.target.matches('#dropbtn-Solutions') && !event.target.matches('#dropbtn-Support')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
      support_btn.classList.remove("opened");
      solutions_btn.classList.remove("opened");
    }
});
