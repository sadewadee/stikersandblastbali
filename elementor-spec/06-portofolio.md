# 06 — Portofolio (`/portofolio/`)

Sections in mockup: **3** `<section>` di dalam `<main>` (hero foto, galeri foto dengan filter `#foto`, grid 6 kartu video `#video`) + CTA partial, ditambah satu dialog modal video di luar `<main>` (`#video-modal`). Sumber: `mockup/portofolio.html` (kode `mockup/src/pages/portofolio.html`; JS `assets/js/app.js` modul `gallery`, `pages-b.js` fungsi `initLoadMore` dan `initVideoModal`; CSS `styles.css` bagian 5.08 dan `pages-b.css` bagian 3–4). Mockup memuat **30 foto** (`g-*`), 9 kategori (+ chip "Semua"), 12 foto tampil awal, dan 6 kartu video. Resep di `../ELEMENTOR-SPEC.md` bagian 2.9 dan 5; hero mengikuti master bagian 2.10 "Hero foto besar" (CSS `sbb-hero-photo*`) dan file foto master bagian 2.11 "Pustaka media".

Dokumen ini menggabungkan spec lama `07-galeri-video.md` (halaman `/galeri-video/`, dihapus): galeri video kini bagian dari halaman ini pada anchor `#video`. **Anchor (wajib persis):** `#foto` `#video`.

## 1. Pengaturan halaman

| Item | Nilai |
|---|---|
| URL / tipe | `/portofolio/` · Page statis. Isi galeri dari CPT `proyek` (tanpa halaman single: `publicly_queryable = false`, tidak masuk sitemap) |
| Page Layout | Elementor Full Width · Hide Title On |
| Header / Footer | Header standar (menu aktif: Portofolio + Galeri Foto, `@active portofolio portofolio-foto`) · Footer global |
| Kelas hook | `sbb-page-portofolio`; hero `sbb-hero-photo sbb-hero-photo--page sbb-hero-photo--tall`; grid galeri class `sbb-gallery`; kartu video `sbb-video-card`; modal `sbb-modal` |
| CSS halaman | Advanced > Custom CSS (page, Pro): salin `pages-b.css` bagian 3 (`.gallery__more`) dan bagian 4 (`.video-card*`, `.modal*`). Ganti `.section--frost`/`.section--alt` menjadi `sbb-section--frost`/`sbb-section--alt`. Di Free-only: Additional CSS |
| Kode halaman | `initVideoModal` dari `pages-b.js` (blok "3. MODAL VIDEO") di Custom Code Body End — **wajib**, untuk section 4. Galeri foto (bagian 3) bergantung opsi |

## 2. Tabel section

