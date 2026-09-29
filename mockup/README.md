# Mockup HTML: Sticker Sandblast Bali

Mockup statis (HTML/CSS/JS murni) yang menjadi acuan visual untuk dibangun ulang di Elementor. Sumber kebenaran desain: `../DESIGN-BRIEF.md`. Struktur URL: `../SITE-STRUCTURE.md`.

## Struktur

```
mockup/
  build.py                  perakit halaman (Python 3, stdlib saja)
  src/partials/             header.html (sprite ikon + header), footer.html (footer + tombol mengambang),
                            cta-final.html (bar CTA akhir)
  src/pages/*.html          isi tiap halaman (dengan komentar metadata)
  assets/css/styles.css     SATU stylesheet bersama: token, base, layout, 17 komponen, utilities
  assets/css/styleguide.css hanya untuk _components.html
  assets/js/app.js          semua perilaku bersama (namespace window.SBB)
  assets/img/               logo.svg (latar terang), logo-light.svg (latar gelap), favicon.svg
  assets/img/photos/        foto demo Pexels (.webp) + manifest.json (peran, file, ukuran, pexels_id)
  DEMO-DATA.md              nilai demo bersama (REAL vs DEMO) yang dipakai semua halaman
  tools/contrast.py         pemeriksa kontras WCAG dari token (termasuk overlay hero foto)
  tools/check_render.py     pemeriksa render (Playwright): overflow, konsol, tap target, keyboard
  tools/make_dist.py        paket folder deploy: build + salin ke dist/ + validasi noindex
  deploy/                   _headers dan robots.txt untuk Cloudflare Pages (disalin ke dist/)
  *.html                    HASIL build (jangan diedit tangan; edit src/ lalu build ulang)
  _components.html          style guide hidup: token, 17 komponen, hero foto, komponen foto
```

Nama file keluaran datar (tanpa subfolder) supaya bisa dibuka lewat `file://` dengan path aset relatif.

## Build

```
python3 mockup/build.py            # dari direktori mana pun
python3 mockup/build.py --strict   # peringatan lint dianggap gagal (exit 1)
```

`build.py` membaca setiap `src/pages/*.html`, mengganti `<!--@header-->` dan `<!--@footer-->` dengan partial, mengisi metadata, lalu menulis `mockup/{nama}.html`. Exit code 0 bila sukses. Lint yang dijalankan (sebagai peringatan): satu `<h1>`, heading tidak loncat level, ada `<main id="main">`, `id` ganda, panjang title (maks 60) dan description (maks 155), tautan internal hanya ke nama file yang diizinkan, aset relatif ada, dan setiap `<img>` punya `alt` (boleh kosong untuk dekoratif), `width`, dan `height`. Selain peringatan, build mencetak baris `INFO` (tidak memengaruhi `--strict`) berisi jumlah `<mark class="ph">` yang masih tersisa per halaman; target akhirnya 0.

## Komentar metadata halaman

Taruh di baris paling atas file `src/pages/*.html`. Satu direktif per komentar.

| Direktif | Wajib | Fungsi |
|---|---|---|
| `<!--@title Judul-->` | ya | `<title>`, maks 60 karakter, kata kunci di depan |
| `<!--@description ...-->` | ya | meta description, maks 155 karakter |
| `<!--@active layanan layanan-all-->` | tidak | menandai item menu aktif (daftar token dipisah spasi). Tautan mendapat `aria-current="page"`, tombol dropdown mendapat `data-current="true"` |
| `<!--@css pages-b.css-->` | tidak | tambah `<link rel="stylesheet" href="assets/css/pages-b.css">`. Boleh diulang |
| `<!--@js pages-b.js-->` | tidak | tambah `<script src="assets/js/pages-b.js" defer>` sesudah `app.js`. Boleh diulang |
| `<!--@robots ...-->` | tidak | menimpa meta robots. Bawaan: setiap halaman otomatis memakai `noindex, nofollow` |
| `<!--@bodyclass nama-->` | tidak | kelas pada `<body>` |
| `<!--@include cta-final-->` | tidak | sisipkan `src/partials/cta-final.html` (bisa dipakai untuk partial baru) |
| `<!--@header-->`, `<!--@footer-->` | ya | tempat header dan footer |

