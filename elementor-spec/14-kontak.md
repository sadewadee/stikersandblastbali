# 14 — Kontak (`/kontak/`) dan Formulir Penawaran

Sections in mockup: **6** `<section>` di dalam `<main>` (hero foto besar, dua kolom kartu kontak `#hubungi` + formulir `#penawaran`, peta Google Maps, area layanan, FAQ 18 pertanyaan `#faq`, CTA). Sumber: `mockup/kontak.html` (kode `mockup/src/pages/kontak.html`; CSS `pages-c.css` bagian "Kontak" dan `styles.css` bagian 5.13; JS `pages-c.js` fungsi `initQuoteForm` + filter FAQ). Resep di `../ELEMENTOR-SPEC.md` bagian 2.9 dan 5; struktur hero foto di subbagian "Hero foto besar" pada master; tabel foto di master, bagian media library.

Dokumen ini menggabungkan spec lama `11-faq.md` (halaman `/faq/`, dihapus): FAQ 18 pertanyaan + filter kategori kini bagian dari halaman ini pada anchor `#faq`. **Anchor (wajib persis):** `#hubungi` `#penawaran` `#faq`

## 1. Pengaturan halaman

| Item | Nilai |
|---|---|
| URL / tipe | `/kontak/` · Page statis |
| Page Layout | Elementor Full Width · Hide Title On |
| Header / Footer | Header standar (menu aktif: Kontak) · Footer global |
| Kelas hook | `sbb-page-kontak`; kartu kontak `sbb-contact-card`; peta `sbb-map`; CSS ID **`penawaran`** pada container yang membungkus judul "Minta penawaran" dan formulir (tujuan semua tombol "Minta penawaran" di situs: `/kontak/#penawaran`) |
| CSS halaman | Tabel jam (`.hours`), kotak peta `.sbb-map` (bagian 2, section 3), dan gaya galat formulir (bagian 3) |
| Kode | Formulir native: tidak perlu JS. Formulir persis mockup (Opsi B bagian 3) memuat `initQuoteForm` |

## 2. Tabel section

