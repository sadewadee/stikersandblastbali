# DESIGN-BRIEF — Sticker Sandblast Bali

Dokumen acuan tunggal untuk mockup HTML dan spec Elementor. Semua halaman harus mengikuti token dan komponen di sini. Konteks: `SITE-STRUCTURE.md` (URL dan halaman), `COMPETITOR-ANALYSIS.md` (celah yang dimenangkan).

## 1. Arah visual

Keputusan user: **bersih profesional, hitam/merah**. Palet mengikuti acuan `stickersandblastbali.com` (hitam solid + merah `#ec2327` untuk topbar, tombol, dan band besar). Kompetitor memakai palet serupa, jadi pembeda datang dari layout, konten, dan satu motif khas, bukan dari palet.

**Motif khas: "frosted glass".** Produk utamanya sticker sandblast (kaca buram). Panel translucent putih dengan blur di atas foto atau blok merah menjadi elemen visual berulang: kartu di hero, badge kepercayaan, dan panel harga. Dipakai hemat (paling banyak 1–2 panel per section), bukan glassmorphism di semua tempat.

**Nada**: tenang, presisi, dapat dipercaya. Target pembaca: pemilik villa, hotel, restoran, kantor, dan toko di Bali yang ingin tahu harga, waktu, dan hasilnya sebelum menghubungi.

**Yang dihindari**: emoji sebagai ikon, gradient ungu-biru generik, kartu dengan bayangan berlebihan, stok foto senyum generik, slider otomatis di hero, angka klaim yang dikarang.

## 2. Design tokens

### Warna

| Token | Hex | Pemakaian |
|---|---|---|
| `--ink-900` | `#111111` | Background section gelap, footer, teks judul, tombol sekunder |
| `--ink-700` | `#2B2B2B` | Hover gelap, gradien gelap |
| `--red-600` | `#CA1317` | Warna primer: tombol primer, link, eyebrow, ikon, focus ring di atas terang (putih di atasnya 5,8:1) |
| `--red-500` | `#EC2327` | Merah brand: dekoratif, garis, glow, blok besar (bukan teks kecil di atas putih: 4,3:1) |
| `--red-300` | `#FF3333` | Aksen di atas `--ink-900` (eyebrow/link/ikon/focus), `::selection` |
| `--red-800` | `#A30F12` | Ujung gradien band merah `section--pane` |
| `--gray-50` | `#F8F8F8` | Background section selang-seling, lingkaran ikon, callout |
| `--frost` | `#F4F4F4` | Background halaman alternatif, panel |
| `--border` | `#DDDDDD` | Garis, border kartu; juga teks sekunder di atas `--ink-900` |
| `--text` | `#333333` | Teks isi |
| `--text-muted` | `#666666` | Teks pendukung (harus ≥ 4,5:1 di atas putih dan `--frost`) |
| `--wa-green` | `#0B7A3B` | **Hanya** tombol WhatsApp (putih di atas hijau ini 5,4:1) |
| `--white` | `#FFFFFF` | |
| `--ph-base-1/2/3` | `#E0E0E0` / `#A8A8A8` / `#6E6E6E` | Gradasi abu netral untuk gambar placeholder `.ph-img` (lihat bagian 7) |
| `--error` | `#C2410C` | Galat form (merah-oranye, sengaja beda dari merah brand) |
| `--shadow` | `0 8px 30px rgba(17,17,17,.08)` | Bayangan kartu |

Semua pasangan teks/background harus lolos WCAG AA (4,5:1 untuk teks normal, 3:1 untuk teks ≥ 24px atau ≥ 18,66px tebal). Hijau WhatsApp resmi `#25D366` **tidak** dipakai untuk tombol bertulisan putih karena kontrasnya hanya 2:1.

### Tipografi (Google Fonts, cukup 2 keluarga)

