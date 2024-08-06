// hamburger menu
function toggleMenu() {
  var menu = document.querySelector('.menu');
  menu.classList.toggle('show');
}

// Validate registration function
function validateRegistration(event) {
  console.log('validateRegistration function called');

  var fName = document.getElementById('fName').value;
  var lName = document.getElementById('LName').value;
  var username = document.getElementById('Username').value;
  var password = document.getElementById('password').value;

  // Check if any of the fields are empty
  if (fName.trim() === '' || lName.trim() === '' || username.trim() === '' || password.trim() === '') {
      alert('Please fill out all fields.');
      event.preventDefault(); // Prevent form submission
      console.log('Validation failed: Some fields are empty.');
      return false;
  }

  // All fields are filled, allow form submission
  console.log('Validation successful. Form will be submitted.');

  return true;
}
