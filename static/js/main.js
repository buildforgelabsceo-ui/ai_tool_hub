/* AIToolHub — Main JavaScript */

// ─── Search Autocomplete ──────────────────────────────────
const searchInput = document.getElementById('hero-search');
const searchDropdown = document.getElementById('search-dropdown');

let searchTimeout;

if (searchInput) {
  searchInput.addEventListener('input', function () {
    clearTimeout(searchTimeout);
    const q = this.value.trim();

    if (q.length < 2) {
      hideDropdown();
      return;
    }

    searchTimeout = setTimeout(() => {
      fetch(`/api/search?q=${encodeURIComponent(q)}`)
        .then(r => r.json())
        .then(data => renderDropdown(data, q));
    }, 250);
  });

  searchInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      window.location.href = `/tools?q=${encodeURIComponent(this.value)}`;
    }
    if (e.key === 'Escape') hideDropdown();
  });

  document.addEventListener('click', function (e) {
    if (!e.target.closest('.search-wrapper')) hideDropdown();
  });
}

function renderDropdown(tools, query) {
  if (!searchDropdown) return;
  if (!tools.length) {
    searchDropdown.innerHTML = `
      <div style="padding:20px 24px;color:var(--text-muted);font-size:0.875rem;text-align:center;">
        No tools found for "<strong>${escHtml(query)}</strong>"
      </div>`;
    searchDropdown.classList.add('active');
    return;
  }

  searchDropdown.innerHTML = tools.map(t => `
    <a class="search-result-item" href="/tools/${t.slug}">
      <div class="search-result-logo">
        ${t.logo_url
    ? `<img src="${escHtml(t.logo_url)}" alt="${escHtml(t.name)}" onerror="this.parentElement.innerHTML='🤖'">`
    : getCategoryEmoji(t.category)
  }
      </div>
      <div>
        <div class="search-result-name">${highlight(t.name, query)}</div>
        <div class="search-result-cat">${escHtml(t.category)}</div>
      </div>
    </a>
  `).join('') + `
    <div style="padding:12px 20px;border-top:1px solid var(--border);">
      <a href="/tools?q=${encodeURIComponent(query)}" 
         style="font-size:0.82rem;color:var(--blue);font-weight:600;">
        View all results for "${escHtml(query)}" →
      </a>
    </div>`;

  searchDropdown.classList.add('active');
}

function hideDropdown() {
  if (searchDropdown) searchDropdown.classList.remove('active');
}

// ─── Nav search ───────────────────────────────────────────
const navSearchInput = document.getElementById('nav-search');
if (navSearchInput) {
  navSearchInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && this.value.trim()) {
      window.location.href = `/tools?q=${encodeURIComponent(this.value)}`;
    }
  });
}

// ─── Filter chips on /tools page ─────────────────────────
document.querySelectorAll('.filter-chip[data-filter]').forEach(chip => {
  chip.addEventListener('click', function () {
    const type = this.dataset.filterType;
    const val = this.dataset.filter;
    const url = new URL(window.location.href);
    if (url.searchParams.get(type) === val) {
      url.searchParams.delete(type);
    } else {
      url.searchParams.set(type, val);
    }
    url.searchParams.delete('page');
    window.location.href = url.toString();
  });
});

// ─── Live search on tools page ───────────────────────────
const toolsSearchInput = document.getElementById('tools-search');
if (toolsSearchInput) {
  let toolsSearchTimeout;
  toolsSearchInput.addEventListener('input', function () {
    clearTimeout(toolsSearchTimeout);
    const val = this.value;
    toolsSearchTimeout = setTimeout(() => {
      const url = new URL(window.location.href);
      if (val) { url.searchParams.set('q', val); } else { url.searchParams.delete('q'); }
      url.searchParams.delete('page');
      window.location.href = url.toString();
    }, 600);
  });

  toolsSearchInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      clearTimeout(toolsSearchTimeout);
      const url = new URL(window.location.href);
      if (this.value) { url.searchParams.set('q', this.value); } else { url.searchParams.delete('q'); }
      url.searchParams.delete('page');
      window.location.href = url.toString();
    }
  });
}

// ─── Smooth card animations on scroll ────────────────────
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.tool-card, .category-card').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(16px)';
  el.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
  observer.observe(el);
});

// ─── Submit form character counter ───────────────────────
const descField = document.getElementById('description');
const descCounter = document.getElementById('desc-counter');
if (descField && descCounter) {
  descField.addEventListener('input', function () {
    descCounter.textContent = this.value.length;
  });
}

// ─── Helpers ─────────────────────────────────────────────
function escHtml(str) {
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function highlight(text, query) {
  const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
  return escHtml(text).replace(regex, '<mark style="background:var(--yellow-soft);color:inherit;border-radius:3px;padding:0 2px;">$1</mark>');
}

function getCategoryEmoji(cat) {
  const map = {
    'AI Writing Tools': '✍️',
    'AI Image Generation': '🎨',
    'AI Video Tools': '🎬',
    'AI Coding Tools': '💻',
    'AI Productivity Tools': '⚡',
    'AI Marketing Tools': '📣',
    'AI Automation Tools': '🤖',
  };
  return map[cat] || '🔮';
}