- **Judul**: Plus Jakarta Sans, bobot 700 dan 800.
- **Isi**: DM Sans, bobot 400, 500, dan 600.
- `font-display: swap`. Muat hanya bobot yang dipakai.

| Level | Desktop | Mobile (≤ 767px) | Line height |
|---|---|---|---|
| H1 | 56px | 36px | 1.1 |
| H2 | 40px | 28px | 1.2 |
| H3 | 24px | 20px | 1.3 |
| Isi | 17px | 16px | 1.65 |
| Kecil / caption | 14px | 14px | 1.5 |

Batas lebar baris isi: 68 karakter (sekitar 680px).

### Spasi, radius, bayangan

- Skala spasi: 4, 8, 12, 16, 24, 32, 48, 64, 96 px. Padding vertikal section: 96px desktop, 56px mobile.
- Container maksimal 1200px, gutter 24px (mobile 16px).
- Radius: 14px kartu, 10px tombol dan input, 999px badge/chip.
- Bayangan: satu level saja, `0 8px 30px rgba(17,17,17,.08)`. Kartu biasa memakai border, bukan bayangan.
- **Panel frosted**: `background: rgba(255,255,255,.72)`, `backdrop-filter: blur(14px)`, `border: 1px solid rgba(255,255,255,.65)`, dengan fallback background solid `rgba(255,255,255,.92)` bila `backdrop-filter` tidak didukung.

### Breakpoint (selaras dengan Elementor)

Mobile ≤ 767px · Tablet 768–1024px · Desktop ≥ 1025px.

### Gerak

Transisi 150–250ms untuk hover/focus, reveal saat scroll dengan fade + 12px translate satu kali per elemen. Wajib menghormati `prefers-reduced-motion: reduce` (matikan semua animasi non-esensial).

### Aksesibilitas

- Target sentuh minimal 44×44px.
- Focus ring terlihat (2px `--red-600` dengan offset 2px), jangan dihapus.
- Semua gambar punya `alt` yang deskriptif. Ikon dekoratif memakai `aria-hidden="true"`.
- Satu `<h1>` per halaman, hierarki heading berurutan.
- Accordion FAQ dan menu mobile bisa dioperasikan dengan keyboard.

## 3. Komponen

Setiap komponen dibuat sekali di mockup dan dipakai ulang. Di Elementor, komponen yang berulang menjadi Saved Template atau Global Widget.

