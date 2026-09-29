# ELEMENTOR-SPEC: Sticker Sandblast Bali

Spesifikasi build Elementor untuk situs `stikersandblastbali.com`, diturunkan dari mockup HTML final di `mockup/` (14 halaman, satu design system, hero foto besar di setiap halaman, foto Pexels di semua kartu dan galeri, copy lengkap). Dokumen ini master; detail per halaman ada di `elementor-spec/`. Baca master dulu (terutama bagian 2.9 Resep), lalu file halaman yang sedang dibangun.

Sumber kebenaran: nilai token, teks, dan perilaku diambil dari `mockup/assets/css/styles.css`, `pages-b.css`, `pages-c.css`, `assets/js/app.js`, `pages-b.js`, `pages-c.js`, dan `mockup/src/`. Bila ada perbedaan, mockup menang untuk tampilan dan copy; `SITE-STRUCTURE.md` menang untuk URL. Nilai konten (identitas, kontak, angka, harga, testimoni, caption galeri, artikel) ada di `DEMO-CONTENT.md` dan `mockup/DEMO-DATA.md`; foto di `mockup/assets/img/photos/` dengan peta peran di `manifest.json` (bagian 2.11). Status data: dibaca 2026-09-21.

| File | Halaman | Section di mockup |
|---|---|---|
| `elementor-spec/01-home.md` | Beranda `/` | 13 (+ promo bar) |
| `elementor-spec/02-tentang-kami.md` | `/tentang-kami/` (`#cerita`, `#testimoni`, `#area`) | 7 |
| `elementor-spec/03-layanan-index.md` | `/layanan/` (9 blok + harga + estimator) | 16 |
| `elementor-spec/06-portofolio.md` | `/portofolio/` (`#foto`, `#video`) | 3 |
| `elementor-spec/12-artikel-index.md` | `/artikel/` | 5 |
| `elementor-spec/13-artikel-single.md` | Single Artikel | 6 |
| `elementor-spec/14-kontak.md` | `/kontak/` | 6 |

Struktur final = **5 halaman** (Beranda, Tentang Kami, Layanan, Portofolio, Kontak) + Artikel (index + single, di luar hitungan). Spec lama `04-layanan-template.md`, `04b-layanan-fields.md`, `05-harga.md`, `07-galeri-video.md`, `08-testimoni.md`, `09-area-index.md`, `10-area-template.md`, `11-faq.md` tidak lagi dipakai: isinya digabung ke spec Layanan (bagian harga/estimator), `/tentang-kami/#area`, `/tentang-kami/#testimoni`, `/portofolio/#video`, dan `/kontak/#faq`. Delapan halaman tersebut dihapus dari struktur; belum semua file spesifikasinya dibersihkan (lihat catatan di akhir dokumen).

Tidak ada CPT `layanan` dan tidak ada CPT `area` lagi. Sembilan layanan adalah sembilan blok beranchor di satu halaman `/layanan/` (bagian 4.1 dan 4.2 sudah disesuaikan); daftar harga, teka, dan kalkulator juga berada di halaman yang sama.

---

## 1. Overview, asumsi, plugin, urutan build

### 1.1 Asumsi

- WordPress 6.x, tema **Hello Elementor** (dengan child theme kosong untuk PHP helper), **Elementor** (terbaru) + **Elementor Pro** (Theme Builder, Loop Grid, Form, Nested Elements, Popup, Custom Code, Table of Contents, Author Box, Motion Effects). Bila Pro tidak tersedia, lihat tabel "Free-only fallback" di bagian 8.4.
- Breakpoint Elementor hanya dua, sama dengan mockup: **Mobile ≤ 767 px**, **Tablet ≤ 1024 px**, Desktop ≥ 1025 px. Matikan breakpoint tambahan (Mobile Extra, Tablet Extra, Laptop, Widescreen) di Site Settings > Layout > Breakpoints.
- Notasi nilai responsif: `a / b / c` = Desktop / Tablet / Mobile. Notasi jalur UI: `Style > Typography`.
- Semua teks, angka, harga, dan caption ditulis persis seperti di mockup; sumber tunggalnya `DEMO-CONTENT.md` (ringkasan bersama di `mockup/DEMO-DATA.md`). Setiap halaman dan template memakai nilai yang sama, sehingga satu angka tidak pernah berbeda antar halaman.
- Identitas dan kontak: nama "Sticker Sandblast Bali", WhatsApp/telepon 0822-2692-0230 (`https://wa.me/6282226920230`, `tel:+6282226920230`), email info@stikersandblastbali.com, alamat Jl. Cokroaminoto Gg. Jempiring No. 15, Ubung, Kec. Denpasar Utara, Kota Denpasar, Bali 80111, jam Senin-Minggu 09.00-17.00, rating Google 4,9 dari 57 ulasan (tautan GBP `https://share.google/dNneYg3jdOXi641aj`), sosial Instagram/TikTok `@stikersandblastbali`, Facebook dan YouTube "Sticker Sandblast Bali".
- Harga "mulai dari" per m²: Sandblast Rp 135.000, One Way Vision Rp 195.000, Printing Rp 175.000, Riben Rp 95.000, Kaca Film Rp 165.000, Cutting Rp 60.000, Wrapping & Branding Mobil Rp 250.000, Neon Box & Papan Nama Rp 950.000; Huruf Timbul 3D Rp 35.000 per huruf (bukan per m²).
- Bila kontrol Elementor yang disebut tidak ditemukan di versi Anda, terapkan hasil fungsionalnya (deskripsi ada di kolom yang sama) dan catat penyimpangannya; nama kontrol bisa bergeser antar versi.

### 1.2 Plugin minimal

| Plugin | Fungsi | Justifikasi | Dampak Core Web Vitals |
|---|---|---|---|
| Hello Elementor + child theme | Tema kosong | Tanpa CSS/JS tema; child theme menampung PHP helper (bagian 6) | Terbaik: hampir nol beban |
| Elementor + Elementor Pro | Builder, Theme Builder, Loop, Form | Semua template dinamis dan form ditangani native | Sedang: nyalakan Optimized Markup/Improved Asset Loading di Elementor > Settings > Performance |
| ACF atau SCF (Secure Custom Fields), versi gratis | Field CPT dan taxonomy | Field datar, tanpa repeater (Pro tidak mengiterasi repeater ACF native) | Kecil: hanya di admin dan query |
| Satu plugin SEO (Rank Math, Yoast, atau SEOPress) | Title/meta, canonical, sitemap XML, breadcrumb schema | Satu sumber tunggal; jangan pasang dua | Kecil |
| Satu plugin cache + optimasi gambar (mis. LiteSpeed Cache bila server LiteSpeed) | Cache halaman, WebP, lazy-load | Target LCP ≤ 2,5 dtk | Menguntungkan |
| SMTP (WP Mail SMTP atau FluentSMTP) | Pengiriman notifikasi form | Form Elementor memakai `wp_mail`; tanpa SMTP email sering masuk spam. Kredensial SMTP dibuat kuat (≥ 16 karakter) | Tidak ada |
| Code Snippets (opsional, pengganti child theme) | Menaruh PHP helper tanpa file | Hanya bila child theme tidak dipakai | Tidak ada |

Jangan tambahkan: plugin slider, add-on paket Elementor pihak ketiga, plugin ikon-font, plugin popup lain. Ikon memakai SVG inline (sprite mockup) atau Elementor Icons/SVG upload. Font Awesome dinonaktifkan bila tidak dipakai.

### 1.3 Urutan build

1. Instal tema dan plugin (1.2). Settings > Permalinks: struktur kustom `/artikel/%postname%/` dan Category base `kategori` (untuk artikel; halaman dan CPT memakai slug sendiri); simpan ulang permalink setiap kali CPT/taxonomy baru dibuat. Settings > Reading: Homepage = "Home", Posts page = "Artikel", Posts per page 7 (sama dengan Loop Grid "Baca juga").
2. Site Settings (bagian 2): Colors, Fonts, Buttons, Form fields, Images, Layout, Lightbox, Custom CSS (2.8, lalu hero foto 2.10 dan foto konten 2.11); unggah 71 foto ke Media Library dengan nama berkas asli dan Alternative Text (2.11).
3. Content model (bagian 4): CPT, taxonomy, field group, isi 9 layanan + 7 area + 32 proyek + 6 testimoni dengan nilai dari `DEMO-CONTENT.md` (tabel nilai awal di 4.3).
4. Kode: helper PHP (bagian 6) termasuk prioritas gambar hero (K17), JS kecil (bagian 6), Query ID.
5. Saved/Global templates (bagian 5): `TPL-*`, `LI-*`.
6. Theme Builder (bagian 3): Header, Footer, Single, Archive, 404, Popup, bar bawah mobile.
7. Halaman statis berurutan: Home, Layanan index, Harga, Tentang, Portofolio, Galeri video, Testimoni, Area index, FAQ, Kontak; lalu isi template dinamis.
8. Menu WP, SEO, schema (bagian 7), lalu QA (bagian 8).

---

## 2. Site Settings (Kit)

### 2.1 Global Colors

Buat 14 System/Custom Colors dengan nama persis di bawah; semua widget memakai Global Color, bukan hex lepas.

| Nama Global | Hex | Pemakaian | Kontras terverifikasi |
|---|---|---|---|
| Ink 900 | `#111111` | Judul, latar section gelap/CTA/footer, tombol sekunder | Teks Border di atasnya 12,08:1 |
| Ink 700 | `#2B2B2B` | Hover primary, latar gelap sekunder | Putih di atasnya 11,88:1 |
| Red 600 | `#CA1317` | Tombol primary, link, ikon, focus ring | Putih 5,82:1; di Gray 50 5,27:1 |
| Red 500 | `#EC2327` | Dekoratif (gradien, bayangan kaca) | Bukan untuk teks |
| Red 300 | `#FF3333` | Link/focus di latar gelap | Di Ink 900 8,48:1 |
| Red 800 | `#A30F12` | Ujung gradien band merah `section--pane` | Bukan untuk teks |
| Gray 50 | `#F8F8F8` | Latar section alternatif | Ink 900 di atasnya 14,07:1 |
| Frost | `#F4F4F4` | Latar section frost, kartu | Text Muted 5,69:1 |
| Border | `#DDDDDD` | Garis 1px, pemisah, teks di latar gelap | |
| Text | `#333333` | Teks isi | Di putih 12,48:1 |
| Text Muted | `#666666` | Teks pendukung, teks contoh di dalam field | Di putih 6,07:1 |
| WA Green | `#0B7A3B` | Tombol WhatsApp | Putih di atasnya 5,44:1 |
| WA Green Hover | `#095F2E` | Hover tombol WhatsApp | Putih 7,81:1 |
| Error | `#C2410C` | Pesan galat form | Di putih 6,57:1 |
| White | `#FFFFFF` | Latar dasar, teks di latar gelap | |

Overlay hero foto memakai Ink 900 dengan alfa (bukan warna Global baru): nilainya ada di 2.10.

### 2.2 Global Fonts

Keluarga: **Plus Jakarta Sans** (700, 800) untuk judul, **DM Sans** (400, 500, 600) untuk isi. `font-display: swap`. Muat lokal (hosting sendiri): aktifkan opsi Google Fonts lokal di Elementor > Settings > Performance bila tersedia, atau unggah WOFF2 lewat Custom Fonts. Hanya dua keluarga dan lima bobot ini.

Mockup memakai `clamp()` fluid; Elementor memakai angka tetap per breakpoint. Desktop dan mobile = ujung clamp; tablet = titik tengah.

| Nama Global | Keluarga / bobot | Desktop / Tablet / Mobile (px) | Line-height | Catatan |
|---|---|---|---|---|
| H1 | Plus Jakarta Sans 800 | 56 / 46 / 36 | 1,1 | Letter-spacing -0,015em; satu H1 per halaman |
| H2 | Plus Jakarta Sans 800 | 40 / 34 / 28 | 1,2 | -0,01em |
| H3 | Plus Jakarta Sans 700 | 24 / 22 / 20 | 1,3 | |
| H4 / Card Title | Plus Jakarta Sans 700 | 18 / 18 / 18 | 1,35 | |
| Body | DM Sans 400 | 17 / 16,5 / 16 | 1,65 | Lebar baris maks 68 karakter (`max-width: 68ch`) |
| Lead | DM Sans 400 | 20 / 19 / 17 | 1,6 | Maks 60ch |
| Small | DM Sans 400 | 14 / 14 / 14 | 1,5 | |
| Eyebrow | DM Sans 600 | 14 / 14 / 14 | 1,2 | Uppercase, letter-spacing 0,06em, Red 600; diawali garis 22x2 px (CSS `.sbb-eyebrow`, bagian 2.8) |
| Button | DM Sans 600 | 16 / 16 / 16 | 1,2 | Tombol kecil 15 px |

Site Settings > Typography: Default Generic Fonts sans-serif. Semua Heading widget: pilih Global Font H1/H2/H3; Text Editor: Body.

### 2.3 Buttons (Theme Style > Buttons)

Default Button = **Primary**. Varian lain dibuat sebagai widget dengan warna Global atau Saved Template `BTN-*` (bagian 5).

| Varian | Latar | Teks | Border | Hover | Kode |
|---|---|---|---|---|---|
| Primary | Red 600 | White | 2px transparan | latar Ink 900 | `BTN-PRI` |
| WhatsApp | WA Green | White | 2px transparan | latar WA Green Hover | `BTN-WA` |
| Secondary | transparan | Ink 900 | 2px Ink 900 | latar Ink 900, teks White | `BTN-SEC` |
| Secondary on dark (outline light; kelas `sbb-btn--outline-light`, CSS 2.10) | transparan | White | 2px White | latar White, teks Ink 900 | `BTN-SEC-L` |
| Text link + panah | tanpa latar | Red 600 600 | tanpa | teks Ink 900, panah geser 3px | `LINK-ARROW` |

Ukuran bersama: tinggi min 48 (kecil 44), padding 0 / 24 (kecil 0 / 16), radius 10, DM Sans 600 16 px (kecil 15), gap ikon 8 dengan ikon 20 px. State: **hover** 200 ms ease `cubic-bezier(.2,.7,.2,1)`; **active** geser 1 px ke bawah; **focus-visible** ring 2px Red 600 offset 2 (Red 300 di latar gelap; White di pane/promo/hero; aturan di CSS bagian 2.8). Tinggi target sentuh min 44 px. Tautan WhatsApp `target="_blank"` `rel="noopener"`.

Ikon WhatsApp: SVG dari sprite mockup (`i-whatsapp`), 20 px, stroke 1,75; upload sebagai SVG atau HTML widget inline. Bar bawah mobile memakai tombol WA + Telepon (bagian 3.7).

### 2.4 Form fields (Theme Style > Form Fields)

| Properti | Nilai |
|---|---|
| Label | DM Sans 600 15 px, Ink 900; penanda opsional "(opsional)" Text Muted 500 |
| Input, select, textarea | Latar White, teks Text, tinggi min 48, padding 10 / 14, border 1px Text Muted, radius 10 |
| Hover | Border Ink 900 |
| Focus | Border Red 600 + outline 2px Red 600 offset 2 (outline via CSS bagian 2.8) |
| Teks contoh di dalam field | Text Muted, opasitas 1 |
| Textarea | Tinggi min 112, resize vertikal |
| Select | Panah kustom Ink 900, padding kanan 40 |
| Hint | 14 px Text Muted di bawah field |
| Galat | Teks dan ikon Error (`#C2410C`), `aria-invalid="true"`, pesan terhubung `aria-describedby`; jangan mengandalkan warna saja (ikon + teks) |
| Input file | Tombol pilih berkas: padding 8, border Border, radius 10 |
| Gap | Row 16, column 16; grid 2 kolom di ≥ 768, 1 kolom di mobile |

Form widget: jangan menjadikan teks contoh di dalam field sebagai pengganti label; setiap field wajib punya label terlihat. Teks kirim "Kirim permintaan"; status sukses `role=status`.

### 2.5 Images

| Item | Nilai |
|---|---|
| Format | WebP (AVIF opsional); file dari `mockup/assets/img/photos/` diunggah apa adanya: hero 1920 px lebar, kartu dan galeri 900 px lebar (tabel di 2.11) |
| Atribut | Selalu `width`/`height` (Elementor mengisi otomatis), `alt` yang menggambarkan isi foto (aturan di 2.11); dekoratif `alt=""` |
| Loading | Lazy di bawah fold; **satu** gambar hero per halaman dimuat cepat (LCP): tanpa lazy dan dengan `fetchpriority="high"` (snippet K17 di 2.10) |
| Theme Style > Images | Tanpa radius dan bayangan global; radius 14 diterapkan pada container kartu dengan Overflow Hidden |
| Rasio | Elementor Image tidak punya kontrol aspect-ratio native: pakai kelas `sbb-ar-16x9`, `sbb-ar-4x3`, `sbb-ar-1x1`, `sbb-ar-3x2`, `sbb-ar-banner` (CSS 2.8) pada widget Image, dengan Object Fit Cover. Galeri proyek memakai rasio asli foto (Loop Grid Masonry), tanpa crop |
| Foto hero | Satu gambar per halaman, bukan slider (SITE-STRUCTURE bagian 9); dibangun sebagai hero foto besar (2.10) |
| Foto konten | Foto Pexels di semua kartu, galeri, strip, dan ilustrasi; peta peran ke file, halaman, dan ukuran ada di 2.11 |

### 2.6 Layout