| # | Section | Container | Widget dan setelan utama (copy persis mockup) | Responsif | Interaksi / kode | Sumber konten |
|---|---|---|---|---|---|---|
| 1 | Hero foto besar `--page` | `HERO-FOTO` varian `page` (master 2.10): Container Full Width `sbb-hero-photo sbb-hero-photo--page` (62vh, batas 440–620; mobile 56vh, batas 400–520), Custom CSS `selector{--focus:50% 50%}` > Image latar + Container overlay + Container Boxed 1200 `sbb-hero-photo__inner` | Image `sbb-hero-photo__img` `hero-kontak.webp` (1920×1280), Object Position 50% 50% (`--focus`), Loading **eager** tanpa lazy + `fetchpriority\|high`, `decoding\|async`; alt "Ruang kantor berdinding dan bersekat kaca bening dengan meja kerja dan jendela besar menghadap kota". Inner: `TPL-BC` "Beranda > Kontak" (varian terang `sbb-bc--light`, teks White) · Eyebrow terang "Kontak" (pil Ink 900 alfa .72, teks Red 300) · **H1** White "Kontak & Minta Penawaran Sticker Kaca di Denpasar" · Lead White "Kirim foto kaca dan ukuran kira-kira lewat WhatsApp, atau isi formulir di bawah. Kami membalas dengan estimasi awal, dan harga final dipastikan setelah kaca diukur langsung." · Button Row: `BTN-WA` "Chat WhatsApp" (`https://wa.me/6282226920230`, tab baru, `rel="noopener"`) + `BTN-SEC-L` "Isi formulir penawaran" (anchor `#penawaran`) · **Badge chips** (Icon List horizontal Wrap, `aria-label` "Ringkasan kontak"; pil frosted gelap Ink 900 alfa .45, blur 10, border White alfa .32, teks White 15px 600, ikon Red 300 20px): ikon jam "Senin–Minggu 09.00–17.00" · ikon penggaris "Survey lokasi gratis" · ikon pesan "4,9 dari 57 ulasan Google" | Overlay master 2.10: ≥ 1025 gradasi 90° alfa .88 → .72 → .30; 768–1024 .72; ≤ 767 .12 + gradasi pelindung teks, teks menempel di bawah, tombol penuh lebar, chip wrap | Tanpa Reveal di hero | Statis |
| 2 | Kartu kontak + formulir | `SEC(frost)` (`aria-labelledby` "Hubungi kami") > container Row "contact-grid": kolom kiri 42,5% (0,85fr) dan kanan 57,5% (1,15fr), gap 64, Align Start (≥ 1025); ≤ 1024: Column, gap 48 | **Kiri**: H2 "Hubungi kami" + 6 kartu (container Grid 48px + 1fr, gap 16, padding 24, border 1px Border, radius 14, bg White, Reveal; ikon lingkaran Gray 50 48px, ikon Red 600 32px; label 14px 600 uppercase Text Muted; nilai Plus Jakarta 700 19px Ink 900; catatan 15px Text Muted): (1) **WhatsApp** · link "0822-2692-0230" (`https://wa.me/6282226920230`, tab baru) · "Cara tercepat: kirim foto kaca dan ukuran kira-kira." · `BTN-WA` kecil (min-height 44) "Chat WhatsApp". (2) **Telepon** · link "0822-2692-0230" (`tel:+6282226920230`) · "Nomor yang sama dengan WhatsApp." (3) **Alamat workshop** · "Jl. Cokroaminoto Gg. Jempiring No. 15, Ubung, Kec. Denpasar Utara, Kota Denpasar, Bali 80111" · link "Buka di Google Maps" (`https://share.google/dNneYg3jdOXi641aj`, tab baru). (4) **Jam operasional** · HTML widget tabel `.hours` (`<caption>` sr-only "Jam operasional Sticker Sandblast Bali"; baris `th scope=row` + `td`: Senin, Selasa, Rabu, Kamis, Jumat, Sabtu, Minggu, masing-masing 09.00–17.00; garis bawah 1px Border, padding 6/0, 15px). (5) **Email** · link "info@stikersandblastbali.com" (`mailto:info@stikersandblastbali.com`) · "Untuk penawaran proyek besar dan kerja sama." (6) **Media sosial** (ikon Instagram) · 4 tautan (tab baru, tinggi 44, 600): "Instagram @stikersandblastbali" (`https://www.instagram.com/stikersandblastbali/`) · "TikTok @stikersandblastbali" (`https://www.tiktok.com/@stikersandblastbali`) · "Facebook Sticker Sandblast Bali" (`https://www.facebook.com/stikersandblastbali`) · "YouTube Sticker Sandblast Bali" (`https://www.youtube.com/@stikersandblastbali`). **Kanan** (ID `penawaran`): H2 "Minta penawaran" · Text "Isi formulir singkat ini. Isian bertanda wajib dibutuhkan agar kami bisa membalas." · **Form widget** (bagian 3) | Kartu 1 kolom di semua ukuran. Formulir: 2 kolom field di ≥ 768, 1 kolom di mobile | Tautan telepon dan WhatsApp diberi event GA4 (master bagian 7); Reveal kartu berurutan | Kartu statis (NAP identik dengan footer dan JSON-LD) |
| 3 | Peta Google Maps | `SEC(putih)` (`aria-labelledby` "peta-title"): `HEAD` + container peta | Eyebrow "Lokasi" · H2 "Workshop kami di Ubung, Denpasar Utara" · **HTML widget** berisi kotak peta `sbb-map` + iframe (kode di bawah tabel). Di bawah kotak (Row space-between, Wrap, gap 12/24, margin atas 16): Text (maks 60ch) "Jl. Cokroaminoto Gg. Jempiring No. 15, Ubung, Kec. Denpasar Utara, Kota Denpasar, Bali 80111. Buka Senin–Minggu, 09.00–17.00." + `BTN-SEC` "Buka di Google Maps" (ikon peta, `https://share.google/dNneYg3jdOXi641aj`, tab baru, `rel="noopener"`) | Rasio kotak peta 4:3 (mobile) dan 21:9 (≥ 768); baris alamat dan tombol wrap, tombol penuh di mobile | iframe di bawah lipatan: `loading="lazy"`. Bila persetujuan cookie diterapkan, muat setelah izin | Embed Google Maps berdasar alamat workshop; koordinat tidak dimasukkan ke schema |
| 4 | Area layanan | `SEC(frost)`: `HEAD` + `CHIPS` | Eyebrow "Area layanan" · H2 "Kawasan yang kami layani" · Lead "Kawasan Anda belum tercantum? Teknisi datang ke seluruh Bali. Kirim lokasi lewat WhatsApp untuk jadwal dan biaya transport." · 7 chip (Denpasar, Ubud, Seminyak, Canggu, Sanur, Nusa Dua, Kuta → `/area/{kota}/`) | Chip wrap | `TPL-AREA-CHIPS`; Reveal | Statis |
| 5 | FAQ (`#faq`, 18 pertanyaan + filter kategori) | `SEC(alt)` (CSS ID `faq`): `HEAD` + container ber-`data-faq` (filter + Nested Accordion) | Eyebrow "Sebelum menghubungi" · H2 "Pertanyaan yang sering masuk" · Lead "Delapan belas jawaban singkat tentang harga, pemasangan, garansi, dan bahan. Pilih kategori untuk mempersempit daftar." **Filter kategori** (container `sbb-faq-filters`, `role="group"`, `aria-label` "Filter kategori pertanyaan", disembunyikan sampai JS aktif — atribut `hidden` pada markup, dilepas skrip bila JS hidup): 6 chip 44px `sbb-chip` `data-faq-filter` + `aria-pressed`: "Semua" (`all`, pressed true) · "Umum" (`umum`) · "Harga" (`harga`) · "Pemasangan" (`pemasangan`) · "Garansi" (`garansi`) · "Bahan" (`bahan`). Chip aktif: latar Ink 900, teks White. **Nested Accordion 18 item** (item 1 terbuka, Title HTML Tag H3, Max Items Expanded 1; tiap item `data-faq-cat` untuk filter: `umum` 3, `harga` 4, `pemasangan` 5, `garansi` 3, `bahan` 3). Pertanyaan & jawaban final: lihat bagian 3._filter di bawah. Notifikasi jumlah: baris status `aria-live="polite"` (`.sbb-faq-status`) menampilkan "Menampilkan N dari 18 pertanyaan" setelah filter | Chip wrap; grid 2 kolom ≥ 768, 1 kolom mobile; jawaban max 68ch; 1 item terbuka | Filter: JS kecil membaca `data-faq-cat` tiap item, menyembunyikan yang tidak cocok, memperbarui status, `aria-pressed` chip; **tanpa JS semua 18 tampil dan filter tetap tersembunyi** (progressive enhancement). FAQ Schema **On** (bagian 5) | Statis; 18 item ditulis di halaman ini |
| 6 | Bar CTA akhir | `TPL-CTA` | H2 "Kirim foto kaca Anda, kami hitungkan estimasinya." + Text "Sebutkan jenis layanan dan ukuran kira-kira. Balasan awal lewat WhatsApp, dan harga final dipastikan setelah kaca diukur langsung." + `BTN-WA` "Chat WhatsApp" + `BTN-SEC-L` "Minta penawaran" (`#penawaran` di halaman ini) | Tumpuk di ≤ 1024 | Reveal | Template global |

