# SEO-STRATEGY — Sticker Sandblast Bali

Tanggal: 2026-09-21 · Template: `local-service` · Mode: situs baru (domain belum live)
Dokumen pendukung: `SITE-STRUCTURE.md`, `COMPETITOR-ANALYSIS.md`, `CONTENT-CALENDAR.md`, `IMPLEMENTATION-ROADMAP.md`, `DESIGN-BRIEF.md`.

## 1. Discovery

| Aspek | Status |
|---|---|
| Jenis bisnis | Jasa lokal: sticker sandblast, one way vision, riben, kaca film, cutting, printing, wrapping, huruf timbul, neon box |
| Wilayah | Bali. Basis: Ubung, Denpasar Utara (alamat dari GBP) |
| Target pelanggan | Pemilik/pengelola villa, hotel, restoran, kantor, klinik, toko, dan rumah tinggal; pemilik kendaraan untuk cutting dan wrapping |
| Konversi utama | Chat WhatsApp (0822-2692-0230), lalu formulir permintaan penawaran, lalu klik telepon dan rute Maps |
| Domain | `stikersandblastbali.com` (dikonfirmasi user) |
| Situs saat ini | Belum ada situs untuk domain ini |
| Google Business Profile | Ada. Kategori Percetakan Komersial, 4,9 dari 57 ulasan, jam 09.00–17.00 setiap hari, ada daftar produk dengan harga dan postingan rutin (terakhir 9 Sep 2026). Website yang tertaut di GBP adalah `stickersandblastbali.com` (ejaan berbeda), bukan domain baru |
| Belum diketahui | Harga cutting dan layanan lain, anggaran, target bulanan |

## 2. Posisi kompetitif

Ringkasan dari `COMPETITOR-ANALYSIS.md`: kompetitor lokal (Art Sticker, Triwikrama, Dafodil) seragam biru/putih, tanpa harga, tanpa alur order jelas, dan halaman area hanya berupa daftar nama kota. Peluang menang ada di: **harga transparan, bukti kerja yang bisa diperiksa, halaman layanan yang lebih dalam, halaman area berkonten lokal, dan kecepatan mobile.**

Otoritas domain kompetitor tidak diperkirakan karena tidak ada data backlink. Asumsi yang perlu diuji: kompetitor yang sudah beroperasi bertahun-tahun memiliki keunggulan backlink dan ulasan, jadi kemenangan di 6 bulan pertama datang dari long-tail lokal (layanan + kawasan) dan Google Business Profile, bukan dari keyword kepala seperti "sticker bali".

## 3. Strategi keyword

Hipotesis (belum ada data volume; verifikasi dengan Google Keyword Planner atau DataForSEO sebelum menetapkan target):

| Cluster | Contoh keyword | Halaman |
|---|---|---|
| Layanan inti | sticker sandblast bali, pasang sticker kaca bali, kaca film bali, cutting sticker bali, wrapping mobil bali, huruf timbul bali, neon box bali | `/layanan/#{slug}` (sembilan anchor di satu halaman) |
| Layanan + kota | sticker sandblast denpasar, kaca film canggu, jasa sticker ubud | `/tentang-kami/#area` (satu blok area dengan 7 paragraf kawasan) |
| Harga | harga sticker sandblast per meter, biaya pasang kaca film | `/layanan/#harga` (dan `#estimasi` untuk kalkulator) |
| Informasional | sandblast vs one way vision, cara memilih sticker kaca, perawatan sticker sandblast | `/artikel/` |
| Kepercayaan/brand | nama brand + testimoni/portofolio | `/tentang-kami/#testimoni`, `/portofolio/` |

Aturan: satu halaman satu maksud pencarian. Halaman layanan menangkap maksud "pakai jasa" (sembilan blok di satu halaman, masing-masing H2 berkeyword), artikel menangkap maksud "belajar", dan blok area di `/tentang-kami/#area` menangkap maksud "di kota saya" dengan satu paragraf per kawasan.

## 4. Arsitektur dan konten

Lihat `SITE-STRUCTURE.md`. Prinsip: satu halaman layanan dengan sembilan blok beranchor sebagai pilar, blok area di `/tentang-kami/#area` sebagai penopang lokal, `#harga` + `#estimasi` sebagai pembeda, artikel sebagai jalur informasional, dan internal linking sesuai aturan bagian 6 dokumen tersebut.

## 5. E-E-A-T (bagi bisnis jasa lokal)

- **Experience**: foto proyek asli dengan kawasan, jenis kaca, ukuran, dan tanggal; before/after; video pemasangan.
- **Expertise**: halaman layanan mendalam (bahan, ketahanan, perawatan, batasan), penulis artikel bernama dengan bio singkat.
- **Authoritativeness**: profil di Google Business Profile, direktori lokal, mention dari klien (dengan izin).
- **Trustworthiness**: alamat dan jam operasional nyata, NAP konsisten, kebijakan garansi tertulis, harga "mulai dari" yang jujur, kebijakan privasi, dan testimoni asli dengan izin.

Tidak ada satu pun klaim (tahun pengalaman, jumlah proyek, klien, garansi) yang boleh ditulis sebelum bisa dibuktikan.

