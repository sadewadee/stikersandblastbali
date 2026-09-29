# SITE-STRUCTURE — Sticker Sandblast Bali

Tanggal: 2026-09-21 · Mode: new-site planning (domain belum live) · Platform: WordPress + Elementor
Template industri: `local-service` (claude-seo) · Sumber blueprint halaman: stickerbalisandblast.com (Art Sticker)

## 1. Asumsi dan sumber

- **Brand**: Sticker Sandblast Bali (dikonfirmasi user). **Domain**: `stikersandblastbali.com` (dikonfirmasi user; perhatikan ejaan "stikers", berbeda dengan domain kompetitor `stickersandblastbali.com`).
- **Data kontak terkonfirmasi**:
  - WhatsApp: 0822-2692-0230 (`https://wa.me/6282226920230`), dari user.
  - Alamat: Jl. Cokroaminoto Gg. Jempiring No. 15, Ubung, Kec. Denpasar Utara, Kota Denpasar, Bali 80111. Sumber: Google Business Profile (GBP), dibaca 2026-09-21.
  - Jam operasional: Senin–Minggu 09.00–17.00. Sumber: GBP, dibaca 2026-09-21.
  - Peta: memakai GBP yang sama (embed Google Maps). GBP milik klien.
  - Harga referensi dari daftar produk GBP, satuan per m²: sticker sandblast Rp 135.000, one way vision Rp 195.000, sticker printing Rp 175.000. Cutting sticker tercatat "Rp 60" (terpotong di halaman), angka lengkapnya perlu dikonfirmasi. Layanan lain belum ada harga.
- **Telepon dan WhatsApp memakai nomor yang sama**, 0822-2692-0230 (keputusan user). Nomor yang tercantum di GBP (0813-3730-2965) tidak dipakai di situs. Email, koordinat, dan sosial media masih placeholder.
- **Blueprint halaman** diambil dari Art Sticker (Themify Ultra, 9 halaman inti + halaman layanan + ~30 artikel). Yang diambil hanya struktur dan urutan section. Copy, angka, klien, testimoni, alamat, dan nomor telepon mereka tidak dipakai.
- **Elementor Pro diasumsikan tersedia** (Theme Builder, Form, Loop Grid, Gallery filter, Testimonial Carousel). Kalau hanya Elementor Free, lihat catatan fallback di `ELEMENTOR-SPEC.md`.
- Volume pencarian belum diverifikasi (tidak ada akses DataForSEO/Keyword Planner). Pemetaan keyword di bawah adalah hipotesis dari pola judul kompetitor, bukan data volume.

## 2. Hierarki URL

```
/                                   Beranda
├── /tentang-kami/                  Tentang Kami
│   ├── #cerita                     Cerita bisnis
│   ├── #testimoni                  Testimoni
│   └── #area                       Info area layanan
├── /layanan/                       SEMUA layanan (satu halaman, 9 blok beranchor)
│   ├── #sticker-sandblast
│   ├── #sticker-one-way-vision
│   ├── #sticker-riben
│   ├── #kaca-film
│   ├── #sticker-printing
│   ├── #cutting-sticker
│   ├── #wrapping-branding-mobil
│   ├── #huruf-timbul-3d
│   ├── #neon-box-papan-nama
│   ├── #harga                      Kartu harga 9 layanan + kalkulator estimasi
│   ├── #estimasi                   Kalkulator estimasi biaya
│   ├── #proses                     Alur order 3 langkah
│   └── #faq-layanan                FAQ layanan & harga
├── /portofolio/                    Galeri foto, filter per kategori
│   ├── #foto
│   └── #video                      Galeri video
├── /kontak/
│   ├── #hubungi
│   ├── #penawaran                  Formulir penawaran
│   └── #faq
├── /artikel/                       Blog index (di luar hitungan 5 halaman)
│   └── /artikel/{slug}/            Artikel
└── /kebijakan-privasi/
```

**Situs final = 5 halaman**: Beranda, Tentang Kami, Layanan, Portofolio, Kontak. Artikel (index + single) tetap ada sebagai blog, di luar hitungan tersebut. Tidak ada CPT `layanan` lagi: sembilan layanan adalah sembilan blok beranchor di dalam satu halaman `/layanan/`.

**Dihapus dan pemindahan isinya**:

| URL lama | Isi pindah ke |
|---|---|
| `/harga/` | `/layanan/#harga` (kartu harga) dan `/layanan/#estimasi` (kalkulator) |
| `/layanan/sticker-sandblast/` (dan 8 URL layanan lain) | `/layanan/#{slug}` |
| `/testimoni/` | `/tentang-kami/#testimoni` |
| `/area/`, `/area/{kota}/` (7 halaman) | `/tentang-kami/#area` |
| `/galeri-video/` | `/portofolio/#video` |
| `/faq/` | `/kontak/#faq` |