| Item | Nilai |
|---|---|
| Content Width (Boxed) | **1200 px** |
| Container padding (gutter) | 24 / 24 / 16 (kiri-kanan) |
| Section padding vertikal | 96 / 76 / 56 (variabel `--section-y`) |
| Widgets Space | 16 |
| Default Page Layout | Elementor Full Width; Hide Title On |
| Breakpoints | Mobile 767, Tablet 1024; lainnya nonaktif |
| Tinggi header (untuk offset scroll) | 76 (≥ 768) / 68 (mobile); `scroll-padding-top` = tinggi + 16 |
| Section `SEC` | **Satu** container Boxed 1200 dengan padding X = gutter; padding Y = section padding; latar diatur di container yang sama |

### 2.7 Lightbox

Site Settings > Lightbox: Image Lightbox **On**, latar overlay Ink 900 pada opasitas 94% (`rgba(17,17,17,.94)`), ikon dan teks White, navigasi panah On, penghitung (counter) On, keterangan (caption) dari Title/Caption 15 px Border, Share Off, Fullscreen Off, Zoom Off, Download Off. Pengguna bisa menutup dengan Esc dan tombol Close; fokus kembali ke pemicu (perilaku bawaan). Video: widget Video dengan Lightbox On (menggantikan modal `pages-b.js`, lihat `07-galeri-video.md`).

### 2.8 Custom CSS paste-ready (Site Settings > Custom CSS)

Tempel seluruh blok di bawah satu kali. Token `--sbb-*` menduplikasi Global Colors (ubah keduanya bila warna berubah). Kelas diberikan lewat **Advanced > CSS Classes** pada container atau widget. Di container yang memakai kelas `sbb-frost`, `sbb-pane`, **jangan** mengisi Background/Border/Radius secara native (kelas sudah mengaturnya). CSS hero foto besar (`sbb-hero*`) ada di 2.10 dan foto konten (`sbb-photo`, `sbb-ba--simulate`) di 2.11; tempel keduanya di bawah blok ini. Di Free-only, tempel di Appearance > Customize > Additional CSS.

```css
:root{--sbb-ink-900:#111111;--sbb-ink-700:#2B2B2B;--sbb-red-600:#CA1317;--sbb-red-500:#EC2327;--sbb-red-300:#FF3333;--sbb-red-800:#A30F12;--sbb-gray-50:#F8F8F8;--sbb-frost:#F4F4F4;--sbb-border:#DDDDDD;--sbb-text:#333333;--sbb-muted:#666666;--sbb-wa:#0B7A3B;--sbb-wa-h:#095F2E;--sbb-error:#C2410C;--sbb-header-h:68px;--sbb-bar-h:68px;--sbb-ease:cubic-bezier(.2,.7,.2,1);--sbb-dur:200ms}
@media(min-width:768px){:root{--sbb-header-h:76px}}
html{scroll-behavior:smooth;scroll-padding-top:calc(var(--sbb-header-h) + 16px)}
@media(max-width:767px){body{padding-bottom:calc(var(--sbb-bar-h) + env(safe-area-inset-bottom,0px))}}

/* Focus ring: 2px Red 600 offset 2; Red 300 di latar gelap; White di pane, promo bar, hero */
::focus-visible{outline:2px solid var(--sbb-red-600);outline-offset:2px}
.sbb-section--dark :focus-visible,.sbb-cta-bar :focus-visible,.elementor-location-footer :focus-visible{outline-color:var(--sbb-red-300)}
.sbb-pane :focus-visible,.sbb-promo-bar :focus-visible,.sbb-hero-photo :focus-visible{outline-color:var(--sbb-white)}

/* ::selection: merah brand dengan teks putih */
::selection{background:var(--sbb-red-600);color:var(--sbb-white)}
.sbb-section--dark :focus-visible,.sbb-pane :focus-visible,.sbb-cta-bar :focus-visible,.elementor-location-footer :focus-visible{outline-color:var(--sbb-red-300)}
.sbb-stretch a:focus-visible{outline:none}
.sbb-stretch a:focus-visible::after{outline:2px solid var(--sbb-red-600);outline-offset:2px}
.elementor-button{transition:background-color var(--sbb-dur) var(--sbb-ease),color var(--sbb-dur) var(--sbb-ease),border-color var(--sbb-dur) var(--sbb-ease),transform var(--sbb-dur) var(--sbb-ease)}
.elementor-button:active{transform:translateY(1px)}
.sbb-link-arrow .elementor-button-icon{transition:transform var(--sbb-dur) var(--sbb-ease)}
.sbb-link-arrow:hover .elementor-button-icon{transform:translateX(3px)}
.sr-only{position:absolute!important;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}

/* Reduced motion */
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}

/* Scroll reveal: tersembunyi hanya bila JS kecil (bagian 6) menambahkan html.sbb-js. Stagger: --sbb-i (0,1,2...) x 70ms */
html.sbb-js .sbb-reveal{opacity:0;transform:translateY(12px);transition:opacity 420ms var(--sbb-ease),transform 420ms var(--sbb-ease);transition-delay:calc(var(--sbb-i,0)*70ms)}
html.sbb-js .sbb-reveal.is-visible{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){html.sbb-js .sbb-reveal{opacity:1;transform:none;transition:none}}

/* Panel frosted + fallback @supports */
.sbb-frost{background:rgba(255,255,255,.72);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.65);box-shadow:0 0 0 1px rgba(17,17,17,.07);border-radius:14px}
@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){.sbb-frost{background:rgba(255,255,255,.92)}}

/* Latar section */
.sbb-section{position:relative}
.sbb-section--alt{background:var(--sbb-gray-50)}.sbb-section--frost{background:var(--sbb-frost)}.sbb-section--dark{background:var(--sbb-ink-900)}.sbb-section--flush-top{padding-top:0!important}
.sbb-pane{background:linear-gradient(115deg,transparent 0 58%,rgba(255,255,255,.055) 58% 62%,transparent 62% 66%,rgba(255,255,255,.03) 66% 67.5%,transparent 67.5%),linear-gradient(160deg,#CA1317 0%,#A30F12 100%);overflow:hidden}
.sbb-cta-bar{background:linear-gradient(115deg,transparent 0 62%,rgba(255,255,255,.06) 62% 66%,transparent 66% 70%,rgba(255,255,255,.035) 70% 71.5%,transparent 71.5%),#111111;border-radius:14px;overflow:hidden}

/* Eyebrow: garis potong 22x2 di depan teks */
.sbb-eyebrow .elementor-heading-title{display:inline-flex;align-items:center;gap:10px;text-transform:uppercase;letter-spacing:.06em}
.sbb-eyebrow .elementor-heading-title::before{content:"";width:22px;height:2px;background:currentColor;border-radius:2px}
/* Eyebrow: garis potong 22x2 di depan teks. Di band merah pane & promo bar
   eyebrow jadi PUTIH (Red 300 hanya 4,43:1 di atas merah, gagal AA). */
.sbb-section--dark .sbb-eyebrow,.sbb-cta-bar .sbb-eyebrow{color:var(--sbb-red-300)}
.sbb-pane .sbb-eyebrow{color:var(--sbb-white)}

/* Band pane merah: semua teks yang LANGSUNG di atas merah = White.
   Latar gelap lain (dark, cta-bar, footer) = Ink 900 dengan aksen Red 300. */
.sbb-section--dark h1,.sbb-section--dark h2,.sbb-section--dark h3,
.sbb-pane h1,.sbb-pane h2,.sbb-pane h3,
.sbb-cta-bar h2{color:var(--sbb-white)}
.sbb-section--dark{color:var(--sbb-border)}
.sbb-pane{color:var(--sbb-white)}
.sbb-section--dark a:not(.btn){color:var(--sbb-red-300)}
.sbb-pane a:not(.btn){color:var(--sbb-white)}
.sbb-section--dark .sbb-text-muted{color:var(--sbb-border)}
.sbb-pane .sbb-text-muted{color:var(--sbb-white)}
.sbb-section--dark .sbb-lead{color:var(--sbb-border)}
.sbb-pane .sbb-lead{color:var(--sbb-white)}
.sbb-pane .sbb-factor-list span{color:var(--sbb-white)}

/* Kartu/panel TERANG di dalam band pane merah: teks kembali gelap, link/eyebrow/
   ring merah. Daftar ini harus persis sama dengan yang dipakai di styles.css. */
.sbb-pane :is(.sbb-frost,.sbb-card-price,.sbb-card-value,.sbb-estimator,.sbb-hero-card,.sbb-photo__cap,.sbb-badge-trust,.sbb-ba-slider__tag,.sbb-ph-img__label){color:var(--sbb-text)}
.sbb-pane :is(.sbb-frost,.sbb-card-price,.sbb-card-value,.sbb-estimator,.sbb-hero-card,.sbb-photo__cap,.sbb-badge-trust,.sbb-ba-slider__tag,.sbb-ph-img__label) :is(h1,h2,h3,h4){color:var(--sbb-ink-900)}
.sbb-pane :is(.sbb-frost,.sbb-card-price,.sbb-card-value,.sbb-estimator,.sbb-hero-card,.sbb-photo__cap,.sbb-badge-trust,.sbb-ba-slider__tag,.sbb-ph-img__label) a:not(.btn),
.sbb-pane :is(.sbb-frost,.sbb-card-price,.sbb-card-value,.sbb-estimator,.sbb-hero-card,.sbb-photo__cap,.sbb-badge-trust,.sbb-ba-slider__tag,.sbb-ph-img__label) .sbb-link-arrow,
.sbb-pane :is(.sbb-frost,.sbb-card-price,.sbb-card-value,.sbb-estimator,.sbb-hero-card,.sbb-photo__cap,.sbb-badge-trust,.sbb-ba-slider__tag,.sbb-ph-img__label) .sbb-eyebrow{color:var(--sbb-red-600)}
.sbb-pane :is(.sbb-frost,.sbb-card-price,.sbb-card-value,.sbb-estimator,.sbb-hero-card,.sbb-photo__cap,.sbb-badge-trust,.sbb-ba-slider__tag,.sbb-ph-img__label) .sbb-text-muted{color:var(--sbb-text-muted)}
.sbb-pane :is(.sbb-frost,.sbb-card-price,.sbb-card-value,.sbb-estimator,.sbb-hero-card,.sbb-photo__cap,.sbb-badge-trust,.sbb-ba-slider__tag,.sbb-ph-img__label) .sbb-lead{color:var(--sbb-text)}
.sbb-pane :is(.sbb-frost,.sbb-card-price,.sbb-card-value,.sbb-estimator,.sbb-hero-card,.sbb-photo__cap,.sbb-badge-trust,.sbb-ba-slider__tag,.sbb-ph-img__label) :focus-visible{outline-color:var(--sbb-red-600)}

/* Rasio gambar (Elementor Image tanpa aspect-ratio native) */
[class*="sbb-ar-"] img{width:100%;height:auto;object-fit:cover}
.sbb-ar-16x9 img{aspect-ratio:16/9}.sbb-ar-4x3 img{aspect-ratio:4/3}.sbb-ar-1x1 img{aspect-ratio:1/1}.sbb-ar-3x4 img{aspect-ratio:3/4}.sbb-ar-3x2 img{aspect-ratio:3/2}
.sbb-ar-banner img{aspect-ratio:3/2}
@media(min-width:768px){.sbb-ar-banner img{aspect-ratio:21/9}}

/* Kartu (loop item / kartu klik penuh) */
.sbb-card,.sbb-card-post,.sbb-card-area{position:relative;background:#fff;border:1px solid var(--sbb-border);border-radius:14px;overflow:hidden;transition:border-color var(--sbb-dur) var(--sbb-ease)}
.sbb-card:hover,.sbb-card-post:hover,.sbb-card-area:hover{border-color:var(--sbb-red-600)}
.sbb-card img,.sbb-card-post img,.sbb-card-area img{transition:transform 320ms var(--sbb-ease)}
.sbb-card:hover img,.sbb-card-post:hover img,.sbb-card-area:hover img{transform:scale(1.03)}
.sbb-stretch a::after{content:"";position:absolute;inset:0}

/* Chip filter dan menu chip (Nav Menu / Button) */
.sbb-chip .elementor-button,.sbb-chip-menu .elementor-item{min-height:44px;padding:0 18px;border:1px solid var(--sbb-border);border-radius:999px;background:#fff;color:var(--sbb-ink-900);font-size:15px;font-weight:500;display:inline-flex;align-items:center;justify-content:center}
.sbb-chip .elementor-button:hover,.sbb-chip-menu .elementor-item:hover{border-color:var(--sbb-red-600);color:var(--sbb-red-600)}
.sbb-chip[aria-pressed="true"] .elementor-button,.sbb-chip.is-active .elementor-button,.sbb-chip-menu .elementor-item-active{background:var(--sbb-ink-900);border-color:var(--sbb-ink-900);color:#fff}

/* Pagination Loop Grid (Numbers + Previous/Next): 44x44, radius 10, aktif Ink 900 */
.elementor-pagination{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin-top:48px}
.elementor-pagination .page-numbers{min-width:44px;min-height:44px;padding:0 12px;display:inline-flex;align-items:center;justify-content:center;border:1px solid var(--sbb-border);border-radius:10px;background:#fff;color:var(--sbb-ink-900);font-weight:500}
.elementor-pagination a.page-numbers:hover{border-color:var(--sbb-red-600);color:var(--sbb-red-600)}
.elementor-pagination .page-numbers.current{background:var(--sbb-ink-900);border-color:var(--sbb-ink-900);color:#fff}
.elementor-pagination .page-numbers.dots{border:0;background:none}

/* Langkah proses: mobile garis vertikal, >=768 tiga kolom + garis horizontal */
.sbb-steps{display:grid;gap:32px}
@media(min-width:768px){.sbb-steps{grid-template-columns:repeat(3,minmax(0,1fr));gap:32px}}
.sbb-step{position:relative;padding-left:76px}
.sbb-step__num{position:absolute;left:0;top:0;width:56px;height:56px;border-radius:50%;background:var(--sbb-red-600);color:#fff;display:grid;place-items:center;font-weight:800;font-size:24px;line-height:1}
.sbb-step:not(:last-child)::before{content:"";position:absolute;left:27px;top:64px;bottom:-24px;width:2px;background:var(--sbb-border)}
@media(min-width:768px){.sbb-step{padding-left:0;padding-top:80px}.sbb-step:not(:last-child)::before{left:68px;right:-12px;top:27px;bottom:auto;width:auto;height:2px}}

/* Tabel perbandingan: mobile menjadi kartu (data-label per sel) */
.sbb-compare-wrap{border:1px solid var(--sbb-border);border-radius:14px;overflow:hidden;background:#fff}
.sbb-compare{width:100%;border-collapse:collapse;font-size:15.5px;line-height:1.5}
.sbb-compare caption{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap}
.sbb-compare th,.sbb-compare td{padding:16px;text-align:left;vertical-align:top;border-bottom:1px solid var(--sbb-border)}
.sbb-compare thead th{background:var(--sbb-ink-900);color:#fff;font-weight:700;border-bottom:0}
.sbb-compare tbody th{font-weight:700;color:var(--sbb-ink-900);background:var(--sbb-frost)}
.sbb-compare tbody tr:last-child :is(th,td){border-bottom:0}
@media(max-width:767px){.sbb-compare thead{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0)}.sbb-compare,.sbb-compare tbody,.sbb-compare tr,.sbb-compare th,.sbb-compare td{display:block;width:100%}.sbb-compare tr{border-bottom:1px solid var(--sbb-border)}.sbb-compare td{display:grid;grid-template-columns:8.5rem 1fr;gap:12px;padding:12px 16px}.sbb-compare td::before{content:attr(data-label);font-weight:600;color:var(--sbb-ink-900)}}
@media(min-width:768px){.sbb-compare thead th:first-child,.sbb-compare tbody th{width:17%}}

/* Daftar centang dan callout (juga di isi artikel) */
.check-list{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.check-list li{position:relative;padding-left:32px}
.check-list li::before{content:"";position:absolute;left:0;top:.22em;width:22px;height:22px;border-radius:50%;background:var(--sbb-gray-50)}
.check-list li::after{content:"";position:absolute;left:8px;top:calc(.22em + 4px);width:6px;height:11px;border:solid var(--sbb-red-600);border-width:0 2px 2px 0;transform:rotate(45deg)}
.sbb-section--alt .check-list li::before{background:#fff}
.sbb-callout{display:flex;gap:16px;align-items:flex-start;padding:24px;background:var(--sbb-gray-50);border:1px solid var(--sbb-border);border-radius:14px}
.sbb-section--alt .sbb-callout{background:#fff}

/* Isi artikel (Post Content, kelas sbb-article) */
.sbb-article>:is(p,ul,ol,h2,h3){max-width:68ch}
.sbb-article>.lead{max-width:60ch;font-size:20px;margin-bottom:24px}
.sbb-article h2{margin-top:1.9em;font-size:clamp(26px,1.3rem + 1vw,32px)}.sbb-article h3{margin-top:1.6em}
.sbb-article>:first-child{margin-top:0}.sbb-article li{margin-bottom:.4em}
.sbb-article figure{margin:32px 0}.sbb-article figcaption{margin-top:8px;font-size:14px;color:var(--sbb-muted)}
.sbb-article .sbb-compare-wrap{margin:24px 0 12px}.sbb-article .sbb-callout{margin:32px 0}

/* Tombol WhatsApp mengambang (desktop/tablet) dan bar bawah mobile */
.sbb-wa-float{position:fixed;right:20px;bottom:20px;z-index:60;display:none;place-items:center;width:56px;height:56px;border-radius:50%;background:var(--sbb-wa);color:#fff;box-shadow:0 8px 30px rgba(17,17,17,.08)}
.sbb-wa-float:hover{background:var(--sbb-wa-h);transform:scale(1.06)}
@media(min-width:768px){.sbb-wa-float{display:grid}}
.sbb-mobile-bar{position:fixed;left:0;right:0;bottom:0;z-index:60;display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:8px 16px calc(8px + env(safe-area-inset-bottom,0px));background:#fff;border-top:1px solid var(--sbb-border)}
@media(min-width:768px){.sbb-mobile-bar{display:none}}

/* Header sticky: garis bawah muncul setelah scroll (kelas bawaan Elementor Sticky Effects; tanpa JS). Label CTA panjang/pendek: dua Button (.sbb-cta-long "Chat WhatsApp", .sbb-cta-short "Chat") */
.sbb-header{background:#fff;border-bottom:1px solid transparent;transition:border-color var(--sbb-dur) var(--sbb-ease)}
.sbb-header.is-scrolled,.sbb-header.elementor-sticky--effects{border-bottom-color:var(--sbb-border)}
.sbb-cta-short{display:none}@media(max-width:1199px){.sbb-cta-long{display:none}.sbb-cta-short{display:block}}

/* Peta area Home (HTML widget SVG inline) */
.area-map{width:100%;max-width:420px;margin-inline:auto}.area-map svg{display:block;width:100%;height:auto}
.area-map__land{fill:var(--sbb-gray-50)}.area-map__sea{fill:var(--sbb-frost)}.area-map__dot{fill:var(--sbb-red-600);stroke:#fff;stroke-width:3}.area-map__dot--hq{fill:var(--sbb-ink-900)}
.area-map__coast{fill:none;stroke:var(--sbb-red-300);stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}
.area-map__label{font-size:15px;font-weight:600;fill:var(--sbb-ink-900)}.area-map__note{margin:8px 0 0;text-align:center;font-size:14px;color:var(--sbb-muted)}

/* Form: galat dan berkas (Form widget) */
.elementor-message-danger,.elementor-field-group .elementor-message{color:var(--sbb-error);font-weight:600;font-size:14px}
.elementor-field-group.elementor-error .elementor-field{border-color:var(--sbb-error);box-shadow:0 0 0 1px var(--sbb-error)}
.elementor-field:focus-visible{outline:2px solid var(--sbb-red-600);outline-offset:2px}
```