| # | Section | Container | Widget dan setelan utama (copy persis mockup) | Responsif | Interaksi / kode | Sumber konten |
|---|---|---|---|---|---|---|
| 1 | Hero foto besar (`HERO-FOTO` varian `page`) | **Container terluar** Full Width, Column, Justify Center, Position Relative, Overflow Hidden, background Ink 900, tinggi diatur kelas (`clamp(440px, 62vh, 620px)`; Min Height native dikosongkan); kelas `sbb-hero-photo sbb-hero-photo--page sbb-hero-photo--tall`; Advanced > Custom CSS `selector{--focus:50% 42%}` | (0) **Image** `hero-portofolio.webp` 1920×1329, Absolute inset 0, Object Fit Cover, Object Position `50% 42%`; alt "Tulisan emas pada kaca jendela restoran dengan dinding bata putih di sampingnya"; tanpa lazy-load, `fetchpriority="high"`. (1) **Container overlay** `sbb-hero-photo__overlay`: Gradient 90° Ink 900 alfa .88 → .72 (66%) → .30 di ≥1025; .72 rata di 768–1024; .12 rata di mobile. (2) **Container inner** (boxed 1200, Column, Gap 16, padding Y 88 (`--tall`) / 40 / 28, anak maks 640px atau 62% di ≥1025): `TPL-BC` terang (`sbb-bc--light`) "Beranda > Portofolio" · Heading p `sbb-eyebrow--light` "Galeri foto" · **H1** putih (48→32px) "Portofolio Sticker Sandblast, Kaca Film & Cutting di Bali" · Lead putih (max 56ch) "500+ proyek di Denpasar, Canggu, Seminyak, Ubud, Sanur, Nusa Dua, dan Kuta. Pilih kategori, lalu klik foto untuk memperbesarnya." · Row Wrap tombol Gap 12, margin-top 24: `BTN-WA` "Chat WhatsApp" (`https://wa.me/6282226920230`) + `BTN-SEC-L` outline light (`sbb-btn--outline-light`) "Lihat galeri video" (`/galeri-video/`). Tanpa badge dan kartu | Tablet: overlay .72. Mobile: Min Height 56vh (min 400, max 520), Justify End, padding-top 80–132px, inner Gradient 180° alfa 0 → .72 di 72px, tombol Width 100% | LCP: `hero-portofolio.webp` tanpa lazy-load | Statis |
| 2 | Galeri + filter | `SEC(frost)` > container Column gap 0 (`sbb-gallery`). Urutan: filter · status · grid · load more · catatan | H2 sr-only "Galeri foto pemasangan" (Heading, class `sr-only`; definisi di CSS master 2.8). **Filter** 10 chip (`role=group`, `aria-label` "Filter kategori portofolio"): Semua · Sandblast · One Way · Riben · Kaca Film · Cutting · Printing · Wrapping · Huruf Timbul · Neon Box (tinggi 44px, pill radius 999, aktif: latar Ink 900 teks putih, `aria-pressed`). Status (14px Text Muted, `aria-live=polite`): "Menampilkan 12 dari 30 foto". **Grid**: 30 item, masonry 3 / 2 / 1 kolom (gap 24/16/16): tiap item Image rasio asli foto (radius 14, hover zoom 1,03, ikon perbesar 36px pojok kanan atas saat hover/fokus; `aria-label` tombol "Perbesar foto: {jenis}, {kawasan}") + caption 14px "**jenis** · kawasan" (daftar 30 foto, file, kategori, dan alt di bagian 4). **Load more**: `BTN-SEC` "Muat lebih banyak" (di tengah, margin-top 32; tampil hanya bila kategori terpilih memuat lebih dari 12 foto; klik memuat semua sisa dan memindahkan fokus ke foto baru pertama). Catatan 14px di bawah: "Ingin hasil serupa di tempat Anda? Kirim foto kaca lewat WhatsApp untuk estimasi awal." | Desktop 3 kolom (`column-count`); tablet 2; mobile: 1 kolom di bawah 480px, 2 kolom 480–767px. Chip: di mobile satu baris yang bisa digeser horizontal tanpa scrollbar (Flex Row, No Wrap, Overflow Auto); tap 44px | Lihat bagian 3. Filter mempertahankan foto multi-kategori (mis. "Printing dekal bodi mobil" muncul di Printing dan Cutting). Jumlah per kategori: Sandblast 7 · Kaca Film 7 · Wrapping 4 · Riben 3 · One Way 3 · Cutting 3 · Printing 3 · Neon Box 3 · Huruf Timbul 2 (jumlah lebih besar dari 30 karena foto multi-kategori). Lightbox: Esc menutup, fokus kembali ke foto, panah kiri/kanan, geser di layar sentuh; caption lightbox = caption foto | CPT `proyek`: featured image `g-*`, `jenis`, `kawasan`, `caption` ("jenis · kawasan"), taxonomy `kategori-layanan` multi |
| 3 | Galeri video (`#video`) | `SEC(alt)` (CSS ID `video`): `HEAD` + `GRID 3` (3 / 2 / 1, Gap 24) | Eyebrow "Galeri video" · H2 "Lihat proses pemasangannya" · Lead "Video pemasangan menunjukkan cara film dipotong, ditempel, dan diratakan di kaca, dari sandblast sampai wrapping mobil. Klik satu video untuk melihat pratinjaunya, lalu tonton versi lengkapnya di YouTube." Enam kartu `sbb-video-card` (Container Column Gap 12): **container poster** (Position Relative, radius 14, Overflow Hidden; `button` pembuka modal `data-video-open`, `aria-haspopup="dialog"`, `aria-label` "Buka video: {judul}, durasi {mm:ss}") berisi Image poster rasio 16:9 (Object Fit Cover, hover zoom 1,03; lazy) + **badge play** (container absolut tengah, `sbb-frost`, lingkaran 64px, ikon play 28px Ink 900, `pointer-events:none`; hover scale 1,08) + **badge durasi** (absolut kanan-atas 12/12, `sbb-frost`, pill 999, padding 4/10, teks 14px 600 Ink 900, `pointer-events:none`); di bawahnya H3 18px judul, teks 14px 600 Red 600 "{layanan} · {kawasan}", teks 15,5px Text keterangan. **Enam kartu (poster → durasi → judul → meta → keterangan):** 1 `g-04-bathroom-frost.webp` · 03:24 · "Proses pasang sticker sandblast pada pintu kamar mandi" · "Sticker Sandblast · Canggu" · "Dari membersihkan kaca sampai meratakan gelembung: urutan pemasangan sticker sandblast pada pintu kaca kamar mandi villa." 2 `g-25-storefront.webp` (fokus `50% 35%`) · 02:48 · "Pemasangan one way vision pada etalase toko" · "Sticker One Way Vision · Seminyak" · "Cara sticker one way vision bergambar dipasang di etalase, agar gambar tampil dari luar dan pandangan dari dalam tetap terbuka." 3 `g-06-office-dark.webp` · 04:10 · "Pemasangan kaca film pada jendela kantor" · "Kaca Film · Renon" · "Langkah memasang kaca film pada jendela lebar: ukur, potong, tempel, lalu rapikan tepi." 4 `svc-cutting.webp` · 02:15 · "Proses cutting sticker logo dari vinyl" · "Cutting Sticker · Denpasar" · "Logo dipotong dari vinyl warna, dibersihkan dari sisa bahan, lalu dipindahkan ke kaca dengan transfer tape." 5 `g-16-wrap-front.webp` · 05:32 · "Wrapping dan branding mobil operasional" · "Wrapping & Branding Mobil · Denpasar" · "Film wrapping dipanaskan dan diratakan di body mobil operasional sampai menempel rapi tanpa gelembung." 6 `g-20-3d-cafe.webp` · 03:48 · "Pemasangan huruf timbul dan neon box papan nama" · "Huruf Timbul & Neon Box · Nusa Dua" · "Huruf timbul 3D dan neon box dipasang di fasad: posisi dicek lebih dulu, baru dikunci." | 3 → 2 → 1 kolom; badge tetap di pojok poster di semua ukuran | Klik atau Enter pada poster membuka modal (bagian 3). **Tanpa iframe YouTube** di halaman | Statis (6 kartu). Alternatif: CPT `video` (`poster`, `judul`, `layanan`, `kawasan`, `durasi`, `keterangan`, `youtube_url`) + Loop Grid bila video bertambah banyak |
| 4 | Bar CTA akhir | `TPL-CTA` | H2 "Kirim foto kaca Anda, kami hitungkan estimasinya." · "Sebutkan jenis layanan dan ukuran kira-kira. Balasan awal lewat WhatsApp, dan harga final dipastikan setelah kaca diukur langsung." · `BTN-WA` "Chat WhatsApp" + `BTN-SEC-L` "Minta penawaran" (`/kontak/#penawaran`) | Tumpuk di ≤1024 | Reveal | Template global |

