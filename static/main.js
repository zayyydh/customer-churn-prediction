// ── Dark Mode ──
const root = document.documentElement;

// Load saved preference
if (localStorage.getItem('theme') === 'dark') {
    root.setAttribute('data-theme', 'dark');
    updateToggleBtn('☀️');
}

function toggleDark() {
    const isDark = root.getAttribute('data-theme') === 'dark';
    root.setAttribute('data-theme', isDark ? 'light' : 'dark');
    localStorage.setItem('theme', isDark ? 'light' : 'dark');
    updateToggleBtn(isDark ? '🌙' : '☀️');
}

function updateToggleBtn(icon) {
    const btn = document.querySelector('.dark-toggle');
    if (btn) btn.textContent = icon;
}

// ── Mobile hamburger menu ──
function toggleMenu() {
    const nav = document.getElementById('nav-links');
    nav.classList.toggle('open');
}