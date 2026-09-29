/*! Sticker Sandblast Bali - app.js
 *  Vanilla JS, tanpa library, tanpa build step. Satu namespace global: window.SBB.
 *
 *  Modul (semua dijalankan otomatis saat DOM siap):
 *    header      sticky header + garis saat scroll, menu mobile, dropdown (keyboard)
 *    accordion   FAQ, satu terbuka dalam satu waktu
 *    slider      before/after (pointer, touch, keyboard, role="slider")
 *    gallery     chip filter [data-category] + lightbox (Esc, focus trap, panah).
 *                Lightbox memakai <img> di .gallery__media; keterangan dari .gallery__cap / figcaption / data-caption
 *    reveal      scroll reveal (.reveal, IntersectionObserver, sekali)
 *    forms       form[data-mock]: validasi native + pesan status (mockup)
 *
 *  API untuk skrip halaman (dimuat sesudah app.js, mis. <!--@js pages-b.js-->):
 *    SBB.init(fn)          jalankan fn(SBB) saat DOM siap (langsung bila sudah siap)
 *    SBB.refresh(scope)    inisialisasi ulang konten yang baru disisipkan (slider, accordion,
 *                          gallery, reveal) di dalam scope (default: document)
 *    SBB.on(name, fn) / SBB.off(name, fn) / SBB.emit(name, detail)
 *                          event: 'accordion:toggle', 'gallery:filter', 'lightbox:open',
 *                          'lightbox:close', 'slider:change'
 *    SBB.modules           akses modul (mis. SBB.modules.gallery.filter(root, 'sandblast'))
 */