Teks title/description ditulis polos; `&` di-escape otomatis. Cangkang halaman (doctype, `<html lang="id">`, viewport, Google Fonts Plus Jakarta Sans 700/800 + DM Sans 400/500/600 dengan `display=swap`, stylesheet, script `defer`, skip link) ada di `build.py`.

### Token `@active` yang tersedia

`home` `tentang` `layanan` (dropdown) `layanan-all` `layanan-sticker-sandblast` `layanan-one-way` `layanan-riben` `layanan-kaca-film` `layanan-printing` `layanan-cutting` `layanan-wrapping` `layanan-huruf-timbul` `layanan-neon-box` `harga` (di dalam dropdown Layanan, bukan menu utama) `portofolio` (dropdown) `portofolio-foto` `portofolio-video` `artikel` `kontak`. Contoh halaman layanan gabungan: `<!--@active layanan layanan-all-->`.

Token `area`, `harga`, dan `portofolio-video` sudah dihapus dari header (menu utama tidak lagi punya item Area atau Harga; Galeri Video kini menuju `/portofolio/#video`). Hanya 8 token yang dipakai 7 halaman yang tersisa: `home` `tentang` `layanan` `layanan-all` `portofolio` `portofolio-foto` `artikel` `kontak`.

## Menambah halaman baru

1. Buat `src/pages/nama-halaman.html` (nama file = salah satu nama yang diizinkan: `index tentang-kami layanan portofolio artikel artikel-single kontak`, plus `_components` untuk style guide internal). **Situs final = 5 halaman** (Beranda, Tentang Kami, Layanan, Portofolio, Kontak) + Artikel (index + single). Tautan antar halaman memakai anchor (`layanan.html#harga`, `tentang-kami.html#area`, `portofolio.html#video`, `kontak.html#faq`), bukan halaman terpisah.

   **Restrukturisasi 5 halaman (sedang berjalan).** Situs final = 5 halaman: `index` (Beranda), `tentang-kami`, `layanan` (semua 9 layanan + harga + estimator), `portofolio`, `kontak`, plus `artikel`/`artikel-single` di luar hitungan. Halaman yang akan dihapus: `harga`, `testimoni`, `area`, `area-denpasar`, `layanan-sticker-sandblast`, `galeri-video`, `faq`. Isinya pindah: harga + estimator → `layanan.html#harga` dan `#estimasi`; detail 9 layanan → `layanan.html#{slug}`; testimoni → `tentang-kami.html#testimoni`; area → `tentang-kami.html#area`; galeri video → `portofolio.html#video`; FAQ → `kontak.html#faq`. Semua halaman ini masih ada di src/ sampai tahap sweep menghapus filenya.
2. Salin kerangka dari halaman yang mirip. Urutan wajib: direktif metadata, `<!--@header-->`, `<main id="main">`, section, `<!--@include cta-final-->`, `</main>`, `<!--@footer-->`.
3. Satu `<h1>`, breadcrumb (kecuali Home), heading berurutan.
4. CSS/JS khusus halaman: `assets/css/nama.css` dan `assets/js/nama.js`, panggil dengan `<!--@css nama.css-->` dan `<!--@js nama.js-->`. **Jangan** menambah ke `styles.css`.
5. Jalankan `python3 mockup/build.py` dan perbaiki peringatan.

Semua tautan internal harus menuju nama file di atas (yang belum ada tidak masalah). Tautan yang belum punya file: `#` dengan `data-real-url="/jalur/asli/"`. Tautan ke Anchor memakai `nama-halaman.html#anchor` dan `data-real-url` dengan bentuk yang sama (mis. `/layanan/#sticker-riben`). Delapan layanan selain sandblast sudah menuju `layanan.html#{slug}` (satu halaman gabungan).

