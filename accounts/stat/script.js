document.addEventListener('DOMContentLoaded', () => {
    // Simple Scroll Animation Function
    function animateOnScroll() {
        const elements = document.querySelectorAll(
            '.hero, .programs, .about, .contact, ' +
            '.section-header, .hero-content, .hero-icons, ' +
            '.program-grid, .program-card, ' +
            '.about-grid, .about-card, .icon-card, ' +
            '.contact-form, footer'
        );

        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;

            if (elementTop < windowHeight * 0.75) {
                element.classList.add('animate-in');
            } else {
                element.classList.remove('animate-in');
            }
        });
    }

    // Attach scroll event listener
    window.addEventListener('scroll', animateOnScroll);
    
    // Initial animation check
    animateOnScroll();

    // Smooth Scrolling for Navigation Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Start Registration Button
    const startRegistrationBtn = document.getElementById('start-registration');
    startRegistrationBtn.addEventListener('click', () => {
        alert('Registration process will be implemented soon. Stay tuned!');
    });

    // Login Button
    const loginBtn = document.getElementById('login-btn');
    loginBtn.addEventListener('click', () => {
        const loginModal = createModal('Login', [
            { type: 'text', placeholder: 'Username' },
            { type: 'password', placeholder: 'Password' }
        ], 'Login');
        document.body.appendChild(loginModal);
    });

    // Signup Button
    const signupBtn = document.getElementById('signup-btn');
    signupBtn.addEventListener('click', () => {
        const signupModal = createModal('Sign Up', [
            { type: 'text', placeholder: 'Full Name' },
            { type: 'email', placeholder: 'Email Address' },
            { type: 'password', placeholder: 'Password' },
            { type: 'password', placeholder: 'Confirm Password' }
        ], 'Sign Up');
        document.body.appendChild(signupModal);
    });

    // Contact Form Submission
    const contactForm = document.getElementById('contact-form');
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Basic form validation
        const nameInput = contactForm.querySelector('input[type="text"]');
        const emailInput = contactForm.querySelector('input[type="email"]');
        const messageInput = contactForm.querySelector('textarea');

        if (nameInput.value.trim() === '' || emailInput.value.trim() === '' || messageInput.value.trim() === '') {
            alert('Please fill out all fields.');
            return;
        }

        // Simulate form submission
        alert('Thank you for your message! We will get back to you soon.');
        contactForm.reset();
    });

    // Modal Creation Function
    function createModal(title, fields, submitText) {
        const modal = document.createElement('div');
        modal.classList.add('modal');
        modal.innerHTML = `
            <div class="modal-content">
                <span class="close-modal">&times;</span>
                <h2>${title}</h2>
                <form id="modal-form">
                    ${fields.map(field => `
                        <input 
                            type="${field.type}" 
                            placeholder="${field.placeholder}" 
                            ${field.type === 'email' ? 'type="email"' : ''} 
                            required
                        >
                    `).join('')}
                    <button type="submit">${submitText}</button>
                </form>
            </div>
        `;

        // Close modal functionality
        modal.querySelector('.close-modal').addEventListener('click', () => {
            document.body.removeChild(modal);
        });

        // Form submission
        modal.querySelector('#modal-form').addEventListener('submit', (e) => {
            e.preventDefault();
            alert(`${title} successful! Welcome.`);
            document.body.removeChild(modal);
        });

        return modal;
    }
});
