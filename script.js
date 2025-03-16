document.addEventListener('DOMContentLoaded', function() {
    // Countdown Timer
    const weddingDate = new Date('May 23, 2025 17:00:00').getTime();
    const countdownElement = document.getElementById('countdown');
    const updateCountdown = () => {
        const now = new Date().getTime();
        const distance = weddingDate - now;
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);
        countdownElement.innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;
        if (distance < 0) {
            clearInterval(countdownInterval);
            countdownElement.innerHTML = "The wedding has started!";
        }
    };
    const countdownInterval = setInterval(updateCountdown, 1000);
    updateCountdown();

    // RSVP Form Submission
    document.getElementById('rsvp-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const guests = document.getElementById('guests').value;
        const message = document.getElementById('message').value;

        const emailBody = `
            Ime i prezime: ${name}\n
            Email: ${email}\n
            Ime i prezime pratnje: ${guests}\n
            Poruka: ${message}\n
        `;

        const mailtoLink = `mailto:akapet00@gmail.com,ante.casanova@gmail.com?subject=RSVP&body=${encodeURIComponent(emailBody)}`;

        window.location.href = mailtoLink;
    });
});
