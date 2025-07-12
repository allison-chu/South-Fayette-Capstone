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

// Search functionality
function performSearch(searchTerm) {
    const courseCards = document.querySelectorAll('.course-card');
    const categoryCards = document.querySelectorAll('.category-card');
    const courseGrid = document.querySelector('.course-grid');
    const searchLower = searchTerm.toLowerCase().trim();
    
    let visibleCount = 0;
    
    // Filter course cards
    courseCards.forEach(card => {
        const title = card.querySelector('.course-title').textContent.toLowerCase();
        const description = card.querySelector('.course-description').textContent.toLowerCase();
        const tags = Array.from(card.querySelectorAll('.tag')).map(tag => tag.textContent.toLowerCase());
        const allTags = tags.join(' ');
        
        const matches = title.includes(searchLower) || 
                       description.includes(searchLower) || 
                       allTags.includes(searchLower);
        
        if (matches || searchLower === '') {
            card.style.display = 'block';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });
    
    // Adjust grid layout based on visible count
    if (searchLower !== '') {
        // During search, keep cards the same size as homepage
        courseGrid.style.gridTemplateColumns = 'repeat(auto-fill, minmax(300px, 1fr))';
        courseGrid.style.justifyContent = 'start';
    } else {
        // Reset to original grid layout
        courseGrid.style.gridTemplateColumns = 'repeat(auto-fit, minmax(300px, 1fr))';
        courseGrid.style.justifyContent = 'initial';
    }
    
    // Show/hide category cards based on search
    const featuredSection = document.querySelector('.featured-categories');
    const recommendedSection = document.querySelector('.recommended-section');
    
    if (searchLower === '') {
        // Show everything when search is empty
        featuredSection.style.display = 'grid';
        categoryCards.forEach(card => {
            card.style.display = 'flex';
        });
        recommendedSection.querySelector('.section-title').textContent = 'Recommended For You';
    } else {
        // Hide featured categories during search
        featuredSection.style.display = 'none';
        
        // Update section title to show search results
        const resultsText = visibleCount === 1 ? '1 result' : `${visibleCount} results`;
        recommendedSection.querySelector('.section-title').textContent = 
            `Search Results: ${resultsText} for "${searchTerm}"`;
    }
    
    // Show "no results" message if needed
    showNoResultsMessage(visibleCount, searchTerm);
}

function showNoResultsMessage(visibleCount, searchTerm) {
    // Remove existing no results message
    const existingMessage = document.querySelector('.no-results-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    if (visibleCount === 0 && searchTerm.trim() !== '') {
        const courseGrid = document.querySelector('.course-grid');
        const noResultsDiv = document.createElement('div');
        noResultsDiv.className = 'no-results-message';
        noResultsDiv.style.cssText = `
            grid-column: 1 / -1;
            text-align: center;
            padding: 60px 20px;
            color: #718096;
            font-size: 1.1rem;
        `;
        noResultsDiv.innerHTML = `
            <div style="font-size: 3rem; margin-bottom: 20px;">🔍</div>
            <h3 style="margin-bottom: 10px; color: #4a5568;">No results found</h3>
            <p>We couldn't find any courses matching "${searchTerm}". Try different keywords or browse our categories above.</p>
        `;
        courseGrid.appendChild(noResultsDiv);
    }
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
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

    // Enhanced search functionality
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        // Create debounced search function
        const debouncedSearch = debounce((searchTerm) => {
            performSearch(searchTerm);
        }, 300);
        
        // Real-time search as user types
        searchInput.addEventListener('input', function() {
            debouncedSearch(this.value);
        });
        
        // Search on Enter key
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch(this.value);
            }
        });
        
        // Visual feedback on focus
        searchInput.addEventListener('focus', function() {
            this.style.transform = 'scale(1.02)';
        });
        
        searchInput.addEventListener('blur', function() {
            this.style.transform = 'scale(1)';
        });
        
        // Clear search when input is cleared
        searchInput.addEventListener('input', function() {
            if (this.value === '') {
                performSearch('');
            }
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

    fetchRecommendations();
});

