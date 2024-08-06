// hamburger menu
function toggleMenu() {
    var menu = document.querySelector('.menu');
    menu.classList.toggle('show');
  }
   // redirect function for submission
   function redirectToRegister() {
    window.location.href = "register.html";
} 
// for login page
// for submission and go to the registration page
function validate() {
    var username = document.getElementById("Username").value;
    var password = document.getElementById("password").value;
    // Check if username and password are not empty
    if (username.trim() === "" || password.trim() === "") {
        alert("Please fill out both username and password fields.");
        return false; // Validation fails
    }
    // Validation passes
    return true;
  }
  document.getElementById("loginForm").addEventListener("submit", function(event) {
    if (!validate()) {
        event.preventDefault(); // Prevent form submission
    }
  });
  function validate() {
    var username = document.getElementById("Username").value;
    var password = document.getElementById("password").value;
    // Check if username and password are not empty
    if (username.trim() === "" || password.trim() === "") {
        alert("Please fill out both username and password fields.");
        return false; // Validation fails
    }
    // Validation passes
    return true;
  }