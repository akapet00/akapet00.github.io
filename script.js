document.addEventListener('DOMContentLoaded', function() {
    // Navigation
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    navToggle.addEventListener('click', () => {
        navMenu.classList.toggle('show');
        navToggle.setAttribute('aria-expanded', 
            navToggle.getAttribute('aria-expanded') === 'true' ? 'false' : 'true'
        );
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!navMenu.contains(e.target) && !navToggle.contains(e.target)) {
            navMenu.classList.remove('show');
            navToggle.setAttribute('aria-expanded', 'false');
        }
    });

    // Close menu when clicking a link
    navMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('show');
            navToggle.setAttribute('aria-expanded', 'false');
        });
    });

    // Countdown Timer
    const weddingDate = new Date('May 23, 2025 17:00:00').getTime();
    const daysElement = document.getElementById('days');
    const hoursElement = document.getElementById('hours');
    const minutesElement = document.getElementById('minutes');
    const secondsElement = document.getElementById('seconds');

    const updateCountdown = () => {
        const now = new Date().getTime();
        const distance = weddingDate - now;

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        daysElement.textContent = String(days).padStart(2, '0');
        hoursElement.textContent = String(hours).padStart(2, '0');
        minutesElement.textContent = String(minutes).padStart(2, '0');
        secondsElement.textContent = String(seconds).padStart(2, '0');

        if (distance < 0) {
            clearInterval(countdownInterval);
            document.getElementById('countdown').innerHTML = "The wedding has started!";
        }
    };

    const countdownInterval = setInterval(updateCountdown, 1000);
    updateCountdown();

    // RSVP Form Submission
    const form = document.getElementById('rsvp-form');
    const notification = document.getElementById('notification');
    const submitButton = form.querySelector('button[type="submit"]');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        const name = formData.get('name');
        const email = formData.get('email');
        const guests = formData.get('guests');
        const message = formData.get('message');

        // Create email body with form data
        const emailBody = `RSVP Response from: ${name}

Guest Information:
${guests}

Message:
${message}`;

        // Create mailto link with subject and body
        const mailtoLink = `mailto:ante.casanova@gmail.com?subject=RSVP Response from ${name}&body=${encodeURIComponent(emailBody)}`;
        
        // Open default email client in a new tab
        window.open(mailtoLink, '_blank');

        // Reset form
        form.reset();

        // Set up focus event listener to show notification when user returns
        const showNotification = () => {
            notification.textContent = 'Hvala na obavijesti!';
            notification.classList.add('show');
            
            // Hide notification after 5 seconds
            setTimeout(() => {
                notification.classList.remove('show');
            }, 5000);

            // Remove the event listener after showing notification
            window.removeEventListener('focus', showNotification);
        };

        window.addEventListener('focus', showNotification);
    });

    // Check if form was submitted when page loads
    if (sessionStorage.getItem('rsvpSubmitted') === 'true') {
        // Show notification
        notification.textContent = 'Hvala na obavijesti!';
        notification.classList.add('show');
        
        // Hide notification after 5 seconds
        setTimeout(() => {
            notification.classList.remove('show');
        }, 5000);
        
        // Clear the flag
        sessionStorage.removeItem('rsvpSubmitted');
    }
});