**HTML widget peta (section 3)**, tempel apa adanya:

```html
<div class="sbb-map">
  <iframe title="Peta lokasi workshop Sticker Sandblast Bali di Jl. Cokroaminoto Gg. Jempiring No. 15, Ubung, Denpasar Utara"
    src="https://www.google.com/maps?q=Jl.+Cokroaminoto+Gg.+Jempiring+No.+15,+Ubung,+Denpasar+Utara,+Bali&amp;output=embed"
    loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
</div>
```

CSS (Site Settings > Custom CSS, atau CSS widget HTML): `.sbb-map{position:relative;aspect-ratio:4/3;overflow:hidden;border:1px solid var(--sbb-border);border-radius:14px;background:var(--sbb-gray-50)}.sbb-map iframe{position:absolute;inset:0;display:block;width:100%;height:100%;border:0}@media(min-width:768px){.sbb-map{aspect-ratio:21/9}}`. Kotak beraspek tetap mencegah CLS saat iframe dimuat; `title` deskriptif menjadi nama aksesibel iframe.

## 3. Formulir penawaran (Form widget Pro), Opsi A native

Nama form "Minta penawaran" (Form Name), ID field lowercase seperti berikut, semua Label tampil, Required sesuai tabel. Urutan dan teks sama dengan `mockup/kontak.html`.