Kelas hook tanpa CSS (hanya penanda untuk penargetan/override dan pelacakan): `sbb-page-*`, `sbb-gallery`, `sbb-gallery-status`, `sbb-faq`, `sbb-video`, `sbb-review-panel`, `sbb-need-row`, `sbb-contact-card`. Bila memakai Grid container native untuk `sbb-steps`, aturan `.sbb-steps` di atas tidak perlu.

Kelas komponen lain yang muncul di file halaman (`.estimator*`, `.faq-*`, `.accordion*`, `.ba-slider*`, `.motif__swatch--*`, `.dash-list`, `.team-card`, `.hours`, `.hero-prices*`, `.facts`, `.file-list`, `.modal`) **tidak** di-copy ke Kit; tiap file halaman menyebut baris sumber di `mockup/assets/css/` yang disalin ke HTML widget/Custom CSS halaman itu hanya bila opsi custom dipilih (daftar di bagian 6).

### 2.9 Resep (konvensi kode yang dipakai file halaman)

| Kode | Struktur Elementor | Setelan |
|---|---|---|
| `SEC(putih/alt/frost/dark/pane)` | 1 container Boxed 1200 | Padding Y 96/76/56, X 24/24/16; latar putih / Gray 50 (`sbb-section--alt`) / Frost (`sbb-section--frost`) / Ink 900 (`sbb-section--dark`) / **band merah gradien Red 600 → Red 800 dengan teks putih** (`sbb-pane`); ID anchor sesuai file halaman |
| `HEAD` | Container Column, Gap 12 | Eyebrow (Heading p, kelas `sbb-eyebrow`) + H2 + Lead (opsional); lebar maks 720; margin bawah 48/36/28; varian center: rata tengah, container margin auto |
| `GRID N` | Container Grid (Elementor 3.27+) atau Flex Row Wrap | Kolom N / 2 / 1; Gap 24 (`GRID 4`: 4/2/1); tablet 2 kolom untuk N ≥ 3; item Align Stretch. Bila Grid container tidak ada, Flex Wrap dengan lebar item `calc((100% - gap)/N)` |
| `SPLIT`, `SPLIT-W`, `SPLIT-T` | Container Row, Align Center | 2 kolom sama (`SPLIT`), 1,15fr/0,85fr (`SPLIT-W`), Align Start (`SPLIT-T`); Gap 64 di ≥ 1025, 32 di tablet/mobile; **Column di ≤ 1024** |
| `HERO-FOTO` (varian `home`, `page`) | Container terluar Full Width, kelas `sbb-hero-photo sbb-hero-photo--home` atau `--page` (`--page` + `--tall` untuk Tentang Kami dan Portofolio; `--article` untuk Single Artikel) | Bagian 2.10: Image absolut (`sbb-hero-photo__img`) + overlay + container inner (`TPL-BC` varian terang, Eyebrow terang, H1, Lead, tombol, badge) + kartu frosted opsional. Satu per halaman, selalu section pertama di bawah header |
| `PAGE-HERO` | Sinonim `HERO-FOTO` varian `page` | Semua halaman dalam memakai hero foto; tidak ada hero berlatar gradien |
| `TPL-BC` | Saved Template breadcrumb | Widget Shortcode breadcrumb plugin SEO (`[rank_math_breadcrumb]` / `[wpseo_breadcrumb]`), atau Icon List horizontal dengan pemisah ">" untuk halaman statis; 14 px Text Muted, item terakhir tanpa link, `aria-label` "Breadcrumb", wrap di mobile. **Varian terang** (kelas tambahan `sbb-bc--light`, dipakai di dalam hero foto): teks White, tautan White bergaris bawah `rgba(255,255,255,.55)` offset 3 px, pemisah `rgba(255,255,255,.8)` (CSS 2.10) |
| `TPL-CTA` | Saved Template, bar CTA akhir | Section putih padding 96/76/56 > container `sbb-cta-bar` (padding 56/40/28; Grid 1fr auto ≥ 1025, tumpuk di bawahnya); H2 White "Kirim foto kaca Anda, kami hitungkan estimasinya." + teks Border 17px "Sebutkan jenis layanan dan ukuran kira-kira. Balasan awal lewat WhatsApp, dan harga final dipastikan setelah kaca diukur langsung."; `BTN-WA` "Chat WhatsApp" + `BTN-SEC-L` "Minta penawaran" (`/kontak/#penawaran`); kelas `sbb-reveal` |
| `BTN-PRI`, `BTN-WA`, `BTN-SEC`, `BTN-SEC-L` | Button widget / Saved Template | Bagian 2.3; tombol penuh lebar di mobile pada konteks hero dan kartu. `BTN-SEC-L` = tombol **outline light** (kelas `sbb-btn--outline-light`): dipakai sebagai tombol kedua di hero foto dan di bar CTA |
| `LINK-ARROW` | Button, gaya text | Bagian 2.3; ikon panah kanan 18 px; kelas `sbb-link-arrow` |
| `CHIPS` | Container Row Wrap Gap 8 | Button gaya chip (`sbb-chip`, bagian 2.8); tap target 44 |
| `BADGE` | Container `sbb-frost` kecil | Pill radius 999, padding 8/16, ikon 18 + teks 14 px 600 Ink 900. Di dalam hero foto badge berupa chip frosted **gelap** (`sbb-hero-photo__badges`, bagian 2.10), bukan `sbb-frost` putih |
| `STEPS` / `TPL-STEPS` | Container Grid 3 (mobile 1) | Tiap langkah kelas `sbb-step` + nomor `sbb-step__num`; judul 20 px 700, teks Text Muted, waktu 14 px dengan ikon jam |
| `CARD-VAL` / `TPL-VALUE-4` | Container Column, kelas `sbb-card` | Padding 24; ikon dalam lingkaran 48 px Gray 50 dengan ikon Red 600; H3 20 px; teks Text Muted; di section alt lingkaran ikon putih. Di dalam `sbb-pane` kartu tetap terang dan teksnya direset ke gelap (aturan reset panel terang, bagian 2.8) |
| `CARD-PRICE` | Container `sbb-frost` padding 32 | Nama (H3) + "mulai dari" 14 px + harga 32 px 800 + Icon List centang (`check-list`) + catatan 14 px |
| `TPL-FAKTOR` | Saved Template | Daftar faktor harga bergaris (border atas/bawah 1px, judul 700, teks Border) di section `dark`/`pane` |
| `TPL-AREA-CHIPS` | Saved Template | `CHIPS` tujuh kota dari CPT `area` (Loop Grid gaya chip) + `LINK-ARROW` "Lihat semua area" |
| `LI-*` | Loop Item (bagian 5) | Container `sbb-card` dengan Link = Post URL; lihat daftar di 5.2 |

### 2.10 Hero foto besar (`HERO-FOTO`)

Setiap halaman dibuka dengan hero foto full-bleed (`.hero-photo` di mockup): foto memenuhi lebar layar, overlay Ink 900 di atasnya, teks putih di atas overlay. Home memakai varian `home` (tinggi), 13 halaman lain varian `page`. Semua angka di bawah disalin dari `mockup/assets/css/styles.css` bagian 5.20 (token `--hero-*` di baris 106-111), `pages-b.css` dan `pages-c.css`.

**Keputusan struktur.** Container terluar **Full Width** berisi **widget Image berposisi absolut sebagai foto cover di belakang teks**; bukan Background Image container. Alasan: (a) foto menjadi `<img>` sungguhan dengan `srcset`, ditemukan browser sejak HTML pertama dan bisa diberi `fetchpriority="high"` tanpa lazy-load, sehingga LCP seluler tetap ≤ 2,5 dtk; background-image CSS ditemukan terlambat, tidak bisa diberi prioritas, dan terkena Lazy Load Background Images; (b) `alt` deskriptif tetap ada; (c) `object-position` per halaman lewat variabel `--focus`, dan tinggi foto di mobile bisa dibatasi; (d) mask pemudaran ke Ink 900 di mobile hanya bisa dipasang pada elemen gambar.

**Fallback** (hanya bila Image berposisi absolut tidak bisa dipakai di versi Elementor Anda): Container yang sama dengan **Background Image** (Size Cover, Position Custom sesuai `--focus`, Attachment Scroll) + tab **Background Overlay** bergradasi dengan stop yang sama seperti tabel di bawah. Matikan Elementor > Settings > Performance > Lazy Load Background Images, dan pasang preload di Custom Code > Head (kondisi: halaman itu): `<link rel="preload" as="image" href=".../hero-home.webp" imagesrcset="..." imagesizes="100vw" fetchpriority="high">`. Konsekuensinya: `alt` diganti `role="img"` + `aria-label` di Advanced > Attributes, dan pemudaran mobile memakai stop gradasi 180° pada Overlay (tanpa mask).

Pohon elemen (selalu dalam urutan ini; tanda z = Z-Index):

```
Container terluar  .sbb-hero-photo .sbb-hero-photo--home|--page   (Full Width, HTML Tag section, Position Relative, Overflow Hidden,
│                  Direction Column, Justify Center, latar Ink 900; Advanced > Attributes: `aria-labelledby|hero-title` (Home) atau `aria-labelledby|page-title`, id yang sama di H1)
├─ Image           .sbb-hero-photo__img      z0  Position Absolute 0/0, W 100%, H 100%, Object Fit Cover, TANPA lazy, fetchpriority high (K17)
├─ Container       .sbb-hero-photo__overlay  z1  kosong, Position Absolute inset 0, Pointer Events none; Background Gradient (tabel di bawah)
├─ Container       .sbb-hero-photo__inner    z2  Boxed 1200, Direction Column, Gap 16, padding X 24/24/16
│    ├─ TPL-BC varian terang (`sbb-bc--light`; tidak ada di Home)
│    ├─ Heading p .sbb-eyebrow .sbb-eyebrow--light   (Eyebrow pil)
│    ├─ Heading H1 (putih)   ├─ Text Editor Lead (putih)
│    ├─ Row Wrap tombol: BTN-WA | BTN-PRI  +  BTN-SEC-L (outline light)
│    └─ Icon List .sbb-hero-photo__badges (opsional; chip frosted gelap)
└─ Container       .sbb-hero-photo__card .sbb-frost   z2  (opsional: Home, Harga, Testimoni, Area Denpasar)
```

| Properti | Desktop ≥ 1025 | Tablet 768-1024 | Mobile ≤ 767 |
|---|---|---|---|
| Min Height `home` (diatur CSS; kosongkan Min Height native) | `clamp(560px, 88vh, 860px)` | sama | `clamp(640px, calc(100svh - 76px), 860px)` |
| Min Height `page` / `tall` | `clamp(440px, 62vh, 620px)` | sama | `clamp(400px, 56vh, 520px)` |
| Posisi teks | Justify Center | Justify Center | Justify **End** (teks menempel di bawah, atas foto dibiarkan terang); padding-top `clamp(88px, 20svh, 200px)` Home, `clamp(80px, 14svh, 132px)` halaman dalam |
| Overlay (Ink 900 `#111111` dengan alfa) | Gradient Linear **90°**: alfa **.88** @ 0%, **.72** @ 66%, **.30** @ 100% (`--hero-a-start`, `--hero-a-min`, `--hero-a-end`) | rata **.72** | rata **.12** (`--hero-a-top`, zona atas hanya foto) |
| Gradasi pelindung teks (background container `inner`) | tidak ada | tidak ada | Gradient **180°**: alfa 0 @ 0 → **.72** @ 72px; padding-top 76px; tinggi Image dibatasi `clamp(560px, 100svh, 900px)` (Home) / `clamp(420px, 76svh, 720px)` (halaman dalam) dengan mask pudar 140 px ke Ink 900 di dasar |
| Lebar blok teks | maks `min(640px, 62%)` | penuh | penuh |
| Padding Y `inner` (Home / halaman dalam) | 104 / 56; `tall` 88 | 72 / 45 | 48 / 28 |
| H1 (override lokal Global H1; Home / halaman dalam) | 64 / 48 | 60 / 45 | 38 / 32; LH 1,08 (Home) atau 1,12; margin bawah 16 / 12; warna White; text-shadow `0 1px 2px rgba(17,17,17,.35)` |
| Lead (Home / halaman dalam) | White, maks 56ch; 22 / 20 | 21 / 19 | 18 / 17 |
| Tombol | Row Wrap Gap 12, margin-top 32 (Home) / 24; `BTN-WA` atau `BTN-PRI` + `BTN-SEC-L` | sama | masing-masing Width 100% |
| Fokus foto | `--focus` per halaman (tabel 2.11), diisi lewat Advanced > Custom CSS container: `selector{--focus:50% 55%}` | sama | sama |

Komponen di dalam hero:

- **Eyebrow terang**: pil Ink 900 alfa **.72** (`--hero-pill-a`), padding 6/14/6/12, radius 999, blur 6 px, teks **White** (Title Color native; Red 300 di pil hanya 4,43:1, gagal AA), garis potong 22x2 tetap.
- **Chip badge**: tiap item Icon List min-height 40, Ink 900 alfa **.45** (`--hero-chip-a`), blur 10 px, border 1px `rgba(255,255,255,.32)`, teks White 15 px 600, ikon Red 300 20 px; Row Wrap Gap 8/12, margin-top 32.
- **Breadcrumb terang**: `TPL-BC` + `sbb-bc--light`, margin bawah 12; teks dan tautan White, pemisah White alfa .8.
- **Kartu frosted** `sbb-frost sbb-hero-photo__card`: padding 24, radius 14, judul 20 px 800 Ink 900, isi 15 px Text. ≥ 1025: Position Absolute, kanan sejajar tepi container 1200, bawah **48**, lebar 340. ≤ 1024: relatif di bawah blok teks, lebar maks 420, margin 0 16 32.
- Varian: `--tall` (Tentang, Harga, Portofolio, Galeri Video, Testimoni) menambah padding Y `inner` 88 di desktop; `--article` (Single Artikel) membatasi H1 26ch dan menambah baris meta (penulis · tanggal · waktu baca, White 15 px 600, ikon **White**).
- Bila `backdrop-filter` tidak didukung: pil `.92`, chip `.8`, kartu putih `.92` (dalam CSS di bawah).

**Kontras (invarian).** Teks tidak pernah berada di atas alfa overlay di bawah **.72** (`--hero-a-min`; `tools/contrast.py` mewajibkan token ≥ .68). Kasus terburuk dihitung dengan foto putih murni di bawah overlay: putih 6,29:1 (H1, lead, breadcrumb, tombol outline light; batas AA 4,5), Red 300 di pil eyebrow 6,76:1, putih di chip 9,66:1, putih di zona gelap mobile 7,05:1, ring fokus Red 300 3,43:1 (batas 3); kartu frosted di atas piksel hitam: judul Ink 900 7,80:1, isi 6,26:1. `python3 mockup/tools/contrast.py` melaporkan 56 pasangan dan 5 invarian, 0 gagal. Jangan menurunkan alfa mana pun tanpa menjalankan skrip itu.

CSS paste-ready (Site Settings > Custom CSS, di bawah blok 2.8):