(function () {
  'use strict';

  var doc = document;
  var root = doc.documentElement;
  var SBB = window.SBB = window.SBB || {};
  var modules = {};
  var queue = [];
  var listeners = {};
  var ready = false;

  root.classList.add('js');

  /* ------------------------------------------------------------------ util */
  function qs(sel, ctx) { return (ctx || doc).querySelector(sel); }
  function qsa(sel, ctx) { return Array.prototype.slice.call((ctx || doc).querySelectorAll(sel)); }
  function clamp(v, min, max) { return Math.min(max, Math.max(min, v)); }
  function safe(fn, arg) {
    try { fn(arg); } catch (err) { if (window.console) { console.error('[SBB]', err); } }
  }
  function reducedMotion() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }
  function isDesktop() {
    return window.matchMedia('(min-width: 1025px)').matches;
  }
  function focusables(ctx) {
    return qsa('a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])', ctx)
      .filter(function (el) { return el.offsetParent !== null || el === doc.activeElement; });
  }

  /* ---------------------------------------------------------- event emitter */
  SBB.on = function (name, fn) { (listeners[name] = listeners[name] || []).push(fn); };
  SBB.off = function (name, fn) {
    listeners[name] = (listeners[name] || []).filter(function (f) { return f !== fn; });
  };
  SBB.emit = function (name, detail) {
    (listeners[name] || []).slice().forEach(function (fn) { safe(function () { fn(detail); }); });
  };

  /* ================================================================ HEADER */
  modules.header = (function () {
    var header, menuBtn, nav, cta;
    var hoverTimer = null;

    function items() { return qsa('.nav__item[data-sub]', nav); }
    function toggleOf(item) { return qs('.nav__toggle', item); }

    function setSub(item, open) {
      var t = toggleOf(item);
      item.classList.toggle('is-open', open);
      if (t) { t.setAttribute('aria-expanded', open ? 'true' : 'false'); }
    }
    function closeSubs(except) {
      items().forEach(function (it) { if (it !== except && it.classList.contains('is-open')) { setSub(it, false); } });
    }

    function menuOpen() { return root.classList.contains('menu-open'); }
    function setMenu(open) {
      if (!menuBtn || !nav) { return; }
      root.classList.toggle('menu-open', open);
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      menuBtn.setAttribute('aria-label', open ? 'Tutup menu' : 'Buka menu');
      if (open) {
        var top = header.getBoundingClientRect().bottom;
        nav.style.setProperty('--menu-h', Math.max(240, window.innerHeight - top) + 'px');
      } else {
        closeSubs(null);
      }
    }

    function onScroll() { header.classList.toggle('is-scrolled', window.scrollY > 4); }

    function bind() {
      var ticking = false;
      window.addEventListener('scroll', function () {
        if (ticking) { return; }
        ticking = true;
        window.requestAnimationFrame(function () { onScroll(); ticking = false; });
      }, { passive: true });
      onScroll();

      window.addEventListener('resize', function () {
        if (isDesktop() && menuOpen()) { setMenu(false); }
        if (menuOpen()) {
          nav.style.setProperty('--menu-h', Math.max(240, window.innerHeight - header.getBoundingClientRect().bottom) + 'px');
        }
      });

      /* klik: hamburger + toggle submenu (delegasi) + klik di luar */
      doc.addEventListener('click', function (e) {
        var mb = e.target.closest('.menu-btn');
        if (mb) { setMenu(!menuOpen()); if (menuOpen()) { var f = focusables(nav)[0]; if (f) { f.focus(); } } return; }

        var tg = e.target.closest('.nav__toggle');
        if (tg && nav.contains(tg)) {
          var item = tg.closest('.nav__item');
          var open = !item.classList.contains('is-open');
          closeSubs(item);
          setSub(item, open);
          return;
        }

        var link = e.target.closest('.nav__sub a, .nav__link');
        if (link && nav.contains(link) && menuOpen()) { setMenu(false); return; }

        if (!header.contains(e.target)) { closeSubs(null); if (menuOpen()) { setMenu(false); } }
      });

      /* hover (hanya mouse, hanya desktop) */
      items().forEach(function (item) {
        item.addEventListener('pointerenter', function (e) {
          if (e.pointerType !== 'mouse' || !isDesktop()) { return; }
          window.clearTimeout(hoverTimer);
          closeSubs(item);
          setSub(item, true);
        });
        item.addEventListener('pointerleave', function (e) {
          if (e.pointerType !== 'mouse' || !isDesktop()) { return; }
          window.clearTimeout(hoverTimer);
          hoverTimer = window.setTimeout(function () { setSub(item, false); }, 140);
        });
      });

      /* keyboard */
      doc.addEventListener('keydown', function (e) {
        var openItem = qs('.nav__item.is-open', nav);

        if (e.key === 'Escape') {
          if (openItem) {
            var t = toggleOf(openItem);
            var inside = openItem.contains(doc.activeElement);
            setSub(openItem, false);
            if (inside && t) { t.focus(); }
            e.preventDefault();
            return;
          }
          if (menuOpen()) { setMenu(false); menuBtn.focus(); e.preventDefault(); }
          return;
        }

        /* panah pada toggle / submenu */
        var active = doc.activeElement;
        if (active && active.classList && active.classList.contains('nav__toggle') && nav.contains(active)) {
          if (e.key === 'ArrowDown') {
            var it = active.closest('.nav__item');
            closeSubs(it);
            setSub(it, true);
            var first = qs('.nav__sub a', it);
            if (first) { first.focus(); }
            e.preventDefault();
            return;
          }
        }
        var subLink = active && active.closest ? active.closest('.nav__sub a') : null;
        if (subLink && nav.contains(subLink)) {
          var list = qsa('.nav__sub a', subLink.closest('.nav__item'));
          var idx = list.indexOf(subLink);
          var next = null;
          if (e.key === 'ArrowDown') { next = list[(idx + 1) % list.length]; }
          else if (e.key === 'ArrowUp') { next = list[(idx - 1 + list.length) % list.length]; }
          else if (e.key === 'Home') { next = list[0]; }
          else if (e.key === 'End') { next = list[list.length - 1]; }
          if (next) { next.focus(); e.preventDefault(); }
        }

        /* focus trap ringan saat menu mobile terbuka */
        if (e.key === 'Tab' && menuOpen() && !isDesktop()) {
          var cycle = focusables(nav).concat(cta ? [cta] : [], [menuBtn]);
          var firstEl = cycle[0];
          var lastEl = cycle[cycle.length - 1];
          if (e.shiftKey && active === firstEl) { lastEl.focus(); e.preventDefault(); }
          else if (!e.shiftKey && active === lastEl) { firstEl.focus(); e.preventDefault(); }
        }
      });

      /* fokus keluar dari item dropdown -> tutup */
      nav.addEventListener('focusout', function (e) {
        var item = e.target.closest ? e.target.closest('.nav__item[data-sub]') : null;
        if (!item) { return; }
        var to = e.relatedTarget;
        if (to && item.contains(to)) { return; }
        if (to === null) { return; } /* klik ke area kosong ditangani handler klik */
        setSub(item, false);
      });
    }

    return {
      init: function () {
        header = qs('.site-header');
        if (!header) { return; }
        menuBtn = qs('.menu-btn', header);
        nav = qs('.nav', header);
        cta = qs('.site-header__cta', header);
        if (!nav) { return; }
        bind();
      },
      closeMenu: function () { setMenu(false); }
    };
  }());

  /* ============================================================= ACCORDION */
  modules.accordion = (function () {
    function setItem(item, open) {
      var trigger = qs('.accordion__trigger', item);
      item.classList.toggle('is-open', open);
      if (trigger) { trigger.setAttribute('aria-expanded', open ? 'true' : 'false'); }
    }
    function toggle(trigger) {
      var item = trigger.closest('.accordion__item');
      var acc = item.closest('.accordion');
      var willOpen = trigger.getAttribute('aria-expanded') !== 'true';
      if (willOpen && acc) {
        qsa('.accordion__item.is-open', acc).forEach(function (other) { if (other !== item) { setItem(other, false); } });
      }
      setItem(item, willOpen);
      SBB.emit('accordion:toggle', { item: item, open: willOpen });
    }
    function sync(scope) {
      qsa('.accordion__item', scope).forEach(function (item) {
        var trigger = qs('.accordion__trigger', item);
        if (trigger) { setItem(item, trigger.getAttribute('aria-expanded') === 'true'); }
      });
    }
    function bind() {
      doc.addEventListener('click', function (e) {
        var t = e.target.closest('.accordion__trigger');
        if (t) { toggle(t); }
      });
      doc.addEventListener('keydown', function (e) {
        var t = e.target.closest ? e.target.closest('.accordion__trigger') : null;
        if (!t) { return; }
        var acc = t.closest('.accordion');
        var all = qsa('.accordion__trigger', acc).filter(function (el) { return !el.closest('[hidden]'); });
        var i = all.indexOf(t);
        var next = null;
        if (e.key === 'ArrowDown') { next = all[(i + 1) % all.length]; }
        else if (e.key === 'ArrowUp') { next = all[(i - 1 + all.length) % all.length]; }
        else if (e.key === 'Home') { next = all[0]; }
        else if (e.key === 'End') { next = all[all.length - 1]; }
        if (next) { next.focus(); e.preventDefault(); }
      });
    }
    return { bind: bind, init: sync, toggle: toggle };
  }());

  /* ============================================================== SLIDER */
  modules.slider = (function () {
    function setup(el) {
      if (el.__sbbSlider) { return; }
      var handle = qs('.ba-slider__handle', el);
      if (!handle) { return; }
      el.__sbbSlider = true;
      var dragging = false;

      function set(v, silent) {
        v = clamp(v, 0, 100);
        el.style.setProperty('--pos', String(v));
        var rounded = Math.round(v);
        handle.setAttribute('aria-valuenow', String(rounded));
        handle.setAttribute('aria-valuetext', 'Sebelum ' + rounded + '%, sesudah ' + (100 - rounded) + '%');
        if (!silent) { SBB.emit('slider:change', { el: el, value: rounded }); }
      }
      function fromEvent(e) {
        var rect = el.getBoundingClientRect();
        set(((e.clientX - rect.left) / rect.width) * 100);
      }

      el.addEventListener('pointerdown', function (e) {
        if (e.button !== undefined && e.button !== 0) { return; }
        dragging = true;
        el.classList.add('is-dragging');
        if (el.setPointerCapture) { try { el.setPointerCapture(e.pointerId); } catch (err) { /* abaikan */ } }
        fromEvent(e);
        handle.focus({ preventScroll: true });
      });
      el.addEventListener('pointermove', function (e) { if (dragging) { fromEvent(e); } });
      function stop(e) {
        if (!dragging) { return; }
        dragging = false;
        el.classList.remove('is-dragging');
        if (el.releasePointerCapture && e && e.pointerId !== undefined) { try { el.releasePointerCapture(e.pointerId); } catch (err) { /* abaikan */ } }
      }
      el.addEventListener('pointerup', stop);
      el.addEventListener('pointercancel', stop);

      handle.addEventListener('keydown', function (e) {
        var cur = parseFloat(handle.getAttribute('aria-valuenow')) || 0;
        var step = e.shiftKey ? 10 : 2;
        var v = null;
        if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') { v = cur - step; }
        else if (e.key === 'ArrowRight' || e.key === 'ArrowUp') { v = cur + step; }
        else if (e.key === 'PageDown') { v = cur - 10; }
        else if (e.key === 'PageUp') { v = cur + 10; }
        else if (e.key === 'Home') { v = 0; }
        else if (e.key === 'End') { v = 100; }
        if (v !== null) { set(v); e.preventDefault(); }
      });

      set(parseFloat(handle.getAttribute('aria-valuenow')) || 50, true);
    }
    return { init: function (scope) { qsa('.ba-slider', scope).forEach(setup); } };
  }());

  /* ======================================================= GALLERY + LIGHTBOX */
  modules.gallery = (function () {
    var lb = null;          /* elemen lightbox */
    var state = { items: [], index: 0, opener: null };

    function filter(galleryEl, cat) {
      var items = qsa('.gallery__item', galleryEl);
      var shown = 0;
      items.forEach(function (it) {
        var cats = (it.getAttribute('data-category') || '').split(/\s+/);
        var match = cat === 'all' || cats.indexOf(cat) !== -1;
        it.hidden = !match;
        if (match) { shown += 1; }
      });
      qsa('.chip[data-filter]', galleryEl).forEach(function (c) {
        c.setAttribute('aria-pressed', c.getAttribute('data-filter') === cat ? 'true' : 'false');
      });
      var status = qs('.gallery__status', galleryEl);
      if (status) { status.textContent = 'Menampilkan ' + shown + ' dari ' + items.length + ' foto'; }
      SBB.emit('gallery:filter', { gallery: galleryEl, category: cat, shown: shown });
    }

    /* ---- lightbox ---- */
    function build() {
      lb = doc.createElement('div');
      lb.className = 'lightbox';
      lb.setAttribute('role', 'dialog');
      lb.setAttribute('aria-modal', 'true');
      lb.setAttribute('aria-label', 'Pratinjau foto');
      lb.innerHTML =
        '<p class="lightbox__count" aria-live="polite"></p>' +
        '<button type="button" class="lightbox__btn lightbox__close" aria-label="Tutup pratinjau"><svg class="icon" aria-hidden="true"><use href="#i-close"/></svg></button>' +
        '<button type="button" class="lightbox__btn lightbox__prev" aria-label="Foto sebelumnya"><svg class="icon" aria-hidden="true"><use href="#i-chevron-left"/></svg></button>' +
        '<div class="lightbox__stage"></div>' +
        '<button type="button" class="lightbox__btn lightbox__next" aria-label="Foto berikutnya"><svg class="icon" aria-hidden="true"><use href="#i-chevron-right"/></svg></button>' +
        '<p class="lightbox__caption"></p>';
      doc.body.appendChild(lb);

      lb.addEventListener('click', function (e) {
        if (e.target.closest('.lightbox__close') || e.target === lb) { close(); }
        else if (e.target.closest('.lightbox__prev')) { go(-1); }
        else if (e.target.closest('.lightbox__next')) { go(1); }
      });

      /* geser kiri/kanan di layar sentuh */
      var startX = null;
      var stage = qs('.lightbox__stage', lb);
      stage.addEventListener('pointerdown', function (e) { startX = e.clientX; });
      stage.addEventListener('pointerup', function (e) {
        if (startX === null) { return; }
        var dx = e.clientX - startX;
        startX = null;
        if (Math.abs(dx) > 50) { go(dx < 0 ? 1 : -1); }
      });
      stage.addEventListener('pointercancel', function () { startX = null; });
    }

    function render() {
      var item = state.items[state.index];
      var stage = qs('.lightbox__stage', lb);
      var caption = qs('.lightbox__caption', lb);
      var count = qs('.lightbox__count', lb);
      stage.innerHTML = '';
      var media = qs('.gallery__media', item) || item;
      var img = qs('img', media);
      var node;
      if (img) {
        node = doc.createElement('img');
        node.src = img.getAttribute('data-full') || img.currentSrc || img.src;
        node.alt = img.alt || '';
      } else {
        var ph = qs('.ph-img', media);
        node = ph ? ph.cloneNode(true) : doc.createElement('div');
        node.classList.remove('ph-img--sm');
      }
      stage.appendChild(node);

      var cap = qs('.gallery__cap', item) || qs('figcaption', item);
      if (cap) {
        caption.innerHTML = cap.innerHTML;
      } else {
        caption.textContent = item.getAttribute('data-caption') || (img && img.getAttribute('data-caption')) || '';
      }
      count.textContent = (state.index + 1) + ' / ' + state.items.length;
      qs('.lightbox__prev', lb).disabled = state.index === 0;
      qs('.lightbox__next', lb).disabled = state.index === state.items.length - 1;
    }

    function go(delta) {
      var n = state.index + delta;
      if (n < 0 || n >= state.items.length) { return; }
      state.index = n;
      render();
    }

    function open(galleryEl, item, opener) {
      if (!lb) { build(); }
      state.items = qsa('.gallery__item', galleryEl).filter(function (i) { return !i.hidden; });
      state.index = Math.max(0, state.items.indexOf(item));
      state.opener = opener;
      render();
      lb.classList.add('is-open');
      root.classList.add('no-scroll');
      qs('.lightbox__close', lb).focus();
      SBB.emit('lightbox:open', { index: state.index });
    }

    function close() {
      if (!lb || !lb.classList.contains('is-open')) { return; }
      lb.classList.remove('is-open');
      root.classList.remove('no-scroll');
      qs('.lightbox__stage', lb).innerHTML = '';
      if (state.opener && state.opener.focus) { state.opener.focus(); }
      SBB.emit('lightbox:close', {});
    }

    function bind() {
      doc.addEventListener('click', function (e) {
        var chip = e.target.closest('.chip[data-filter]');
        if (chip) {
          var g = chip.closest('[data-gallery]');
          if (g) { filter(g, chip.getAttribute('data-filter')); }
          return;
        }
        var opener = e.target.closest('.gallery__open');
        if (opener) {
          var gal = opener.closest('[data-gallery]');
          var item = opener.closest('.gallery__item');
          if (gal && item) { open(gal, item, opener); }
        }
      });

      doc.addEventListener('keydown', function (e) {
        if (!lb || !lb.classList.contains('is-open')) { return; }
        if (e.key === 'Escape') { close(); e.preventDefault(); }
        else if (e.key === 'ArrowLeft') { go(-1); e.preventDefault(); }
        else if (e.key === 'ArrowRight') { go(1); e.preventDefault(); }
        else if (e.key === 'Tab') {
          var f = focusables(lb);
          if (!f.length) { e.preventDefault(); return; }
          var first = f[0];
          var last = f[f.length - 1];
          if (e.shiftKey && (doc.activeElement === first || !lb.contains(doc.activeElement))) { last.focus(); e.preventDefault(); }
          else if (!e.shiftKey && (doc.activeElement === last || !lb.contains(doc.activeElement))) { first.focus(); e.preventDefault(); }
        }
      });
    }

    return {
      bind: bind,
      init: function (scope) {
        /* sinkronkan status awal ("Menampilkan N dari N foto") */
        qsa('[data-gallery]', scope).forEach(function (g) {
          var status = qs('.gallery__status', g);
          if (status && !status.textContent.trim()) {
            var n = qsa('.gallery__item', g).length;
            status.textContent = 'Menampilkan ' + n + ' dari ' + n + ' foto';
          }
        });
      },
      filter: filter,
      open: open,
      close: close
    };
  }());

  /* ============================================================== REVEAL */
  modules.reveal = (function () {
    var io = null;
    function show(el) { el.classList.add('is-visible'); }
    function init(scope) {
      qsa('[data-stagger]', scope).forEach(function (group) {
        qsa(':scope > .reveal', group).forEach(function (child, i) { child.style.setProperty('--reveal-i', String(Math.min(i, 5))); });
      });
      var els = qsa('.reveal:not(.is-visible)', scope);
      if (!els.length) { return; }
      if (reducedMotion() || !('IntersectionObserver' in window)) { els.forEach(show); return; }
      if (!io) {
        io = new IntersectionObserver(function (entries) {
          entries.forEach(function (en) {
            if (en.isIntersecting) { show(en.target); io.unobserve(en.target); }
          });
        }, { rootMargin: '0px 0px -6% 0px', threshold: 0.06 });
      }
      els.forEach(function (el) { io.observe(el); });
    }
    return { init: init };
  }());

  /* ================================================================ FORMS */
  modules.forms = (function () {
    return {
      bind: function () {
        doc.addEventListener('submit', function (e) {
          var form = e.target;
          if (!form.matches || !form.matches('form[data-mock]')) { return; }
          e.preventDefault();
          if (form.checkValidity && !form.checkValidity()) { form.reportValidity(); return; }
          var status = qs('.form-quote__status', form);
          if (status) {
            status.hidden = false;
            status.textContent = form.getAttribute('data-mock') || 'Ini mockup: formulir belum terhubung ke server.';
          }
        });
      }
    };
  }());

  /* ================================================================= BOOT */
  SBB.modules = modules;
  SBB.version = '1.0.0';

  SBB.refresh = function (scope) {
    scope = scope || doc;
    safe(function () { modules.accordion.init(scope); });
    safe(function () { modules.slider.init(scope); });
    safe(function () { modules.gallery.init(scope); });
    safe(function () { modules.reveal.init(scope); });
  };

  SBB.init = function (fn) {
    if (typeof fn !== 'function') { return; }
    if (ready) { safe(fn, SBB); } else { queue.push(fn); }
  };

  function boot() {
    if (ready) { return; }
    ready = true;
    safe(modules.header.init);
    safe(modules.accordion.bind);
    safe(modules.gallery.bind);
    safe(modules.forms.bind);
    SBB.refresh(doc);
    queue.splice(0).forEach(function (fn) { safe(fn, SBB); });
  }

  if (doc.readyState === 'loading') { doc.addEventListener('DOMContentLoaded', boot); }
  else { boot(); }
}());