| Field (Type) | Label | Required | Setelan |
|---|---|---|---|
| `nama` (Text) | "Nama (wajib)" | Ya | Tanpa teks contoh di dalam field; lebar 50% |
| `whatsapp` (Tel) | "Nomor WhatsApp (wajib)" | Ya | Teks contoh di dalam field "08xx-xxxx-xxxx"; teks bantu "Nomor yang aktif di WhatsApp." (Description); lebar 50% |
| `layanan` (Select) | "Jenis layanan (wajib)" | Ya | Opsi: Pilih layanan (nilai kosong), Sticker Sandblast, Sticker One Way Vision, Sticker Riben, Kaca Film, Sticker Printing, Cutting Sticker, Wrapping & Branding Mobil, Huruf Timbul 3D, Neon Box & Papan Nama, Belum tahu, minta rekomendasi; lebar 50% |
| `ukuran` (Text) | "Perkiraan ukuran (m²)" | Tidak | Teks contoh di dalam field "mis. 4"; teks bantu "Kira-kira saja. Ukuran pasti dicek saat kaca diukur."; desimal 4,5 dan 4.5 diterima; lebar 50% |
| `area` (Select) | "Area atau kota (wajib)" | Ya | Opsi: Pilih area (nilai kosong), Denpasar, Ubud, Seminyak, Canggu, Sanur, Nusa Dua, Kuta, Kawasan lain di Bali; lebar 100% |
| `foto` (File Upload) | "Unggah foto kaca" | Tidak | Multiple Files On, tipe jpg, jpeg, png, webp; Max File Size 5 MB, Max Files 5; teks bantu "Foto dari dalam dan luar membantu estimasi. Format JPG, PNG, atau WebP."; lebar 100% |
| `catatan` (Textarea) | "Catatan" | Tidak | Rows 4; teks contoh di dalam field "Ceritakan kebutuhan Anda, misalnya motif, tinggi kaca, atau batas waktu."; lebar 100% |
| HTML | (pernyataan privasi) | - | "Dengan mengirim formulir, Anda setuju data ini dipakai untuk membalas permintaan Anda. Data tidak dibagikan ke pihak lain." (14px Text Muted) |
| Honeypot | - | - | Anti-spam tanpa skrip pihak ketiga |

- **Tombol kirim**: Text "Kirim permintaan", gaya `BTN-PRI` (Style > Button). Di sebelahnya Button widget `LINK-ARROW` "Atau chat langsung lewat WhatsApp" (`https://wa.me/6282226920230`, tab baru).
- **Layout field**: Column Width 50% untuk `nama`, `whatsapp`, `layanan`, `ukuran`; 100% untuk sisanya (tablet 50%, mobile 100%). Gap row 16, gap column 16. Gaya field: lihat master 2.4 (min-height 48, border 1px Text Muted, radius 10, fokus Red 600 2px offset 2px).
- **Actions After Submit**: Email (To `info@stikersandblastbali.com`, From = alamat domain (bukan alamat pengunjung), Subject "Permintaan penawaran baru: [field id="layanan"]", isi menyertakan semua field via `[all-fields]`), **Collect Submissions** (arsip di dasbor). Opsional: Webhook ke otomasi WhatsApp/CRM.
- **Custom Messages** (Additional Options): Success "Terima kasih. Permintaan penawaran Anda sudah kami terima. Balasan awal dikirim lewat WhatsApp ke nomor yang Anda isi, biasanya dalam 1 jam pada jam kerja (09.00–17.00)." · Error "Permintaan belum terkirim. Coba lagi, atau chat langsung lewat WhatsApp." · Required "Isian ini wajib diisi." · Invalid "Periksa kembali isian ini."
- **Gaya galat**: warna galat `--error` #C2410C (6,57:1 di atas putih), 14px 600, ikon "!" lewat CSS pada `.elementor-message-danger::before`; garis field invalid 1px + ring 1px `--error`.