```css
/* HERO FOTO (2.10) */
:root{--sbb-hero-a-start:.88;--sbb-hero-a-min:.72;--sbb-hero-a-end:.30;--sbb-hero-a-top:.12;--sbb-hero-pill-a:.72;--sbb-hero-chip-a:.45}
.sbb-hero-photo{position:relative;isolation:isolate;overflow:hidden;display:flex;flex-direction:column;justify-content:center;background:var(--sbb-ink-900);color:#fff}
.sbb-hero-photo--home{min-height:clamp(560px,88vh,860px)}
.sbb-hero-photo--page{min-height:clamp(440px,62vh,620px)}
.sbb-hero-photo__img{position:absolute!important;inset:0;z-index:0;width:100%;height:100%;margin:0}
.sbb-hero-photo__img .elementor-widget-container{height:100%}
.sbb-hero-photo__img img{display:block;width:100%;height:100%;object-fit:cover;object-position:var(--focus,50% 50%)}
.sbb-hero-photo__overlay{position:absolute!important;inset:0;z-index:1;pointer-events:none;background:rgba(17,17,17,var(--sbb-hero-a-min))}
.sbb-hero-photo__inner{position:relative;z-index:2}
.sbb-hero-photo--home .sbb-hero-photo__inner{padding-block:clamp(48px,8vw,104px)}
.sbb-hero-photo--page .sbb-hero-photo__inner{padding-block:clamp(28px,5vw,56px)}
.sbb-hero-photo h1{color:#fff;text-shadow:0 1px 2px rgba(17,17,17,.35)}
.sbb-hero-photo--article h1{max-width:26ch}
.sbb-hero-photo :focus-visible{outline-color:var(--sbb-red-300)}
.sbb-eyebrow--light .elementor-heading-title{padding:6px 14px 6px 12px;border-radius:999px;background:rgba(17,17,17,var(--sbb-hero-pill-a));-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
.sbb-bc--light,.sbb-bc--light a,.sbb-bc--light .elementor-icon-list-text{color:#fff}
.sbb-bc--light a{text-decoration:underline;text-decoration-color:rgba(255,255,255,.55);text-underline-offset:3px}.sbb-bc--light a:hover{text-decoration-color:#fff}
.sbb-btn--outline-light .elementor-button{background:transparent;border:2px solid #fff;color:#fff}
.sbb-btn--outline-light .elementor-button:hover{background:#fff;color:var(--sbb-ink-900)}
.sbb-hero-photo__badges .elementor-icon-list-items{display:flex;flex-wrap:wrap;gap:8px 12px}
.sbb-hero-photo__badges .elementor-icon-list-item{display:inline-flex;align-items:center;gap:8px;min-height:40px;padding:6px 16px 6px 12px;border-radius:999px;background:rgba(17,17,17,var(--sbb-hero-chip-a));border:1px solid rgba(255,255,255,.32);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);font-size:15px;font-weight:600;line-height:1.3}
.sbb-hero-photo__badges .elementor-icon-list-text{color:#fff}
.sbb-hero-photo__badges .elementor-icon-list-icon svg,.sbb-hero-photo__badges .elementor-icon-list-icon i{width:20px;height:20px;color:var(--sbb-red-300);fill:var(--sbb-red-300)}
@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){.sbb-eyebrow--light .elementor-heading-title{background:rgba(17,17,17,.92)}.sbb-hero-photo__badges .elementor-icon-list-item{background:rgba(17,17,17,.8)}}
.sbb-hero-photo__card{position:relative;z-index:2;width:min(420px,calc(100% - 32px));margin:0 16px 32px;padding:24px;color:var(--sbb-ink-900)}
@media(min-width:1025px){
.sbb-hero-photo__overlay{background:linear-gradient(90deg,rgba(17,17,17,var(--sbb-hero-a-start)) 0%,rgba(17,17,17,var(--sbb-hero-a-min)) 66%,rgba(17,17,17,var(--sbb-hero-a-end)) 100%)}
.sbb-hero-photo__inner>*{max-width:min(640px,62%)}
.sbb-hero-photo--tall .sbb-hero-photo__inner{padding-block:clamp(48px,6vw,88px)}
.sbb-hero-photo__card{position:absolute;right:max(16px,calc((100% - 1200px)/2));bottom:48px;width:340px;margin:0}}
@media(max-width:767px){
.sbb-hero-photo{justify-content:flex-end}
.sbb-hero-photo--home{min-height:clamp(640px,calc(100vh - 76px),860px);min-height:clamp(640px,calc(100svh - 76px),860px);padding-top:clamp(88px,20svh,200px)}
.sbb-hero-photo--page{min-height:clamp(400px,56vh,520px);padding-top:clamp(80px,14svh,132px)}
.sbb-hero-photo__overlay{background:rgba(17,17,17,var(--sbb-hero-a-top))}
.sbb-hero-photo--home .sbb-hero-photo__img{height:clamp(560px,100svh,900px)}
.sbb-hero-photo--page .sbb-hero-photo__img{height:clamp(420px,76svh,720px)}
.sbb-hero-photo__img{-webkit-mask-image:linear-gradient(180deg,#000 calc(100% - 140px),transparent);mask-image:linear-gradient(180deg,#000 calc(100% - 140px),transparent)}
.sbb-hero-photo__inner{--sbb-hero-fade:72px;padding-top:calc(var(--sbb-hero-fade) + 4px);background:linear-gradient(180deg,rgba(17,17,17,0) 0,rgba(17,17,17,var(--sbb-hero-a-min)) var(--sbb-hero-fade))}
.sbb-hero-photo--home .sbb-hero-photo__inner{padding-bottom:32px}
.sbb-hero-photo__inner::after{content:"";position:absolute;z-index:-1;left:0;right:0;top:calc(100% - 1px);height:100vh;background:rgba(17,17,17,var(--sbb-hero-a-min));pointer-events:none}}
```

Aturan pakai: kelas ini mengatur Min Height, padding Y `inner`, latar overlay, dan posisi kartu, jadi kontrol native yang sama dikosongkan di container hero. Warna teks (White / Red 300), tipografi, Gap, dan padding X tetap diisi native. Gambar dan overlay yang absolut tidak boleh masuk hitungan tinggi hero: tinggi hero ditentukan `inner` + Min Height.

**Prioritas muat (K17).** Widget Image hero harus dirender tanpa `loading="lazy"` dan dengan `fetchpriority="high"`. Child theme `functions.php` atau Code Snippets:

```php
add_filter( 'elementor/widget/render_content', function ( $html, $widget ) {
	if ( 'image' !== $widget->get_name() ) { return $html; }
	$cls = (string) $widget->get_settings_for_display( '_css_classes' );
	if ( false === strpos( ' ' . $cls . ' ', ' sbb-hero-photo__img ' ) ) { return $html; }
	$html = preg_replace( '/\s(?:loading|fetchpriority)="[^"]*"/i', '', $html );
	return preg_replace( '/<img\s/i', '<img loading="eager" fetchpriority="high" decoding="async" ', $html, 1 );
}, 10, 2 );
```

Di plugin cache, kecualikan kelas `sbb-hero-photo__img` dari lazy-load (LiteSpeed Cache: Page Optimization > Media > Lazy Load Image Class Name Excludes). Tepat satu gambar `fetchpriority="high"` per halaman.

### 2.11 Pustaka media (foto Pexels)

Semua foto sudah berupa WebP siap pakai di `mockup/assets/img/photos/`; `manifest.json` di folder yang sama memetakan tiap peran ke `file`, `width`, `height`, `pexels_id`, `kind` (`hero` = 1920 px lebar, `card` = 900 px lebar). 71 peran; tabel di bawah diturunkan dari manifest dan dari `src="assets/img/photos/` di 14 halaman mockup.

**Konvensi unggah dan nama.**
- Unggah berkas apa adanya di Media > Add New; **jangan ganti nama berkas** (`hero-home.webp`, `svc-sandblast.webp`, `g-01-frosted-doors.webp`, ...): nama berkas adalah kunci antara mockup, tabel ini, dan file halaman.
- Format tetap WebP; jangan biarkan plugin optimasi mengonversi ulang atau menimpa berkas asli (LiteSpeed Image Optimization: hanya buat ukuran turunan). `width`/`height` mengikuti manifest (Elementor mengisinya otomatis dari berkas).
- Isi kolom **Description** Media Library dengan `https://www.pexels.com/photo/{pexels_id}/` (dari manifest). Lisensi Pexels: bebas dipakai komersial tanpa atribusi.
- **Alt text**: tulis apa yang tampak di foto, satu kalimat, tanpa awalan "foto/gambar", tanpa kata kunci berulang, tanpa klaim bahwa itu hasil kerja kami (contoh mockup: "Lorong kantor dengan dinding kaca dan sekat bermotif titik yang menjaga ruangan tetap terang"). Isi di Media Library (Alternative Text) agar sama di semua pemakaian; salin dari atribut `alt` di `mockup/*.html`. Foto dekoratif: `alt` kosong. Caption galeri berformat "jenis · kawasan" (kolom Caption, dipakai lightbox).
- **Lazy-load**: hero **dikecualikan** (tanpa `loading="lazy"`, `fetchpriority="high"`, satu per halaman, K17). Semua gambar lain `loading="lazy"` + `decoding="async"` (bawaan Elementor/WordPress).
- Ukuran WordPress bawaan (768 / 1024 / 1536) menjadi `srcset`; pilih Image Size di widget sesuai tabel agar `srcset` tidak memuat berkas yang lebih besar dari kolomnya.

| Kelompok | Ukuran sumber | Image Size Elementor | `sizes` yang diharapkan | Loading |
|---|---|---|---|---|
| Hero (`hero-*`, 14) | 1920 x 1280 (rasio bervariasi, lihat tabel) | Full | `100vw` | Eager, `fetchpriority="high"` |
| Kartu layanan (`svc-*`, 9), Loop Item `LI-LAYANAN` | 900 x 600 | Full (900) | `(min-width:1025px) 384px, (min-width:768px) 50vw, 100vw` | Lazy |
| Galeri proyek (`g-01..g-32`) | 900 lebar, tinggi 599-1600 (rasio asli, tanpa crop) | Full (900) | `(min-width:1025px) 384px, (min-width:480px) 50vw, 100vw` | Lazy |
| Kartu area (`area-*`, 7) | 900 lebar | Full (900) | `(min-width:1025px) 282px, (min-width:768px) 50vw, 100vw` | Lazy |
| Bengkel, ruang, testimoni (`workshop-*`, `clinic-reception`, dst.) | 900 lebar | Full (900) | `(min-width:1025px) 384px, 100vw` (foto split: `(min-width:1025px) 560px, 100vw`) | Lazy |
| Kartu artikel | 900 lebar | Full (900) | `(min-width:1025px) 384px, (min-width:768px) 50vw, 100vw` | Lazy |

Singkatan halaman: **Beranda**, **Tentang** (incl. `#testimoni`, `#area`), **Layanan** (incl. `#harga`, `#estimasi`), **Porto** (incl. `#video`), **Artikel** (index), **S.Artikel**, **Kontak** (incl. `#faq`).

**Hero (14).** Fokus = nilai `--focus` (object-position) pada container hero halaman itu (bagian 2.10).

| Peran | Berkas | Ukuran | Halaman | Fokus |
|---|---|---|---|---|
| `hero-home` | `hero-home.webp` | 1920 x 1280 | Home | `50% 55%` |
| `hero-layanan` | `hero-layanan.webp` | 1920 x 1285 | Layanan | `70% 50%` |
| `hero-sandblast` | `hero-sandblast.webp` | 1920 x 1280 | S.Layanan | `50% 50%` |
| `hero-tentang` | `hero-tentang.webp` | 1920 x 1440 | Tentang | `50% 62%` |
| `hero-harga` | `hero-harga.webp` | 1920 x 1280 | Harga | `50% 45%` |
| `hero-portofolio` | `hero-portofolio.webp` | 1920 x 1329 | Porto | `50% 42%` |
| `hero-galeri-video` | `hero-galeri-video.webp` | 1920 x 1281 | Video | `50% 35%` |
| `hero-testimoni` | `hero-testimoni.webp` | 1920 x 1280 | Testi | `50% 30%` |
| `hero-area` | `hero-area.webp` | 1920 x 1440 | Area; S.Area untuk enam area selain Denpasar | `50% 55%` |
| `hero-area-denpasar` | `hero-area-denpasar.webp` | 1920 x 1280 | S.Area | `50% 60%` |
| `hero-faq` | `hero-faq.webp` | 1920 x 1440 | FAQ | `50% 45%` |
| `hero-artikel` | `hero-artikel.webp` | 1920 x 1278 | Artikel | `50% 40%` |
| `hero-artikel-single` | `hero-artikel-single.webp` | 1920 x 1280 | S.Artikel | `50% 50%` |
| `hero-kontak` | `hero-kontak.webp` | 1920 x 1280 | Kontak | `50% 50%` |

**Layanan (9)**, foto unggulan CPT `layanan` = `svc-*` (satu foto per layanan, urutan sama dengan menu order).

| Peran | Berkas | Ukuran | Halaman |
|---|---|---|---|
| `svc-sandblast` | `svc-sandblast.webp` | 900 x 600 | Home, Tentang, Layanan, Harga, S.Area, S.Artikel |
| `svc-one-way` | `svc-one-way.webp` | 900 x 600 | Home, Tentang, Layanan, S.Layanan, Harga, S.Area, S.Artikel |
| `svc-riben` | `svc-riben.webp` | 900 x 675 | Home, Tentang, Layanan, S.Layanan, Harga, Artikel |
| `svc-kaca-film` | `svc-kaca-film.webp` | 900 x 602 | Home, Tentang, Layanan, S.Layanan, Harga, S.Area, S.Artikel |
| `svc-printing` | `svc-printing.webp` | 900 x 600 | Home, Layanan |
| `svc-cutting` | `svc-cutting.webp` | 900 x 601 | Home, Tentang, Layanan, Harga, Video |
| `svc-wrapping` | `svc-wrapping.webp` | 900 x 600 | Home, Layanan, Harga |
| `svc-huruf-timbul` | `svc-huruf-timbul.webp` | 900 x 600 | Home, Tentang, Layanan, Harga |
| `svc-neon-box` | `svc-neon-box.webp` | 900 x 601 | Home, Tentang, Layanan, Harga |

**Area (7)**, foto unggulan CPT `area` = `area-*`.

| Peran | Berkas | Ukuran | Halaman |
|---|---|---|---|
| `area-denpasar` | `area-denpasar.webp` | 900 x 1350 | Area |
| `area-ubud` | `area-ubud.webp` | 900 x 1200 | Area |
| `area-seminyak` | `area-seminyak.webp` | 900 x 600 | Area |
| `area-canggu` | `area-canggu.webp` | 900 x 1291 | Area |
| `area-sanur` | `area-sanur.webp` | 900 x 1200 | Area |
| `area-nusa-dua` | `area-nusa-dua.webp` | 900 x 675 | Area, Artikel |
| `area-kuta` | `area-kuta.webp` | 900 x 1349 | Area |

**Bengkel, ruang, dan pendukung.**

| Peran | Berkas | Ukuran | Halaman |
|---|---|---|---|
| `workshop-plotter` | `workshop-plotter.webp` | 900 x 1353 | Home, Tentang, FAQ |
| `workshop-printing-hall` | `workshop-printing-hall.webp` | 900 x 675 | Layanan |
| `workshop-printer` | `workshop-printer.webp` | 900 x 600 | Home, Tentang |
| `workshop-installer` | `workshop-installer.webp` | 900 x 600 | Home, Tentang, Area, S.Artikel |
| `clinic-reception` | `clinic-reception.webp` | 900 x 1348 | Testi, S.Area |
| `hotel-reception` | `hotel-reception.webp` | 900 x 1200 | Testi |
| `stickers-wall` | `stickers-wall.webp` | 900 x 1350 | Tentang |
| `villa-living` | `villa-living.webp` | 900 x 1350 | Testi |
| `villa-bedroom` | `villa-bedroom.webp` | 900 x 1200 | tidak terpasang di halaman (cadangan bank foto) |

**Galeri proyek (32)**, foto unggulan CPT `proyek` = `g-*`. Caption tiap foto (format "jenis · kawasan") ada di `DEMO-CONTENT.md` bagian "Pemetaan foto dan caption galeri" dan bagian Portofolio; slider before/after di blok `#sticker-sandblast` pada halaman `/layanan/` memakai `g-03-conference` dengan kelas `ba--simulate` (bagian 6, K6).

| Peran | Ukuran | Halaman |
|---|---|---|
| `g-01-frosted-doors` | 900 x 1350 | Home, S.Layanan, Porto, S.Area |
| `g-02-glass-hallway` | 900 x 600 | Home, S.Layanan, Harga, Porto, Testi, S.Area, Artikel, S.Artikel |
| `g-03-conference` | 900 x 602 | Home, S.Layanan, Porto |
| `g-04-bathroom-frost` | 900 x 601 | S.Layanan, Porto, Video, S.Area, Artikel, S.Artikel |
| `g-05-shower-glass` | 900 x 601 | Home, Porto, S.Area, Artikel, S.Artikel |
| `g-06-office-dark` | 900 x 600 | Porto, Video |
| `g-07-corporate-doors` | 900 x 1125 | Porto, S.Area |
| `g-08-door-glass` | 900 x 1200 | Porto, S.Area |
| `g-09-frosted-panels` | 900 x 1350 | S.Layanan, Porto, S.Area |
| `g-10-etched-leaf` | 900 x 600 | Home, Porto |
| `g-11-etched-portrait` | 900 x 1350 | S.Layanan, Porto |
| `g-12-decal-window` | 900 x 601 | Tentang, Harga, Porto |
| `g-13-car-decal` | 900 x 1125 | Porto |
| `g-14-wrap-hood` | 900 x 600 | Home, Tentang, Porto |
| `g-15-wrap-glove` | 900 x 600 | Porto |
| `g-16-wrap-front` | 900 x 600 | Porto, Video |
| `g-17-wrap-blue` | 900 x 600 | Porto |
| `g-18-neon-tattoo` | 900 x 600 | Porto |
| `g-19-neon-shoplocal` | 900 x 900 | Porto |
| `g-20-3d-cafe` | 900 x 600 | Porto, Video |
| `g-21-3d-coffee` | 900 x 600 | Porto |
| `g-22-glass-lettering` | 900 x 623 | Home, S.Layanan, S.Area, Artikel |
| `g-23-cafe-logo-door` | 900 x 1350 | Porto, S.Area |
| `g-24-cafe-glass-sign` | 900 x 1350 | Porto |
| `g-25-storefront` | 900 x 1350 | Home, Porto, Video, S.Area |
| `g-26-store-logo-glass` | 900 x 1350 | Porto, S.Area |
| `g-27-cafe-interior` | 900 x 1350 | Porto |
| `g-28-cafe-windows` | 900 x 1349 | Porto, Artikel, S.Artikel |
| `g-29-cafe-terrace` | 900 x 1200 | Home, Porto |
| `g-30-window-tint` | 900 x 1600 | Porto |
| `g-31-tint-installer` | 900 x 600 | S.Layanan, Porto, S.Area, Artikel, S.Artikel |
| `g-32-film-luxury` | 900 x 599 | Porto |