## 3. Cara membangun galeri (section 2)

**Opsi A (disarankan, CPT-driven)**: Loop Grid `proyek` (template `LI-PROYEK`: Image featured, Link: Media File, Lightbox On; caption `{caption}`). Pengaturan Loop Grid: Posts Per Page 12, Order By Menu Order asc (urutan foto = tabel bagian 4), Masonry On, Columns 3 / 2 / 1, Pagination **Load on Click** dengan teks tombol "Muat lebih banyak" (memuat 12 foto per klik: 12 → 24 → 30). Filter kategori: widget **Taxonomy Filter** (Pro, bila ada di panel widget versi Anda; targetkan Loop Grid ini, taxonomy `kategori-layanan`, label "Semua"), gaya chip lewat Style tab + class `sbb-chip`. Foto multi-kategori otomatis benar karena satu proyek boleh punya beberapa term.

**Opsi B (Gallery widget Pro)**: Gallery Type **Multiple**, satu grup per kategori (judul grup = nama chip; label semua "Semua"), Layout Masonry, Columns 3 / 2 / 1, Link: Lightbox, Overlay atau Caption dari judul/keterangan media. Batasan: foto multi-kategori harus dimasukkan ke dua grup (tampil dobel di "Semua"); tidak ada "Muat lebih banyak" (pakai 30 foto sekaligus dengan lazy-load, atau tambahkan kode); tidak ada status aria-live.

