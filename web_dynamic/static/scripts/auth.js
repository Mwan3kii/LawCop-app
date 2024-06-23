document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');

    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            // Login logic (e.g., AJAX request to backend)
            const username = document.getElementById('username').value;
            const password = document.getElementById('passwd').value;
            // Perform AJAX request or form submission
            console.log('Login:', { username, password });
        });
    }

    if (signupForm) {
        signupForm.addEventListener('submit', (e) => {
            e.preventDefault();
            // Signup logic (e.g., AJAX request to backend)
            const username = document.getElementById('username').value;
            const password = document.getElementById('passwd').value;
            const email = document.getElementById('email').value;
            // Perform AJAX request or form submission
            console.log('Signup:', { username, password, email });
        });
    }
});