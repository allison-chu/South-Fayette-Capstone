// Recommendation scrolling functionality
function scrollRecommendations(dir) {
    const grid = document.getElementById('recGrid');
    grid.scrollBy({ left: dir * 250, behavior: 'smooth' });
}

// Navigation functions
function goBack() {
    window.history.back();
}

function selectCourse(card) {
    alert('Selected course: ' + card.querySelector('.card-title').textContent);
}

function viewDetails(button) {
    const card = button.closest('.recommendation-card');
    const title = card.querySelector('.card-title').textContent;
    alert('Viewing details for: ' + title);
}

function addToStack(button) {
    const card = button.closest('.recommendation-card');
    const title = card.querySelector('.card-title').textContent;
    alert('Added to stack: ' + title);
}

// Main DOM Content Loaded Handler
document.addEventListener('DOMContentLoaded', function() {
    // Course image interactivity
    const courseImage = document.querySelector('.course-image');
    if (courseImage) {
        courseImage.addEventListener('click', function() {
            alert('Course image clicked - could open full view or video');
        });
    }

    // Sidebar navigation handlers
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            // Remove active class from all items
            navItems.forEach(nav => nav.classList.remove('active'));
            // Add active class to clicked item
            this.classList.add('active');
        });
    });

    // Search functionality
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        searchInput.addEventListener('focus', function() {
            this.style.transform = 'scale(1.02)';
        });
        
        searchInput.addEventListener('blur', function() {
            this.style.transform = 'scale(1)';
        });
    }

    // Category card click handlers
    const categoryCards = document.querySelectorAll('.category-card');
    categoryCards.forEach(card => {
        card.addEventListener('click', function() {
            const title = this.querySelector('.category-title').textContent.trim();
            console.log(`Navigating to: ${title}`);
            // Add navigation logic here
        });
    });

    // Course card button handlers
    const viewDetailsButtons = document.querySelectorAll('.btn-primary');
    const addToStackButtons = document.querySelectorAll('.btn-secondary');
    
    addToStackButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const courseTitle = this.closest('.course-card').querySelector('.course-title').textContent;
            this.textContent = 'Added ✓';
            this.style.background = '#48bb78';
            this.style.color = 'white';
            this.style.borderColor = '#48bb78';
            
            setTimeout(() => {
                this.textContent = 'Add to Stack';
                this.style.background = 'transparent';
                this.style.color = '#4a5568';
                this.style.borderColor = '#e2e8f0';
            }, 2000);
        });
    });

    // Course menu handlers
    const courseMenus = document.querySelectorAll('.course-menu');
    courseMenus.forEach(menu => {
        menu.addEventListener('click', function(e) {
            e.stopPropagation();
            alert('Course menu clicked - Add dropdown menu here');
        });
    });

    // Add subtle animations on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    const courseCards = document.querySelectorAll('.course-card');
    courseCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = `all 0.6s ease ${index * 0.1}s`;
        observer.observe(card);
    });
});