## Konvensi CSS

BEM sederhana: `.blok`, `.blok__elemen`, `.blok--modifier`. Mobile-first. Breakpoint: mobile <=767px, tablet 768-1024px, desktop >=1025px. Token ada di `:root` (nilai persis dari brief; token turunan ditandai "derived"). Skala tipografi memakai `clamp()`: nilai mobile sampai nilai desktop.

Layout: `.container` `.section` (+ `--alt` abu muda, `--frost`, `--dark`, `--pane` band merah gradien) `.section__head` `.section__foot` `.grid` (+ `--2 --3 --4`) `.split` (+ `--wide-left --reverse --top`) `.prose` `.stack` `.cluster` `.btn-row`.
Utilitas: `.sr-only` `.eyebrow` `.lead` `.small` `.text-muted` `.mt-3..mt-7` `.reveal` `.frost` `.icon` (`--sm --md --lg`).
Ikon: sprite `<symbol id="i-nama">` di `header.html`, dipakai `<svg class="icon" aria-hidden="true"><use href="#i-nama"/></svg>`. Gaya garis 1.75, ujung bulat, viewBox 24. Tanpa emoji.

## Katalog komponen (17 + hero foto + foto)

Tiap komponen ada di `_components.html` (`#c01` sampai `#c19`, dan `#extra` untuk foto) dan dipakai di halaman nyata. Potongan HTML di bawah minimal; salin dari halaman untuk versi lengkap.

1. **Header** `.site-header` `.site-header__inner` `.brand` `.nav` `.nav__list` `.nav__item[data-sub]` `.nav__link` `.nav__toggle` `.nav__sub` `.menu-btn` `.site-header__cta`. Sumber: `src/partials/header.html`. Menu: Beranda | Tentang Kami | Layanan ▾ | Portofolio ▾ | Artikel | Kontak. Dropdown Layanan = 9 item menuju `layanan.html#{slug}` + "Lihat semua layanan" (`layanan.html`) + "Harga & estimasi" (`layanan.html#harga`); dropdown Portofolio = Galeri Foto (`portofolio.html#foto`) dan Galeri Video (`portofolio.html#video`). Dropdown dan menu mobile dikendalikan `app.js`.
2. **Tombol** `.btn` + `--primary` `--wa` `--secondary` `--secondary-light` `--sm` `--block`; `.link-arrow`.
   `<a class="btn btn--wa" href="https://wa.me/6282226920230"><svg class="icon icon--md" aria-hidden="true"><use href="#i-whatsapp"/></svg>Chat WhatsApp</a>`
3. **Kartu layanan** `.card-service` `__media` `__body` `__title` `__text` `__link`.
   `<article class="card-service"><div class="card-service__media"><img src="assets/img/photos/svc-sandblast.webp" alt=".." width="900" height="600" loading="lazy" decoding="async"></div><div class="card-service__body"><h3 class="card-service__title">..</h3><p class="card-service__text">..</p><a class="card-service__link" href="..">Lihat layanan</a></div></article>`
