// hamburger menu
function toggleMenu() {
    var menu = document.querySelector('.menu');
    menu.classList.toggle('show');
  }
  
  // Validate registration function
  function validateRegistration(event) {
    console.log('validateRegistration function called');
  
    
    var username = document.getElementById('newPass').value;
    var password = document.getElementById('confirmpass').value;
  
    // Check if any of the fields are empty
    if ( username.trim() === '' || password.trim() === '') {
        alert('Please fill out all fields.');
        event.preventDefault(); // Prevent form submission
        console.log('Validation failed: Some fields are empty.');
        return false;
    }
  
    // All fields are filled, allow form submission
    console.log('Validation successful. Form will be submitted.');
  
    return true;
  }
  