1. **Header**: logo kiri, menu tengah (Beranda · Tentang Kami · Layanan ▾ · Portofolio ▾ · Artikel · Kontak), tombol WhatsApp kanan. Sticky dengan background putih dan garis bawah tipis saat scroll. Di mobile: logo, tombol WhatsApp kecil, hamburger. Dropdown "Layanan" berisi 9 layanan (anchor ke `/layanan/`) + "Lihat semua layanan" + "Harga & estimasi".
2. **Tombol**: primer (`--red-600`, teks putih, hover `--ink-900`), WhatsApp (`--wa-green`, ikon WhatsApp SVG, teks putih), sekunder (`--ink-900`, hover `--red-600`), tautan-teks dengan panah. Tinggi 48px, padding horizontal 24px.
3. **Kartu layanan**: gambar 4:3 (placeholder), judul H3, deskripsi 2 baris, tautan "Lihat layanan". Hover: border `--red-600` dan gambar zoom 1.03.
4. **Kartu nilai (icon box)**: ikon SVG garis 28px di dalam lingkaran `--gray-50` dengan ikon merah, judul, 1–2 kalimat. Di dalam band merah `section--pane` kartu tetap terang (putih) dan teksnya kembali gelap.
5. **Langkah proses (3 langkah)**: nomor besar, judul, deskripsi, estimasi waktu. Garis penghubung horizontal di desktop, vertikal di mobile.
6. **Kartu harga/paket**: nama layanan, "mulai dari Rp [X] / m²" (placeholder), 4–5 poin yang termasuk, faktor yang mengubah harga, tombol WhatsApp.
7. **Before/after slider**: dua gambar dengan handle geser (bisa dengan keyboard). Placeholder: blok "SEBELUM" dan "SESUDAH".
8. **Galeri**: grid masonry 3 kolom (2 di tablet, 1–2 di mobile), filter kategori berupa chip, lightbox saat diklik, caption di bawah setiap item (jenis, lokasi kawasan).
9. **Kartu testimoni**: kutipan, nama, jenis bangunan/lokasi, tanggal. Tidak ada bintang yang dikarang.
10. **Accordion FAQ**: satu terbuka dalam satu waktu, ikon plus/minus, tinggi minimal 56px.
11. **Kartu artikel**: gambar 16:9, kategori, judul, ringkasan, tanggal, waktu baca.
12. **Bar CTA akhir**: background `--ink-900`, heading, dua tombol (WhatsApp dan "Minta penawaran").
13. **Formulir penawaran**: nama, nomor WhatsApp, jenis layanan (select), perkiraan ukuran, area/kota, unggah foto, catatan. Ada pernyataan privasi singkat.
14. **Footer**: 4 kolom (lihat `SITE-STRUCTURE.md` bagian 5).
15. **Tombol WhatsApp mengambang**: bulat 56px, kanan bawah. Di mobile menjadi bar bawah dua tombol (WhatsApp, Telepon).
16. **Breadcrumb**: di semua halaman kecuali Beranda.
17. **Badge kepercayaan (frosted)**: chip kecil di hero, mis. "Survey lokasi", "Garansi pemasangan". Hanya menampilkan klaim yang dikonfirmasi bisnis, sisanya ditandai placeholder.

## 4. Blueprint halaman

Situs final = **5 halaman**: Beranda, Tentang Kami, Layanan, Portofolio, Kontak — plus Artikel (index + single) di luar hitungan. Halaman `harga`, `testimoni`, `area` (index + 7 halaman kota), `layanan/{slug}` (9 halaman), `galeri-video`, dan `faq` **dihapus**; isinya menjadi anchor di dalam halaman yang tersisa (peta lengkap di `SITE-STRUCTURE.md` bagian 2). Blueprint di bawah sudah mengikuti struktur tersebut.

### 4.1 Beranda (`/`)
1. Header + bar promo tipis (merah, opsional, mis. jam operasional).
2. **Hero foto besar**: H1, subjudul 1–2 kalimat, tombol WhatsApp + "Lihat portofolio", deretan 3 badge frosted, kartu frosted rating/jam.
3. **Tentang singkat** + daftar 5 layanan utama (tautan ke anchor layanan) + tombol ke `/tentang-kami/`.
4. **Nilai jual (4 kartu)** dalam band merah `section--pane`: harga jelas, pemasangan rapi, pengerjaan cepat, bahan berkualitas.
5. **Layanan (grid 3 kolom, 9 kartu)** menuju anchor di `/layanan/`.
6. **Home service, garansi, one-day service (3 kartu)**: klaim placeholder sampai dikonfirmasi.
7. **Harga mulai dari**: 4 kartu paket ringkas + tautan ke `/layanan/#harga`.
8. **Proses 3 langkah**: Konsultasi → Ukur dan penawaran → Pemasangan.
9. **Before/after + portofolio pilihan**: slider + 6 foto terbaru.
10. **Area layanan**: chip 7 kota + peta ilustrasi, tautan ke `/tentang-kami/#area`.
11. **Testimoni**: 3 kartu + tautan ke `/tentang-kami/#testimoni`.
12. **Artikel terbaru**: 3 kartu.
13. **FAQ (6 pertanyaan)** + tautan ke `/kontak/#faq`.
14. **Bar CTA akhir** → footer + tombol WhatsApp mengambang.

Blok "Rekam jejak dalam angka" (statistik) **dihapus** dari Beranda dan Tentang Kami.