**Pemetaan foto ke CPT dan field.**

| Objek | Field foto | Sumber berkas |
|---|---|---|
| `layanan` | Featured image (kartu 900 px, tampil di `LI-LAYANAN`, Harga, Home) | `svc-*` yang sesuai layanan (Sandblast → `svc-sandblast`, One Way Vision → `svc-one-way`, Riben → `svc-riben`, Kaca Film → `svc-kaca-film`, Printing → `svc-printing`, Cutting → `svc-cutting`, Wrapping → `svc-wrapping`, Huruf Timbul 3D → `svc-huruf-timbul`, Neon Box → `svc-neon-box`) |
| `layanan` | ACF `hero_foto` (Image, hero 1920 px di Single Layanan) | `hero-sandblast.webp`; nilai awal sama untuk sembilan layanan, tiap layanan bisa diganti foto 1920 px lewat field yang sama |
| `area` | Featured image (kartu Area index) | `area-{kota}.webp` (Denpasar, Ubud, Seminyak, Canggu, Sanur, Nusa Dua, Kuta) |
| `area` | ACF `hero_gambar` (hero Single Area) dan `hero_fokus` (`--focus`) | Denpasar `hero-area-denpasar.webp` (`50% 60%`); enam area lain `hero-area.webp` (`50% 55%`); tiap area bisa diganti lewat field yang sama |
| `post` (artikel) | ACF `hero_gambar` (hero Single Artikel) | `hero-artikel-single.webp` (default) |
| `proyek` | Featured image (galeri) | `g-*`; caption "jenis · kawasan" di field `caption` |
| `post` (artikel) | Featured image kartu dan unggulan | Unggulan (sandblast vs one way vs kaca film) `g-02-glass-hallway`; Harga `g-05-shower-glass`; Kaca film `g-31-tint-installer`; Mengukur kaca `g-28-cafe-windows`; Persiapan `g-04-bathroom-frost`; Membersihkan `svc-riben`; Umur di Bali `area-nusa-dua`; Kafe `g-22-glass-lettering`. Hero: `hero-artikel` (index), `hero-artikel-single` (single). Kartu artikel di Home memakai tiga artikel terbaru dengan foto unggulan yang sama |
| `testimoni` | tanpa foto | Strip foto di halaman Testimoni memakai `villa-living`, `hotel-reception`, `clinic-reception`, `g-02-glass-hallway` |

**Foto konten dan simulasi before/after (CSS paste-ready, di bawah blok 2.10).** Foto dengan keterangan frosted memakai widget Image dengan kelas `sbb-photo` (+ rasio `sbb-ar-*`) dan Caption diaktifkan; foto tanpa keterangan cukup memakai kelas rasio. Simulasi efek sandblast dari satu foto memakai kelas `ba--simulate` pada slider (K6): kedua lapisan memakai foto yang sama, lapisan "Sesudah" diberi blur, dan keterangan "Ilustrasi efek sandblast" di bawah slider.

```css
/* FOTO KONTEN (2.11) */
.sbb-photo{position:relative;overflow:hidden;isolation:isolate;border-radius:14px;background:var(--sbb-gray-50)}
.sbb-photo img{display:block;width:100%;height:100%;object-fit:cover;object-position:var(--focus,50% 50%)}
.sbb-photo figcaption,.sbb-photo__cap{position:absolute;left:12px;bottom:12px;z-index:1;width:fit-content;max-width:calc(100% - 24px);margin:0;padding:8px 12px;border-radius:10px;font-size:14px;font-weight:600;line-height:1.35;color:var(--sbb-ink-900);background:rgba(255,255,255,.72);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.65);box-shadow:0 0 0 1px rgba(17,17,17,.07)}
@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){.sbb-photo figcaption,.sbb-photo__cap{background:rgba(255,255,255,.92)}}
.ba--simulate .ba-slider__layer--after img{filter:blur(5px) brightness(1.08) saturate(.85);transform:scale(1.04)}
.ba__note{display:flex;align-items:flex-start;justify-content:center;gap:8px;margin:12px 0 0;font-size:14px;line-height:1.5;color:var(--sbb-muted);text-align:center}
```

---

## 3. Theme Builder

Semua template: Layout Elementor Full Width, Header dan Footer global dari Theme Builder. Setelah tiap template dibuat, atur **Preview Settings** ke contoh konten (layanan Sticker Sandblast, area Denpasar, artikel contoh) agar dynamic tag terlihat di editor.

| Template | Tipe | Display Conditions | File detail |
|---|---|---|---|
| Header — Standar | Header | Include: Entire Site; Exclude: Front Page | 3.1 |
| Header — Home | Header | Include: Front Page | 3.1 |
| Footer | Footer | Include: Entire Site | 3.2 |
| Single — Artikel | Single Post | Include: Singular > Posts | `13-artikel-single.md` |
| Archive — Artikel | Archive | Include: Archive > Posts Archive | `12-artikel-index.md` |
| Archive — Artikel (Kategori) | Archive | Include: Archive > Categories | `12-artikel-index.md` |
| Error 404 | Error 404 | Otomatis | 3.5 |
| Popup | Popup | Tidak dibuat saat peluncuran | 3.6 |

### 3.1 Header (desktop + mobile, sticky)

Bangun satu Saved Container **`TPL-HEADER-BAR`** (bar header) lalu sisipkan dengan Template widget di kedua header, agar tidak ada dua sumber.

- **Header — Standar**: hanya `TPL-HEADER-BAR`.
- **Header — Home (Beranda)**: promo bar (container **Red 600**, padding 10/0, teks White 14 px lh 1,4, tiga item rata tengah Gap 2 / 24, wrap di mobile): "Buka setiap hari, 09.00–17.00" · "Ubung, Denpasar Utara" · "Survey lokasi gratis" (tiga Text/Heading terpisah; dibaca "Buka setiap hari, 09.00–17.00 · Ubung, Denpasar Utara · Survey lokasi gratis"), lalu `TPL-HEADER-BAR`. Promo bar **hanya di Beranda** dan ikut scroll (tidak sticky); yang sticky hanya bar header. Tautan di promo bar **White** bergaris bawah (`text-underline-offset: 3px`); focus ring di promo bar juga **White**. Hero foto dimulai tepat di bawah header sticky (header tidak transparan, tidak menimpa foto).

`TPL-HEADER-BAR` (kelas `sbb-header`, Boxed 1200, padding X 24/24/16, tinggi min 76 / 68 di mobile, Row Align Center Gap 12, latar White):

| Bagian | Widget dan setelan | Responsif / kode |
|---|---|---|
| Sticky | Advanced > Motion Effects > **Sticky: Top**, Offset 0, **Effects Offset 4 px**, semua device; z-index 50 | Garis bawah 1px Border muncul setelah scroll (kelas `elementor-sticky--effects`, CSS 2.8). Tanpa JS |
| Logo | Site Logo/Image: `logo.svg` (232x40, tampil tinggi 36 desktop / 34 lainnya), `alt` "Sticker Sandblast Bali, ke beranda", link `/`; margin kanan auto di ≤ 1024 | Logo terang untuk footer: `logo-light.svg` |
| Menu | **Nav Menu** (menu WP "Menu Utama"): Beranda · Tentang Kami · Layanan (submenu) · Portofolio (submenu) · Artikel · Kontak. Teks 15 px 500 Ink 900, tinggi 44, padding 0/10, gap 2. Hover: latar Gray 50 + teks Red 600. **Item aktif**: teks Red 600 600 + garis bawah 2px Red 600 (inset 10 px). Submenu terbuka **On Click** (juga bisa Enter/Spasi), tutup dengan Esc; indikator chevron 16 px berputar 180° saat terbuka | Rata tengah di ≥ 1025 (margin auto); di ≤ 1024 berubah menjadi hamburger |
| Submenu Layanan | 9 item menuju anchor `/layanan/#slug` + dua baris pemisah (garis atas 1px Border, memenuhi 2 kolom): 9 layanan dengan warna teks Red 600 600, lalu "Lihat semua layanan" (`/layanan/`) dan "Harga & estimasi" (`/layanan/#harga`). Urutan: Sticker Sandblast · Sticker One Way Vision · Sticker Riben · Kaca Film · Sticker Printing · Cutting Sticker · Wrapping & Branding Mobil · Huruf Timbul 3D · Neon Box & Papan Nama. Panel: latar White, border 1px Border, radius 14, bayangan `0 8px 30px rgba(17,17,17,.08)`, padding 8, lebar min 500, **2 kolom** | **Opsi A (disarankan)**: widget **Mega Menu** (Pro) dengan item "Layanan" berisi container Grid 2 kolom dari Button gaya teks. **Opsi B**: Nav Menu satu kolom lebar min 260 (11 item vertikal). Bila 2 kolom tetap diinginkan di Nav Menu, butuh CSS kustom (bagian 8.3) |
| Submenu Portofolio | "Galeri Foto" (`/portofolio/#foto`), "Galeri Video" (`/portofolio/#video`); panel lebar min 260 | Sama seperti di atas |
| CTA | Dua Button `BTN-WA` ukuran kecil (tinggi 44, padding 0/16, ikon WhatsApp 20 px): `.sbb-cta-long` "Chat WhatsApp" (tampil ≥ 1200) dan `.sbb-cta-short` "Chat" (< 1200), link `https://wa.me/6282226920230`, buka tab baru `rel="noopener"` | Tetap terlihat di semua ukuran |
| Hamburger | Toggle bawaan Nav Menu (atau Mega Menu) di ≤ 1024: tombol 44x44, border 1px Border, radius 10, ikon 24 px, `aria-label` "Buka menu" / "Tutup menu", `aria-expanded` sinkron | Panel dropdown penuh lebar di bawah header: latar putih, border atas/bawah 1px Border, padding 12 / gutter / 24, maks tinggi (100vh − tinggi header) dan scroll, item tinggi 48 px 17 px 500 dengan garis pemisah 1px Border; submenu berbentuk akordeon (Layanan, Portofolio), item submenu 16 px 400 tinggi 44. Kunci scroll body saat terbuka (CSS `html:has(.elementor-menu-toggle.elementor-active){overflow:hidden}`) |

Header QA: menu bisa dijelajahi dengan keyboard (Tab, Enter/Spasi membuka, Esc menutup dan fokus kembali ke pemicu); fokus tidak terjebak di panel mobile; item aktif sesuai halaman (di `/layanan/` menu "Layanan" aktif beserta baris "Lihat semua layanan"; Single Artikel: "Artikel"). Halaman yang tidak lagi ada item aktif sendiri: hanya konten di dalam halaman (testimoni, area, FAQ kini bagian dari halaman lain), sehingga tidak ada kondisi menu khusus untuk mereka.

### 3.2 Footer

Container Full Width latar Ink 900, teks Border; isi Boxed 1200, padding Y 64/56/48, X gutter.

| Blok | Isi persis mockup |
|---|---|
| Grid 4 kolom | Desktop 1,3fr / 0,8fr / 1fr / 1,2fr, Gap 48; tablet 2 kolom; mobile 1 kolom |
| Kolom 1 (brand) | Logo `logo-light.svg` (link `/`, alt "Sticker Sandblast Bali, ke beranda") · teks 15 px "Pemasangan sticker sandblast, one way vision, kaca film, dan cutting sticker untuk villa, hotel, restoran, kantor, dan toko di Bali." · ikon sosial (Instagram, Facebook, YouTube; 44x44, ikon 24; `aria-label` "Instagram Sticker Sandblast Bali", "Facebook Sticker Sandblast Bali", "YouTube Sticker Sandblast Bali"; tab baru `rel="noopener"`). URL: `https://www.instagram.com/stikersandblastbali`, `https://www.facebook.com/stikersandblastbali`, `https://www.youtube.com/@stikersandblastbali`. TikTok `https://www.tiktok.com/@stikersandblastbali` ditampilkan di Kontak (`14-kontak.md`) |
| Kolom 2 | Judul (H2 secara semantik, tampil 16 px 700 White) "Menu utama" + **Nav Menu** vertikal (menu WP "Footer — Menu utama"): Beranda · Tentang Kami · Layanan · Harga & estimasi · Portofolio · Galeri Video · Testimoni · Area layanan · FAQ · Artikel · Kontak. Tautan: `/`, `/tentang-kami/`, `/layanan/`, `/layanan/#harga`, `/portofolio/`, `/portofolio/#video`, `/tentang-kami/#testimoni`, `/tentang-kami/#area`, `/kontak/#faq`, `/artikel/`, `/kontak/` |
| Kolom 3 | Judul "Layanan" + 9 tautan ke anchor di `/layanan/`: **Nav Menu** vertikal dengan 9 item (atau Icon List) menuju `/layanan/#sticker-sandblast`, `#sticker-one-way-vision`, `#sticker-riben`, `#kaca-film`, `#sticker-printing`, `#cutting-sticker`, `#wrapping-branding-mobil`, `#huruf-timbul-3d`, `#neon-box-papan-nama` (Heading tautan 16 px Border). Daftar statis 9 item; tidak ada CPT yang perlu disinkronkan |
| Kolom 4 | Judul "Kontak" + Icon List (ikon 20 px Red 300, teks 15 px): WhatsApp 0822-2692-0230 (`wa.me/6282226920230`) · Telepon 0822-2692-0230 (`tel:+6282226920230`) · Email `info@stikersandblastbali.com` (`mailto:info@stikersandblastbali.com`, ikon surat) · Jl. Cokroaminoto Gg. Jempiring No. 15, Ubung, Kec. Denpasar Utara, Kota Denpasar, Bali 80111 · Senin–Minggu, 09.00–17.00 · "Buka di Google Maps" (`https://share.google/dNneYg3jdOXi641aj`, tab baru `rel="noopener"`) |
| Bar bawah | Garis atas 1px `rgba(255,255,255,.15)`, padding 24/0; kiri "© 2026 Sticker Sandblast Bali. Hak cipta dilindungi." (tahun via Dynamic Tag Current Date-Time format `Y`), kanan "Kebijakan privasi" (`/kebijakan-privasi/`, halaman harus ada sebelum tayang) |

Link footer: 15 px, hover White + garis bawah; tinggi target min 44 px; fokus Red 300.

### 3.3 Single Artikel

Struktur section, ACF, dan Query ID ada di `13-artikel-single.md`. Aturan bersama: H1 = Post Title, satu H1 per halaman; breadcrumb `TPL-BC`; `TPL-CTA` di akhir. Slug: `/artikel/{slug}/`.

Tidak ada lagi template Single Layanan, Single Area, atau Single Testimoni: ketiganya dihapus dan isinya menjadi bagian dari halaman statis (lihat bagian 4.1).

### 3.4 Archive Artikel

Lihat `12-artikel-index.md`: satu template blog index (satu artikel unggulan + 7 kartu "Baca juga") dan satu salinan untuk halaman kategori (tanpa unggulan). Loop Grid grid **Current Query**, 7 per halaman (unggulan dikeluarkan lewat snippet 6.3), pagination Numbers + Previous/Next.

### 3.5 Error 404

Copy: H1 "Halaman tidak ditemukan" · teks "Alamat yang Anda buka tidak ada atau sudah dipindahkan. Pilih layanan di bawah, atau kirim pesan lewat WhatsApp." · `BTN-PRI` "Ke beranda" + `BTN-WA` "Chat WhatsApp" · `CHIPS` 9 layanan menuju `/layanan/#slug`. Layout: `HERO-FOTO` varian `page` dengan `hero-kontak.webp` (fokus `50% 50%`), tanpa breadcrumb dan tanpa badge. Server harus mengirim status 404 (bukan 200).

### 3.6 Popup (opsional)

Mockup tidak punya popup. Peluncuran tanpa popup (popup menambah risiko CLS/INP dan tidak ada padanan desain). Bila kelak dipakai: satu popup "Minta penawaran cepat" dengan trigger **On Click** saja (bukan auto-open, bukan exit-intent), tombol tutup 44 px, fokus terjebak di dalam popup, kembali ke pemicu saat ditutup.

### 3.7 Tombol WhatsApp mengambang dan bar bawah mobile

Tempatkan di **Footer** (dua container di luar grid), keduanya `position: fixed` lewat kelas CSS 2.8:

- `.sbb-wa-float` (tampil ≥ 768): Button tanpa teks, ikon WhatsApp 30 px putih, latar WA Green, hover WA Green Hover + scale 1,06, 56x56 bulat, kanan 20 bawah 20, `aria-label` "Chat WhatsApp", link `wa.me/6282226920230` (tab baru, `rel="noopener"`).
- `.sbb-mobile-bar` (tampil ≤ 767): grid 2 kolom, Gap 8, padding 8/16 + safe-area, latar White, garis atas 1px Border; kiri `BTN-WA` "WhatsApp" (`wa.me/6282226920230`), kanan `BTN-SEC` "Telepon" (`tel:+6282226920230`), tinggi 48, `role="group"` `aria-label` "Hubungi kami". Body diberi padding bawah 68 px + safe-area (CSS 2.8) agar konten terakhir tidak tertutup.

Jangan menampilkan keduanya bersamaan. Klik keduanya dicatat sebagai event GA4 (bagian 7.4).

