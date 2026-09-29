/* ==========================================================================
   pages-b.js
   Perilaku khusus halaman Harga, Portofolio, dan Galeri Video.
   Didaftarkan lewat SBB.init (app.js). Vanilla JS, tanpa library.

     1. Estimator harga   form[data-estimator]      (layanan.html)
     2. Muat lebih banyak [data-gallery][data-load-more]  (portofolio.html)
     3. Modal video       #video-modal + [data-video-open] (portofolio.html): poster besar,
                          judul, keterangan, dan tombol "Tonton di YouTube" (tanpa iframe)

   Tiap modul hanya jalan bila elemennya ada di halaman.
   ========================================================================== */
(function () {
  'use strict';

  var doc = document;
  var root = doc.documentElement;

  function qs(sel, ctx) { return (ctx || doc).querySelector(sel); }
  function qsa(sel, ctx) { return Array.prototype.slice.call((ctx || doc).querySelectorAll(sel)); }
  function safe(fn) {
    try { fn(); } catch (err) { if (window.console) { console.error('[pages-b]', err); } }
  }

  /* -------------------------------------------------------------- format id-ID */
  function fmtInt(n) {
    try { return new Intl.NumberFormat('id-ID', { maximumFractionDigits: 0 }).format(n); }
    catch (e) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, '.'); }
  }
  function fmtArea(n) {
    var r = Math.round(n * 100) / 100;
    try { return new Intl.NumberFormat('id-ID', { maximumFractionDigits: 2 }).format(r); }
    catch (e) { return String(r).replace('.', ','); }
  }

  /* =================================================================== 1. ESTIMATOR
     Estimasi = luas x harga per m2 (atribut data-price pada <option>).
     Huruf Timbul 3D memakai data-unit="huruf" + data-unit-price: dihitung per huruf setelah
     desain disepakati, jadi luas diabaikan. Tidak ada pengali atau kisaran karangan. */
  function initEstimator(form) {
    /* form berada di dalam .estimator; kotak hasil adalah saudara form, jadi cari di wadahnya */
    var box = form.closest('.estimator') || form;
    var area = qs('[data-est-area]', box);
    var svc = qs('[data-est-service]', box);
    var errEl = qs('[data-est-error]', box);
    var errText = qs('[data-est-error-text]', box);
    var label = qs('[data-est-label]', box);
    var amount = qs('[data-est-amount]', box);
    var detail = qs('[data-est-detail]', box);
    var wa = qs('[data-est-wa]', box);
    if (!area || !svc || !label || !amount || !detail) { return; }

    var WA_BASE = wa ? (wa.getAttribute('data-wa-base') || wa.getAttribute('href')) : '';
    var timer = null;

    function readArea() {
      if (area.validity && area.validity.badInput) { return { state: 'bad' }; }
      var raw = String(area.value || '').trim().replace(',', '.');
      if (raw === '') { return { state: 'empty' }; }
      var n = Number(raw);
      if (!isFinite(n)) { return { state: 'bad' }; }
      if (n < 0.1) { return { state: 'low' }; }
      return { state: 'ok', value: n };
    }

    function setText(el, text) { if (el.textContent !== text) { el.textContent = text; } }

    function setError(msg) {
      if (!errEl) { return; }
      if (msg) {
        if (errText) { setText(errText, msg); }
        errEl.hidden = false;
        area.setAttribute('aria-invalid', 'true');
      } else {
        errEl.hidden = true;
        if (errText) { setText(errText, ''); }
        area.removeAttribute('aria-invalid');
      }
    }

    function setWa(text) {
      if (!wa || !WA_BASE) { return; }
      wa.setAttribute('href', text ? WA_BASE + '?text=' + encodeURIComponent(text) : WA_BASE);
    }

    function showAmount(text, isText) {
      setText(amount, text);
      amount.classList.toggle('estimator__amount--text', !!isText);
    }

    function render(opts) {
      opts = opts || {};
      var opt = svc.options[svc.selectedIndex];
      var name = opt ? (opt.getAttribute('data-name') || opt.textContent.trim()) : '';
      var priceAttr = opt ? opt.getAttribute('data-price') : null;
      var price = priceAttr ? Number(priceAttr) : NaN;
      var hasPrice = isFinite(price) && price > 0;
      var unit = opt ? opt.getAttribute('data-unit') : null;
      var unitPrice = opt ? Number(opt.getAttribute('data-unit-price')) : NaN;

      /* Layanan yang dihitung per huruf (bukan per m2): luas tidak relevan */
      if (unit === 'huruf' && isFinite(unitPrice) && unitPrice > 0) {
        setError('');
        setText(label, 'Estimasi mulai dari');
        showAmount('Rp ' + fmtInt(unitPrice) + ' / huruf', true);
        setText(detail, name + ' dihitung per huruf setelah desain disepakati (mulai Rp ' + fmtInt(unitPrice) +
          ' / huruf), bukan per m². Kirim desain atau tulisan yang diinginkan lewat WhatsApp.');
        setWa('Halo Sticker Sandblast Bali, saya ingin penawaran ' + name + ' (mulai Rp ' + fmtInt(unitPrice) + ' / huruf).');
        return 'ok';
      }

      var a = readArea();

      if (a.state === 'bad') {
        setError('Isi luas dengan angka, misalnya 2,5.');
      } else if (a.state === 'low') {
        setError('Luas minimal 0,1 m². Isi angka yang lebih besar.');
      } else if (a.state === 'empty' && opts.submitted) {
        setError('Isi luas kaca dalam m² lebih dulu, misalnya 2,5.');
      } else {
        setError('');
      }

      if (a.state !== 'ok') {
        setText(label, hasPrice ? 'Estimasi mulai dari' : 'Harga');
        showAmount(hasPrice ? 'Rp —' : 'Ditentukan setelah survey', !hasPrice);
        setText(detail, a.state === 'empty'
          ? 'Isi luas dan pilih layanan untuk melihat estimasi.'
          : 'Isi luas yang valid untuk melihat estimasi.');
        setWa(name ? 'Halo Sticker Sandblast Bali, saya ingin tanya harga ' + name + '.' : '');
        return a.state;
      }

      var areaTxt = fmtArea(a.value);
      if (hasPrice) {
        var total = Math.round(a.value * price);
        setText(label, 'Estimasi mulai dari');
        showAmount('Rp ' + fmtInt(total), false);
        setText(detail, areaTxt + ' m² × Rp ' + fmtInt(price) + ' / m² (' + name + ')');
        setWa('Halo Sticker Sandblast Bali, saya ingin penawaran ' + name + ' seluas ' + areaTxt +
          ' m² (estimasi mulai dari Rp ' + fmtInt(total) + ').');
      } else {
        setText(label, 'Harga');
        showAmount('Ditentukan setelah survey', true);
        setText(detail, 'Harga ' + name + ' ditentukan setelah survey. Kirim foto dan ukuran kaca lewat WhatsApp untuk penawaran.');
        setWa('Halo Sticker Sandblast Bali, saya ingin penawaran ' + name + ' seluas ' + areaTxt + ' m².');
      }
      return 'ok';
    }

    function schedule() {
      clearTimeout(timer);
      timer = setTimeout(function () { render(); }, 350);
    }

    area.addEventListener('input', schedule);
    area.addEventListener('change', function () { clearTimeout(timer); render(); });
    svc.addEventListener('change', function () { clearTimeout(timer); render(); });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      clearTimeout(timer);
      var state = render({ submitted: true });
      if (state !== 'ok') { area.focus(); }
    });

    render();
  }

  /* ========================================================= 2. MUAT LEBIH BANYAK
     Menumpang di komponen galeri (app.js). Filter chip memakai atribut `hidden` pada
     item; di sini "batas awal" diterapkan ulang tiap kali filter berjalan
     (event gallery:filter), jadi keduanya tidak saling menimpa dan lightbox hanya
     berpindah antar item yang benar-benar tampil. */
  function initLoadMore(gal) {
    var limit = parseInt(gal.getAttribute('data-load-more'), 10) || 12;
    var wrap = qs('[data-more]', gal);
    var btn = qs('[data-more-btn]', gal);
    var status = qs('.gallery__status', gal);
    if (!wrap || !btn) { return; }

    var pressed = qs('.chip[data-filter][aria-pressed="true"]', gal);
    var state = { cat: pressed ? pressed.getAttribute('data-filter') : 'all', expanded: false };

    function items() { return qsa('.gallery__item', gal); }
    function matches(it) {
      if (state.cat === 'all') { return true; }
      return (it.getAttribute('data-category') || '').split(/\s+/).indexOf(state.cat) !== -1;
    }

    function apply(focusNew) {
      var all = items();
      var seen = 0;
      var total = 0;
      var shown = 0;
      var firstNew = null;
      all.forEach(function (it) {
        var match = matches(it);
        var visible = match && (state.expanded || seen < limit);
        if (match) { seen += 1; total += 1; }
        var wasHidden = it.hidden;
        it.hidden = !visible;
        if (visible) {
          shown += 1;
          if (focusNew && wasHidden && !firstNew) { firstNew = it; }
        }
      });
      wrap.hidden = state.expanded || total <= limit;
      if (status) { status.textContent = 'Menampilkan ' + shown + ' dari ' + all.length + ' foto'; }
      if (firstNew) {
        var opener = qs('.gallery__open', firstNew);
        if (opener) { opener.focus(); }
      }
    }

    btn.addEventListener('click', function () {
      state.expanded = true;
      apply(true);
    });

    if (window.SBB && window.SBB.on) {
      window.SBB.on('gallery:filter', function (d) {
        if (d && d.gallery === gal) { state.cat = d.category; apply(false); }
      });
    }

    apply(false);
  }

  /* ================================================================ 3. MODAL VIDEO
     Dialog buatan sendiri: role="dialog" + aria-modal, fokus pindah ke tombol tutup,
     Tab berputar di dalam dialog, Esc menutup, fokus kembali ke tombol pembuka.
     Isi: poster besar (dari kartu yang diklik), judul, keterangan, dan tombol
     "Tonton di YouTube" (href "#"). Tanpa iframe dan tanpa autoplay. */
  function initVideoModal(modal) {
    var openers = qsa('[data-video-open]');
    var titleEl = qs('.modal__title', modal);
    var metaEl = qs('[data-video-meta]', modal);
    var descEl = qs('[data-video-desc]', modal);
    var posterEl = qs('[data-video-poster]', modal);
    var stageEl = qs('.modal__stage', modal);
    var timeEl = qs('[data-video-time]', modal);
    var closeBtn = qs('.modal__close', modal);
    var last = null;
    if (!openers.length || !titleEl || !closeBtn) { return; }

    function isOpen() { return !modal.hidden; }

    function focusables() {
      return qsa('a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])', modal)
        .filter(function (el) { return el.offsetParent !== null; });
    }

    function textOf(el) { return el ? el.textContent.trim() : ''; }

    function open(btn) {
      var card = btn.closest('.video-card');
      var img = qs('img', btn);
      titleEl.textContent = textOf(card && qs('.video-card__title', card)) || 'Video';
      if (metaEl) { metaEl.textContent = textOf(card && qs('.video-card__meta', card)); }
      if (descEl) { descEl.textContent = textOf(card && qs('.video-card__desc', card)); }
      if (timeEl) { timeEl.textContent = textOf(qs('.video-card__time', btn)); }
      if (posterEl && img) {
        posterEl.setAttribute('src', img.getAttribute('src'));
        posterEl.setAttribute('alt', img.getAttribute('alt') || '');
        posterEl.setAttribute('width', img.getAttribute('width') || '900');
        posterEl.setAttribute('height', img.getAttribute('height') || '600');
        var frame = img.closest('.photo');
        var focus = frame ? frame.style.getPropertyValue('--focus') : '';
        if (stageEl) {
          if (focus) { stageEl.style.setProperty('--focus', focus); }
          else { stageEl.style.removeProperty('--focus'); }
        }
      }
      last = btn;
      modal.hidden = false;
      root.classList.add('no-scroll');
      closeBtn.focus();
    }

    function close() {
      if (!isOpen()) { return; }
      modal.hidden = true;
      root.classList.remove('no-scroll');
      if (last && doc.contains(last)) { last.focus(); }
      last = null;
    }

    openers.forEach(function (btn) {
      btn.addEventListener('click', function () { open(btn); });
    });

    closeBtn.addEventListener('click', close);
    modal.addEventListener('click', function (e) { if (e.target === modal) { close(); } });
    /* tombol YouTube masih "#": jangan loncat ke atas halaman */
    qsa('a[href="#"]', modal).forEach(function (a) {
      a.addEventListener('click', function (e) { e.preventDefault(); });
    });

    doc.addEventListener('keydown', function (e) {
      if (!isOpen()) { return; }
      if (e.key === 'Escape') { e.preventDefault(); close(); return; }
      if (e.key === 'Tab') {
        var f = focusables();
        if (!f.length) { e.preventDefault(); return; }
        var first = f[0];
        var end = f[f.length - 1];
        if (e.shiftKey && (doc.activeElement === first || !modal.contains(doc.activeElement))) { e.preventDefault(); end.focus(); }
        else if (!e.shiftKey && (doc.activeElement === end || !modal.contains(doc.activeElement))) { e.preventDefault(); first.focus(); }
      }
    });
  }

  /* ==================================================================== BOOT */
  function boot() {
    qsa('form[data-estimator]').forEach(function (f) { safe(function () { initEstimator(f); }); });
    qsa('[data-gallery][data-load-more]').forEach(function (g) { safe(function () { initLoadMore(g); }); });
    var modal = qs('#video-modal');
    if (modal) { safe(function () { initVideoModal(modal); }); }
  }

  if (window.SBB && typeof window.SBB.init === 'function') { window.SBB.init(boot); }
  else if (doc.readyState === 'loading') { doc.addEventListener('DOMContentLoaded', boot); }
  else { boot(); }
}());
