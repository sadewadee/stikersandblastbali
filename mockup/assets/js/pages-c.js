/*! Sticker Sandblast Bali - pages-c.js
 *  Skrip halaman FAQ, Artikel single, dan Kontak. Vanilla JS, dipasang lewat SBB.init (app.js).
 *    initFaq        filter kategori FAQ (atribut hidden) + navigasi panah pada item yang terlihat
 *    initToc        sorot bagian aktif pada daftar isi (IntersectionObserver)
 *    initQuoteForm  validasi formulir penawaran (mock): galat inline aksesibel + status sukses
 *  Semua konten tetap terbaca tanpa JS.
 */
(function () {
  'use strict';

  var doc = document;
  function qs(sel, ctx) { return (ctx || doc).querySelector(sel); }
  function qsa(sel, ctx) { return Array.prototype.slice.call((ctx || doc).querySelectorAll(sel)); }
  function safe(fn) {
    try { fn(); } catch (err) { if (window.console) { console.error('[SBB pages-c]', err); } }
  }

  /* ================================================================== FAQ */
  function initFaq() {
    var root = qs('[data-faq]');
    if (!root) { return; }
    var list = qs('[data-faq-list]', root);
    var filters = qs('.faq-filters', root);
    var status = qs('[data-faq-status]', root);
    if (!list || !filters) { return; }
    var items = qsa('.accordion__item', list);
    var chips = qsa('[data-faq-filter]', filters);

    function closeItem(item) {
      var trigger = qs('.accordion__trigger', item);
      if (!trigger || trigger.getAttribute('aria-expanded') !== 'true') { return; }
      if (window.SBB && SBB.modules && SBB.modules.accordion) {
        SBB.modules.accordion.toggle(trigger);
      } else {
        item.classList.remove('is-open');
        trigger.setAttribute('aria-expanded', 'false');
      }
    }

    function apply(cat) {
      var shown = 0;
      var label = '';
      items.forEach(function (item) {
        var match = cat === 'all' || item.getAttribute('data-cat') === cat;
        item.hidden = !match;
        if (match) { shown += 1; } else { closeItem(item); }
      });
      chips.forEach(function (chip) {
        var on = chip.getAttribute('data-faq-filter') === cat;
        chip.setAttribute('aria-pressed', on ? 'true' : 'false');
        if (on) { label = chip.textContent.trim(); }
      });
      if (status) {
        status.textContent = 'Menampilkan ' + shown + ' dari ' + items.length + ' pertanyaan' +
          (cat === 'all' ? '' : ', kategori ' + label);
      }
    }

    filters.addEventListener('click', function (e) {
      var chip = e.target.closest('[data-faq-filter]');
      if (chip) { apply(chip.getAttribute('data-faq-filter')); }
    });

    filters.hidden = false; /* chip hanya tampil bila JS aktif */
    apply('all');
  }

  /* ================================================================== TOC */
  function initToc() {
    var links = qsa('.toc a[href^="#"]');
    if (!links.length) { return; }
    var seen = {};
    var heads = [];
    links.forEach(function (a) {
      var id = a.getAttribute('href').slice(1);
      var el = id ? doc.getElementById(id) : null;
      if (el && !seen[id]) { seen[id] = true; heads.push({ id: id, el: el }); }
    });
    if (!heads.length) { return; }

    function offset() {
      var header = qs('.site-header');
      return (header ? header.getBoundingClientRect().height : 76) + 32;
    }
    function update() {
      var off = offset();
      var current = null;
      heads.forEach(function (h) { if (h.el.getBoundingClientRect().top <= off) { current = h.id; } });
      links.forEach(function (a) {
        if (current && a.getAttribute('href') === '#' + current) { a.setAttribute('aria-current', 'location'); }
        else { a.removeAttribute('aria-current'); }
      });
    }

    if (!('IntersectionObserver' in window)) { return; }
    var io = new IntersectionObserver(update, {
      rootMargin: '-' + Math.round(offset()) + 'px 0px 0px 0px',
      threshold: [0, 1]
    });
    heads.forEach(function (h) { io.observe(h.el); });
    window.addEventListener('resize', update);
    update();
  }

  /* ========================================================== FORM PENAWARAN */
  function initQuoteForm() {
    var form = qs('form[data-quote-form]');
    if (!form) { return; }
    var wrap = form.parentNode;
    var alertBox = qs('.form-quote__alert', form);
    var success = qs('.form-success', wrap);
    var fileList = qs('.file-list', form);
    var submitted = false;

    var labels = { nama: 'Nama', whatsapp: 'Nomor WhatsApp', layanan: 'Jenis layanan', ukuran: 'Perkiraan ukuran', area: 'Area atau kota', foto: 'Foto' };
    var rules = {
      nama: function (v) { return v.trim().length >= 2 ? '' : 'Tulis nama Anda, minimal 2 huruf.'; },
      whatsapp: function (v) {
        var d = v.replace(/[\s.\-()]/g, '');
        if (!d) { return 'Isi nomor WhatsApp Anda.'; }
        return /^(\+62|62|0)8\d{8,11}$/.test(d) ? '' : 'Nomor belum valid. Gunakan nomor seluler Indonesia yang diawali 08.';
      },
      layanan: function (v) { return v ? '' : 'Pilih jenis layanan yang Anda butuhkan.'; },
      ukuran: function (v) {
        v = v.trim();
        if (!v) { return ''; }
        var n = parseFloat(v.replace(',', '.'));
        return (/^[0-9]+([.,][0-9]+)?$/.test(v) && n > 0 && n <= 10000) ? '' : 'Isi angka saja, misalnya 4 atau 6,5 (dalam m²).';
      },
      area: function (v) { return v ? '' : 'Pilih area atau kota pemasangan.'; },
      foto: function (v, el) {
        var files = el.files || [];
        for (var i = 0; i < files.length; i += 1) {
          if (!/^image\//.test(files[i].type)) { return 'Hanya berkas gambar (JPG, PNG, atau WebP) yang bisa diunggah.'; }
        }
        return '';
      }
    };

    function controls() {
      return qsa('input, select, textarea', form).filter(function (el) { return rules[el.name]; });
    }
    function setError(el, msg) {
      var err = doc.getElementById('err-' + el.name);
      if (!err) { return !msg; }
      if (msg) {
        err.textContent = msg;
        err.hidden = false;
        el.setAttribute('aria-invalid', 'true');
      } else {
        err.textContent = '';
        err.hidden = true;
        el.removeAttribute('aria-invalid');
      }
      return !msg;
    }
    function check(el) { return setError(el, rules[el.name](el.value, el)); }

    function renderFiles() {
      var input = qs('input[type="file"]', form);
      if (!input || !fileList) { return; }
      fileList.textContent = '';
      Array.prototype.forEach.call(input.files || [], function (f) {
        var li = doc.createElement('li');
        li.textContent = f.name;
        fileList.appendChild(li);
      });
    }

    /* Galat yang muncul saat blur menggeser tata letak; bila pointer sedang menekan tombol kirim,
       tombol ikut bergeser dan klik hilang. Selama itu validasi blur dilewati (submit tetap memvalidasi semua). */
    var pressing = false;
    var pressTimer = null;
    form.addEventListener('pointerdown', function (e) {
      if (e.target.closest && e.target.closest('button[type="submit"]')) { pressing = true; window.clearTimeout(pressTimer); }
    });
    ['pointerup', 'pointercancel'].forEach(function (evt) {
      form.addEventListener(evt, function () {
        window.clearTimeout(pressTimer);
        pressTimer = window.setTimeout(function () { pressing = false; }, 400);
      });
    });

    form.addEventListener('focusout', function (e) {
      var el = e.target;
      if (pressing || !el || !el.name || !rules[el.name]) { return; }
      if (submitted || el.value) { check(el); }
    });
    form.addEventListener('input', function (e) {
      var el = e.target;
      if (el && el.name && rules[el.name] && el.getAttribute('aria-invalid') === 'true') { check(el); }
    });
    form.addEventListener('change', function (e) {
      var el = e.target;
      if (!el || !el.name || !rules[el.name]) { return; }
      if (el.type === 'file') { renderFiles(); }
      if (pressing) { return; } /* 'change' pada input teks terbit saat blur oleh klik tombol kirim */
      if (submitted || el.type === 'file' || el.tagName === 'SELECT') { check(el); }
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      e.stopPropagation(); /* jangan diteruskan ke penanganan generik form[data-mock] di app.js */
      submitted = true;
      var bad = controls().filter(function (el) { return !check(el); });
      if (bad.length) {
        if (alertBox) {
          alertBox.textContent = 'Ada ' + bad.length + ' isian yang perlu diperbaiki: ' +
            bad.map(function (el) { return labels[el.name]; }).join(', ') + '.';
          alertBox.hidden = false;
        }
        bad[0].focus();
        return;
      }
      if (alertBox) { alertBox.hidden = true; alertBox.textContent = ''; }
      if (success) {
        var who = qs('[data-success-name]', success);
        var nameEl = qs('[name="nama"]', form);
        if (who && nameEl) { who.textContent = nameEl.value.trim(); }
        form.hidden = true;
        success.hidden = false;
        success.focus();
      }
    });

    var again = success ? qs('[data-form-again]', success) : null;
    if (again) {
      again.addEventListener('click', function () {
        form.reset();
        submitted = false;
        controls().forEach(function (el) { setError(el, ''); });
        renderFiles();
        success.hidden = true;
        form.hidden = false;
        var first = controls()[0];
        if (first) { first.focus(); }
      });
    }
  }

  /* ================================================================== BOOT */
  function run() {
    safe(initFaq);
    safe(initToc);
    safe(initQuoteForm);
  }
  if (window.SBB && typeof window.SBB.init === 'function') { window.SBB.init(run); }
  else if (doc.readyState === 'loading') { doc.addEventListener('DOMContentLoaded', run); }
  else { run(); }
}());