**Pesan validasi final (satu sumber untuk Opsi B, Fluent Forms, dan Contact Form 7)**

| Field | Kondisi | Pesan |
|---|---|---|
| `nama` | kosong atau kurang dari 2 huruf | Tulis nama Anda, minimal 2 huruf. |
| `whatsapp` | kosong | Isi nomor WhatsApp Anda. |
| `whatsapp` | tidak cocok `^(\+62\|62\|0)8\d{8,11}$` setelah spasi, titik, tanda hubung, dan tanda kurung dibuang | Nomor belum valid. Gunakan nomor seluler Indonesia yang diawali 08. |
| `layanan` | belum dipilih | Pilih jenis layanan yang Anda butuhkan. |
| `ukuran` | terisi tetapi bukan angka lebih dari 0 dan maks 10000 (koma atau titik desimal) | Isi angka saja, misalnya 4 atau 6,5 (dalam m²). |
| `area` | belum dipilih | Pilih area atau kota pemasangan. |
| `foto` | berkas bukan gambar | Hanya berkas gambar (JPG, PNG, atau WebP) yang bisa diunggah. |
| Ringkasan (di atas formulir, `role="alert"`, saat kirim gagal) | N = jumlah field bermasalah | Ada N isian yang perlu diperbaiki: Nama, Nomor WhatsApp, Jenis layanan, Perkiraan ukuran, Area atau kota, Foto. (hanya label field yang bermasalah; fokus pindah ke field pertama yang salah) |

Perilaku galat: pesan tampil di bawah field (`aria-describedby`, `aria-invalid="true"`), divalidasi saat field kehilangan fokus bila sudah terisi atau setelah kirim pertama, dan divalidasi ulang tiap ketikan selama masih salah. Validasi ditunda saat pointer menekan tombol kirim agar tombol tidak bergeser.

**Layar sukses (mockup)**: formulir disembunyikan dan diganti panel putih (border 1px Border, radius 14, padding 40/24, `role="status"`, menerima fokus): lingkaran ikon centang 56px Gray 50 · H3 "Terima kasih, {nama}." · teks "Permintaan penawaran Anda sudah kami terima. Balasan awal dikirim lewat WhatsApp ke nomor yang Anda isi, biasanya dalam 1 jam pada jam kerja (09.00–17.00)." · `BTN-SEC` "Kirim permintaan lain" (mengosongkan formulir, menghapus galat, fokus ke field pertama).

**Cakupan Opsi A** (Form widget native): validasi browser (bubble) + pesan Elementor generik; pesan per field dan ringkasan "Ada N isian…", daftar nama berkas terpilih, serta layar sukses bernama dengan tombol "Kirim permintaan lain" berasal dari Opsi B. **Opsi B (persis mockup)**: HTML/Shortcode widget berisi markup `form.form-quote[data-quote-form]` dari `kontak.html` dan `initQuoteForm` (`pages-c.js`, dibungkus `DOMContentLoaded`, tanpa `SBB`), dengan pengiriman sebenarnya lewat `fetch` ke endpoint WordPress (admin-ajax atau REST) yang menyimpan berkas dan memicu email ke `info@stikersandblastbali.com`; endpoint wajib memakai nonce, validasi server, batas ukuran 5 MB × 5 berkas, dan antispam. **Fallback gratis**: Contact Form 7 atau Fluent Forms (unggah berkas, `aria-invalid`/`aria-describedby`, dan pesan per field dari tabel di atas).

## 3b. Daftar 18 pertanyaan FAQ (section 5, `data-faq-cat`)