**Redirect 301 yang disarankan** (dipakai saat migrasi; domain belum live jadi cukup di `.htaccess`/plugin redirect):

| Dari | Ke |
|---|---|
| `/harga/` | `/layanan/#harga` |
| `/layanan/sticker-sandblast/` | `/layanan/#sticker-sandblast` |
| `/layanan/sticker-one-way-vision/` | `/layanan/#sticker-one-way-vision` |
| `/layanan/sticker-riben/` | `/layanan/#sticker-riben` |
| `/layanan/kaca-film/` | `/layanan/#kaca-film` |
| `/layanan/sticker-printing/` | `/layanan/#sticker-printing` |
| `/layanan/cutting-sticker/` | `/layanan/#cutting-sticker` |
| `/layanan/wrapping-branding-mobil/` | `/layanan/#wrapping-branding-mobil` |
| `/layanan/huruf-timbul-3d/` | `/layanan/#huruf-timbul-3d` |
| `/layanan/neon-box-papan-nama/` | `/layanan/#neon-box-papan-nama` |
| `/testimoni/` | `/tentang-kami/#testimoni` |
| `/area/` dan `/area/{kota}/` | `/tentang-kami/#area` |
| `/galeri-video/` | `/portofolio/#video` |
| `/faq/` | `/kontak/#faq` |

Catatan: WordPress tidak mengirim fragment (`#anchor`) ke server, sehingga redirect 301 di atas hanya berlaku bila klien mengirim URL tanpa fragment. URL tujuan tetap wajib benar; untuk kasus yang memerlukan, pakai halaman pengalihan yang menampilkan ringkasan singkat dan tautan ke anchor tujuan.

## 3. Inventaris halaman

| # | Halaman | URL | Template (Elementor) | Keyword utama (hipotesis) | Prioritas |
|---|---|---|---|---|---|
| 1 | Beranda | `/` | Page | sticker sandblast bali, jasa pasang sticker kaca bali | P1 |
| 2 | Tentang Kami | `/tentang-kami/` | Page (`#cerita`, `#testimoni`, `#area`) | (brand + kepercayaan) | P1 |
| 3 | Layanan (9 blok + harga + estimasi) | `/layanan/` | Page | jasa sticker bali, harga sticker sandblast bali | P1 |
| 4 | Portofolio | `/portofolio/` | Page (Gallery + filter; `#foto`, `#video`) | contoh sticker sandblast | P2 |
| 5 | Kontak | `/kontak/` | Page (`#hubungi`, `#penawaran`, `#faq`) | (konversi) | P1 |
| 6 | Index artikel | `/artikel/` | Archive template (di luar 5 halaman) | (informasional) | P2 |
| 7 | Template artikel | `/artikel/{slug}/` | Single Post template | per artikel | P2 |

Halaman yang sudah dihapus: `harga`, `testimoni`, `area` + 7 halaman kota, `layanan` (template 9 halaman), `galeri-video`, `faq` — isi masing-masing pindah ke anchor di halaman 5 halaman (lihat tabel di bagian 2).

Global (Theme Builder): Header, Footer, floating tombol WhatsApp, 404, dan popup opsional "Minta penawaran".

## 4. Pemetaan anchor layanan ke keyword

Tiap baris adalah satu blok di dalam `/layanan/`, bukan URL terpisah. H2 blok diberi kata kunci utama sebagai heading, dan paragraf pembuka memakai varian.

| Anchor di `/layanan/` | Keyword utama (H2 blok) | Varian |
|---|---|---|
| `#sticker-sandblast` | sticker sandblast bali | pasang sticker sandblast, sandblast kaca bali, sticker kaca buram |
| `#sticker-one-way-vision` | sticker one way vision bali | one way bali, sticker kaca tembus pandang satu arah |
| `#sticker-riben` | sticker riben bali | film riben, sticker kaca riben |
| `#kaca-film` | kaca film bali | kaca film gedung, kaca film 3M bali, kaca film rumah villa |
| `#sticker-printing` | print sticker bali | cetak sticker, sticker promosi |
| `#cutting-sticker` | cutting sticker bali | cutting sticker motor mobil, sticker logo toko |
| `#wrapping-branding-mobil` | wrapping mobil bali | branding mobil, sticker mobil kantor |
| `#huruf-timbul-3d` | huruf timbul bali | huruf timbul akrilik, papan nama huruf timbul |
| `#neon-box-papan-nama` | neon box bali | papan nama, signage |
| `#harga` | harga sticker sandblast bali | harga sticker per meter, biaya pasang kaca film |

