# IMPLEMENTATION-ROADMAP — Sticker Sandblast Bali

Tanggal disusun: 2026-09-21. Empat fase mengikuti kerangka `seo-plan`. Anggaran dan tim belum diketahui, jadi estimasi durasi memakai asumsi: satu pemilik bisnis yang memasok data dan foto, satu pembuat situs Elementor, satu penulis.

## Data wajib sebelum konten final (blocker peluncuran)

Tanpa ini, situs hanya bisa berupa mockup dengan placeholder. Daftar lengkap ada di `DESIGN-BRIEF.md` bagian 7. Sudah terkonfirmasi: brand (Sticker Sandblast Bali), domain (`stikersandblastbali.com`), WhatsApp, alamat, dan jam operasional. Yang masih menentukan: logo, email, harga cutting dan layanan lain, foto proyek asli beserta kawasan, dan klaim yang boleh dipublikasikan (garansi, one-day service, home service). Untuk GBP: samakan nama, telepon, dan website dengan situs (lihat `SEO-STRATEGY.md` bagian 5.1).

## Fase 1 — Fondasi (minggu 1–4)

Tujuan: situs inti yang bisa dipakai, cepat, dan terlacak.

| Minggu | Pekerjaan | Keluaran |
|---|---|---|
| 1 | Kumpulkan data wajib; tetapkan nama, domain, hosting; audit dan rapikan Google Business Profile (nama, kategori, NAP) | Data bisnis lengkap; GBP konsisten |
| 1–2 | Setup WordPress + Elementor Pro; tema ringan (Hello Elementor); Global Colors/Fonts dari `DESIGN-BRIEF.md`; Theme Builder (header, footer, single page/post, archive, 404) | Kit dan template global siap |
| 2–3 | Bangun 5 halaman sesuai `ELEMENTOR-SPEC.md`: Beranda, Tentang Kami, Layanan (9 blok + harga + estimator), Portofolio, Kontak | Halaman inti dengan konten final |
| 3 | Schema (LocalBusiness, Service, BreadcrumbList), plugin SEO, sitemap, `robots.txt`, redirect, HTTPS | Schema tervalidasi di Rich Results Test |
| 3–4 | Analytics: GA4, Search Console, event WhatsApp/telepon/formulir/Maps; formulir penawaran + notifikasi | Pelacakan konversi aktif |
| 4 | QA: PageSpeed mobile, aksesibilitas, tautan, uji formulir dan WhatsApp di perangkat nyata; pengiriman sitemap | Situs siap tayang |

Kriteria selesai fase 1: semua halaman inti terbit tanpa placeholder tersisa; LCP mobile ≤ 2,5 s; formulir dan tombol WhatsApp teruji; sitemap terkirim; GBP dan situs memakai NAP yang sama.

## Fase 2 — Ekspansi (minggu 5–12)

| Pekerjaan | Keluaran |
|---|---|
| Portofolio (`#foto` + `#video`) dan testimoni asli di `/tentang-kami/#testimoni` (dengan izin) | Bukti sosial di semua halaman utama |
| Blok area di `/tentang-kami/#area`: satu paragraf spesifik per kawasan, **hanya** bila ada proyek nyata di sana | 7 kawasan dengan konten lokal unik dalam satu section |
| Blog: publikasi artikel bulan 1–3 dari `CONTENT-CALENDAR.md` | 8–12 artikel |
| Internal linking sesuai aturan `SITE-STRUCTURE.md` bagian 6 (anchor layanan, anchor area, artikel) | Cluster layanan-area-artikel terhubung |
| Optimasi GBP: foto rutin, postingan, layanan, permintaan review asli | Review dan sinyal lokal bertambah |
| Sitasi lokal: direktori bisnis Bali/Indonesia dengan NAP identik | 10–20 sitasi konsisten |

Kriteria selesai: seluruh halaman terindeks, minimal 5 review Google baru, artikel pertama mulai menerima impresi.

## Fase 3 — Skala (minggu 13–24)

| Pekerjaan | Keluaran |
|---|---|
| Studi kasus dan video pemasangan | Konten bukti yang sulit ditiru |
| Link building yang wajar: mitra lokal (kontraktor, arsitek, pengelola properti), direktori, mention media lokal | Backlink relevan, bukan massal |
| Optimasi GEO/AI search: jawaban ringkas di awal halaman, tabel, FAQ terstruktur, pemantauan kutipan di ChatGPT/Perplexity/AI Overviews | Peluang dikutip AI |
| Perbaikan berdasarkan Search Console: judul, meta, halaman dengan impresi tinggi klik rendah | CTR naik |
| Optimasi performa lanjutan (gambar, font, script pihak ketiga) | CWV tetap lolos saat konten bertambah |

## Fase 4 — Otoritas (bulan 7–12)

Seri proyek bulanan, panduan tahunan harga dan bahan, kolaborasi dengan profesional lokal, PR lokal, pembaruan schema lanjutan (mis. `ImageGallery`, `VideoObject`), dan optimasi berkelanjutan berbasis data konversi. Evaluasi ulang strategi keyword dan cakupan kawasan setelah 6 bulan data nyata.

## Sumber daya

- Pemilik bisnis: data, foto, video, review, persetujuan klaim (±2–4 jam per minggu pada fase 1).
- Pembuat situs Elementor: fase 1 penuh, lalu ±4–8 jam per bulan.
- Penulis/editor: 1 artikel per minggu mulai fase 2.
- Alat: Elementor Pro, plugin SEO, hosting + CDN, GA4, Search Console, alat keyword (Keyword Planner gratis atau alat berbayar).

## Dependensi dan risiko

- Peluncuran bergantung pada data bisnis dan foto asli. Tanpa itu, tunda bagian yang membutuhkannya (blok harga, blok area, testimoni) daripada menayangkan klaim yang tidak terbukti.
- Elementor Pro dibutuhkan untuk Theme Builder, Form, Loop Grid, dan Gallery dengan filter. Kalau hanya Elementor Free, `ELEMENTOR-SPEC.md` mencantumkan pengganti.
- Perubahan nama brand setelah tayang berdampak pada GBP, schema, dan sitasi; putuskan nama sebelum fase 1 minggu 2.
- Mitigasi risiko lain ada di `SEO-STRATEGY.md` bagian 8.

## Kriteria sukses per fase

| Fase | Ukuran keberhasilan |
|---|---|
| 1 | Situs tayang tanpa placeholder, CWV mobile lolos, konversi terlacak |
| 2 | Semua halaman terindeks, ≥ 5 review baru, permintaan penawaran organik pertama masuk |
| 3 | Keyword long-tail lokal mulai posisi 1–10, chat WhatsApp organik naik bulan ke bulan |
| 4 | Pertumbuhan stabil klik organik dan permintaan penawaran; artikel/halaman kunci dikutip AI |