Nomor = urutan di mockup. `data-faq-cat` dipakai filter kategori. Kategori: Umum 3, Harga 4, Pemasangan 5, Garansi 3, Bahan 3 (total 18).

| 1 | umum | Layanan apa saja yang tersedia? | Ada sembilan layanan: sticker sandblast, sticker one way vision, sticker riben, kaca film, sticker printing, cutting sticker, wrapping dan branding mobil, huruf timbul 3D, serta neon box dan papan nama. Semuanya ada di [halaman layanan] (`/layanan/`). |
| 2 | umum | Di mana lokasi workshop dan kapan jam operasionalnya? | Jl. Cokroaminoto Gg. Jempiring No. 15, Ubung, Kec. Denpasar Utara, Kota Denpasar, Bali 80111. Buka Senin–Minggu, 09.00–17.00. Kabari lebih dulu lewat WhatsApp sebelum datang agar tim siap menyambut Anda. |
| 3 | umum | Kawasan mana saja yang dilayani? | Denpasar, Ubud, Seminyak, Canggu, Sanur, Nusa Dua, dan Kuta, serta kawasan lain di seluruh Bali lewat home service. Survey lokasi gratis untuk Denpasar dan sekitarnya. Di luar Denpasar dikenakan biaya transport yang disepakati lewat WhatsApp. Kebutuhan tiap kawasan dibahas di [halaman area] (`/area/`). |
| 4 | harga | Berapa harga sticker sandblast? | Mulai dari Rp 135.000 / m². Harga final ditentukan setelah kaca diukur, karena dipengaruhi luas, kerumitan motif, ketinggian pemasangan, jumlah kaca, dan lokasi. |
| 5 | harga | Berapa harga one way vision, printing, cutting, dan layanan lain? | Harga mulai dari per m²: sticker one way vision Rp 195.000, sticker printing Rp 175.000, cutting sticker Rp 60.000, sticker riben Rp 95.000, kaca film Rp 165.000, wrapping dan branding mobil Rp 250.000, serta neon box dan papan nama Rp 950.000. Huruf timbul 3D dihitung Rp 35.000 per huruf. Ringkasannya ada di [halaman harga] (`/harga/`). |
| 6 | harga | Apa yang memengaruhi harga, dan apa saja yang sudah termasuk? | Harga dipengaruhi luas kaca, kerumitan motif atau desain, ketinggian dan akses pemasangan, jumlah kaca, serta lokasi. Harga sudah termasuk bahan, tenaga pemasangan, dan pembersihan setelah pemasangan. Pembuatan desain rumit, pembongkaran sticker lama, dan pemasangan di ketinggian yang butuh perancah tidak termasuk dan dihitung terpisah. |
| 7 | harga | Bagaimana cara pembayarannya? | Pembayaran lewat transfer bank atau tunai. Untuk pekerjaan produksi (huruf timbul 3D, neon box, dan wrapping), kami meminta DP 50% sebelum produksi dimulai. Sisanya dilunasi setelah pemasangan selesai. Untuk sticker kaca, pembayaran dilakukan setelah Anda mengecek hasil pemasangan. |
| 8 | pemasangan | Bagaimana alur pemesanannya? | Ada tiga langkah: konsultasi lewat WhatsApp dengan foto kaca, pengukuran dan penawaran, lalu pemasangan. Setelah film terpasang, Anda mengecek hasilnya di tempat bersama teknisi. |
| 9 | pemasangan | Berapa lama pemasangannya? | Sticker kaca 1–2 hari, kaca film gedung 2–5 hari, wrapping mobil 3–5 hari, dan huruf timbul serta neon box 5–10 hari (termasuk produksi). Untuk luas hingga 20 m² tersedia one-day service: pengerjaan selesai dalam 1 hari, tergantung antrean. |
| 10 | pemasangan | Apakah ada survey ke lokasi sebelum pemasangan? | Ada. Teknisi mengukur kaca langsung agar harga final akurat. Survey lokasi gratis untuk Denpasar dan sekitarnya. Di luar Denpasar dikenakan biaya transport yang disepakati lewat WhatsApp. |
| 11 | pemasangan | Apakah teknisi bisa datang ke lokasi saya? | Bisa. Home service tersedia di seluruh Bali: teknisi datang ke lokasi Anda untuk mengukur dan memasang. Biaya transport mengikuti jarak dan kami sebutkan sebelum Anda menyetujui penawaran. Kirim alamat atau lokasi lewat WhatsApp untuk memulai. |
| 12 | pemasangan | Apa yang perlu disiapkan sebelum pemasangan? | Geser perabot dan tirai dari area kaca, pastikan kaca bisa dijangkau, dan beri tahu bila kaca berada di ketinggian atau lantai atas. Kaca yang bersih dan bebas debu membantu hasil yang rapi. |
| 13 | garansi | Apakah ada garansi pemasangan? | Ada. Garansi pemasangan berlaku 30 hari: bila muncul gelembung atau sambungan terangkat, kami memperbaikinya tanpa biaya. Garansi tidak mencakup kerusakan akibat kesalahan pemakaian. |
| 14 | garansi | Berapa lama sticker bertahan? | Film sandblast kami umumnya bertahan 3–5 tahun di dalam ruangan. Pada kaca yang terkena matahari langsung, umurnya sekitar 2–3 tahun, tergantung kualitas bahan, kelembapan, dan cara perawatan. |
| 15 | garansi | Bagaimana jika film mengelupas atau bergelembung setelah dipasang? | Foto bagian yang bermasalah, lalu kirim lewat WhatsApp bersama keterangan lokasi dan tanggal pemasangan. Selama masa garansi 30 hari, perbaikan pemasangan seperti gelembung dan sambungan yang terangkat kami kerjakan tanpa biaya, dan kami jadwalkan teknisi untuk memperbaikinya. |
| 16 | bahan | Apa beda sandblast, one way vision, dan kaca film? | Sandblast menyamarkan pandangan dan tetap meneruskan cahaya. One way vision menampilkan gambar dari luar sambil membuka pandangan dari dalam. Kaca film membantu mengurangi panas dan silau. Bandingkan lengkapnya di [tabel perbandingan] (`/layanan/#perbandingan`) atau [artikel panduan] (`/artikel/sticker-sandblast-vs-one-way-vision-vs-kaca-film/`). |
| 17 | bahan | Apakah sticker bisa dilepas tanpa merusak kaca? | Bisa. Film dilepas perlahan dengan bantuan panas ringan, lalu sisa perekat dibersihkan. Makin lama film menempel dan makin terpapar matahari, makin sulit dilepas, jadi serahkan pada teknisi bila kacanya luas. Pembongkaran sticker lama dihitung terpisah dari harga pemasangan baru. |
| 18 | bahan | Bagaimana cara membersihkan kaca yang sudah ber-sticker? | Gunakan kain mikrofiber lembap dan sabun ringan. Hindari pisau, sikat kasar, dan pelarut seperti thinner atau pembersih beralkohol keras. Tunggu beberapa hari setelah pemasangan sebelum membersihkan, sesuai anjuran teknisi. |

