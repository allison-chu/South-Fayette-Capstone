// Recommendation scrolling functionality
function scrollRecommendations(dir) {
    const grid = document.getElementById('recGrid');
    grid.scrollBy({ left: dir * 250, behavior: 'smooth' });
}

// Navigation functions
function goBack() {
    window.history.back();
}

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

// Create a card (homepage or explore page)
function createCard(item, type) {
    const card = document.createElement("div");
    card.className = `course-card ${type}`;

    const tags = (item.tags || "")
        .split(",")
        .map(tag => capitalizeWords(tag.trim()))
        .slice(0, 2);

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

// Create detail page content + You May Also Like
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

        <div class="recommendations-title">You May Also Like</div>
        <div class="recommendations-wrapper">
            <div class="nav-arrow" onclick="scrollRecommendations(-1)">‹</div>

            <div class="recommendations-grid" id="recGrid">
                <p>Loading recommendations…</p>
            </div>

            <div class="nav-arrow" onclick="scrollRecommendations(1)">›</div>
        </div>
    `;

    document.querySelector('.container').innerHTML = detailContent;
    document.title = title;
    window.scrollTo(0, 0);

    fetchDummyRecommendations();
}

// Fetch dummy recs for the detail page
function fetchDummyRecommendations() {
    const recGrid = document.getElementById('recGrid');
    recGrid.innerHTML = '';

    fetch("/recommendations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: "dummy" })
    })
        .then(res => res.json())
        .then(data => {
            const all = [...(data.classes || []), ...(data.activities || [])];
            if (all.length > 3) {
                all.splice(3); // keep only 3
            }

            all.forEach(item => {
                const tags = (item.tags || "")
                    .split(",")
                    .map(tag => capitalizeWords(tag.trim()))
                    .slice(0, 2);

                const card = document.createElement("div");
                card.className = "recommendation-card";
                card.style.flex = "1"; // Make cards expand to fill space
                card.style.width = "auto"; // Override fixed width
                card.style.minWidth = "200px"; // Minimum width to prevent too small cards

                card.innerHTML = `
                    <div class="card-image"></div>
                    <div class="course-content" data-full-description="${item.description}">
                        <div class="card-title course-title">${capitalizeWords(item.name)}</div>
                        <div class="card-tags course-tags">
                            ${tags.map(tag => `<span class="tag">${tag}</span>`).join("")}
                        </div>
                        <div class="card-description course-description">${truncate(item.description, 100)}</div>
                        <div class="course-actions" style="display: flex; gap: 10px;">
                            <button class="btn btn-primary" onclick="viewDetails(this)">View Details</button>
                            <button class="btn btn-secondary" onclick="addToStack(this)">Add to Stack</button>
                        </div>
                    </div>
                `;
                recGrid.appendChild(card);
            });
        })
        .catch(err => {
            console.error("Failed to load recommendations:", err);
            recGrid.innerHTML = `<p style="color: #e53e3e;">Failed to load recommendations.</p>`;
        });
}
function goBackToExplore() {
    document.querySelector('.container').innerHTML = sessionStorage.getItem('explorePage');
    document.title = 'Explore';
    initializeEventListeners();
}

// Save Explore state *once* when page loads:
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    fetchRecommendations();

    // Save explore page at start
    const exploreContent = document.querySelector('.container').innerHTML;
    sessionStorage.setItem('explorePage', exploreContent);
});


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

// Homepage fetch
function fetchRecommendations() {
    const recommendedSection = document.querySelector(".recommended-section");
    const courseGrid = recommendedSection.querySelector(".course-grid");
    courseGrid.innerHTML = ""; // clear old cards

    fetch("/recommendations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: "homepage" })
    })
        .then(res => res.json())
        .then(data => {
            const classes = data.classes || [];
            const activities = data.activities || [];

            if (classes.length > 0) {
                const classHeader = document.createElement("h2");
                classHeader.className = "section-title";
                classHeader.textContent = "Classes";
                courseGrid.appendChild(classHeader);

                classes.forEach(cls => {
                    const card = createCard(cls, "class-card");
                    courseGrid.appendChild(card);
                });
            }

            if (activities.length > 0) {
                const activityHeader = document.createElement("h2");
                activityHeader.className = "section-title";
                activityHeader.textContent = "Extracurricular Activities";
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

// Initialize listeners
function initializeEventListeners() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function () {
            navItems.forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

// DOM Ready
document.addEventListener('DOMContentLoaded', function () {
    initializeEventListeners();
    fetchRecommendations();
});