4. **Kartu nilai** `.card-value` `__icon` `__title` `__text`. `<article class="card-value"><span class="card-value__icon"><svg class="icon icon--lg">..</svg></span><h3 class="card-value__title">..</h3><p class="card-value__text">..</p></article>`
5. **Langkah proses** `ol.steps` > `li.step` > `.step__num` `.step__title` `.step__text` `.step__time`.
6. **Kartu harga** `.card-price` `__name` `__price` (`__from`, `__amount`) `__list` `__factors` `__cta`; varian `--frost` (di atas `.section--pane`) dan `--featured`.
7. **Before/after** `.ba-slider[data-ba]` > `__layer--after` + `__layer--before` (masing-masing berisi `<img>` dengan `alt`, `width`, `height`), `__tag--before/--after`, `__handle[role="slider"][tabindex=0][aria-valuenow]` > `__knob`. Varian `--4x3`. Kotak pembungkus lebar: `.ba-wrap`. **Simulasi dari satu foto:** tambahkan `.ba--simulate` (pada `.ba-slider` atau `.ba-wrap`), pakai foto yang sama di kedua lapisan; lapisan `__layer--after` otomatis diberi `filter: blur(5px) brightness(1.08) saturate(.85)` dan `scale(1.04)` (menutup tepi yang memudar). Label "Sebelum"/"Sesudah" tetap; beri keterangan lewat `p.ba__note` di bawah slider (mis. "Ilustrasi efek sandblast").
8. **Galeri** `[data-gallery]` > `.gallery__filters` (`button.chip[data-filter][aria-pressed]`, `data-filter="all"` untuk semua) + `p.gallery__status[aria-live]` + `.gallery__grid` (masonry kolom) > `figure.gallery__item[data-category="a b"]` > `button.gallery__open` > `.gallery__media` (berisi `<img>`) + `.gallery__zoom`, dan `figcaption.gallery__cap`. Lightbox dibuat JS: klik `.gallery__open`; JS memakai `data-full` (bila ada) atau `src` pada `<img>`. Keterangan lightbox diambil dari `.gallery__cap`, lalu `figcaption` mana pun di item, lalu `data-caption` pada `.gallery__item` atau `<img>`. Format caption: "jenis · kawasan".
9. **Testimoni** `figure.card-quote` > `blockquote.card-quote__text` + `figcaption.card-quote__meta` (`__source` `__name`). Tanpa bintang buatan. Ringkasan rating: `.review-summary`.
10. **Accordion FAQ** `.accordion` > `.accordion__item[.is-open]` > `h3.accordion__heading > button.accordion__trigger[aria-expanded][aria-controls]` (+ `span.accordion__icon`) dan `.accordion__panel[role=region]` > `.accordion__panel-inner` > `.accordion__body`. Selaraskan `aria-expanded` dengan `.is-open` di markup awal. Tanpa JS semua panel terbuka.
11. **Kartu artikel** `.card-post` `__media` `__body` `__cat` `__title` (tautan di dalamnya diperluas ke seluruh kartu) `__excerpt` `__meta`.
12. **Bar CTA akhir** `.cta-section` > `.container` > `.cta-bar` (`__title` `__text`) + `.btn-row`. Sisipkan dengan `<!--@include cta-final-->`.
13. **Formulir penawaran** `form.form-quote[data-mock]` > `.form-quote__grid` > `.field` (`__label` `__input` `__select` `__textarea` `__hint`, `.field--full`), `.form-quote__privacy`, `.form-quote__status[hidden]`. `data-mock="pesan"` menahan pengiriman dan menampilkan pesan; hapus atribut ini saat formulir disambungkan.
14. **Footer** `.site-footer` `.footer__grid` (4 kolom) `__brand` `__title` `__list` `__contact` `__social` `__bottom`. Sumber: `src/partials/footer.html`.
15. **Tombol WhatsApp mengambang** `.wa-float` (>=768px) dan `.mobile-bar` (<=767px: WhatsApp + Telepon). Ada di `footer.html`.
16. **Breadcrumb** `nav.breadcrumb[aria-label]` > `ol.breadcrumb__list` > `li.breadcrumb__item`; item terakhir `aria-current="page"`.
17. **Badge kepercayaan** `ul.badge-row` > `li.badge-trust` (ikon + teks). Klaim mengikuti `DEMO-DATA.md`. Di atas hero foto pakai `ul.hero-photo__badges` (lihat komponen 18).

