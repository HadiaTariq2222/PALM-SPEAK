document.getElementById('execution-form').addEventListener('submit', function(e) {
    e.preventDefault();
    fetch('{% url "execute_code" %}', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token
        },
        // Other fetch options...
    })
    .then(response => response.json())
    .then(data => {
        // Handle response data
    })
    .catch(error => console.error('Error:', error));
});

// Function to get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Get CSRF token if found
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