Ejaan: KBBI menulis "stiker", tetapi kompetitor dan kemungkinan besar pencarian memakai "sticker". Domain memakai "stikers". Tulis "sticker" di title, H1, dan nama anchor layanan untuk mengikuti pola pencarian, dan sebut "stiker" sebagai varian di isi teks. Verifikasi dengan Google Keyword Planner sebelum final.

## 5. Navigasi

**Header**: Logo · Beranda · Tentang Kami · Layanan (dropdown: 9 layanan + "Lihat semua layanan" + "Harga & estimasi") · Portofolio (Galeri Foto, Galeri Video) · Artikel · Kontak · tombol "Chat WhatsApp" (CTA, sticky di mobile).

**Footer** (4 kolom): (1) logo, deskripsi singkat, sosial media · (2) Menu utama: Beranda, Tentang Kami, Layanan, Harga & estimasi, Portofolio, Galeri Video, Testimoni, Area layanan, FAQ, Artikel, Kontak · (3) Layanan: 9 tautan ke anchor di `/layanan/` · (4) Kontak: WhatsApp, alamat, jam, link Maps. Baris bawah: hak cipta, kebijakan privasi.

**Floating**: tombol WhatsApp bulat, kanan bawah, semua halaman. Di mobile diganti bar bawah "WhatsApp" dan "Telepon".

## 6. Aturan internal linking

- Halaman `/layanan/`: tiap blok layanan menaut ke blok lain yang relevan, ke `#harga`, ke `/portofolio/#foto`, ke `/kontak/#penawaran`, dan ke 1 artikel pendukung. Grid kartu di bagian atas menaut ke anchor blok masing-masing.
- Halaman `/tentang-kami/`: bagian `#area` menaut ke 3 layanan utama di `/layanan/#slug`, ke portofolio, dan ke `/kontak/`.
- Setiap artikel menaut ke 1 anchor layanan di `/layanan/` dan, bila relevan, ke `/tentang-kami/#area` (anchor deskriptif, bukan "klik di sini").
- Breadcrumb di semua halaman selain Beranda.

## 7. Quality gate

- Tidak ada halaman per layanan, jadi tidak ada risiko doorway dari pengulangan. Kedalaman konten dijaga lewat 9 blok yang masing-masing punya H2 berkeyword, 1–2 paragraf unik, dan 3–4 poin manfaat; target 250+ kata unik per blok (bukan 800 kata per halaman).
- Blok area di `/tentang-kami/#area` memuat satu daftar kawasan dengan satu paragraf per kawasan — tanpa 7 halaman terpisah, teks tetap spesifik per lokasi (villa di Canggu, toko di Denpasar, hotel di Nusa Dua).
- Halaman Artikel tetap punya target 800+ kata unik per artikel (situs referensi hanya sekitar 550–650 kata, ini celah).

## 8. Schema markup

| Halaman | Schema |
|---|---|
| Beranda | `LocalBusiness` (lengkap: alamat, geo, jam, `areaServed`, `priceRange`, `sameAs`), `WebSite` |
| Layanan | `Service` (provider = LocalBusiness, satu per blok, `Service` di dalam `ItemList`), `BreadcrumbList` |
| Tentang Kami | `AboutPage`, `BreadcrumbList` |
| Portofolio | `ImageGallery` dengan `ImageObject` |
| Artikel | `BlogPosting`, `BreadcrumbList` |
| Kontak | `ContactPage`, `LocalBusiness` |

Catatan kebijakan Google yang membuat template industri perlu disesuaikan:
- **Jangan pasang `AggregateRating` untuk review milik sendiri** pada LocalBusiness/Organization. Google tidak menampilkan bintang untuk self-serving reviews. Testimoni ditampilkan sebagai konten biasa. Bintang di hasil pencarian datang dari Google Business Profile.
- **`FAQPage`** tidak lagi memunculkan rich result untuk situs biasa sejak 2023. Tetap dipasang karena struktur pertanyaan-jawaban eksplisit membantu AI search, bukan untuk mengharapkan tampilan khusus di SERP.
- **`HowTo`** tidak dipakai (rich result sudah dihentikan). Alur order 3 langkah cukup sebagai konten.

## 9. Core Web Vitals (target)

LCP ≤ 2,5 detik, INP ≤ 200 ms, CLS ≤ 0,1 di mobile. Konsekuensi untuk Elementor: hero memakai satu gambar (bukan slider seperti Slider Revolution di situs referensi), gambar WebP/AVIF dengan `width`/`height`, lazy-load di bawah fold, font maksimal 2 keluarga dengan `font-display: swap`, dan minim add-on pihak ketiga.