### Filter kategori (6 chip)

Tombol `sbb-chip` dengan `data-faq-filter` (`all` | `umum` | `harga` | `pemasangan` | `garansi` | `bahan`) dan `aria-pressed`; `all` pressed true. Container `sbb-faq-filters` ber-`role="group"` + `aria-label` "Filter kategori pertanyaan" dan **atribut `hidden`** pada markup — skrip yang melepasnya hanya hidup bila JS aktif, sehingga tanpa JS chip tidak pernah tampil tanpa fungsi. JS kecil (~20 baris, Custom Code Body End): klik chip → set `aria-pressed` chip itu, lalu untuk tiap `.accordion__item` set `hidden` bila `data-faq-cat` ≠ nilai chip; perbarui baris status `aria-live="polite"` ("Menampilkan N dari 18 pertanyaan"). Tanpa JS: 18 item tampil apa adanya.

## 4. Aset media

| File (`mockup/assets/img/photos/`) | Ukuran | Dipakai di | Loading |
|---|---|---|---|
| `hero-kontak.webp` | 1920×1280 | Section 1, Image latar hero | eager, `fetchpriority=high` |

Halaman ini tidak memakai foto lain: peta adalah iframe Google Maps (section 3), kartu kontak memakai ikon. Foto hero adalah stok Pexels; alt menggambarkan isi foto.

