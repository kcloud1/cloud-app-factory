let demoCount = 0;
const demoResult = document.getElementById('demo-result');
const themeToggle = document.getElementById('theme-toggle');
document.getElementById('demo-action').addEventListener('click', () => {
  demoCount += 1;
  demoResult.textContent = `Demo action completed ${demoCount} time${demoCount === 1 ? '' : 's'}. No cloud changes.`;
});
themeToggle.addEventListener('click', () => {
  const dark = document.documentElement.dataset.theme !== 'dark';
  document.documentElement.dataset.theme = dark ? 'dark' : 'light';
  themeToggle.setAttribute('aria-pressed', String(dark));
  themeToggle.textContent = dark ? 'Light mode' : 'Dark mode';
});
