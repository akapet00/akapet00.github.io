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

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Add loading state
        submitButton.classList.add('loading');
        submitButton.disabled = true;
        
        // Simulate form submission (replace with actual API call)
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // Show notification
        notification.classList.add('show');
        
        // Hide notification after 5 seconds
        setTimeout(() => {
            notification.classList.remove('show');
        }, 5000);
        
        // Reset form and remove loading state
        form.reset();
        submitButton.classList.remove('loading');
        submitButton.disabled = false;
    });
});
