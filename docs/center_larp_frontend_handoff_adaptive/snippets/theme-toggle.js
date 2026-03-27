(function () {
  const KEY = 'center-larp-theme';
  const root = document.documentElement;
  const buttons = Array.from(document.querySelectorAll('[data-theme-choice]'));
  const allowed = new Set(['auto', 'day', 'night']);

  function readTheme() {
    const stored = window.localStorage.getItem(KEY);
    if (stored && allowed.has(stored)) return stored;
    return root.dataset.theme || 'auto';
  }

  function applyTheme(mode) {
    const next = allowed.has(mode) ? mode : 'auto';
    root.dataset.theme = next;
    window.localStorage.setItem(KEY, next);
    buttons.forEach(function (button) {
      const pressed = button.dataset.themeChoice === next;
      button.setAttribute('aria-pressed', pressed ? 'true' : 'false');
    });
  }

  buttons.forEach(function (button) {
    button.addEventListener('click', function () {
      applyTheme(button.dataset.themeChoice);
    });
  });

  applyTheme(readTheme());
})();