---

## 4. Content model

### 4.1 Statis vs CPT-driven (pernyataan eksplisit)

| Halaman / area | Sumber konten | Alasan |
|---|---|---|
| Beranda | **Statis** (Page) + Loop Grid dinamis untuk kartu proyek (`proyek`) dan artikel (`post`) | Copy hero/keunggulan/harga tetap; kartu berubah bersama CPT. Kartu layanan dan harga memakai data yang sama dengan `/layanan/`, jadi keduanya disalin dari satu sumber ACF Options (lihat catatan di bawah) |
| Tentang Kami, Layanan, Kontak | **Statis** (tidak ada CPT) | Isi per halaman sudah satu halaman penuh; loop tidak perlu mengiterasi sub-item |
| Portofolio | **CPT-driven** (`proyek`, Opsi A) atau Gallery statis (Opsi B/C) | Lihat `06-portofolio.md` |
| Artikel index, Single Artikel | **WordPress posts** (kategori bawaan) | Alur editorial biasa |
| Menu Header/Footer | **Menu WP manual** (Appearance > Menus) | Header butuh urutan dan submenu manual |

**Harga tanpa CPT `layanan`.** Karena tidak ada lagi post type per layanan, data harga disimpan di **ACF Options page** (satu entri, bukan sembilan): `harga_sandblast`, `harga_one_way`, `harga_riben`, `harga_kaca_film`, `harga_printing`, `harga_cutting`, `harga_wrapping`, `harga_huruf_timbul`, `harga_neon_box` (Number, rupiah; `harga_huruf_timbul` per huruf). Kartu harga di `/layanan/#harga` dan opsi kalkulator di `/layanan/#estimasi` membacanya lewat helper PHP (bagian 6.2). Kalau Options page belum dibuat, angka ditulis literal di kedua tempat — semuanya ada di satu halaman, jadi tidak ada duplikasi lintas halaman.

### 4.2 Post type dan taxonomy

| Nama | Slug / rewrite | Setelan | Catatan |
|---|---|---|---|
| CPT `proyek` | tanpa single publik (`publicly_queryable` **false**) | supports title, editor, thumbnail; `show_in_rest` true | Dikeluarkan dari sitemap dan pencarian; 32 foto `g-*` dari Media Library (2.11) |
| Taxonomy `kategori-layanan` | non-hierarchical, objek: `proyek` | 9 term = 9 layanan (slug sama dengan slug/anchor layanan) | Filter portofolio dan galeri per layanan |
| `post` | `/artikel/{slug}/` | Kategori: Panduan, Harga, Perawatan, Bahan | Field ACF `waktu_baca`, `ringkasan_singkat`, `hero_gambar` |

CPT `layanan`, `area`, dan `testimoni` **dihapus** (lihat 4.1). Karena itu `/layanan/{slug}/` dan `/area/{kota}/` tidak lagi ada sebagai URL; kontennya hidup di anchor halaman statis. Field group `layanan` dan `area` di bawah tidak lagi didaftarkan — angka harga pindah ke ACF Options page (4.1), dan field area/testimoni tidak perlu karena isinya sekarang statis di dalam halaman.

### 4.3 Field group (ringkas; detail di file halaman)

| Objek | Field |
|---|---|
| Data bisnis (ACF Options page) | `wa_link`, `telepon`, `alamat`, `jam`, `email`, `gbp_url`, `rating_skor`, `rating_jumlah`, `rating_tanggal`, `sosial_ig/tt/fb/yt`; dipakai lewat Dynamic Tag agar NAP diubah satu tempat. Tambahan: sembilan field harga layanan (`harga_sandblast` … `harga_neon_box`, lihat 4.1). File halaman menulis nilai literal bila Options page belum dibuat |

Field group `layanan` (`04b-layanan-fields.md`) dan `area` (`10-area-template.md`) **dihapus bersama CPT-nya**; isinya (harga, poin termasuk, faktor harga, pengerjaan, teks area) ditulis langsung di halaman statis `/layanan/` dan `/tentang-kami/`, dengan harga yang tetap dibaca dari Options page agar kartu harga dan kalkulator konsisten.

Nilai awal harga (sumber `mockup/DEMO-DATA.md`; dibaca kartu harga `/layanan/#harga` dan opsi kalkulator `/layanan/#estimasi`):

| Layanan | Satuan | Nilai | Tampil |
|---|---|---|---|
| Sticker Sandblast | m² | 135000 | Rp 135.000 / m² |
| Sticker One Way Vision | m² | 195000 | Rp 195.000 / m² |
| Sticker Riben | m² | 95000 | Rp 95.000 / m² |
| Kaca Film | m² | 165000 | Rp 165.000 / m² |
| Sticker Printing | m² | 175000 | Rp 175.000 / m² |
| Cutting Sticker | m² | 60000 | Rp 60.000 / m² |
| Wrapping & Branding Mobil | m² | 250000 | Rp 250.000 / m² |
| Huruf Timbul 3D | huruf | 35000 | Rp 35.000 / huruf |
| Neon Box & Papan Nama | m² | 950000 | Rp 950.000 / m² |

### 4.4 Cara Loop Grid mengonsumsi data

Setiap Loop Grid memakai Loop Item template (`LI-*`, bagian 5) dan, bila perlu, **Query ID** yang dihubungkan ke PHP di bagian 4.5. Aturan: Source = post type yang tepat; Order By Menu Order untuk layanan/area; **Nothing Found** wajib berisi pesan atau menyembunyikan section (section kosong dilarang).

| Query ID | Dipakai di | Perilaku |
|---|---|---|
| `sbb_artikel_unggulan` | Artikel index bagian 2 (`LI-ARTIKEL-UNGGULAN`) | Satu artikel sticky; grid "Baca juga" (Current Query, bagian 3) mengeluarkan artikel sticky lewat `pre_get_posts` (6.3) |
| `sbb_artikel_terkait` | Single Artikel bagian 4 ("Artikel terkait", `LI-ARTIKEL-TERKAIT`) | `post__in` dari field `artikel_terkait` (3 artikel, urutan sesuai isian) — bukan dari ACF relationship, karena tidak ada CPT `layanan` lagi; field `artikel_terkait` pada `post` tetap dipakai |
| `sbb_proyek_by_layanan` | Portofolio bagian 2 (filter kategori) | `proyek` dengan term `kategori-layanan` yang dipilih; tanpa Query ID bila filter memakai taxonomy bawaan Gallery |
| Pagination Current Query | Portofolio bagian 3 ("Muat lebih banyak") | Query `proyek` dengan halaman berikutnya (12 per halaman); cukup tombol yang mengganti offset query, tanpa Query ID khusus |
Query ID yang dihapus bersama CPT-nya: `sbb_acf_layanan_terkait`, `sbb_acf_area_terkait`, `sbb_acf_layanan_populer`, `sbb_acf_area_tetangga`, `sbb_acf_layanan_dibahas`, `sbb_testimoni_google`, `sbb_proyek_by_area`, `sbb_layanan_berharga` (digantikan pembacaan Options page). Kode PHPnya boleh dibiarkan di child theme (tidak terpakai, tidak merusak), tapi tidak perlu memanggilnya.

### 4.5 PHP Query ID (child theme `functions.php` atau Code Snippets)

```php
function sbb_query_from_acf( $q, $field, $limit ) {
	$ids = function_exists( 'get_field' ) ? get_field( $field, get_queried_object_id(), false ) : array();
	$ids = array_values( array_filter( array_map( 'absint', (array) $ids ) ) );
	$q->set( 'post__in', $ids ? $ids : array( 0 ) );
	$q->set( 'orderby', 'post__in' );
	$q->set( 'posts_per_page', $limit );
	$q->set( 'ignore_sticky_posts', true );
}
foreach ( array(
	// Hanya query yang masih dipakai (CPT `layanan` dan `area` sudah dihapus; lihat 4.1)
	'sbb_artikel_terkait'     => array( 'artikel_terkait', 3 ),
) as $qid => $cfg ) {
	add_action( "elementor/query/{$qid}", function ( $q ) use ( $cfg ) { sbb_query_from_acf( $q, $cfg[0], $cfg[1] ); } );
}
add_action( 'elementor/query/sbb_proyek_by_layanan', function ( $q ) {
	$t  = function_exists( 'get_field' ) ? get_field( 'kategori_proyek', get_queried_object_id() ) : 0;
	$id = is_object( $t ) ? (int) $t->term_id : absint( $t );
	if ( ! $id ) { $q->set( 'post__in', array( 0 ) ); return; }
	$q->set( 'tax_query', array( array( 'taxonomy' => 'kategori-layanan', 'field' => 'term_id', 'terms' => array( $id ) ) ) );
} );
add_action( 'elementor/query/sbb_proyek_by_area', function ( $q ) {
	$q->set( 'meta_query', array( array( 'key' => 'area_terkait', 'value' => '"' . get_queried_object_id() . '"', 'compare' => 'LIKE' ) ) );
} );
add_action( 'elementor/query/sbb_layanan_berharga', function ( $q ) {
	$q->set( 'meta_query', array(
		'relation' => 'OR',
		array( 'key' => 'harga_per_m2', 'value' => 0, 'type' => 'NUMERIC', 'compare' => '>' ),
		array( 'key' => 'harga_per_huruf', 'value' => 0, 'type' => 'NUMERIC', 'compare' => '>' ),
	) );
} );
```

Query ID `sbb_testimoni_google` (Home) memfilter `testimoni` menurut field `sumber`:

```php
add_action( 'elementor/query/sbb_testimoni_google', function ( $q ) {
	$q->set( 'meta_query', array( array( 'key' => 'sumber', 'value' => 'Ulasan Google' ) ) );
	$q->set( 'orderby', 'menu_order' );
	$q->set( 'order', 'ASC' );
	$q->set( 'posts_per_page', 3 );
} );
```

Query ID `sbb_artikel_unggulan` dan pengecualian artikel unggulan di grid ada di 6.3. Nama field ACF harus sama persis dengan tabel 4.3. Loop Grid tetap memakai Source = post type yang benar; di editor Elementor hasil kosong sampai Preview Settings dipilih.

---

## 5. Global widgets dan saved templates

Buat di Templates > Saved Templates (tipe Container/Section) sebelum membangun halaman. Bila fitur Global Widget tersedia di versi Anda, jadikan `BTN-*` Global Widget; bila tidak, salin dari Saved Template. Ubah sekali di template, berlaku di semua halaman yang memakai Template widget.

### 5.1 Saved templates

| Kode | Dipakai di | Isi |
|---|---|---|
| `TPL-HEADER-BAR` | Header — Standar, Header — Beranda | Bagian 3.1 |
| `TPL-BC` | Semua halaman kecuali Beranda | Bagian 2.9 |
| `TPL-CTA` | Semua halaman (varian); Beranda memakainya di section terakhir | Bagian 2.9 (teks persis mockup) |
| `TPL-CTA-DATANG` | Tentang Kami | Salinan `TPL-CTA`, teks diganti (lihat `02-tentang-kami.md` bagian 7) |
| `TPL-POST-CTA` | Isi Single Artikel (shortcode `[elementor-template id="…"]`) | Kotak CTA tengah, Ink 900, radius 14, padding 32/20 (`13-artikel-single.md`) |
| `TPL-STEPS` | Beranda, Layanan | Tiga langkah proses (Konsultasi → Ukur dan penawaran → Pemasangan) sesuai file halaman |
| `TPL-VALUE-4` | Tentang Kami | Empat `CARD-VAL` |
| `TPL-FAKTOR` | Layanan (`#harga`) | Daftar faktor harga bergaris |
| `TPL-AREA-CHIPS` | Tentang Kami (`#area`), Kontak | Tujuh chip kota + `LINK-ARROW` menuju `/tentang-kami/#area` |
| `BTN-PRI`, `BTN-WA`, `BTN-SEC`, `BTN-SEC-L`, `LINK-ARROW` | Semua | Bagian 2.3 |

`TPL-STATS` **dihapus**: blok "Rekam jejak dalam angka" dihapus dari Beranda dan Tentang Kami, tidak ada lagi halaman yang memakainya. `TPL-VALUE-4` tetap (dipakai di Tentang Kami). Kartu layanan dan kartu harga di Beranda/Layanan tidak lagi memakai Loop Item CPT; keduanya disusun manual di halaman statis dengan harga dari Options page (lihat 4.1 dan `03-layanan-index.md`).

### 5.2 Loop Item templates (Templates > Loop Item; semua kartu `sbb-card` + kelas `sbb-reveal`)

| Kode | Tata letak | Sumber data |
|---|---|---|
| `LI-PROYEK` | Image rasio asli foto (tanpa crop; Loop Grid **Masonry** On, 3 kolom ≥ 1025, 2 kolom ≥ 480, 1 kolom di bawahnya; link Media File, Lightbox On, ikon zoom saat hover) + caption 15 px `{caption}` (format "jenis · kawasan", mis. "Sandblast pintu kaca · Canggu") | CPT `proyek` |
| `LI-ARTIKEL` | `sbb-card-post`: Image 16:9 (hover zoom 1,03), kategori 14 px 700 uppercase Red 600, H3 19 px (tautan `sbb-stretch`), excerpt 15 px Text Muted, meta 14 px (tanggal, `waktu_baca`) | `post` |
| `LI-ARTIKEL-UNGGULAN` | Container Grid 2 kolom (1fr / 0,9fr ≥ 1025; gambar min-height 380), H2 judul, excerpt 17 px | `post` (pilihan manual) |
| `LI-VIDEO` | Poster 16:9 + ikon play + durasi; klik membuka lightbox Video Elementor | Video (YouTube), tanpa CPT |

`LI-TESTI` **dihapus** bersama CPT `testimoni`: enam kartu testimoni di `/tentang-kami/#testimoni` ditulis manual sebagai container `sbb-card-quote` (kutipan, label sumber, avatar lingkaran berisi inisial, nama, keterangan) — lihat `02-tentang-kami.md` bagian 2 section 5. Kutipan Google, ejaan asli, dan urutan enam entri diatur di halaman itu. |

Loop Item `LI-LAYANAN` yang berbau CPT `layanan` (`LI-LAYANAN`, `LI-LAYANAN-HARGA`, `LI-HARGA`, `LI-HARGA-BARIS`, `LI-TESTI`, `LI-LINK`) **dihapus**: kartu layanan, kartu harga, dan testimoni sekarang statis di dalam halaman. `LI-TESTI` masih berguna bila testimoni kembali menjadi CPT, tetapi saat ini ditulis manual di `/tentang-kami/#testimoni`.

Klik penuh: container Link = Post URL bila kartu tidak memuat tautan lain; jika ada tautan di dalam, pakai stretched link (H3 bertautan dengan kelas `sbb-stretch` pada widget Heading; container `position: relative`). Fokus terlihat 2px Red 600 offset 2 pada kartu.

---

## 6. Daftar custom code

Prinsip: pakai widget native sebisa mungkin; kode hanya untuk yang tidak punya padanan native. Tabel memuat **semua** kode dari mockup dan nasibnya. "Sumber" = file di `mockup/assets/` (baris untuk membantu menyalin). Halaman yang **selalu** butuh CSS/JS kustom: Beranda (peta, reveal), Layanan (before/after di blok sandblast + estimator), Kontak (bila Opsi B); halaman lain hanya Kit CSS + reveal.