### 4.2 Tentang Kami (`/tentang-kami/`)
Hero foto → cerita bisnis (`#cerita`, placeholder ditulis bersama pemilik) → nilai jual 4 kartu → tim/workshop (foto placeholder) → **testimoni (`#testimoni`)**: ringkasan jumlah review + grid kartu → **area layanan (`#area`)**: chip 7 kota, peta ilustrasi, dan satu paragraf spesifik per kawasan → CTA "Kami siap datang ke lokasi".

### 4.3 Layanan (`/layanan/`) — semua layanan, harga, dan estimator dalam satu halaman
Hero foto + kartu "Harga mulai dari" → intro 2 paragraf → grid 9 kartu (tautan ke anchor) → **sembilan blok detail layanan**, masing-masing `<section id="{slug}">` berisi foto, deskripsi, poin manfaat, harga "mulai dari", dan tombol WhatsApp; blok pertama (`#sticker-sandblast`) memuat before/after slider → **band merah harga (`#harga`)**: kartu harga 9 layanan + "yang termasuk / tidak termasuk" → **kalkulator estimasi (`#estimasi`)**: input luas m² + pilihan layanan, hasil = harga awal, dengan catatan "estimasi, harga final setelah survey" → **proses order 3 langkah (`#proses`)** → **FAQ layanan & harga 8 pertanyaan (`#faq-layanan`)** → CTA.

Latar tiap blok berselang-seling putih dan abu muda agar tidak monoton; band merah dipakai sekali, di blok harga.

### 4.4 Portofolio (`/portofolio/`)
Hero foto → chip filter (Semua, Sandblast, One Way, Riben, Kaca Film, Cutting, Printing, Wrapping, Huruf Timbul, Neon Box) → grid masonry dengan lightbox dan caption (`#foto`) → tombol "Muat lebih banyak" → CTA → **galeri video (`#video`)**: grid thumbnail video dengan lightbox YouTube.

### 4.5 Artikel (`/artikel/` dan `/artikel/{slug}/`)
Index: hero foto → artikel unggulan (1 besar) → grid kartu 3 kolom → kategori → pagination. Artikel: breadcrumb → H1 + meta (tanggal, waktu baca, penulis) → daftar isi → isi (H2/H3, gambar, callout) → kotak CTA di tengah → penulis singkat → artikel terkait → layanan terkait → CTA. Target 800+ kata unik.

### 4.6 Kontak (`/kontak/`)
Hero foto → dua kolom: kiri kartu kontak (`#hubungi`: WhatsApp, telepon, email, alamat, jam operasional, sosial media) dan kanan formulir penawaran (`#penawaran`) → peta (Google Maps embed) → area layanan → **FAQ singkat (`#faq`)** → footer.

## 5. Pemetaan ke Elementor

- **Kit (Site Settings)**: Global Colors = token warna bagian 2, Global Fonts = tipografi bagian 2, container width 1200px, breakpoint default Elementor.
- **Struktur**: semua section memakai **Container (Flexbox)**, bukan Section/Column klasik.
- **Widget**: Heading, Text Editor, Button, Icon Box, Image, Gallery (Pro, filter + lightbox), Nested Accordion, Nested Tabs, Counter, Testimonial Carousel (Pro), Form (Pro) atau CF7, Google Maps, Loop Grid (Pro) untuk layanan dan artikel, Video (lightbox), Image Comparison (butuh add-on atau HTML widget ringan), HTML widget untuk kalkulator estimasi.
- **Theme Builder**: Header, Footer, Single Page (layanan, area), Single Post, Archive (artikel), 404.
- **Global Widget/Saved Template**: bar CTA akhir, kartu harga, badge kepercayaan, blok proses 3 langkah.

Detail per halaman (ID container, widget, setelan responsif) ada di `ELEMENTOR-SPEC.md`.

## 6. Aturan copy