**Opsi C (paling setia mockup)**: HTML widget atau Shortcode berisi markup `[data-gallery data-load-more="12"]` mockup dan memuat `app.js` modul `gallery` (filter chip, lightbox dengan focus trap) + `pages-b.js` `initLoadMore` (batas 12, semua sisa sekaligus). Butuh dua file JS kecil di Custom Code (Body End, halaman ini); tanpa dependensi lain. Pakai bila persyaratan lightbox berurutan dan status aria-live tidak boleh hilang.

Catatan kualitas untuk semua opsi:

- Lightbox: Site Settings > Lightbox aktif; caption sumber = Caption; warna latar Ink 900 (rgba .94), tombol navigasi tampil. Slideshow prev/next antar item Loop Grid perlu diuji; bila tidak berpindah antar foto, pakai Opsi B atau C.
- Status "Menampilkan N dari 30 foto": tidak ada widget native. Opsional HTML widget `<p class="sbb-gallery-status" aria-live="polite">` yang diisi skrip kecil setelah filter/muat ulang (hitung `.e-loop-item` yang terlihat; total 30).
- Foto: WebP, lebar 900 px (file di bagian 4), `alt` deskriptif dari mockup, lazy-load semua foto di bawah fold, `width`/`height` terisi agar CLS ≤ 0,1.

## 3b. Modal video (section 3)

Satu modal untuk keenam video; data diambil dari kartu yang diklik. Markup mockup `#video-modal` (`hidden`, di luar `<main>`), CSS `pages-b.css` bagian 4, JS `initVideoModal` (`pages-b.js`).

Isi modal: H2 `#video-modal-title` (20px, judul video) + tombol tutup bulat 44px (`aria-label` "Tutup video", ikon close) · poster besar rasio 16:9 (radius 10; poster yang sama dengan kartu) dengan badge durasi frosted kanan-atas · teks meta 14px 600 Red 600 ("Sticker Sandblast · Canggu") · teks keterangan 16px Text (`#video-modal-desc`) · dua tombol: `BTN-PRI` ikon YouTube "Tonton di YouTube" (isi URL YouTube di field Link tiap video) dan `BTN-WA` "Tanya pemasangan serupa" (`https://wa.me/6282226920230`). Panel putih lebar maks 880px, radius 14, padding 28/16, di atas overlay Ink 900 alfa .94. Perilaku: fokus ke tombol tutup, Tab berputar di modal, Esc menutup, klik overlay menutup, fokus kembali ke poster pembuka, scroll terkunci. Tanpa iframe dan tanpa autoplay.

| Opsi | Cara |
|---|---|
| **A (Elementor Pro, tanpa custom code)** | Enam **Popup** ("Video — 1" sampai "Video — 6"), masing-masing berisi Container dengan isi di atas. Overlay Ink 900 alfa .94, Close on ESC + Overlay Click On, Prevent Scrolling On, tombol tutup 44px bulat, Entrance Fade In. Trigger: Link container poster tiap kartu = Dynamic Tag **Popup > Open Popup** (pilih Popup kartu itu). Uji focus trap dan pengembalian fokus |
| **B (paling setia mockup)** | HTML widget untuk 6 kartu (`.video-card`, tombol `data-video-open`) + satu HTML widget untuk `#video-modal`, CSS `pages-b.css` bagian 4, dan `initVideoModal` di Custom Code Body End |

