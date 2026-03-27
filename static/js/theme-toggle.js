(function () {
  var KEY = 'center-larp-theme';
  var root = document.documentElement;
  var buttons = Array.from(document.querySelectorAll('[data-theme-choice]'));
  var allowed = new Set(['auto', 'day', 'night']);

  function readTheme() {
    try {
      var stored = window.localStorage.getItem(KEY);
      if (stored && allowed.has(stored)) return stored;
    } catch (_) { /* private browsing or storage disabled */ }
    return root.dataset.theme || 'auto';
  }

  function applyTheme(mode) {
    var next = allowed.has(mode) ? mode : 'auto';
    root.dataset.theme = next;
    try { window.localStorage.setItem(KEY, next); } catch (_) { /* ignore */ }
    buttons.forEach(function (button) {
      var pressed = button.dataset.themeChoice === next;
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