- Bahasa Indonesia, "Anda" (formal-ramah), kalimat pendek.
- Sebut kota dan kawasan konkret, bukan "seluruh Indonesia".
- **Jangan mengarang** angka pengalaman, jumlah proyek, klien, garansi, harga, testimoni, atau alamat. Semua yang belum dikonfirmasi ditulis sebagai placeholder (bagian 7).
- Jangan menyalin heading atau kalimat dari situs referensi.
- Heading memuat keyword secara natural. Tidak ada pengulangan keyword yang dipaksakan.

## 7. Aturan placeholder

Setiap data yang belum dikonfirmasi tampil di mockup dengan `<mark class="ph">…</mark>` supaya jelas apa yang harus diganti. Penanda ini sengaja **tanpa warna** (tanpa background dan tanpa garis bawah) agar tidak mengganggu penilaian warna di mockup; tombol kecil di pojok "Sembunyikan penanda placeholder" menyembunyikannya untuk melihat tampilan bersih. Setelah Task 5 semua data demo sudah terisi, sehingga build tidak lagi memunculkan penanda sama sekali.

Gambar dan ilustrasi sementara memakai `.ph-img`: gradasi abu netral (`--ph-base-1` `#E0E0E0` → `--ph-base-2` `#A8A8A8` → `--ph-base-3` `#6E6E6E`) dengan kilau kaca diagonal dan butir pasir halus di atasnya. Varian `.ph-img--frosted`, `.ph-img--deep`, dan `.ph-img--map` memakai token abu yang lebih terang/gelap agar hierarkinya terbaca.

Yang sudah dikonfirmasi (tidak ditandai placeholder):
- Brand: **Sticker Sandblast Bali**. Domain: `stikersandblastbali.com`.
- WhatsApp dan telepon: **0822-2692-0230** (`https://wa.me/6282226920230`, `tel:+6282226920230`). Satu nomor untuk keduanya, sesuai keputusan user. Nomor GBP 0813-3730-2965 tidak dipakai di situs.
- Google Business Profile: milik klien. Datanya (alamat, jam, rating, review, peta) dipakai sebagai milik bisnis ini.
- Alamat: **Jl. Cokroaminoto Gg. Jempiring No. 15, Ubung, Kec. Denpasar Utara, Kota Denpasar, Bali 80111** (dari GBP).
- Jam operasional: **Senin–Minggu 09.00–17.00** (dari GBP).
- Rating dan review Google: **4,9 dari 57 ulasan** per 2026-09-21 (dari GBP). Tampilkan sebagai "Ulasan Google", bukan bintang buatan sendiri. Kutipan review yang terbaca (tanpa nama dan tanggal): "Pelayanan memuaskan dan respon yg baik", "Benar benar bagus banget", "Terima kasih banyak om..owner saya puas dengan hasilnya". Nama dan tanggal reviewer ditandai placeholder.

Harga dari daftar produk GBP, **satuan per m²** (dikonfirmasi user), ditampilkan sebagai "mulai dari": sticker sandblast **Rp 135.000 / m²**, one way vision **Rp 195.000 / m²**, sticker printing **Rp 175.000 / m²**. Cutting sticker tercatat "Rp 60" (angka terpotong di halaman): tampilkan sebagai `<mark class="ph">Rp 60.000 / m²</mark>` sampai angkanya dikonfirmasi. Layanan lain belum ada harga (`Rp [harga] / m²` sebagai placeholder).

Daftar yang masih harus dilengkapi: logo · email · koordinat peta · link sosial media · semua angka statistik · klaim garansi, one-day service, home service · harga cutting dan layanan lain · nama dan tanggal reviewer · foto proyek asli beserta kawasan dan tanggal · nama penulis artikel.

Foto: mockup memakai blok placeholder dengan label jelas ("FOTO: sandblast kaca villa, Canggu"), tanpa stok foto dan tanpa gambar yang dikarang.
