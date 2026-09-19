(() => {
/* Progressive enhancement only: links, articles, photos, and video fallbacks
   still work without JavaScript. No frameworks, cookies, or analytics. */
'use strict';
document.documentElement.classList.add('js');

// Mobile navigation: explicit state, Escape handling, and predictable focus.
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.getElementById('site-nav');
function closeMenu(returnFocus = false) {
  if (!menuButton || !navigation) return;
  const wasOpen = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', 'false');
  navigation.classList.remove('is-open');
  menuButton.innerHTML = 'Menu <span aria-hidden="true">+</span>';
  if (returnFocus && wasOpen) menuButton.focus();
}
menuButton?.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  navigation.classList.toggle('is-open', open);
  menuButton.innerHTML = open ? 'Close <span aria-hidden="true">&times;</span>' : 'Menu <span aria-hidden="true">+</span>';
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') closeMenu(true);
});
document.addEventListener('click', (event) => {
  if (menuButton && !event.target.closest('.site-header')) closeMenu();
});
window.matchMedia('(min-width: 701px)').addEventListener('change', () => closeMenu());

// Project search and categories work together. Query parameters make a filter
// shareable and preserve it when navigating back from a project.
const controls = document.querySelector('.catalog-controls');
if (controls) {
  controls.hidden = false;
  const cards = [...document.querySelectorAll('[data-project]')];
  const filters = [...document.querySelectorAll('[data-filter]')];
  const search = document.getElementById('project-search');
  const clear = document.querySelector('[data-clear-search]');
  const status = document.querySelector('[data-project-count]');
  const empty = document.querySelector('.empty-state');
  const validCategories = new Set(filters.map((button) => button.dataset.filter));
  let category = 'all';
  const normalize = (value) => value.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '');
  function applyFilters(writeUrl = true) {
    const query = normalize(search.value.trim());
    const words = query.split(/\s+/).filter(Boolean);
    let count = 0;
    cards.forEach((card) => {
      const matchesCategory = category === 'all' || card.dataset.category === category;
      const haystack = normalize(card.dataset.search);
      const matchesText = words.every((word) => haystack.includes(word));
      card.hidden = !(matchesCategory && matchesText);
      if (!card.hidden) count += 1;
    });
    filters.forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
    status.textContent = `${count} ${count === 1 ? 'project' : 'projects'}`;
    empty.hidden = count !== 0;
    clear.hidden = search.value.length === 0;
    if (writeUrl) {
      const url = new URL(location.href);
      if (category !== 'all') url.searchParams.set('category', category);
      else url.searchParams.delete('category');
      if (search.value.trim()) url.searchParams.set('q', search.value.trim());
      else url.searchParams.delete('q');
      try { history.replaceState(null, '', url); } catch { /* file preview fallback */ }
    }
  }
  function readUrl() {
    const params = new URLSearchParams(location.search);
    category = validCategories.has(params.get('category')) ? params.get('category') : 'all';
    search.value = params.get('q') || '';
    applyFilters(false);
  }
  filters.forEach((button) => button.addEventListener('click', () => {
    category = button.dataset.filter;
    applyFilters();
  }));
  search.addEventListener('input', () => applyFilters());
  clear.addEventListener('click', () => { search.value = ''; applyFilters(); search.focus(); });
  document.querySelector('[data-reset-filters]').addEventListener('click', () => {
    category = 'all'; search.value = ''; applyFilters(); search.focus();
  });
  window.addEventListener('popstate', readUrl);
  window.addEventListener('pageshow', readUrl);
  readUrl();
}

