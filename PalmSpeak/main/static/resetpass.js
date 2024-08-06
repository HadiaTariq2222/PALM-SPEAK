
// hamburger menu
function toggleMenu() {
  var menu = document.querySelector('.menu');
  menu.classList.toggle('show');
}

// Validate reset password function
function validateResetPassword(event) {
  console.log('validateResetPassword function called');

  var newPass = document.getElementById('newPass').value;
  var confirmPass = document.getElementById('confirmpass').value;

  // Check if any of the fields are empty
  if (newPass.trim() === '' || confirmPass.trim() === '') {
      alert('Please fill out all fields.');
      event.preventDefault(); // Prevent form submission
      console.log('Validation failed: Some fields are empty.');
      return false;
  }

  // Check if passwords match
  if (newPass !== confirmPass) {
      alert('Passwords do not match. Please try again.');
      event.preventDefault(); // Prevent form submission
      console.log('Validation failed: Passwords do not match.');
      return false;
  }

  // All fields are filled, and passwords match, allow form submission
  console.log('Validation successful. Form will be submitted.');

  return true;
}

  