Gaya badge Opsi A (Kit CSS): `.sbb-video-card__disc{width:64px;height:64px;border-radius:50%;display:grid;place-items:center}` dan `.sbb-video-card__time{position:absolute;top:12px;right:12px;padding:4px 10px;border-radius:999px;font-size:14px;font-weight:600;color:var(--sbb-ink-900)}`; keduanya memakai `sbb-frost` (fallback putih .92 tanpa `backdrop-filter`).

## 4. Aset media (dari `mockup/assets/img/photos/`; alt persis mockup)

Foto 1–12 tampil awal; foto 13–30 muncul setelah "Muat lebih banyak". Semua foto lazy-load; ukuran dari `manifest.json`. Kolom "Kategori" = term `kategori-layanan` proyek (satu atau lebih). | `g-04-bathroom-frost.webp` | 900×601 | Poster video 1 (+ modal) | Kamar mandi modern dengan pintu kaca shower dan wastafel | Lazy |
| `g-25-storefront.webp` | 900×1350 | Poster video 2 (crop 16:9, fokus `50% 35%`) | Fasad toko berpintu dan berjendela kayu dengan kaca bersekat | Lazy |
| `g-06-office-dark.webp` | 900×600 | Poster video 3 | Ruang kantor berdinding kaca gelap dengan meja dan jendela besar | Lazy |
| `svc-cutting.webp` | 900×601 | Poster video 4 | Sticker vinyl putih hasil cutting berbentuk huruf pada kaca mobil | Lazy |
| `g-16-wrap-front.webp` | 900×600 | Poster video 5 | Teknisi memanaskan film wrapping putih di kap mobil abu-abu dalam bengkel | Lazy |
| `g-20-3d-cafe.webp` | 900×600 | Poster video 6 | Huruf timbul hitam bertuliskan CAFE pada dinding kayu yang disorot lampu | Lazy |

Foto adalah stok Pexels dan bukan hasil kerja bisnis ini; alt menggambarkan isi foto.