18. **Hero foto (besar, full-bleed)** `section.hero-photo` + `--home` (tinggi `clamp(560px, 88vh, 860px)`) atau `--page` (halaman dalam, `clamp(440px, 62vh, 620px)`; `.hero-photo--tall` = alias, sama dengan `--page`; di <=767px `clamp(400px, 56vh, 520px)`). Markup wajib:
    ```html
    <section class="hero-photo hero-photo--home|hero-photo--page" style="--focus:50% 50%">
      <img class="hero-photo__img" src="assets/img/photos/hero-xxx.webp" alt=".." width="1920" height="1280" fetchpriority="high" decoding="async">
      <div class="hero-photo__overlay" aria-hidden="true"></div>
      <div class="container hero-photo__inner">
        <nav class="breadcrumb breadcrumb--light">..</nav>              <!-- hanya halaman dalam -->
        <p class="eyebrow eyebrow--light">..</p><h1>..</h1><p class="lead">..</p>
        <div class="hero-photo__actions">.btn--wa / .btn--primary + .btn--outline-light</div>
        <ul class="hero-photo__badges"><li><svg class="icon">..</svg>..</li></ul>   <!-- opsional -->
      </div>
      <aside class="hero-photo__card frost">..</aside>                  <!-- opsional -->
    </section>
    ```
    Foto memenuhi section (`object-fit: cover`, `object-position: var(--focus, 50% 50%)`); hero di atas lipatan memakai `fetchpriority="high"` dan tanpa `loading="lazy"`. Overlay Ink 900: gradasi kiri-ke-kanan di >=1025px, seragam di 768-1024px, dan di <=767px teks menempel di bawah dengan bagian atas foto terang (`--hero-a-top` .12, tanpa teks; gradasi dipasang di `.hero-photo__inner` sehingga teks selalu di alfa >= `--hero-a-min`, foto memudar ke Ink 900 di bawah teks dan kartu frosted), dengan token `--hero-a-start` (.88), `--hero-a-min` (.72), `--hero-a-end` (.30). Teks hanya berada di area beralfa >= `--hero-a-min` (blok teks dibatasi `min(640px, 62%)`), sehingga tetap AA walau piksel foto putih murni. `.eyebrow--light` adalah pil Ink 900 translusen (`--hero-pill-a`) berteks putih; `.hero-photo__badges li` adalah chip frosted gelap (`--hero-chip-a`) berteks putih; `.btn--outline-light` untuk tombol sekunder; `.breadcrumb--light` berteks putih. `.hero-photo__card` berada di kanan bawah pada >=1025px dan menumpuk di bawah teks pada layar lebih kecil. Judul boleh memakai `.hero-photo__title` bila elemennya bukan `h1` (mis. di style guide).
19. **Foto demo** `figure.photo` + rasio `--4x3` `--16x9` `--1x1` `--3x4` `--3x2` `--banner` (3:2 di mobile, 21:9 di >=768px) atau `--free` (rasio asli dari `width`/`height`) > `img[src][alt][width][height][loading="lazy"][decoding="async"]` + `figcaption.photo__cap` opsional (panel frosted kiri bawah). `object-fit: cover`, sudut 14px, tanpa layout shift. Di dalam `.card-service__media`, `.card-post__media`, `.gallery__media`, dan lapisan `.ba-slider__layer`, cukup taruh `<img>` langsung; CSS mengatur rasio dan zoom hover.

Pendukung: `.crop-marks`, `.page-hero`, `.hero` (`__media` `.hero-card`), `.promo-bar`, `.compare-wrap > table.compare` (baris menjadi kartu di mobile lewat `data-label`), `.motif` (swatch pola kaca), `.facts`, `.callout`, `.check-list`, `.factor-list`, `.chip-list`, `.mini-list`, `.area-map`.

## API JavaScript (`assets/js/app.js`)

Satu global: `window.SBB`. Semua modul jalan otomatis saat DOM siap. Tanpa library.