## 5.1 Google Business Profile dan NAP

- **Nama**: GBP klien bernama "pusat sticker Bali & sticker sandblast bali | kaca film" dan deskripsinya menyebut "dafodil printing", sedangkan brand situs ini "Sticker Sandblast Bali". Rekomendasi untuk klien: samakan nama GBP dengan nama bisnis yang dipakai di papan nama, situs, dan kontak. Nama yang dijejali keyword melanggar pedoman GBP dan berisiko ditangguhkan.
- **Website**: field website di GBP menaut ke `stickersandblastbali.com` (ejaan "stickers"), bukan `stikersandblastbali.com`. Ubah ke domain baru setelah situs live.
- **Telepon**: situs memakai 0822-2692-0230 untuk WhatsApp dan telepon, sedangkan GBP mencantumkan 0813-3730-2965. Samakan nama, alamat, dan nomor (NAP) di situs, GBP, dan direktori (mis. jadikan 0822-2692-0230 nomor utama di GBP dan 0813-3730-2965 nomor tambahan) supaya sinyal lokal tidak terpecah.
- **Review**: 4,9 dari 57 ulasan Google per 2026-09-21. Halaman pencarian hanya menampilkan 3 kutipan tanpa nama dan tanggal. Untuk menampilkan review lengkap dengan atribusi resmi, pakai widget review Google atau Places API dari akun pengelola.
- Setelah data lengkap: kategori utama dan tambahan, layanan beserta deskripsi, area layanan berupa kota/kawasan (bukan seluruh provinsi), foto proyek rutin, tautan WhatsApp, dan strategi meminta review asli.

## 6. Fondasi teknis

- WordPress + Elementor, hosting dengan PHP 8.2+, cache server-level, dan CDN gambar.
- Target Core Web Vitals mobile: LCP ≤ 2,5 s, INP ≤ 200 ms, CLS ≤ 0,1. Hero satu gambar (tanpa slider), gambar WebP/AVIF, font maksimal 2 keluarga.
- Plugin SEO (Yoast, Rank Math, atau SEOPress) untuk meta, sitemap XML, dan schema; hindari dua plugin sitemap bersamaan.
- HTTPS, canonical, `robots.txt` yang mengizinkan crawler, sitemap dikirim ke Search Console.
- Schema: lihat `SITE-STRUCTURE.md` bagian 8 (LocalBusiness, Service, BlogPosting, dan catatan kebijakan review/FAQ/HowTo).
- Kesiapan AI search: jawaban ringkas di awal tiap blok layanan, tabel harga dan kalkulator yang bisa dikutip, FAQ terstruktur di `#faq-layanan` dan `/kontak/#faq`, dan `robots.txt` yang tidak memblokir crawler AI yang diinginkan. `llms.txt` bersifat opsional dan tidak dipakai Google Search.
- Analytics: GA4 + Search Console, event untuk klik WhatsApp, klik telepon, kirim formulir, dan klik "Lihat Maps".

## 7. KPI

Baseline semua nol karena situs baru. Target berikut adalah **asumsi perencanaan**, bukan prediksi; revisi setelah 4–6 minggu data pertama.

| Metrik | Baseline | 3 bulan | 6 bulan | 12 bulan |
|---|---|---|---|---|
| Halaman terindeks | 0 | 25–35 | 45–60 | 70–90 |
| Keyword posisi 1–10 (long-tail lokal) | 0 | 5–10 | 20–35 | 50–80 |
| Klik organik per bulan | 0 | 50–150 | 300–800 | 1.000–2.500 |
| Chat WhatsApp dari organik per bulan | 0 | 5–15 | 25–60 | 80–200 |
| Review Google (asli) | dari GBP saat ini | +5 | +15 | +40 |
| Core Web Vitals (mobile, lolos) | — | 100% halaman inti | 100% | 100% |

Metrik bisnis yang lebih penting daripada traffic: jumlah permintaan penawaran per bulan, rasio permintaan menjadi order, dan biaya per lead dibandingkan iklan.

## 8. Risiko dan mitigasi

| Risiko | Mitigasi |
|---|---|
| Kompetitor lama unggul di backlink dan review | Fokus long-tail layanan + kawasan, GBP, dan review asli; bangun sitasi lokal |
| Konten tipis atau mirip antar kawasan | Gate kualitas di `SITE-STRUCTURE.md` bagian 7; setiap kawasan dapat satu paragraf spesifik (tipe bangunan, contoh kebutuhan), tidak boleh menyalin |
| Klaim tidak terbukti (angka, klien, testimoni) | Semua ditandai placeholder sampai ada bukti |
| Nama, telepon, dan website di GBP berbeda dari situs | Samakan sesuai bagian 5.1; dikerjakan oleh pengelola GBP (klien) |
| Elementor berat di mobile | Container flexbox, tanpa slider, minim add-on, audit PageSpeed tiap rilis |
| Data belum lengkap (alamat, harga, foto) menahan peluncuran | Roadmap fase 1 memuat daftar data wajib; peluncuran ditunda sampai lengkap |
| Ketergantungan pada satu kanal (WhatsApp) | Tambah formulir penawaran dan klik telepon sebagai jalur cadangan |