| File | Ukuran | Dipakai di | Alt | Loading |
|---|---|---|---|---|
| `hero-portofolio.webp` | 1920×1329 | Hero (#1) | Tulisan emas pada kaca jendela restoran dengan dinding bata putih di sampingnya | Eager, fetchpriority high |
| `g-17-wrap-blue.webp` | 900×600 | Tautan galeri video (#3) | Teknisi meratakan film bening di atas bodi mobil biru dengan heat gun | Lazy |

Daftar 30 foto galeri (urutan tampil; `caption` = kolom "Caption"):

| # | File | Ukuran | Caption (`jenis` · `kawasan`) | Kategori | Alt |
|---|---|---|---|---|---|
| 1 | `g-01-frosted-doors.webp` | 900×1350 | Sandblast pintu kaca · Canggu | Sandblast | Pintu kaca ganda berlapis sandblast buram dengan gagang panjang |
| 2 | `g-14-wrap-hood.webp` | 900×600 | Wrapping kap mobil · Denpasar | Wrapping | Dua tangan menarik film wrapping putih di atas kap mobil gelap |
| 3 | `g-04-bathroom-frost.webp` | 900×601 | Riben kaca kamar mandi · Seminyak | Riben | Kamar mandi modern dengan pintu kaca shower dan wastafel |
| 4 | `g-18-neon-tattoo.webp` | 900×600 | Neon box studio tato · Kuta | Neon Box | Papan neon hijau dan merah bertuliskan Electric Age Tattoo pada malam hari |
| 5 | `g-25-storefront.webp` | 900×1350 | One way vision etalase · Seminyak | One Way | Fasad toko berpintu dan berjendela kayu dengan kaca bersekat |
| 6 | `g-13-car-decal.webp` | 900×1125 | Printing dekal bodi mobil · Kuta | Printing, Cutting | Bumper belakang mobil putih dengan dekal bunga sakura dan tulisan merah |
| 7 | `g-03-conference.webp` | 900×602 | Sandblast sekat kantor · Renon | Sandblast | Ruang meeting dengan meja panjang dan sekat kaca bermotif garis |
| 8 | `g-20-3d-cafe.webp` | 900×600 | Huruf timbul kafe · Nusa Dua | Huruf Timbul | Huruf timbul hitam bertuliskan CAFE pada dinding kayu yang disorot lampu |
| 9 | `g-19-neon-shoplocal.webp` | 900×900 | Neon box toko lokal · Sanur | Neon Box | Neon merah muda bertuliskan Shop Local pada dinding beton abu-abu |
| 10 | `g-16-wrap-front.webp` | 900×600 | Wrapping kap dan bemper · Denpasar | Wrapping | Teknisi memanaskan film wrapping putih di kap mobil abu-abu dalam bengkel |
| 11 | `g-06-office-dark.webp` | 900×600 | Kaca film gelap ruang kantor · Renon | Kaca Film, One Way | Ruang kantor berdinding kaca gelap dengan meja dan jendela besar |
| 12 | `g-10-etched-leaf.webp` | 900×600 | Sandblast motif daun · Ubud | Sandblast | Kaca dengan ukiran sandblast motif daun dan bunga bertekstur halus |
| 13 | `g-28-cafe-windows.webp` | 900×1349 | Kaca film jendela lengkung kafe · Sanur | Kaca Film | Jendela kaca lengkung besar sebuah kafe dengan kursi dan meja di dalam |
| 14 | `g-05-shower-glass.webp` | 900×601 | Kaca film kamar mandi villa · Ubud | Kaca Film | Kamar mandi krem dengan bilik shower kaca dan cermin |
| 15 | `g-23-cafe-logo-door.webp` | 900×1350 | Cutting logo pintu kafe · Canggu | Cutting | Logo melingkar pada kaca pintu sebuah kedai kopi dengan interior kayu |
| 16 | `g-12-decal-window.webp` | 900×601 | Cutting sticker kaca belakang mobil · Denpasar | Cutting, Printing | Kaca belakang mobil putih dengan tulisan sticker besar |
| 17 | `g-24-cafe-glass-sign.webp` | 900×1350 | Printing logo kaca kafe · Seminyak | Printing | Tulisan dan logo emas pada kaca depan kafe dengan pantulan jalan |
| 18 | `g-15-wrap-glove.webp` | 900×600 | Wrapping pintu mobil · Kuta | Wrapping | Tangan bersarung menempelkan film wrapping putih pada bodi mobil |
| 19 | `g-07-corporate-doors.webp` | 900×1125 | Sandblast strip pintu kantor · Denpasar | Sandblast | Pintu kaca kantor bergagang panjang dengan strip buram horizontal |
| 20 | `g-21-3d-coffee.webp` | 900×600 | Huruf timbul kayu · Ubud | Huruf Timbul | Huruf putih besar berbentuk timbul pada panel kayu, terbaca sebagian bertuliskan Coffee |
| 21 | `g-26-store-logo-glass.webp` | 900×1350 | Papan nama fasad showroom · Denpasar | Neon Box | Fasad showroom malam hari dengan logo menyala di atas pintu kaca |
| 22 | `g-02-glass-hallway.webp` | 900×600 | Sandblast motif titik koridor · Renon | Sandblast | Koridor kantor berdinding kaca dengan motif titik buram dan lantai kayu |
| 23 | `g-09-frosted-panels.webp` | 900×1350 | Riben strip pintu kaca · Sanur | Riben, Sandblast | Pintu kaca berbingkai hitam dengan panel buram bergaris di dinding bata |
| 24 | `g-31-tint-installer.webp` | 900×600 | Pemasangan kaca film · Nusa Dua | Kaca Film | Teknisi bertato merapikan film pada kaca jendela mobil dengan pantulan wajah |
| 25 | `g-11-etched-portrait.webp` | 900×1350 | Sandblast ukir potret · Ubud | Sandblast | Kaca dengan ukiran sandblast potret perempuan dalam bingkai lingkaran |
| 26 | `g-32-film-luxury.webp` | 900×599 | Film pelindung bodi mobil · Nusa Dua | Wrapping, Kaca Film | Dua teknisi merentangkan film transparan di atas mobil sport abu-abu di showroom |
| 27 | `g-27-cafe-interior.webp` | 900×1350 | One way vision kaca kafe · Canggu | One Way | Interior kafe terlihat dari luar kaca dengan meja bulat dan lampu hangat |
| 28 | `g-08-door-glass.webp` | 900×1200 | Riben pintu kaca kantor · Denpasar | Riben | Pintu kaca terbuka ke ruang kantor dengan kursi dan meja kerja |
| 29 | `g-29-cafe-terrace.webp` | 900×1200 | Kaca film teras kafe · Sanur | Kaca Film | Teras kafe berkaca lebar dengan atap anyaman dan kursi kayu |
| 30 | `g-30-window-tint.webp` | 900×1600 | Kaca film jendela mobil · Kuta | Kaca Film | Teknisi memasang film pada kaca jendela mobil dari atas bodi |

## 5. SEO

| Item | Nilai |
|---|---|
| `<title>` (≤ 60) | Portofolio Sticker Sandblast & Kaca Film Bali (45 karakter) |
| Meta description (≤ 155) | Lihat contoh pemasangan sticker sandblast, one way vision, kaca film, cutting, printing, wrapping, huruf timbul, dan neon box di Bali. Filter per kategori. (155 karakter) |
| H1 | Portofolio Sticker Sandblast, Kaca Film & Cutting di Bali |
| Target keyword | contoh sticker sandblast (varian: portofolio kaca film bali) |
| Schema | `ImageGallery` dengan `ImageObject` (URL gambar, caption, `contentLocation` kawasan) untuk bagian `#foto`, `BreadcrumbList`. **Tanpa `VideoObject`**: bagian `#video` menampilkan poster dan tautan YouTube, bukan pemutar tersemat. Bukan `AggregateRating` |
| Internal link wajib | Tiap kategori ke anchor layanan di `/layanan/` yang sesuai (di caption atau teks pengantar), `/layanan/#harga`, `/tentang-kami/#area` |

## 6. QA

- [ ] Hero: `hero-portofolio.webp` tanpa lazy-load; teks putih terbaca di atas overlay; bagian atas foto di mobile terang; tombol "Lihat galeri video" menuju anchor `#video`
- [ ] `#foto` dan `#video` keduanya ada dan berfungsi; tidak ada lagi tautan ke `/galeri-video/`
- [ ] Klik atau Enter pada poster video membuka modal berisi poster besar, judul, meta, keterangan, badge durasi, "Tonton di YouTube" dan "Tanya pemasangan serupa"; Esc dan tombol tutup menutup, fokus kembali ke poster pembuka, Tab tidak keluar dari modal
- [ ] Tidak ada iframe atau permintaan ke `youtube.com` saat halaman dimuat dan saat modal dibuka (cek tab Network)
- [ ] Badge play dan durasi tidak menghalangi klik poster; durasi 03:24 · 02:48 · 04:10 · 02:15 · 05:32 · 03:48 sesuai kartu dan modal
- [ ] Awalnya 12 foto tampil, status "Menampilkan 12 dari 30 foto", dan tombol "Muat lebih banyak" muncul; setelah diklik, semua tampil dan tombol hilang; fokus pindah ke foto baru pertama
- [ ] Filter "Sandblast" menampilkan 7 foto (termasuk "Riben strip pintu kaca · Sanur"); "Printing" dan "Cutting" sama-sama menampilkan "Printing dekal bodi mobil · Kuta" dan "Cutting sticker kaca belakang mobil · Denpasar"; "Kaca Film" 7 foto; "Huruf Timbul" 2 foto tanpa tombol "Muat lebih banyak"
- [ ] Filter + Load more tidak saling menimpa (filter menyetel ulang batas 12)
- [ ] Chip aktif memakai `aria-pressed="true"` atau setara (`aria-current`) dan kontras putih di atas Ink 900 lolos
- [ ] Lightbox: Esc, panah, fokus kembali ke foto pembuka, focus trap; caption "jenis · kawasan" tampil; di mobile geser kiri/kanan
- [ ] Foto potret (mis. `g-30-window-tint.webp` 900×1600) tampil utuh tanpa crop; CLS ≤ 0,1 (gambar punya dimensi), LCP tidak terpengaruh galeri (foto di bawah fold lazy)
- [ ] 390 px: chip dapat digeser, tap target ≥ 44 px, satu kolom di bawah 480 px