| ID | Tujuan | Lokasi pasang | Sumber mockup | Widget native menggantikan? |
|---|---|---|---|---|
| K1 | Token, focus ring, frost, latar, kartu, tabel, artikel, mobile bar, WA float, hero foto (2.10), foto konten (2.11) | Site Settings > Custom CSS | `css/styles.css` (bagian 0-5, hero foto di 5.20 baris 1524-1718) | Sebagian: warna/tipografi/tombol sudah native; sisanya CSS 2.8, 2.10, dan 2.11 |
| K2 | Sprite ikon SVG (`<use href="#i-…">`) | Custom Code (Pro) > Location Body - Start, Entire Site | `src/partials/header.html` baris 2-48 | Ya, bila semua ikon memakai widget Icon/SVG; dibutuhkan bila HTML widget/shortcode mockup dipakai (K6, K7, K11) |
| K3 | Reveal: flag `html.sbb-js` + IntersectionObserver + stagger | Custom Code: Head dan Body - End | `js/app.js` modul `reveal` (492-514) | Sebagian: Entrance Animation "Fade In Up" (Advanced > Motion Effects), tanpa stagger 70 ms |
| K4 | Query ID (bagian 4.5) dan artikel unggulan (6.3) | Child theme `functions.php` / Code Snippets | (baru, tidak ada di mockup) | Tidak |
| K5 | `[sbb_rupiah]`, `[sbb_estimator]` (harga dari ACF Options page) | Sama dengan K4 | (baru; markup dari `mockup/src/pages/layanan.html`) | `[sbb_rupiah]`: Dynamic Tag ACF (Before "Rp ", After " / m²") hanya cukup untuk layanan per m²; Huruf Timbul 3D ("/ huruf") dan `harga_label` butuh shortcode |
| K6 | Before/after slider (blok `#sticker-sandblast` di Layanan), termasuk simulasi satu foto `ba--simulate` | CSS: Custom CSS halaman/Kit; JS: Custom Code Body - End (hanya halaman berslider) | `css/styles.css` 834-929 (bagian 5.08, memuat `.ba--simulate` dan `.ba__note`; + aturan `.icon`, bagian 4); `js/app.js` modul `slider` (268-325) | **Tidak ada** widget before/after native di Elementor Pro. Tanpa kode: dua gambar bersebelahan "Sebelum" / "Sesudah" |
| K7 | Estimator harga (delapan layanan per m² + Huruf Timbul 3D per huruf), di `/layanan/#estimasi` | CSS: `css/pages-b.css` 108-183; JS: `js/pages-b.js` 25-34 dan 36-168; markup dari `[sbb_estimator]` (6.2) | `src/pages/layanan.html` bagian `#estimasi` | **Tidak ada** kalkulator native. Tanpa kode: hapus section, tampilkan rumus "luas × harga per m²" dan tautan WhatsApp |
| K8 | "Muat lebih banyak" portofolio | (tidak perlu) | `js/pages-b.js` 169-228; `css/pages-b.css` 215-223 | **Ya**: Loop Grid > Pagination "Load on Click" |
| K9 | Filter galeri + lightbox | (tidak perlu untuk Opsi A) | `js/app.js` modul `gallery` (326-491); `css/styles.css` 930-1043 | **Ya**: Loop Grid + Taxonomy Filter (Pro), lightbox Elementor. Teks status "Menampilkan N dari M" butuh JS kecil (opsional, `06-portofolio.md`) |
| K10 | Modal video | (tidak perlu) | `js/pages-b.js` 229-312; `css/pages-b.css` 227-333 | **Ya**: Video widget dengan Lightbox |
| K11 | Accordion FAQ (satu terbuka, panah/Home/End) | (tidak perlu untuk Nested Accordion) | `js/app.js` modul `accordion` (223-267); `css/styles.css` 1074-1131 | **Ya**: Nested Accordion (Max Items Expanded 1) |
| K12 | Filter kategori FAQ + status (di `/kontak/#faq`) | Halaman Kontak saja | `js/pages-c.js` 18-67; `css/pages-c.css` 60-75; `css/styles.css` 933-955 | Sebagian: Nested Tabs (tanpa tampilan "Semua") |
| K13 | Daftar isi artikel + highlight | (tidak perlu) | `js/pages-c.js` 68-104; `css/pages-c.css` 117-165 | **Ya**: Table of Contents (Pro) |
| K14 | Formulir penawaran (validasi, unggah foto, sukses) | Hanya Opsi B `14-kontak.md` | `js/pages-c.js` 105-240; `css/pages-c.css` 166-203; `css/styles.css` 1196-1260 | **Ya (Opsi A)**: Form widget; batasan unggah/format pesan WA ada di `14-kontak.md` |
| K15 | Header sticky, dropdown, menu mobile | (tidak perlu) | `js/app.js` modul `header` (62-222); `css/styles.css` 412-577 | **Ya**: Nav Menu/Mega Menu + Sticky |
| K16 | Binding validasi form umum | (tidak perlu) | `js/app.js` modul `forms` (515-533) | **Ya**: validasi Form widget |
| K17 | Prioritas muat gambar hero (`fetchpriority="high"`, tanpa lazy) | Child theme `functions.php` / Code Snippets (snippet di 2.10) | (baru; padanan atribut `fetchpriority="high"` pada `img.hero-photo__img` di semua halaman) | Sebagian: opsi lazy-load/prioritas di plugin cache; snippet memastikan atributnya ada di markup, apa pun plugin yang aktif |
| K18 | Peta area Home (SVG ilustrasi) | HTML widget di Home | `src/pages/index.html` blok `.area-map` | Tidak ada widget peta ilustrasi; CSS `.area-map*` sudah di 2.8 |
| K19 | JSON-LD (bagian 7) | Custom Code Head / plugin SEO | (baru) | Sebagian: plugin SEO menghasilkan WebSite, BreadcrumbList, BlogPosting |
| K20 | Event GA4 (bagian 7.4) | Custom Code Body - End | (baru) | Sebagian: GTM |
| K21 | Dropdown Layanan 2 kolom di Nav Menu | Kit CSS (8.3) | `css/styles.css` 567-570 | **Ya**: Mega Menu |

Aturan pasang: satu Custom Code per ID di Elementor > Custom Code (mudah dinonaktifkan), lokasi dan kondisi tampil dicatat di judulnya; JS di-defer, tanpa library; tidak ada script di editor (`elementor-editor-active` dicek). Setelah menyalin JS dari mockup, ganti `SBB.on/emit/refresh` dengan fungsi lokal dan bungkus dalam IIFE.

### 6.1 Reveal (K3), paste-ready

Head (mencegah kedipan; tidak aktif di editor, preview, atau bila gerak dikurangi):

```html
<script>(function(){var d=document.documentElement;if(/elementor-preview/.test(location.search)||!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion: reduce)').matches)return;d.classList.add('sbb-js')})();</script>
```

Body - End:

```html
<script>document.addEventListener('DOMContentLoaded',function(){var r=document.documentElement;if(!r.classList.contains('sbb-js'))return;
document.querySelectorAll('.sbb-stagger').forEach(function(g){var n=0;[].slice.call(g.querySelectorAll(':scope > .sbb-reveal')).forEach(function(c){c.style.setProperty('--sbb-i',Math.min(n++,5))})});
var els=[].slice.call(document.querySelectorAll('.sbb-reveal'));var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-visible');io.unobserve(e.target)}})},{rootMargin:'0px 0px -6% 0px',threshold:.06});els.forEach(function(el){io.observe(el)});});</script>
```

Kelas: `sbb-reveal` pada elemen yang muncul; `sbb-stagger` pada induknya (Loop Grid: kelas `sbb-reveal` di Loop Item). Tanpa JS konten tetap terlihat (CSS hanya menyembunyikan bila `html.sbb-js`).

### 6.2 Helper PHP (K5): `[sbb_rupiah]`, `[sbb_estimator]`

Harga dibaca dari **ACF Options page**, bukan dari CPT `layanan` (CPT-nya dihapus; lihat 4.1). Sembilan layanan memakai daftar tetap berikut supaya urutannya sama dengan mockup.

```php
function sbb_rp( $n ) { return 'Rp ' . number_format( (int) $n, 0, ',', '.' ); }

// Kunci Options page per layanan, urutan tampilan sama dengan mockup.
// 'huruf' = harga per huruf (bukan per m²).
function sbb_layanan_harga_daftar() {
	return array(
		array( 'kunci' => 'harga_sandblast',     'nama' => 'Sticker Sandblast',        'satuan' => 'm²' ),
		array( 'kunci' => 'harga_one_way',       'nama' => 'Sticker One Way Vision',   'satuan' => 'm²' ),
		array( 'kunci' => 'harga_riben',         'nama' => 'Sticker Riben',            'satuan' => 'm²' ),
		array( 'kunci' => 'harga_kaca_film',     'nama' => 'Kaca Film',                'satuan' => 'm²' ),
		array( 'kunci' => 'harga_printing',      'nama' => 'Sticker Printing',         'satuan' => 'm²' ),
		array( 'kunci' => 'harga_cutting',       'nama' => 'Cutting Sticker',          'satuan' => 'm²' ),
		array( 'kunci' => 'harga_wrapping',      'nama' => 'Wrapping &amp; Branding Mobil', 'satuan' => 'm²' ),
		array( 'kunci' => 'harga_neon_box',      'nama' => 'Neon Box &amp; Papan Nama',    'satuan' => 'm²' ),
		array( 'kunci' => 'harga_huruf_timbul',  'nama' => 'Huruf Timbul 3D',          'satuan' => 'huruf' ),
	);
}

function sbb_harga( $kunci ) { // 0 = belum diisi
	if ( ! function_exists( 'get_field' ) ) { return 0; }
	return (int) get_field( $kunci, 'options' );
}

add_shortcode( 'sbb_rupiah', function ( $atts ) { // "Rp 135.000 / m²" atau "Rp 35.000 / huruf"
	$kunci = ! empty( $atts['kunci'] ) ? sanitize_key( $atts['kunci'] ) : 'harga_sandblast';
	$s     = ! empty( $atts['satuan'] ) ? ( 'huruf' === $atts['satuan'] ? 'huruf' : 'm²' ) : 'm²';
	$l     = function_exists( 'get_field' ) ? trim( (string) get_field( 'harga_label_' . $kunci, 'options' ) ) : '';
	if ( '' !== $l ) { return esc_html( $l ); }
	$p = sbb_harga( $kunci );
	return $p > 0 ? esc_html( sbb_rp( $p ) . ' / ' . $s ) : esc_html( 'Harga setelah survey' );
} );

add_shortcode( 'sbb_estimator', function () { // markup persis mockup src/pages/layanan.html bagian #estimasi
	$per_m2 = '';
	$per_hr = ''; // layanan per huruf (Huruf Timbul 3D) ditaruh paling akhir, seperti di mockup
	foreach ( sbb_layanan_harga_daftar() as $l ) {
		$hp    = sbb_harga( $l['kunci'] );
		$huruf = 'huruf' === $l['satuan'];
		$attr  = $hp > 0 ? ( $huruf ? ' data-unit="huruf" data-unit-price="' . $hp . '"' : ' data-price="' . $hp . '"' ) : '';
		$row   = sprintf( '<option value="%s" data-name="%s"%s>%s (%s)</option>', esc_attr( $l['kunci'] ), esc_attr( $l['nama'] ), $attr,
			esc_html( $l['nama'] ), $hp > 0 ? 'mulai ' . esc_html( sbb_rp( $hp ) ) . ' / ' . ( $huruf ? 'huruf' : 'm²' ) : 'harga setelah survey' );
		if ( $huruf ) { $per_hr .= $row; } else { $per_m2 .= $row; }
	}
	$opts = preg_replace( '/<option /', '<option selected ', $per_m2 . $per_hr, 1 ); // opsi pertama (Sticker Sandblast) terpilih
	ob_start(); ?>
	<div class="sbb-frost estimator"><h3 class="estimator__title" id="est-title">Estimasi harga awal</h3>
	<form class="estimator__form" action="#" data-estimator novalidate aria-labelledby="est-title"><div class="estimator__fields">
	<div class="field"><label class="field__label" for="est-area">Luas (m²)</label><input class="field__input" id="est-area" name="luas" type="number" inputmode="decimal" min="0.1" step="0.1" placeholder="Contoh: 2,5" autocomplete="off" aria-describedby="est-area-hint est-area-error" data-est-area><span class="field__hint" id="est-area-hint">Minimal 0,1 m². Tidak dipakai untuk Huruf Timbul 3D.</span></div>
	<div class="field"><label class="field__label" for="est-service">Jenis layanan</label><select class="field__select" id="est-service" name="layanan" data-est-service><?php echo $opts; // phpcs:ignore ?></select></div></div>
	<p class="estimator__error" id="est-area-error" data-est-error hidden><span data-est-error-text></span></p>
	<div><button class="btn btn--primary" type="submit">Hitung estimasi</button></div></form>
	<div class="estimator__out"><div class="estimator__live" id="est-output" role="status" aria-live="polite" aria-atomic="true"><p class="estimator__label" data-est-label>Estimasi mulai dari</p><p class="estimator__amount" data-est-amount>Rp —</p><p class="estimator__detail" data-est-detail>Isi luas dan pilih layanan untuk melihat estimasi.</p></div>
	<p class="estimator__note"><span>Estimasi awal. Harga final ditentukan setelah survey/ukur lokasi.</span></p>
	<a class="btn btn--wa btn--block" href="https://wa.me/6282226920230" data-wa-base="https://wa.me/6282226920230" data-est-wa target="_blank" rel="noopener">Kirim estimasi lewat WhatsApp</a>
	<noscript><p class="estimator__noscript">Kalkulator memerlukan JavaScript. Kalikan luas (m²) dengan harga per m² pada kartu harga di atas.</p></noscript></div></div>
	<?php return ob_get_clean();
} );
```

Perilaku estimator (JS K7, `pages-b.js` fungsi `initEstimator`): delapan layanan per m² menghitung luas × harga per m² (mis. 2,5 m² × Rp 135.000 = Rp 337.500) dan mengisi pesan WhatsApp dengan layanan, luas, dan estimasi; Huruf Timbul 3D (opsi ber-`data-unit="huruf"`) mengabaikan luas dan menampilkan "Rp 35.000 / huruf" dengan kalimat "Huruf Timbul 3D dihitung per huruf setelah desain disepakati (mulai Rp 35.000 / huruf), bukan per m². Kirim desain atau tulisan yang diinginkan lewat WhatsApp." Angka tampil dengan format `id-ID` (titik ribuan, koma desimal). Tidak ada pengali atau kisaran tambahan.

Helper `[sbb_ba]` (before/after) dan `[sbb_area_teks]` **dihapus**: keduanya membaca ACF pada CPT `layanan` / `area` yang sudah tidak ada. Slider before/after kini hanya muncul satu kali di blok `#sticker-sandblast` pada halaman `/layanan/`, dan gambarnya bisa berupa field di Page itu sendiri — pakai dua Image widget dengan kelas `ba--simulate` (K6) tanpa shortcode. Teks lokal per kawasan di `/tentang-kami/#area` ditulis langsung di halaman.

### 6.3 Artikel unggulan dan grid "Baca juga" (Artikel index)

Artikel unggulan = satu artikel yang ditandai "Stick this post to the front page". Loop Grid unggulan memakai Query ID `sbb_artikel_unggulan`; grid "Baca juga" memakai Current Query dan tidak memuat artikel sticky (`12-artikel-index.md` bagian 3). Code Snippets atau child theme:

```php
add_filter( 'elementor/query/sbb_artikel_unggulan', function ( $q ) {
	$q->set( 'post__in', array_slice( (array) get_option( 'sticky_posts' ), 0, 1 ) );
	$q->set( 'posts_per_page', 1 );
	$q->set( 'ignore_sticky_posts', 1 );
} );
add_action( 'pre_get_posts', function ( $q ) { // grid tidak memuat unggulan
	if ( is_admin() || ! $q->is_main_query() || ! $q->is_home() ) { return; }
	$q->set( 'ignore_sticky_posts', 1 );
	$q->set( 'post__not_in', (array) get_option( 'sticky_posts' ) );
} );
```

Settings > Reading > Posts per page = 7 harus sama dengan Posts Per Page Loop Grid "Baca juga" (7) agar jumlah halaman pagination konsisten. Halaman kategori artikel tidak memuat section unggulan.

---

## 7. SEO dan schema

### 7.1 Setelan plugin SEO

- Title dan meta description ditulis **per halaman** sesuai blok SEO di tiap file (title ≤ 60, meta ≤ 155); matikan akhiran otomatis nama situs agar tidak melebihi 60.
- Canonical: self-canonical semua halaman; halaman 2+ arsip artikel self-canonical; `noindex` untuk hasil pencarian, 404, dan tag. Jangan `noindex` kategori artikel.
- Sitemap XML: sertakan Pages, `layanan`, `area`, Posts, kategori artikel; **kecualikan** `proyek`, `testimoni`, `faq`, tag, pengarsipan penulis. Kirim ke Google Search Console setelah tayang.
- Breadcrumb: aktifkan breadcrumb plugin (label Home "Beranda", pemisah ">"), yang juga menghasilkan `BreadcrumbList`; judul pendek per halaman lewat kolom "Breadcrumbs title".
- Open Graph/Twitter: gambar default 1200x630 yang dipotong dari `hero-home.webp` (fokus 50% 55%); tiap halaman memakai hero-nya sendiri (`hero-*.webp`, tabel 2.11) dipotong 1200x630, dan artikel memakai foto unggulannya.
- Robots.txt: izinkan crawl; tidak memblokir CSS/JS Elementor.
- Hanya **satu** sumber schema: bila plugin SEO memakai skema Organization/LocalBusiness sendiri, matikan supaya tidak ada dua `LocalBusiness`.

### 7.2 LocalBusiness JSON-LD (Home; ref `@id` di Kontak dan Layanan)

Tempel di Custom Code > Head, Display Condition: Front Page. **Tanpa `AggregateRating`, tanpa `Review`, tanpa `geo`.** Nilai `image` adalah URL berkas `hero-home.webp` di Media Library (sesuaikan folder unggahan bulan berjalan).

```html
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"LocalBusiness","@id":"https://stikersandblastbali.com/#localbusiness",
"name":"Sticker Sandblast Bali","url":"https://stikersandblastbali.com/","telephone":"+6282226920230","email":"info@stikersandblastbali.com","priceRange":"$$",
"image":"https://stikersandblastbali.com/wp-content/uploads/2026/09/hero-home.webp",
"address":{"@type":"PostalAddress","streetAddress":"Jl. Cokroaminoto Gg. Jempiring No. 15, Ubung","addressLocality":"Denpasar","addressRegion":"Bali","postalCode":"80111","addressCountry":"ID"},
"openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"09:00","closes":"17:00"}],
"areaServed":[{"@type":"City","name":"Denpasar"},{"@type":"City","name":"Ubud"},{"@type":"City","name":"Seminyak"},{"@type":"City","name":"Canggu"},{"@type":"City","name":"Sanur"},{"@type":"City","name":"Nusa Dua"},{"@type":"City","name":"Kuta"}],
"hasMap":"https://www.google.com/maps?q=Jl.+Cokroaminoto+Gg.+Jempiring+No.+15,+Ubung,+Denpasar+Utara,+Bali","sameAs":["https://www.instagram.com/stikersandblastbali","https://www.tiktok.com/@stikersandblastbali","https://www.facebook.com/stikersandblastbali","https://www.youtube.com/@stikersandblastbali"]}
</script>
```

`priceRange` memakai "$$" (nilai skala harga yang valid untuk schema; rentang rupiah per m² tidak dituliskan di sini). `geo` tidak dipasang. Bagian `WebSite` (`name`, `url`) dan `BreadcrumbList` dari plugin SEO.

### 7.3 Schema per halaman