```js
SBB.init(function (sbb) { /* dijalankan setelah semua modul siap; langsung jalan bila sudah siap */ });
SBB.refresh(scopeEl);         // inisialisasi ulang slider/accordion/gallery/reveal di konten yang baru disisipkan
SBB.on('lightbox:open', fn);  // juga: accordion:toggle, gallery:filter, lightbox:close, slider:change
SBB.off(name, fn); SBB.emit(name, detail);
SBB.modules.gallery.filter(galleryEl, 'sandblast');   // akses modul: header, accordion, slider, gallery, reveal, forms
```

Skrip halaman: buat `assets/js/nama.js`, panggil dengan `<!--@js nama.js-->`, dan bungkus dalam `SBB.init(...)` (skrip dimuat `defer` sesudah `app.js`, jadi `window.SBB` sudah ada).

Perilaku: header sticky dengan garis saat scroll (`.is-scrolled`); menu mobile dengan `aria-expanded`/`aria-controls`, Esc menutup, focus trap ringan; dropdown (klik, hover mouse di desktop, Enter/Spasi, panah bawah/atas, Home/End, Esc mengembalikan fokus); accordion satu terbuka; slider before/after (pointer, sentuh, keyboard); filter chip + lightbox (Esc, focus trap, panah, geser); scroll reveal `.reveal` (fade + 12px, sekali; disembunyikan hanya bila `html.js`; `data-stagger` pada induk memberi jeda antar anak). `prefers-reduced-motion` mematikan animasi.

## Foto dan kebijakan konten demo

Mockup ini adalah demo lengkap: tidak ada penanda placeholder di halaman. Semua teks dan foto tampil sebagai konten biasa.

- **Foto:** stok Pexels di `assets/img/photos/*.webp` (lisensi Pexels: gratis untuk pemakaian komersial tanpa kewajiban atribusi). `assets/img/photos/manifest.json` memetakan tiap peran foto ke `file`, `width`, `height`, `pexels_id`, `source`, dan `kind` (`hero` untuk 1920 px, `card` untuk 900 px). Peran: `hero-*` (satu per halaman), `svc-*` (sembilan layanan), `g-01..g-32` (galeri), `area-*`, `workshop-*`, dan beberapa foto ruang. Pakai `width`/`height` dari manifest, `alt` yang menggambarkan isi foto (jangan mengklaim itu hasil kerja bisnis ini), dan `loading="lazy"` kecuali hero di atas lipatan. Foto itu bukan hasil kerja Sticker Sandblast Bali.
- **Data:** `DEMO-DATA.md` adalah sumber nilai demo bersama (identitas, kontak, angka, harga, testimoni, proyek galeri, artikel). Tiap nilai ditandai **REAL** (dikonfirmasi user atau dari Google Business Profile) atau **DEMO** (contoh; harus diverifikasi atau diganti sebelum situs tayang). Di halaman keduanya tampil polos. Data REAL: brand **Sticker Sandblast Bali**, domain `stikersandblastbali.com`, WhatsApp dan telepon **0822-2692-0230** (`https://wa.me/6282226920230`, `tel:+6282226920230`), alamat Jl. Cokroaminoto Gg. Jempiring No. 15, Ubung, Kec. Denpasar Utara, Kota Denpasar, Bali 80111, jam Senin-Minggu 09.00-17.00, rating Google 4,9 dari 57 ulasan, tiga kutipan ulasan, dan harga sandblast Rp 135.000, one way vision Rp 195.000, printing Rp 175.000 per m2.
- **Sisa `mark.ph`:** kelas lama tidak lagi bergaya (aturan netral membuatnya tampil sebagai teks biasa). Halaman yang belum dimigrasi masih memilikinya; `build.py` melaporkan jumlahnya sebagai `INFO`. Migrasi berarti mengganti isinya dengan teks demo dari `DEMO-DATA.md`. CSS `.ph-img` dipertahankan sementara sampai semua halaman memakai `<img>`.

## Hosting (Cloudflare Pages)

Mockup ini hanya untuk peninjauan, jadi tidak boleh masuk indeks mesin pencari. Buat folder deploy bersih lalu unggah:

```
python3 mockup/tools/make_dist.py
wrangler pages deploy mockup/dist --project-name stikersandblastbali
```

`make_dist.py` menjalankan `build.py --strict`, menghapus dan membuat ulang `mockup/dist/`, lalu menyalin hanya 15 halaman `*.html`, `assets/`, `deploy/_headers`, dan `deploy/robots.txt`. `src/`, `tools/`, `_screens/`, `demo-content/`, `build.py`, `README.md`, dan `DEMO-DATA.md` tidak ikut. Skrip mencetak ringkasan (jumlah file, ukuran) dan exit 1 bila validasi gagal: satu meta robots per halaman, `_headers` dan `robots.txt` ada, tidak ada file internal, tidak ada file > 25 MiB, jumlah file < 20.000. Folder `dist/` adalah hasil generate; jangan diedit tangan.

Tiga lapis noindex:

1. **Meta tag**: `build.py` menyisipkan `<meta name="robots" content="noindex, nofollow">` di setiap halaman (direktif `@robots` pada halaman boleh menimpa).
2. **HTTP header**: `deploy/_headers` mengirim `X-Robots-Tag: noindex, nofollow, noarchive, nosnippet` untuk semua path, plus `Referrer-Policy` dan `X-Content-Type-Options`; `/assets/*` diberi `Cache-Control: public, max-age=3600` (singkat karena mockup sering berubah).
3. **robots.txt**: `deploy/robots.txt` berisi `User-agent: *` dan `Disallow: /`.

## Kontras (WCAG AA)

`python3 mockup/tools/contrast.py` membaca token dari `styles.css`, menghitung rasio semua pasangan teks/latar yang dipakai (termasuk panel frosted pada latar terburuk), dan exit 0 hanya bila semua lolos (4,5:1 teks normal, 3:1 teks besar dan komponen UI). Untuk hero foto, kasus terburuk dihitung dari nilai CSS `--hero-*` (bukan angka yang ditulis ulang): teks putih (termasuk eyebrow dalam pil), dan chip badge di atas piksel foto putih yang ditumpuk overlay hitam (`--ink-900`) beralfa minimum; kartu frosted dihitung di atas piksel hitam. Skrip juga memeriksa invarian `--hero-a-min >= 0.68`.

## Penyimpangan kecil dari brief (disengaja)

- Ring fokus di latar gelap (footer, CTA, section gelap, lightbox) memakai `--red-300`, bukan `--red-600`, karena red-600 di atas Ink 900 hanya 3,3:1. Ring fokus di atas pane merah, promo-bar, dan hero foto memakai putih (red-300 di overlay hero kasus terburuk hanya 2,1:1).
- Panel frosted diberi garis tipis `0 0 0 1px rgba(43,43,43,.07)` agar tepinya terbaca di latar terang.
- Menu inline mulai 1025px; di 1025-1199px label tombol header dipendekkan menjadi "Chat".
- Token turunan: `--wa-green-hover` (#095F2E), `--error` (#C2410C), dan `--hero-a-start`/`--hero-a-min`/`--hero-a-end`/`--hero-pill-a`/`--hero-chip-a` (alfa overlay hero foto).
- Ditambahkan partial `cta-final.html`, `styleguide.css`, dan `logo-light.svg` di luar daftar berkas awal.
- Border input formulir memakai `--text-muted` (kontras komponen UI 3:1).
- Tema hitam-merah: di dalam `.section--pane` (band merah) SEMUA teks putih — `--red-300` di atas `--red-600` hanya 1,6:1. `.eyebrow--light` di hero foto berteks putih karena red-300 di pil overlay hanya 4,43:1 (< 4,5). Ikon `.post-meta` di hero foto memakai putih (red-300 di overlay hitam hanya 2,09:1). Pasangan red-300 di atas ink-700 hanya 3,89:1 sehingga diperiksa sebagai komponen UI (3:1), bukan teks — tidak ada teks red-300 di atas ink-700 di UI.