## 5. SEO

| Item | Nilai |
|---|---|
| `<title>` (≤ 60) | Kontak & Minta Penawaran Sticker Kaca Denpasar (46 karakter) |
| Meta description (≤ 155) | Hubungi Sticker Sandblast Bali lewat WhatsApp 0822-2692-0230 atau isi formulir penawaran. Workshop di Ubung, Denpasar, buka Senin-Minggu 09.00-17.00. |
| H1 | Kontak & Minta Penawaran Sticker Kaca di Denpasar |
| Target keyword | kontak sticker sandblast denpasar (konversi, prioritas P1) |
| Schema | `ContactPage` + `LocalBusiness`; `FAQPage` untuk 18 pertanyaan di `#faq` (NAP: Jl. Cokroaminoto Gg. Jempiring No. 15, Ubung, Kec. Denpasar Utara, Kota Denpasar, Bali 80111; `openingHoursSpecification` Mo–Su 09:00–17:00; `telephone` +6282226920230; `email` info@stikersandblastbali.com; `sameAs` Instagram, TikTok, Facebook, YouTube). Tanpa `geo` dan tanpa `AggregateRating` |
| Internal link wajib | `/tentang-kami/#area` (chip kawasan), `/layanan/` + 9 anchor layanan, `/layanan/#harga`, `/portofolio/#foto` |

## 6. QA

- [ ] Anchor `#hubungi`, `#penawaran`, `#faq` berfungsi
- [ ] `#faq` menampilkan 18 accordion item dengan `data-faq-cat` benar (umum 3, harga 4, pemasangan 5, garansi 3, bahan 3)
- [ ] Filter 6 chip bekerja: memilih "Harga" menyisakan 4 item dan status menyebut jumlahnya; `aria-pressed` pindah; "Semua" mengembalikan 18
- [ ] Tanpa JS: 18 item tetap tampil dan container filter tetap tersembunyi (atribut `hidden`)
- [ ] Hanya satu item terbuka pada satu waktu; Esc/panah dapat dipakai keyboard
- [ ] FAQ Schema valid di Rich Results Test (tanpa markup yang tidak diizinkan)
- [ ] Hero: teks putih terbaca di atas foto pada 1440, 768, 390; tiga chip badge tidak menutupi tombol; tombol "Isi formulir penawaran" menggulir ke `#penawaran`; gambar hero eager + `fetchpriority=high`
- [ ] Kirim formulir terisi lengkap: email masuk ke `info@stikersandblastbali.com`, entri tersimpan di Submissions, berkas foto terlampir/tertaut, pesan sukses tampil
- [ ] Kirim kosong: field wajib ditandai, pesan galat sama dengan tabel pesan validasi, warna `--error` lolos kontras; uji dengan keyboard dan screen reader
- [ ] Nomor WhatsApp non-08xx ditolak dengan pesan tabel; ukuran `abc` ditolak; ukuran `6,5` diterima
- [ ] Unggah berkas non-gambar ditolak; berkas melebihi 5 MB atau lebih dari 5 berkas ditolak dengan pesan jelas
- [ ] `/kontak/#penawaran` (dari tombol di seluruh situs) menggulir ke formulir dengan offset sticky header
- [ ] Event GA4: klik WhatsApp, klik telepon, kirim formulir, klik "Buka di Google Maps"
- [ ] Peta: iframe Google Maps tampil, `title`, `loading="lazy"`, dan `referrerpolicy` terpasang; kotak beraspek 4:3 di 390 dan 21:9 di ≥ 768; tidak memperburuk LCP/CLS; tab order tidak terjebak di peta
- [ ] Jam operasional: tujuh baris Senin–Minggu 09.00–17.00; tautan email `mailto:` dan empat tautan sosial benar
- [ ] Alamat, jam, telepon, dan email sama persis dengan footer dan JSON-LD