function fetchRecommendations() {
    const recommendedSection = document.querySelector(".recommended-section");
    const courseGrid = recommendedSection.querySelector(".course-grid");
    courseGrid.innerHTML = ""; // clear old cards

    fetch("/recommendations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: "What classes or activities do you recommend?" })
    })
        .then(res => {
            if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
            return res.json();
        })
        .then(data => {
            console.log("✅ Received data from server:", data);

            const text = data.result;

            const [classesSection, activitiesSection] =
                text.split("**Extracurricular Activities**:");

            if (!classesSection || !activitiesSection) {
                console.warn("⚠️ Could not parse sections properly. Showing raw response.");
                const card = document.createElement("div");
                card.className = "course-card";
                card.innerHTML = `
                    <div class="course-content">
                        <h3 class="course-title">AI Recommendations</h3>
                        <p class="course-description" style="white-space: pre-wrap;">${text}</p>
                    </div>
                `;
                courseGrid.appendChild(card);
                return;
            }

            const classes = classesSection
                .replace("**Classes**:", "")
                .split("\n")
                .filter(line => line.trim().startsWith("-"))
                .map(line => line.replace("-", "").trim());

            const activities = activitiesSection
                .split("\n")
                .filter(line => line.trim().startsWith("-"))
                .map(line => line.replace("-", "").trim());

            // --- Add Classes Section Title ---
            const classHeader = document.createElement("h2");
            classHeader.className = "section-title";
            classHeader.textContent = "Classes";
            courseGrid.appendChild(classHeader);

            classes.forEach(cls => {
                const card = createRecommendationCard(cls, "class-card");
                courseGrid.appendChild(card);
            });

            // --- Add Activities Section Title ---
            const activityHeader = document.createElement("h2");
            activityHeader.className = "section-title";
            activityHeader.textContent = "Extracurricular Activities";
            courseGrid.appendChild(activityHeader);

            activities.forEach(act => {
                const card = createRecommendationCard(act, "activity-card");
                courseGrid.appendChild(card);
            });
        })
        .catch(err => {
            console.error("❌ Failed to fetch or parse recommendations:", err);
            const errorCard = document.createElement("div");
            errorCard.className = "course-card";
            errorCard.style.gridColumn = "1 / -1";
            errorCard.style.padding = "20px";
            errorCard.style.background = "#fff5f5";
            errorCard.style.border = "1px solid #fed7d7";
            errorCard.style.borderRadius = "8px";
            errorCard.innerHTML = `<p>⚠️ Failed to fetch recommendations.</p>`;
            courseGrid.appendChild(errorCard);
        });
}

// helper to create a card with buttons
function createRecommendationCard(text, type) {
    const card = document.createElement("div");
    card.className = `course-card ${type}`;

    const [title, ...descParts] = text.split(":");
    const description = descParts.join(":").trim();

    card.innerHTML = `
        <div class="course-content">
            <h3 class="course-title">${title.trim()}</h3>
            <p class="course-description">${description}</p>
            <div class="course-actions">
                <a href="details.html" class="btn btn-primary">View Details</a>
                <button class="btn btn-secondary">Add to Stack</button>
            </div>
        </div>
    `;

    // Attach "Add to Stack" behavior
    const addToStackBtn = card.querySelector(".btn-secondary");
    addToStackBtn.addEventListener("click", function () {
        this.textContent = "Added ✓";
        this.style.background = "#48bb78";
        this.style.color = "white";
        this.style.borderColor = "#48bb78";

        setTimeout(() => {
            this.textContent = "Add to Stack";
            this.style.background = "transparent";
            this.style.color = "#4a5568";
            this.style.borderColor = "#e2e8f0";
        }, 2000);
    });

    return card;
}
