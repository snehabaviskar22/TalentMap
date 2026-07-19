/* TalentMap — frontend interactions */
(function () {
  'use strict';

  const TalentMap = {
    toast(message, type) {
      type = type || 'info';
      const container = document.getElementById('toastContainer');
      if (!container) return;
      const palette = {
        success: { bg: '#43AA8B', icon: 'fa-circle-check' },
        error: { bg: '#E63946', icon: 'fa-circle-exclamation' },
        warning: { bg: '#F4A261', icon: 'fa-triangle-exclamation' },
        info: { bg: '#6C63FF', icon: 'fa-circle-info' },
      };
      const c = palette[type] || palette.info;
      const el = document.createElement('div');
      el.className = 'toast show';
      el.setAttribute('role', 'alert');
      el.style.background = c.bg;
      el.style.color = '#fff';
      el.innerHTML =
        '<div class="toast-body d-flex align-items-center gap-2">' +
        '<i class="fa-solid ' + c.icon + '"></i><span>' + message + '</span></div>';
      container.appendChild(el);
      setTimeout(() => {
        el.classList.remove('show');
        el.style.opacity = '0';
        setTimeout(() => el.remove(), 300);
      }, 3200);
    },

    showLoading() {
      const o = document.getElementById('loadingOverlay');
      if (o) o.style.display = 'grid';
    },
    hideLoading() {
      const o = document.getElementById('loadingOverlay');
      if (o) o.style.display = 'none';
    },

    confirm(url, text) {
      const modalEl = document.getElementById('confirmModal');
      if (!modalEl) return;
      const textEl = document.getElementById('confirmText');
      const btn = document.getElementById('confirmActionBtn');
      if (textEl) textEl.textContent = text || 'This action cannot be undone.';
      if (btn) btn.href = url;
      const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
      modal.show();
    },
  };

  window.TalentMap = TalentMap;

  document.addEventListener('DOMContentLoaded', function () {
    // Sidebar toggle (mobile)
    const toggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    if (toggle && sidebar) {
      toggle.addEventListener('click', () => sidebar.classList.toggle('open'));
    }

    // Confirm dialogs
    document.querySelectorAll('[data-confirm]').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const url = btn.getAttribute('data-confirm-url');
        const text = btn.getAttribute('data-confirm-text');
        TalentMap.confirm(url, text);
      });
    });

    // Auto-hide toasts after load
    document.querySelectorAll('.toast.show').forEach((t) => {
      setTimeout(() => {
        t.classList.remove('show');
        setTimeout(() => t.remove(), 300);
      }, 3200);
    });

    // Loading overlay on form submits
    document.querySelectorAll('form[method="post"]').forEach((form) => {
      form.addEventListener('submit', () => TalentMap.showLoading());
    });

    // Global search redirect (simple)
    const gs = document.getElementById('globalSearch');
    if (gs) {
      gs.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && gs.value.trim()) {
          window.location.href = '/employees/?search=' + encodeURIComponent(gs.value.trim());
        }
      });
    }
  });
})();
