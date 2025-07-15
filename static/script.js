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

// Updated function to create dynamic detail page
function viewDetails(button) {
    const card = button.closest('.course-card') || button.closest('.recommendation-card');
    const title = card.querySelector('.course-title').textContent || card.querySelector('.card-title').textContent;
    const description = card.querySelector('.course-description').textContent || card.querySelector('.card-description').textContent;
    const tags = Array.from(card.querySelectorAll('.tag')).map(tag => tag.textContent);
    
    // Create the detail page content
    createDetailPage(title, description, tags);
}

function createDetailPage(title, description, tags) {
    const currentContent = document.querySelector('.container').innerHTML;
    sessionStorage.setItem('previousPage', currentContent);

    const detailContent = `
        <a href="#" onclick="goBackToExplore()" style="font-size:0.85rem; color:#475569; text-decoration:none; display:inline-block; margin-bottom:20px;">⟵ Back to Explore</a>

        <div class="course-header">
            <div class="course-image-details">Image</div>

            <div class="course-info">
                <div class="course-title">${title}</div>
                <div class="course-tags">
                    ${tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>

                <div>
                    <div class="section-title">Overview</div>
                    <div class="course-description">${description}</div>
                </div>

                <div>
                    <div class="section-title">Skills You'll Build</div>
                    <div class="skills-grid">
                        <div class="skills-column">
                            <ul>
                                <li>Critical Thinking</li>
                                <li>Problem Solving</li>
                                <li>Research Skills</li>
                                <li>Communication</li>
                            </ul>
                        </div>
                        <div class="skills-column">
                            <ul>
                                <li>Project Management</li>
                                <li>Collaboration</li>
                                <li>Technical Skills</li>
                                <li>Leadership</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    document.querySelector('.container').innerHTML = detailContent;
    document.title = title;
    window.scrollTo(0, 0);
}



function goBackToExplore() {
    const previousContent = sessionStorage.getItem('previousPage');
    if (previousContent) {
        document.querySelector('.container').innerHTML = previousContent;
        document.title = 'Explore';
        
        // Reinitialize event listeners for the restored content
        initializeEventListeners();
    } else {
        // Fallback - reload the page
        window.location.reload();
    }
}

function addToStack(button) {
    const card = button.closest('.course-card') || button.closest('.recommendation-card');
    const title = card.querySelector('.course-title')?.textContent || card.querySelector('.card-title')?.textContent;
    
    button.textContent = 'Added ✓';
    button.style.background = '#48bb78';
    button.style.color = 'white';
    button.style.borderColor = '#48bb78';
    
    setTimeout(() => {
        button.textContent = 'Add to Stack';
        button.style.background = 'transparent';
        button.style.color = '#4a5568';
        button.style.borderColor = '#e2e8f0';
    }, 2000);
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

function initializeEventListeners() {
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

    // Course card button handlers - Updated to use onclick for View Details
    const addToStackButtons = document.querySelectorAll('.btn-secondary');
    
    addToStackButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            addToStack(this);
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
}

// Main DOM Content Loaded Handler
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    fetchRecommendations();
});

// Capitalize each word in a string
function capitalizeWords(str) {
    return str
        .split(" ")
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ");
}

// Truncate text to a certain length
function truncate(text, maxLength = 150) {
    return text.length > maxLength ? text.slice(0, maxLength) + '…' : text;
}

// Fetch and render recommendations
function fetchRecommendations() {
    const recommendedSection = document.querySelector(".recommended-section");
    const courseGrid = recommendedSection.querySelector(".course-grid");
    courseGrid.innerHTML = ""; // clear old cards

    fetch("/recommendations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: "What classes and extracurricular activities do you recommend?" })
    })
        .then(res => res.json())
        .then(data => {
            const classes = data.classes || [];
            const activities = data.activities || [];

            if (classes.length > 0) {
                const classHeader = document.createElement("h2");
                classHeader.className = "section-title";
                classHeader.textContent = "Recommended Classes";
                courseGrid.appendChild(classHeader);

                classes.forEach(cls => {
                    const card = createCard(cls, "class-card");
                    courseGrid.appendChild(card);
                });
            }

            if (activities.length > 0) {
                const activityHeader = document.createElement("h2");
                activityHeader.className = "section-title";
                activityHeader.textContent = "Recommended Extracurricular Activities";
                courseGrid.appendChild(activityHeader);

                activities.forEach(act => {
                    const card = createCard(act, "activity-card");
                    courseGrid.appendChild(card);
                });
            }
        })
        .catch(err => {
            console.error("❌ Failed to fetch recommendations:", err);
            const errorCard = document.createElement("div");
            errorCard.className = "course-card";
            errorCard.style.gridColumn = "1 / -1";
            errorCard.innerHTML = `<p>⚠️ Failed to fetch recommendations.</p>`;
            courseGrid.appendChild(errorCard);
        });
}

// Create a card (truncated description, full description stored in data attribute)
function createCard(item, type) {
    const card = document.createElement("div");
    card.className = `course-card ${type}`;

    const tags = (item.tags || "")
        .split(",")
        .map(tag => capitalizeWords(tag.trim()))
        .slice(0, 3);

    card.innerHTML = `
        <div class="course-content" data-full-description="${item.description}">
            <h3 class="course-title">${capitalizeWords(item.name)}</h3>
            <div class="course-tags">
                ${tags.map(tag => `<span class="tag">${tag}</span>`).join("")}
            </div>
            <p class="course-description">${truncate(item.description)}</p>
            <div class="course-actions">
                <button class="btn btn-primary" onclick="viewDetails(this)">View Details</button>
                <button class="btn btn-secondary" onclick="addToStack(this)">Add to Stack</button>
            </div>
        </div>
    `;

    return card;
}

// View details — full description
function viewDetails(button) {
    const card = button.closest('.course-card') || button.closest('.recommendation-card');
    const content = card.querySelector('.course-content');

    const title = content.querySelector('.course-title').textContent;
    const description = content.getAttribute('data-full-description');
    const tags = Array.from(content.querySelectorAll('.tag')).map(tag => tag.textContent);

    createDetailPage(title, description, tags);
}

// Create detail page content
function createDetailPage(title, description, tags) {
    const currentContent = document.querySelector('.container').innerHTML;
    sessionStorage.setItem('previousPage', currentContent);

    const detailContent = `
        <a href="#" onclick="goBackToExplore()" style="font-size:0.85rem; color:#475569; text-decoration:none; display:inline-block; margin-bottom:20px;">⟵ Back to Explore</a>

        <div class="course-header">
            <div class="course-image-details">Image</div>

            <div class="course-info">
                <div class="course-title">${title}</div>
                <div class="course-tags">
                    ${tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>

                <div>
                    <div class="section-title">Overview</div>
                    <div class="course-description">${description}</div>
                </div>

                <div>
                    <div class="section-title">Skills You'll Build</div>
                    <div class="skills-grid">
                        <div class="skills-column">
                            <ul>
                                <li>Critical Thinking</li>
                                <li>Problem Solving</li>
                                <li>Research Skills</li>
                                <li>Communication</li>
                            </ul>
                        </div>
                        <div class="skills-column">
                            <ul>
                                <li>Project Management</li>
                                <li>Collaboration</li>
                                <li>Technical Skills</li>
                                <li>Leadership</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    document.querySelector('.container').innerHTML = detailContent;
    document.title = title;
    window.scrollTo(0, 0);
}

// Go back to explore page
function goBackToExplore() {
    const previousContent = sessionStorage.getItem('previousPage');
    if (previousContent) {
        document.querySelector('.container').innerHTML = previousContent;
        document.title = 'Explore';
        initializeEventListeners();
    } else {
        window.location.reload();
    }
}

// Add to stack
function addToStack(button) {
    const card = button.closest('.course-card') || button.closest('.recommendation-card');
    const title = card.querySelector('.course-title')?.textContent || card.querySelector('.card-title')?.textContent;

    button.textContent = 'Added ✓';
    button.style.background = '#48bb78';
    button.style.color = 'white';
    button.style.borderColor = '#48bb78';

    setTimeout(() => {
        button.textContent = 'Add to Stack';
        button.style.background = 'transparent';
        button.style.color = '#4a5568';
        button.style.borderColor = '#e2e8f0';
    }, 2000);
}

// Initialize page
document.addEventListener('DOMContentLoaded', function () {
    initializeEventListeners();
    fetchRecommendations();
});

function initializeEventListeners() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function () {
            navItems.forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');
        });
    });
}
