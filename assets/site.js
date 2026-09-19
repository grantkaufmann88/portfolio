/* Progressive enhancement. The content and every page link work without JavaScript. */
(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#site-nav');
  function closeMenu() {
    if (!menu || !nav) return;
    menu.setAttribute('aria-expanded', 'false');
    nav.classList.remove('is-open');
    menu.textContent = 'Menu +';
  }
  menu?.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
    menu.textContent = open ? 'Close −' : 'Menu +';
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true') {
      closeMenu(); menu.focus();
    }
  });
  document.addEventListener('click', event => {
    if (menu && !event.target.closest('.site-header')) closeMenu();
  });
  window.matchMedia('(min-width: 621px)').addEventListener('change', closeMenu);

  const catalog = document.querySelector('[data-catalog]');
  if (catalog) {
    const cards = [...catalog.querySelectorAll('[data-project]')];
    const filters = [...document.querySelectorAll('[data-filter]')];
    const search = document.querySelector('#project-search');
    const count = document.querySelector('#result-count');
    const empty = document.querySelector('#empty-state');
    let active = 'All';
    const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
    function filterProjects(updateURL = true) {
      const query = normalize(search.value.trim());
      let visible = 0;
      cards.forEach(card => {
        const categoryMatches = active === 'All' || (active === 'Featured' ? card.dataset.featured === 'true' : card.dataset.category === active);
        const matches = categoryMatches && normalize(card.dataset.search).includes(query);
        card.hidden = !matches;
        if (matches) visible++;
      });
      count.textContent = `${visible} of ${cards.length} projects`;
      empty.hidden = visible !== 0;
      filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === active)));
      if (updateURL && location.protocol !== 'file:') {
        const url = new URL(location.href);
        active === 'All' ? url.searchParams.delete('category') : url.searchParams.set('category', active);
        search.value.trim() ? url.searchParams.set('q', search.value.trim()) : url.searchParams.delete('q');
        history.replaceState(null, '', url);
      }
    }
    function restoreFilters() {
      const params = new URLSearchParams(location.search);
      const category = params.get('category');
      active = filters.some(button => button.dataset.filter === category) ? category : 'All';
      search.value = params.get('q') || '';
      filterProjects(false);
    }
    filters.forEach(button => button.addEventListener('click', () => { active = button.dataset.filter; filterProjects(); }));
    search.addEventListener('input', () => filterProjects());
    document.querySelector('#reset-filters').addEventListener('click', () => {
      active = 'All'; search.value = ''; filterProjects(); search.focus();
    });
    window.addEventListener('popstate', restoreFilters);
    restoreFilters();
  }

  const galleryButtons = [...document.querySelectorAll('[data-gallery-src]')];
  const dialog = document.querySelector('#lightbox');
  if (dialog && galleryButtons.length) {
    const image = dialog.querySelector('.lightbox-image');
    const caption = dialog.querySelector('.lightbox-caption');
    const counter = dialog.querySelector('[data-image-count]');
    let current = 0;
    function show(index) {
      current = (index + galleryButtons.length) % galleryButtons.length;
      const button = galleryButtons[current];
      image.src = button.dataset.gallerySrc;
      image.alt = button.dataset.caption;
      caption.textContent = button.dataset.caption;
      counter.textContent = `${String(current + 1).padStart(2, '0')} / ${String(galleryButtons.length).padStart(2, '0')}`;
    }
    galleryButtons.forEach((button, index) => button.addEventListener('click', () => {
      show(index); dialog.showModal(); document.body.classList.add('modal-open');
    }));
    dialog.querySelector('[data-close]').addEventListener('click', () => dialog.close());
    dialog.querySelector('[data-prev]').addEventListener('click', () => show(current - 1));
    dialog.querySelector('[data-next]').addEventListener('click', () => show(current + 1));
    dialog.addEventListener('keydown', event => {
      if (event.key === 'ArrowRight') { event.preventDefault(); show(current + 1); }
      if (event.key === 'ArrowLeft') { event.preventDefault(); show(current - 1); }
    });
    dialog.addEventListener('click', event => {
      const rect = dialog.getBoundingClientRect();
      if (event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) dialog.close();
    });
    dialog.addEventListener('close', () => document.body.classList.remove('modal-open'));
  }

  document.querySelectorAll('[data-copy]').forEach(button => {
    button.addEventListener('click', async () => {
      const status = document.querySelector('#copy-status');
      try {
        if (!navigator.clipboard) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(button.dataset.copy);
        status.textContent = 'Email address copied.';
        button.textContent = 'Copied ✓';
        setTimeout(() => { button.textContent = 'Copy'; }, 2500);
      } catch {
        status.textContent = `Copy this email address: ${button.dataset.copy}`;
      }
    });
  });
})();