| Halaman | Schema | File |
|---|---|---|
| Home | `LocalBusiness` (7.2), `WebSite` | `01-home.md` |
| Layanan (9, satu halaman `/layanan/`) | `Service` (provider = `@id` LocalBusiness) **satu per blok beranchor** — bukan sembilan URL. `ItemList` berisi sembilan `Service` dengan `name`, `description`, `url` = `https://stikersandblastbali.com/layanan/#slug`. `offers` = `Offer` dengan `priceSpecification` `minPrice` dari field Options page (bagian 4.1): delapan layanan per m² (`unitCode` "MTK") dan Huruf Timbul 3D per huruf (`unitText` "huruf"). Tanpa data harga karangan atau rating | `03-layanan-index.md` |
| Area (7, di `/tentang-kami/#area`) | `areaServed` pada `@id` LocalBusiness di Beranda; jangan menggandakan alamat sebagai cabang | `02-tentang-kami.md` |
| Portofolio | `ImageGallery` + `ImageObject` (`contentUrl`, `caption` = "jenis · kawasan") untuk foto galeri | `06-portofolio.md` |
| Galeri video (di `/portofolio/#video`) | **Tanpa** `VideoObject`: halaman menampilkan poster dan tautan YouTube, bukan pemutar tersemat | `06-portofolio.md` |
| Testimoni (di `/tentang-kami/#testimoni`) | **Tidak ada** `Review`/`AggregateRating` (self-serving); skor 4,9 / 57 hanya teks | `02-tentang-kami.md` |
| Artikel | `BlogPosting` + `BreadcrumbList` | `13-artikel-single.md` |
| FAQ (di `/kontak/#faq`) | `FAQPage` untuk 18 pertanyaan + filter kategori | `14-kontak.md` |
| Kontak | `ContactPage` + rujukan LocalBusiness | `14-kontak.md` |
| Lainnya | `BreadcrumbList` saja | file masing-masing |

### 7.4 Event GA4 (Custom Code, Body - End)

Prasyarat: GA4 terpasang lewat Site Kit atau GTM sehingga fungsi `gtag` tersedia.

```html
<script>document.addEventListener('click',function(e){var a=e.target.closest('a[href]');if(!a||typeof gtag!=='function')return;var h=a.getAttribute('href')||'';
var t=h.indexOf('wa.me/')>-1?'whatsapp_click':(h.indexOf('tel:')===0?'phone_click':'');if(t)gtag('event',t,{link_url:h,page_path:location.pathname});});
window.addEventListener('load',function(){if(window.jQuery){jQuery(document).on('submit_success','.elementor-form',function(){if(typeof gtag==='function')gtag('event','generate_lead',{form_name:'minta_penawaran'});});}});</script>
```

---

## 8. Checklist, fallback, dan pra-luncur

### 8.1 Checklist performa (target seluler: LCP ≤ 2,5 dtk, INP ≤ 200 ms, CLS ≤ 0,1)

- [ ] Hero foto (2.10): **satu** `<img>` WebP 1920 px (`hero-*.webp`) dengan `width`/`height`, `loading` eager, `fetchpriority="high"` (K17), `srcset` aktif; bukan slider dan bukan background-image; kelas plugin cache mengecualikan `sbb-hero-photo__img` dari lazy-load
- [ ] Hero seluler: teks selalu di atas alfa overlay ≥ .72 (bukan di zona atas .12); tinggi Home `clamp(640px, 100svh − 76px, 860px)` tanpa scroll horizontal; CLS hero 0 karena tinggi ditentukan Min Height dan foto absolut
- [ ] Gambar lain: lazy-load, `srcset` dari Elementor (Image Size dan `sizes` per kelompok di 2.11), rasio ditetapkan lewat kelas `sbb-ar-*` (galeri: rasio asli) sehingga tidak menggeser layout (CLS)
- [ ] Font: hanya Plus Jakarta Sans 700/800 dan DM Sans 400/500/600, dihosting lokal, `font-display: swap`; preload dua berkas yang dipakai di atas lipatan (mis. DM Sans 400, Plus Jakarta 800)
- [ ] Elementor > Settings > Performance/Features: aktifkan opsi optimasi markup/DOM, pemuatan aset yang ditingkatkan (Improved Asset Loading), lazy-load background bila tersedia; nonaktifkan Font Awesome dan eicons yang tidak dipakai
- [ ] Satu container per `SEC` (tanpa pembungkus ganda); kedalaman DOM tidak berlebihan; tidak ada add-on Elementor pihak ketiga
- [ ] Video YouTube: Video widget dengan **lazy load** (gambar pratinjau), bukan iframe langsung; embed Google Maps `loading="lazy"`
- [ ] Reveal hanya `opacity`/`transform`; tidak ada animasi yang memicu layout; gerak mati saat `prefers-reduced-motion`
- [ ] Script pihak ketiga (GA4) dimuat asinkron; JS kustom di bagian 6 ringan dan hanya di halaman yang membutuhkan (K6, K7)
- [ ] Cache halaman + minify CSS/JS diuji (jangan menggabungkan yang merusak Elementor); hapus emoji/wp-embed/dashicons untuk pengunjung
- [ ] Uji PageSpeed Insights seluler untuk Home, Single Layanan, Harga, Portofolio, Single Artikel; catat LCP/INP/CLS sebelum dan sesudah tayang

### 8.2 Checklist aksesibilitas

- [ ] `lang="id"`; satu H1 per halaman, urutan H2/H3 tidak melompat; H2 sr-only (`sr-only`) di section tanpa judul terlihat
- [ ] Landmark: header, `nav` `aria-label` "Menu utama", `main`, footer; container diberi HTML Tag yang tepat (`header`, `nav`, `section`, `aside`, `article`, `footer`)
- [ ] Skip link ke konten (bawaan Hello Elementor) berfungsi; `scroll-padding-top` mencegah judul tertutup header sticky
- [ ] Kontras sesuai tabel 2.1; teks Text Muted hanya di latar putih/Frost/Gray 50; teks kecil ≥ 14 px
- [ ] Fokus terlihat 2px Red 600 (Red 300 di latar gelap) pada semua elemen interaktif; kartu klik penuh menampilkan ring di kartu
- [ ] Keyboard: menu dan submenu, accordion (Enter/Spasi; panah bila tersedia), before/after (panah), lightbox (Esc, panah), form (label, galat) semua bisa dipakai tanpa mouse
- [ ] Target sentuh ≥ 44 px (tombol, chip, tautan nav, ikon sosial); jarak antar target memadai
- [ ] Setiap gambar informatif punya `alt` deskriptif; dekoratif `alt=""`; ikon SVG `aria-hidden="true"`
- [ ] Form: label terlihat, `aria-invalid`/`aria-describedby` untuk galat, pesan tidak hanya warna; status sukses `role="status"`
- [ ] Zoom 200% dan lebar 390 px: tanpa scroll horizontal; tabel perbandingan menjadi kartu di mobile
- [ ] Tautan berteks deskriptif (bukan "klik di sini"); tautan tab baru (`wa.me`) memakai `rel="noopener"`

### 8.3 CSS tambahan opsional (Nav Menu, bukan Mega Menu)

Untuk dropdown Layanan 2 kolom di Nav Menu (beri item menu Layanan CSS Class `sbb-cols`) dan kunci scroll saat menu mobile terbuka. Uji ulang setiap update Elementor; jalur resmi adalah Mega Menu.

```css
@media(min-width:1025px){
.elementor-nav-menu--main li.sbb-cols>ul.sub-menu{width:500px;padding:8px}
.elementor-nav-menu--main li.sbb-cols>ul.sub-menu[style*="display: block"]{display:grid!important;grid-template-columns:1fr 1fr;gap:0 8px}
}
@media(max-width:1024px){html:has(.elementor-menu-toggle.elementor-active){overflow:hidden}}
```

### 8.4 Tabel Free-only fallback (tanpa Elementor Pro)

Hanya bila Pro benar-benar tidak tersedia. Semua baris kolom "Kode?" bertanda **Ya** menambah pekerjaan custom di bagian 6.

| Fitur Pro | Dipakai di | Alternatif Free | Kode? |
|---|---|---|---|
| Theme Builder (Header, Footer, Single, Archive, 404) | Semua | Header/footer di child theme (`header.php`/`footer.php`) atau plugin header-footer ringan; layanan dan area kini bagian dari Page statis sehingga tidak butuh template; artikel memakai template tema | Ya (PHP/CSS) |
| Loop Grid, Loop Item, Query ID | Kartu proyek dan artikel | Kartu layanan/harga/testimoni disalin manual di halaman (statis); proyek dan artikel tetap dari CPT | Ya |
| Dynamic Tags (ACF) | Template Single, kartu | Shortcode bawaan ACF `[acf field="harga_per_m2"]` atau `[sbb_rupiah]` | Ya (sedikit) |
| Image widget berposisi absolut (Custom Positioning) | Hero foto, semua halaman | Container **Background Image** + Background Overlay gradien (fallback 2.10); CSS `sbb-hero-photo*` (2.10) tetap dipakai, tanpa kelas `sbb-hero-photo__img` | Ya (CSS) |
| Form widget | Kontak | Plugin form gratis (mis. Fluent Forms/Contact Form 7) atau hanya tombol WhatsApp; JS mockup (K14) bila ingin form kustom | Ya |
| Nav Menu / Mega Menu | Header, footer | Menu WP native di tema + CSS (bagian 8.3) dan JS header mockup (K15) untuk hamburger/dropdown | Ya |
| Sticky (Motion Effects) | Header | `position: sticky; top: 0` pada header tema | Ya (1 baris CSS) |
| Custom Code, Custom CSS (Site Settings) | Semua | Code Snippets/child theme (`wp_head`, `wp_footer`) dan Appearance > Customize > Additional CSS | Ya |
| Table of Contents | Artikel | Daftar tautan manual (anchor H2) atau fitur TOC plugin SEO; K13 bila ingin highlight | Ya |
| Author Box | Artikel | Kartu manual (HTML/Text) dari profil pengguna | Ya |
| Gallery Multiple, Taxonomy Filter, Load on Click | Portofolio | Gallery dasar (free) + JS filter/muat lebih banyak dari mockup (K8, K9) | Ya |
| Popup Builder | Tidak dipakai | Tidak perlu | Tidak |
| Global Widget, Template widget | `BTN-*`, `TPL-*` | Salin widget dari Saved Template (tidak terhubung); ubah di semua salinan | Tidak |
| Nested Accordion / Tabs | FAQ, akordeon | Accordion klasik (free) atau K11/K12 | Ya (opsional) |
| Video lightbox, Grid container, Entrance Animation | Galeri video, grid, reveal | Tersedia di versi Free terbaru; bila tidak, K3 dan galeri HTML | Tidak |

### 8.5 Halaman yang selalu butuh CSS/JS kustom (meski Pro tersedia)

| Halaman | Kode | Alasan |
|---|---|---|
| Semua | K1 (Kit CSS, termasuk hero foto 2.10 dan foto konten 2.11), K3 (reveal), K17 (prioritas gambar hero) | Overlay gradien hero, frosted + @supports, focus ring, rasio gambar, tabel, reveal |
| Home | K18 peta SVG (HTML widget) | Tidak ada widget native |
| Single Layanan (9) | K6 before/after | Sama |
| Harga | K5+K7 estimator | Tidak ada kalkulator native |
| Layanan index, Single Artikel | K1 (tabel `sbb-compare`, tipografi artikel) | Tabel via HTML widget |
| FAQ | K11/K12 hanya bila memilih Opsi A (setia mockup) | Filter "Semua" |
| Kontak | K14 hanya bila memilih Opsi B | Form kustom |
| Portofolio | Tidak ada bila Opsi A; K9/K8 bila Opsi B/C | Native Loop Grid mencukupi |

### 8.6 Sumber konten dan aset

Seluruh konten dan aset build sudah lengkap dan tersimpan di repositori; tiap kebutuhan punya satu sumber.

| Kebutuhan | Sumber | Dipakai di |
|---|---|---|
| Teks, angka, harga, testimoni, caption galeri, artikel, jawaban FAQ | `DEMO-CONTENT.md` (memuat `mockup/DEMO-DATA.md` dan tambahan per halaman) | Semua halaman, CPT, template |
| Identitas, alamat, jam, WhatsApp, telepon, email, tautan sosial, tautan Google Maps/GBP | `mockup/DEMO-DATA.md` (bagian Identitas dan kontak, Kontak tambahan); bagian 1.1 | Header, footer, Kontak, JSON-LD (7.2) |
| Harga sembilan layanan (delapan per m², Huruf Timbul 3D per huruf) | `mockup/DEMO-DATA.md` (tabel harga); tabel nilai awal di 4.3 | ACF `layanan`, Harga, Layanan index, estimator |
| 71 foto WebP (14 hero, 9 layanan, 32 galeri, 7 area, 9 bengkel/ruang) | `mockup/assets/img/photos/` dengan `manifest.json`; tabel peran, ukuran, halaman, `sizes` di 2.11 | Media Library, ACF gambar, Loop Item, hero foto (2.10) |
| Alt text | atribut `alt` di `mockup/*.html` (satu kalimat yang menggambarkan isi foto) | Media Library > Alternative Text |
| Logo dan favicon | `mockup/assets/img/logo.svg`, `logo-light.svg`, `favicon.svg` | Header, footer, Site Identity |
| Peta Kontak | iframe Google Maps dengan `src` dan atribut dari `DEMO-DATA.md` (Peta); `title`, `loading="lazy"`, `referrerpolicy="no-referrer-when-downgrade"` | Kontak (HTML widget) |
| Ikon | sprite `mockup/src/partials/header.html` (K2) | Semua halaman |
| CSS dan JS | bagian 2.8, 2.10, 2.11, 6 | Site Settings > Custom CSS, Custom Code, child theme |
| Schema | 7.2 dan 7.3 | Custom Code Head, plugin SEO |

Urutan pengisian: (1) unggah 71 foto sesuai 2.11 dan isi Alternative Text; (2) buat 9 `layanan`, 7 `area`, 32 `proyek`, 6 `testimoni`, artikel dengan nilai dari `DEMO-CONTENT.md`; (3) bangun template dan halaman memakai file di `elementor-spec/`.

### 8.7 QA akhir lintas halaman

- [ ] 14 halaman + 9 layanan + 7 area + artikel dapat dibuka; jumlah section tiap halaman sama dengan header "Sections in mockup"
- [ ] Menu aktif benar; breadcrumb 3 tingkat pada halaman dalam; tidak ada tautan `#` yang tersisa
- [ ] Tombol "Minta penawaran" mengarah ke `/kontak/#penawaran`; anchor `#harga`, `#estimasi`, `/layanan/#perbandingan` menggulir dengan offset header
- [ ] Uji di 390 px, 768 px, 1024 px, dan 1280 px; tidak ada overflow horizontal; bar bawah mobile tidak menutup konten terakhir; WA float tidak menabrak footer
- [ ] Frosted memiliki fallback (uji dengan `backdrop-filter` dimatikan): teks tetap terbaca
- [ ] `prefers-reduced-motion`: reveal dan transisi mati
- [ ] Hero foto di 14 halaman: satu H1, foto tidak terpotong di titik penting (cek `--focus` di tabel 2.11 pada 390 dan 1280 px), teks terbaca di atas foto, `python3 mockup/tools/contrast.py` tetap 0 gagal bila token `--hero-*` diubah
- [ ] Estimator: 2,5 m² × Sticker Sandblast = Rp 337.500; pilih Huruf Timbul 3D menampilkan "Rp 35.000 / huruf" dan kalimat "dihitung per huruf setelah desain disepakati"; pesan WhatsApp terisi layanan dan angka
- [ ] Kontak: iframe Google Maps memuat alamat Jl. Cokroaminoto Gg. Jempiring No. 15 (lazy, `title` terisi)
- [ ] Nomor WhatsApp/telepon sama persis di header, footer, bar mobile, form, dan schema (0822-2692-0230); email `info@stikersandblastbali.com` sama di footer, Kontak, dan JSON-LD
- [ ] SMTP diuji (email form masuk kotak masuk); batas ukuran/jumlah berkas unggah; event GA4 `whatsapp_click`, `phone_click`, `generate_lead` terkirim
- [ ] Permalink disimpan ulang; sitemap dikirim ke Search Console; 404 mengirim status 404; HTTPS dan redirect www/non-www
- [ ] Schema lolos Rich Results Test; **tidak ada** `AggregateRating`/`Review` dan tidak ada `geo`

### 8.8 Keputusan atas ambiguitas mockup

- Sumber URL: `SITE-STRUCTURE.md` menang (bagian 2 sudah disinkronkan ke struktur 5 halaman: video menjadi `/portofolio/#video`, layanan menjadi anchor di `/layanan/`, area dan testimoni menjadi bagian dari `/tentang-kami/`, FAQ menjadi `/kontak/#faq`).
- Area index memakai 8 kartu statis (7 kawasan + "kawasan lain"), bukan Loop, karena jumlahnya tetap; Single Area tetap CPT.
- `LocalBusiness`: `priceRange` "$$" dipasang; `geo` dari `SITE-STRUCTURE.md` bagian 8 tidak dipasang; `AggregateRating` dan `Review` tidak dipasang.
- Hero: semua halaman memakai hero foto besar (`.hero-photo` mockup), bukan hero split gradien lama; dibangun dengan Image absolut + overlay demi LCP (2.10).
- Tipografi mockup fluid (`clamp`), Elementor tetap: 56/46/36, 40/34/28, 24/22/20, 17/16,5/16, 14 (tablet = titik tengah).
- Filter FAQ "Semua" tidak ada native: Opsi A (HTML+JS) atau Opsi B (Nested Tabs tanpa "Semua"); Opsi A bila ingin setia mockup, Opsi B bila ingin tanpa JS kustom (`14-kontak.md` bagian 3b).
- Modal video dengan tombol WhatsApp digantikan Video lightbox; tombol dipindah ke bawah kartu.
- Galeri portofolio memakai rasio asli foto (Loop Grid Masonry), bukan kotak 4:3, mengikuti `.gallery__grid` mockup.

