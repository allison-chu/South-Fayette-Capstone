if (performance.getEntriesByType("navigation")[0]?.type === "reload") {
    sessionStorage.removeItem("explorePage");
}

// Render sidebar
document.getElementById("sidebar").innerHTML = `
  <div class="sidebar-logo"><div class="logo-placeholder">LOGO</div></div>
  <div style="text-align:center;padding:20px;">
    <img src="https://api.dicebear.com/6.x/adventurer/svg?seed=${student.name}" style="border-radius:50%;width:80px;height:80px;margin-bottom:10px;">
    <h3>${student.name}</h3>
    <p style="font-size:0.8rem;color:gray;">${student.email}</p>
    <p style="font-size:0.8rem;color:gray;">Grade: ${student.gradeLevel}</p>
    <p style="font-size:0.8rem;color:gray;">Interests: ${student.interests}</p>
    <button class="logout nav-item" onclick="logout()">Logout</button>
  </div>
`;

fetch("/recommendations", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ student: student.name })
})
.then(res => res.json())
.then(data => {
  const grid = document.getElementById("course-grid");
  grid.innerHTML = "";
  const all = [...(data.classes || []), ...(data.activities || [])];
  all.forEach(rec => {
    const div = document.createElement("div");
    div.className = "course-card";
    div.innerHTML = `
      <div class="course-image-explore"></div>
      <div class="course-content" data-full-description="${rec.description}">
        <h3 class="course-title">${capitalizeWords(rec.name)}</h3>
        <div class="course-tags">
          ${(rec.tags || "").split(",").map(t => `<span class="tag">${capitalizeWords(t.trim())}</span>`).join("")}
        </div>
        <p class="course-description">${truncate(rec.description)}</p>
        <div class="course-actions">
          <button class="btn btn-primary" onclick="viewDetails(this)">View Details</button>
          <button class="btn btn-secondary" onclick="addToStack(this)">Add to Stack</button>
        </div>
      </div>`;
    grid.appendChild(div);
  });
})
.catch(err => {
  console.error("Failed to fetch recommendations:", err);
  document.getElementById("course-grid").innerHTML =
    "<p style='color:red;'>Failed to load recommendations.</p>";
});

function capitalizeWords(str) {
  return str
    .split(" ")
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

function truncate(text, maxLength = 150) {
  return text.length > maxLength ? text.slice(0, maxLength) + '…' : text;
}

function logout() {
  window.location.href = "/logout";
}

function scrollRecommendations(dir) {
    const grid = document.getElementById('recGrid');
    grid.scrollBy({ left: dir * 250, behavior: 'smooth' });
}

function viewDetails(button) {
  const card = button.closest('.course-card');
  const content = card.querySelector('.course-content');
  const title = content.querySelector('.course-title').textContent;
  const description = content.getAttribute('data-full-description');
  const tags = Array.from(content.querySelectorAll('.tag')).map(tag => tag.textContent);
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

      <div class="recommendations-title">You May Also Like</div>
      <div class="recommendations-wrapper">
          <div class="nav-arrow" onclick="scrollRecommendations(-1)">‹</div>
          <div class="recommendations-grid" id="recGrid"><p>Loading recommendations…</p></div>
          <div class="nav-arrow" onclick="scrollRecommendations(1)">›</div>
      </div>
  `;

  document.querySelector('.container').innerHTML = detailContent;
  document.title = title;
  window.scrollTo(0, 0);

  fetchDummyRecommendations();
}

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
      const all = [...(data.classes || []), ...(data.activities || [])].slice(0, 4);
      all.forEach(item => {
          const tags = (item.tags || "")
              .split(",")
              .map(tag => capitalizeWords(tag.trim()))
              .slice(0, 2);
          const card = document.createElement("div");
          card.className = "recommendation-card";
          card.style.flex = "1";
          card.style.width = "auto";
          card.style.minWidth = "200px";
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
              </div>`;
          recGrid.appendChild(card);
      });
  });
}

function goBackToExplore() {
  const cached = sessionStorage.getItem("previousPage");
  document.querySelector('.container').innerHTML = cached;
  document.title = 'Explore';
  initializeEventListeners();
}

function addToStack(button) {
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

function initializeEventListeners() {
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
      item.addEventListener('click', function () {
          navItems.forEach(nav => nav.classList.remove('active'));
          this.classList.add('active');
      });
  });
}

// if you use login screen still:
function handleLogin() {
  const username = document.getElementById("username").value.trim().toLowerCase();
  if (!students[username]) {
    alert("Invalid user!");
    return;
  }
  sessionStorage.setItem("currentStudent", username);
  document.getElementById("login-screen").style.display = "none";
  document.getElementById("main-app").style.display = "flex";
  updateProfile(students[username]);

  fetch('/get-current-student', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      currentStudent: currentStudent
    })
  });
}

function updateProfile(student) {
  const sidebar = document.querySelector(".sidebar");
  sidebar.innerHTML = `
    <div class="sidebar-logo"><div class="logo-placeholder">LOGO</div></div>
    <div style="text-align:center;margin-top:20px;">
      <img src="${student.profilePic}" style="border-radius:50%;width:80px;height:80px;">
      <h3>${student.name}</h3>
    </div>
    <div class="nav-bottom" style="margin-top:auto;">
      <button class="nav-item" onclick="logout()">Logout</button>
    </div>
  `;
}