// Still-image viewer. Native <dialog> supplies modal focus containment. The
// original link remains usable in browsers without a dialog implementation.
const dialog = document.getElementById('lightbox');
if (dialog && typeof dialog.showModal === 'function') {
  const openers = [...document.querySelectorAll('[data-gallery-src]')];
  // A photo may appear in the article and again in the gallery. Show it once
  // in the modal, but restore focus to whichever link the visitor selected.
  const gallery = [...new Map(openers.map((item) => [item.dataset.gallerySrc, item])).values()];
  const picture = dialog.querySelector('.lightbox-image');
  const caption = dialog.querySelector('.lightbox-caption');
  const counter = dialog.querySelector('[data-image-count]');
  const original = dialog.querySelector('[data-original]');
  let index = 0;
  let opener = null;
  function showImage(next) {
    index = (next + gallery.length) % gallery.length;
    const item = gallery[index];
    picture.src = item.dataset.gallerySrc;
    picture.alt = item.dataset.caption || '';
    caption.textContent = item.dataset.caption || '';
    counter.textContent = `${index + 1} / ${gallery.length}`;
    original.href = item.dataset.gallerySrc;
    dialog.querySelector('[data-prev]').disabled = gallery.length < 2;
    dialog.querySelector('[data-next]').disabled = gallery.length < 2;
  }
  openers.forEach((item) => item.addEventListener('click', (event) => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault(); opener = item;
    showImage(gallery.findIndex((photo) => photo.dataset.gallerySrc === item.dataset.gallerySrc));
    dialog.showModal(); document.body.classList.add('dialog-open');
  }));
  dialog.querySelector('[data-prev]').addEventListener('click', () => showImage(index - 1));
  dialog.querySelector('[data-next]').addEventListener('click', () => showImage(index + 1));
  dialog.querySelector('[data-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault(); showImage(index + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  dialog.addEventListener('click', (event) => {
    if (event.target !== dialog) return;
    const bounds = dialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => {
    document.body.classList.remove('dialog-open');
    picture.removeAttribute('src');
    opener?.focus({ preventScroll: true });
  });
}

// Only one video plays at a time. YouTube is not contacted until a visitor
// explicitly selects a video. A direct YouTube link is always visible below it.
function pauseOtherVideos(except = null) {
  document.querySelectorAll('video').forEach((video) => { if (video !== except) video.pause(); });
  document.querySelectorAll('.youtube-player.is-playing').forEach((player) => {
    if (player !== except) {
      player.querySelector('iframe')?.remove();
      const poster = player.querySelector('.youtube-play');
      if (poster) poster.hidden = false;
      player.classList.remove('is-playing');
    }
  });
}
document.querySelectorAll('.youtube-player').forEach((player) => {
  const poster = player.querySelector('.youtube-play');
  poster.addEventListener('click', (event) => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault(); pauseOtherVideos(player);
    const id = player.dataset.youtube;
    if (!/^[A-Za-z0-9_-]{11}$/.test(id)) { window.open(poster.href, '_blank', 'noopener'); return; }
    const src = new URL(`https://www.youtube-nocookie.com/embed/${id}`);
    src.searchParams.set('autoplay', '1');
    src.searchParams.set('playsinline', '1');
    src.searchParams.set('rel', '0');
    const start = parseInt(player.dataset.start, 10);
    if (start > 0) src.searchParams.set('start', String(start));
    const iframe = document.createElement('iframe');
    iframe.src = src.href;
    iframe.title = player.dataset.title || 'Project video';
    iframe.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
    iframe.allowFullscreen = true;
    iframe.referrerPolicy = 'strict-origin-when-cross-origin';
    poster.hidden = true; player.classList.add('is-playing'); player.append(iframe); iframe.focus();
  });
});
document.querySelectorAll('video').forEach((video) => {
  const player = video.closest('.video-player');
  if (!player) return;
  const button = player.querySelector('.local-video-play');
  button?.addEventListener('click', () => {
    pauseOtherVideos(video);
    const promise = video.play();
    if (promise) promise.catch(() => {
      // Expose native controls if a browser blocks programmatic playback.
      player.classList.add('is-playing'); video.focus();
    });
  });
  video.addEventListener('play', () => { pauseOtherVideos(video); player.classList.add('is-playing'); });
  video.addEventListener('pause', () => player.classList.remove('is-playing'));
  video.addEventListener('ended', () => player.classList.remove('is-playing'));
});
window.addEventListener('pagehide', () => pauseOtherVideos());

// Email copy includes a local-preview fallback and a human-readable error.
document.querySelectorAll('[data-copy]').forEach((button) => {
  button.hidden = false;
  button.addEventListener('click', async () => {
    const text = button.dataset.copy;
    const status = document.getElementById('copy-status');
    let copied = false;
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text); copied = true;
      } else {
        const field = document.createElement('textarea');
        field.value = text; field.style.position = 'fixed'; field.style.opacity = '0';
        document.body.append(field); field.select(); copied = document.execCommand('copy'); field.remove();
      }
    } catch { copied = false; }
    button.textContent = copied ? 'Copied' : 'Copy';
    if (status) status.textContent = copied ? 'Email address copied.' : `Copy this address: ${text}`;
    window.setTimeout(() => { button.textContent = 'Copy'; }, 2500);
  });
});

})();
