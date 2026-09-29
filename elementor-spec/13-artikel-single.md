# 13 — Template Artikel (`/artikel/{slug}/`), contoh: Sticker Sandblast vs One Way Vision vs Kaca Film

Sections in mockup: **6** `<section>` di dalam `<main>` (hero foto artikel dengan meta, daftar isi + isi artikel, penulis, artikel terkait, layanan terkait, CTA). Sumber: `mockup/artikel-single.html` (kode `mockup/src/pages/artikel-single.html`; CSS `pages-c.css` bagian "Artikel: single"; JS `pages-c.js` fungsi `initToc`). Resep di `../ELEMENTOR-SPEC.md` bagian 2.9 dan 5; struktur hero foto (varian `--article`) di subbagian "Hero foto besar" pada master; tabel foto di master, bagian media library.

## 1. Pengaturan template

| Item | Nilai |
|---|---|
| Tipe | Theme Builder **Single Post** ("Single — Artikel"); Display Conditions: Include > Singular > Posts (All) |
| URL | `/artikel/{slug}/` lewat permalink kustom `/artikel/%postname%/` |
| Layout | Elementor Full Width. Judul halaman tidak dipakai; H1 = widget Heading dinamis Post Title (tag H1) |
| Header / Footer | Global (menu aktif: Artikel) |
| Kelas hook | `sbb-page-artikel-single`; isi artikel dibungkus class `sbb-article` (Post Content widget: Advanced > CSS Classes); kotak penulis `sbb-author-box` |
| CSS | Tipografi `.sbb-article` dan komponen isi (callout, kotak CTA, figure, tabel) di Kit CSS (master 2.8) |
| Kode | Tidak ada JS: Table of Contents widget (Pro) menggantikan `initToc` |
| Field ACF `post` | `waktu_baca` (Number), `ringkasan_singkat` (Textarea, satu kalimat untuk kartu terkait), `hero_gambar` (Image; default `hero-artikel-single.webp`), `layanan_dibahas` (Relationship layanan, 1–3), `artikel_terkait` (Relationship post, 3; Query ID `sbb_acf_artikel_terkait`, tambahkan `'sbb_acf_artikel_terkait' => array( 'artikel_terkait', 3 )` ke array Query ID di master 4.5) |

## 2. Tabel section

| # | Section | Container | Widget dan setelan utama (copy persis mockup) | Responsif | Interaksi / kode | Sumber konten |
|---|---|---|---|---|---|---|
| 1 | Hero foto artikel (breadcrumb, judul, meta) | `HERO-FOTO` varian `page` + `--article`: Container Full Width `sbb-hero-photo sbb-hero-photo--page sbb-hero-photo--article` (62vh, batas 440–620; mobile 56vh, batas 400–520), Custom CSS `selector{--focus:50% 50%}` > Image latar + Container overlay + Container Boxed 1200 `sbb-hero-photo__inner`; tanpa tombol, badge, atau kartu | Image `sbb-hero-photo__img` `{hero_gambar}` = `hero-artikel-single.webp` (1920×1280), Object Position 50% 50% (`--focus`), Loading **eager** tanpa lazy + `fetchpriority\|high`, `decoding\|async`; alt "Ukiran motif daun dan bunga pada permukaan kaca hasil teknik sandblast, dilihat dari dekat". Inner: `TPL-BC` "Beranda > Artikel > Sandblast vs One Way Vision vs Kaca Film" ("Artikel" bertaut `/artikel/`; judul pendek dari kolom "Breadcrumbs title" SEO plugin; varian terang `sbb-bc--light`, teks White) · Eyebrow terang = kategori post (Post Info > Terms, "Panduan"; pil Ink 900 alfa .72, teks Red 300) · **H1** White Post Title "Sticker Sandblast vs One Way Vision vs Kaca Film: Mana yang Cocok?" (maks 26ch) · **meta** (Icon List horizontal Wrap, gap 4/20, White 15px 600, ikon Red 300 18px): Post Info **Date** "18 September 2026" · **Author** "Tim Sticker Sandblast Bali" · ikon jam + ACF `waktu_baca` "6 menit baca" (After " menit baca") | Overlay master 2.10: ≥ 1025 gradasi 90° alfa .88 → .72 → .30; 768–1024 .72; ≤ 767 .12 + gradasi pelindung teks, teks menempel di bawah. Meta wrap di mobile | Tanpa Reveal di hero | Post: title, kategori, tanggal, penulis, ACF `waktu_baca`, `hero_gambar` |
| 2 | Daftar isi + isi artikel | `SEC(putih)` tanpa padding atas (`sbb-section--flush-top`; `aria-label` "Isi artikel") > container Row "artikel-layout": kolom isi (fleksibel) + kolom TOC 290px, gap 64 (≥ 1025), Align Start. ≤ 1024: Column, TOC di atas isi (Order Start) | **Kolom TOC** (`aria-label` "Daftar isi"): **Table of Contents** widget (Pro): Headings H2, Container = `.sbb-article`, Marker View numbers, Collapse Subitems Off, judul "Daftar isi" (Title, Plus Jakarta 700 16px Ink 900), Minimize Box aktif (Minimized On: Tablet dan Mobile, default tertutup); kotak: bg Frost, border 1px Border, radius 14, padding 16/24; item 15px Text Muted, border kiri 2px Border, tinggi 44px; item aktif (state Active): bg Gray 50, border kiri Red 600, teks Ink 900 600. Desktop: container kolom TOC **Sticky Top** (Motion Effects > Sticky, Offset 100px, hanya Desktop). Entri mengikuti H2: "Tiga bahan, tiga tugas yang berbeda" · "Perbandingan cepat" · "Cara memilih: mulai dari masalahnya" · "Kesalahan yang sering terjadi" · "Berapa harga awalnya?" · "Langkah berikutnya" (anchor `#beda-fungsi`, `#perbandingan`, `#cara-memilih`, `#kesalahan-umum`, `#harga`, `#langkah-berikutnya`). **Kolom isi**: widget **Post Content** (class `sbb-article`, max 68 karakter/baris, kecuali tabel dan figure); isi lengkap di bagian 3 | Desktop: TOC di kanan dan mengikuti scroll. ≤ 1024: TOC di atas isi, terlipat | Highlight bagian aktif bawaan widget (menggantikan `initToc`). Scroll offset: `scroll-padding-top` = tinggi header + 16px (CSS master). ID anchor pada heading H2 (Advanced > CSS ID) | Isi: editor post (Gutenberg atau Elementor). Komponen isi lihat bagian 4 |
| 3 | Penulis | `SEC(putih)` flush-top: H2 sr-only "Tentang penulis" + kartu `sbb-author-box` | Container Grid 72px + 1fr, gap 16, bg Frost, border 1px Border, radius 14, padding 24, Align Start: Image bulat 72×72 (Dynamic Tag ACF user `foto_penulis` = `workshop-installer.webp`, 900×600, Object Fit Cover, Object Position 62% 50%, Loading **lazy**; alt "Tangan teknisi memasang film putih pada kap mobil dengan heat gun") · Column: Heading p 18px 700 Ink 900 (Author Info > Name) "Tim Sticker Sandblast Bali" · Text 14px Text Muted (ACF user `peran_penulis`) "Teknisi dan admin workshop, Ubung, Denpasar Utara" · Text Text Muted (Author Info > Bio) "Kami memasang sticker sandblast, one way vision, dan kaca film untuk villa, kantor, dan toko di Bali sejak lebih dari 10 tahun lalu. Artikel ini ditulis dari pertanyaan yang paling sering kami terima saat mengukur kaca di lokasi." | Sama di semua ukuran; avatar tidak mengecil | Reveal | Profil pengguna WP "Tim Sticker Sandblast Bali" (nama tampilan, bio, ACF user `foto_penulis`, `peran_penulis`) |
| 4 | Artikel terkait | `SEC(alt)`: `HEAD` + Loop Grid 3 | Eyebrow "Artikel terkait" · H2 "Lanjutkan membaca". **Loop Grid** `LI-ARTIKEL-TERKAIT` (= `LI-ARTIKEL` dengan excerpt dari ACF `ringkasan_singkat`): Source Posts, Query ID `sbb_acf_artikel_terkait`, Posts Per Page 3, Columns 3 / 2 / 1, Gap 24. Kartu: Image 16:9 (Loading **lazy**) · kategori · H3 · excerpt 15px · meta. (1) Harga · "Berapa harga pasang sticker sandblast di Bali? Faktor yang menentukan" · "Kenali faktor yang membuat total biaya berbeda dari harga per meter persegi." · 13 September 2026 · 7 menit baca · `g-05-shower-glass.webp` (900×601), alt "Kamar mandi modern dengan pintu kaca shower dan jendela kecil". (2) Panduan · "Cara mengukur kaca sebelum memesan sticker sandblast" · "Ukur tiap panel secara terpisah dan foto bingkainya agar estimasi awal lebih akurat." · 9 September 2026 · 4 menit baca · `g-28-cafe-windows.webp` (900×1349, fokus 50% 35%), alt "Jendela kaca berbingkai lengkung pada kafe dengan meja di sisi dalam". (3) Panduan · "Persiapan sebelum pemasangan sticker kaca: apa yang perlu dilakukan pemilik" · "Daftar persiapan yang bisa Anda lakukan lebih dulu sebelum teknisi datang." · 3 September 2026 · 4 menit baca · `g-04-bathroom-frost.webp` (900×601), alt "Kamar mandi berdinding abu-abu dengan pintu kaca shower dan wastafel" | 3 → 2 → 1 | Kartu klik penuh, ring fokus 2px Red 600 offset 2; Reveal berurutan | Post WordPress; ACF `artikel_terkait`, `ringkasan_singkat`, `waktu_baca` |
| 5 | Layanan terkait | `SEC(putih)`: `HEAD` + Loop Grid 3 | Eyebrow "Layanan terkait" · H2 "Layanan yang dibahas di artikel ini". **Loop Grid** `LI-LAYANAN-HARGA`, Query ID `sbb_acf_layanan_dibahas` (ACF Relationship `layanan_dibahas` pada post, 1–3 layanan). Kartu: Image 4:3 (featured layanan, Loading **lazy**) · H3 · `ringkasan_kartu` · harga "mulai dari [sbb_rupiah]" · "Lihat layanan" + panah. (1) **Sticker Sandblast** · `svc-sandblast.webp` (900×600), alt "Pintu kaca berlapis film frosted dengan bingkai kayu" · "Kaca tampak buram seperti disemprot pasir. Privasi terjaga, cahaya tetap masuk." · Rp 135.000 / m². (2) **Sticker One Way Vision** · `svc-one-way.webp` (900×600), alt "Dinding kaca kantor bernuansa gelap dengan meja kerja di baliknya" · "Cetak gambar atau logo di kaca. Dari dalam Anda tetap bisa melihat keluar." · Rp 195.000 / m². (3) **Kaca Film** · `svc-kaca-film.webp` (900×602), alt "Ruang rapat dengan sekat kaca berlapis film dan kursi hitam mengelilingi meja panjang" · "Film kaca yang membantu mengurangi panas dan silau di rumah, kantor, dan mobil." · Rp 165.000 / m² | 3 → 2 → 1 | Kartu klik penuh; Reveal berurutan | ACF pada post. Memenuhi aturan: 1 layanan wajib + link ke 1 area di isi artikel |
| 6 | Bar CTA akhir | `TPL-CTA` | H2 "Kirim foto kaca Anda, kami hitungkan estimasinya." + Text "Sebutkan jenis layanan dan ukuran kira-kira. Balasan awal lewat WhatsApp, dan harga final dipastikan setelah kaca diukur langsung." + `BTN-WA` "Chat WhatsApp" + `BTN-SEC-L` "Minta penawaran" (`/kontak/#penawaran`) | Tumpuk di ≤ 1024 | Reveal | Template global |

## 3. Isi artikel contoh (teks final untuk Post Content)

Paragraf pertama berkelas `lead`. Heading H2 memakai ID anchor di kurung.

**Lead**: Ketiganya sama-sama film yang ditempel di kaca, tetapi tugasnya berbeda. Salah pilih berarti privasi yang tidak terjaga, ruangan yang tetap panas, atau kaca yang terlalu gelap. Artikel ini membandingkan sticker sandblast, sticker one way vision, dan kaca film dari sisi fungsi, privasi, cahaya, dan harga awal, lalu membantu Anda memilih sesuai kebutuhan.

**H2 (`beda-fungsi`)** Tiga bahan, tiga tugas yang berbeda

- **H3** Sticker sandblast: menyamarkan pandangan. Sticker sandblast meniru tampilan kaca es. Permukaannya menyebarkan cahaya, sehingga benda di balik kaca hanya tampak sebagai bayangan samar sementara cahaya siang tetap masuk. Bahan ini dipilih ketika tujuan utamanya privasi: kamar mandi, ruang rapat, ruang periksa, atau sekat kaca. Sticker sandblast tidak dibuat untuk menahan panas, jadi jangan memilihnya bila panas matahari adalah masalah utama.
- **H3** Sticker one way vision: gambar di luar, pandangan tetap terbuka dari dalam. One way vision adalah film berlubang halus yang dicetak dengan gambar atau logo. Dari luar, yang terlihat adalah gambar cetaknya. Dari dalam, Anda tetap bisa melihat keluar melalui lubang-lubang halus itu. Efeknya bergantung pada cahaya. Saat sisi luar lebih terang daripada bagian dalam, gambar tampak jelas dari luar dan pandangan dari dalam tetap terbuka. Pada malam hari, ketika lampu di dalam menyala, efeknya bisa terbalik dan orang di luar dapat melihat ke dalam. Bahan ini cocok untuk etalase dan kaca depan kantor yang membutuhkan branding tanpa menutup pandangan keluar.
- **H3** Kaca film: mengatur panas dan silau. Kaca film dibuat untuk mengurangi panas, silau, dan sinar UV yang masuk. Tingkat kegelapannya bervariasi, dari bening sampai gelap atau reflektif seperti cermin. Film gelap atau reflektif juga memberi privasi di siang hari, tetapi berkurang saat malam bila lampu di dalam menyala. Sebagian jenis kaca, misalnya kaca tebal, berlapis, atau kaca ganda, perlu dicek lebih dulu karena panas dapat menumpuk di kaca setelah film dipasang.

**H2 (`perbandingan`)** Perbandingan cepat. Paragraf: "Tabel berikut merangkum perbedaan utamanya. Harga adalah harga mulai dari per meter persegi." Lalu tabel (`<caption>` "Perbandingan sticker sandblast, one way vision, dan kaca film"), kolom Bahan · Fungsi utama · Privasi · Cahaya masuk · Harga mulai dari:

| Bahan | Fungsi utama | Privasi | Cahaya masuk | Harga mulai dari |
|---|---|---|---|---|
| Sticker sandblast | Menyamarkan pandangan sekaligus dekoratif. | Tinggi. Benda di balik kaca hanya tampak samar. | Tinggi. Cahaya menyebar lembut. | Rp 135.000 / m² |
| One way vision | Branding atau iklan di kaca tanpa menutup pandangan keluar. | Bergantung cahaya. Efektif saat sisi luar lebih terang. | Berkurang sedikit karena film berlubang halus. | Rp 195.000 / m² |
| Kaca film | Membantu mengurangi panas, silau, dan sinar UV. | Sedang pada film gelap atau reflektif di siang hari. | Bergantung tingkat kegelapan film. | Rp 165.000 / m² |

Catatan 14px Text Muted (`article-note`): "Harga final ditentukan setelah kaca diukur." Figure 16:9: `g-02-glass-hallway.webp` (900×600, lazy), alt "Lorong kantor dengan sekat kaca bermotif titik yang meneruskan cahaya ke ruang kerja", caption "Sekat kaca bermotif titik: privasi sebagian terjaga, cahaya tetap mengalir ke lorong."

**H2 (`cara-memilih`)** Cara memilih: mulai dari masalahnya. Paragraf: "Tanyakan apa yang paling mengganggu pada kaca itu, lalu cocokkan dengan daftar berikut." Daftar centang (`check-list`, 5 butir): Orang di luar bisa melihat ke dalam kamar mandi atau ruang rapat: pilih sticker sandblast. · Anda ingin memasang logo atau promosi di etalase tanpa menutup pandangan keluar: pilih one way vision. · Ruangan terasa panas atau silau oleh matahari sore: pilih kaca film. · Anda ingin privasi sebagian dan ruangan tetap terang: pilih sticker sandblast bermotif strip atau titik. · Anda ingin privasi sekaligus mengurangi panas: tanyakan apakah kombinasi bahan memungkinkan untuk kaca Anda, dan cek jenis kacanya lebih dulu.

**Callout** (ikon info): judul "Satu bahan tidak menyelesaikan semua masalah"; teks "Sticker sandblast membuat ruangan privat, tetapi tidak banyak menahan panas. Kaca film menahan panas, tetapi tidak selalu memberi privasi, terutama malam hari. One way vision memberi tampilan, tetapi bukan pengganti tirai di kamar tidur. Tentukan satu masalah utama lebih dulu."

**Figure 16:9**: `g-31-tint-installer.webp` (900×600, lazy), alt "Teknisi meratakan film pada permukaan kaca jendela dengan alat perata", caption "Film diratakan bagian demi bagian agar tidak ada gelembung udara yang terperangkap."

**Kotak CTA tengah** (`TPL-POST-CTA`, bagian 4): "Masih ragu memilih bahan?" / "Kirim foto kaca Anda lewat WhatsApp, sebutkan masalah utamanya, dan kami bantu menyarankan bahan yang sesuai." / "Chat WhatsApp" + "Minta penawaran".

**H2 (`kesalahan-umum`)** Kesalahan yang sering terjadi. Daftar 5 butir (kalimat pertama tebal): **Memilih one way vision untuk kamar mandi.** Malam hari, saat lampu menyala, orang di luar bisa melihat ke dalam. · **Memilih film gelap tanpa mengecek jenis kaca.** Kaca tebal, berlapis, atau ganda menyerap panas lebih banyak dan perlu dicek lebih dulu. · **Membandingkan harga per m² saja.** Total biaya juga dipengaruhi luas, kerumitan motif, ketinggian kaca, dan jumlah panel. · **Tidak memotret dan mengukur kaca lebih dulu.** Harga awal bisa berubah setelah kaca diukur langsung. · **Memasang di kaca lengkung tanpa konsultasi.** Film mudah berkerut pada permukaan lengkung.

**H2 (`harga`)** Berapa harga awalnya? Dua paragraf: "Harga awal per meter persegi untuk ketiga bahan ini: sticker sandblast mulai dari Rp 135.000 / m², sticker one way vision mulai dari Rp 195.000 / m², dan kaca film mulai dari Rp 165.000 / m²." / "Angka tersebut adalah harga mulai dari. Harga final ditentukan setelah kaca diukur, karena dipengaruhi luas kaca, kerumitan motif, ketinggian dan akses pemasangan, jumlah panel, dan lokasi. Harga sudah termasuk bahan, tenaga pemasangan, dan pembersihan setelah pemasangan. Untuk menghitung luas kira-kira, kalikan lebar dan tinggi tiap panel dalam meter, lalu jumlahkan semuanya. Penjelasan lengkap ada di bagian [harga dan estimasi](/layanan/#harga) pada halaman layanan."

**H2 (`langkah-berikutnya`)** Langkah berikutnya. Paragraf: "Sebelum menghubungi kami, siapkan hal berikut agar estimasi awal bisa diberikan lebih tepat:" Daftar centang (4 butir): Foto kaca dari dalam dan dari luar, termasuk bingkai dan sekitarnya. · Ukuran kira-kira (lebar × tinggi) dan jumlah panel. · Jenis bangunan dan kawasan, misalnya ruko di Denpasar. · Masalah utama yang ingin diselesaikan: privasi, branding, atau panas. Penutup: "Setelah itu, buka [jasa pasang sticker sandblast](/layanan/#sticker-sandblast) untuk melihat penjelasan lengkap layanan itu, lalu bandingkan pilihan lainnya di halaman [layanan](/layanan/). Bila kaca Anda berada di Denpasar, baca juga info kawasan di [area layanan](/tentang-kami/#area). Survey lokasi kami gratis untuk Denpasar dan sekitarnya."

## 4. Komponen di dalam isi artikel

| Komponen mockup | Cara membuatnya di Elementor/WordPress |
|---|---|
| Lead paragraf (`.lead`) | Paragraf pertama dengan class `lead` (Gutenberg: Advanced > Additional CSS class); maks 60ch |
| Daftar centang (`.check-list`) | List block dengan class `check-list` (CSS master 2.8); dipakai di "Cara memilih" dan "Langkah berikutnya" |
| Daftar biasa | List block tanpa class; kalimat pertama tiap butir `strong` (bagian "Kesalahan yang sering terjadi") |
| Tabel perbandingan | Custom HTML block: `<div class="sbb-compare-wrap"><table class="sbb-compare">` dengan `<caption>` dan `data-label` per sel (CSS master 2.8; di mobile baris menjadi kartu berlabel). Kolom: Bahan, Fungsi utama, Privasi, Cahaya masuk, Harga mulai dari (kolom harga tidak dipatahkan di ≥ 768). Isi tabel di bagian 3 |
| Catatan tabel | Paragraf 14px Text Muted (`article-note`) "Harga final ditentukan setelah kaca diukur." |
| Figure + caption | Image block kelas `sbb-photo sbb-ar-16x9` (foto lazy, `width`/`height` dari bagian 5) dengan caption 14px Text Muted; `alt` deskriptif |
| Callout | Custom HTML block `<div class="sbb-callout">` ikon info 32px + judul "Satu bahan tidak menyelesaikan semua masalah" + teks (bagian 3), atau Saved Template callout lewat shortcode |
| **Kotak CTA tengah** ("Masih ragu memilih bahan?") | Saved Template `TPL-POST-CTA` (container bg Ink 900, radius 14, padding 32/20; H "Masih ragu memilih bahan?" 22px 800 putih; teks Border "Kirim foto kaca Anda lewat WhatsApp, sebutkan masalah utamanya, dan kami bantu menyarankan bahan yang sesuai."; `BTN-WA` "Chat WhatsApp" + `BTN-SEC-L` "Minta penawaran") disisipkan lewat Shortcode block `[elementor-template id="…"]` setelah figure kedua |
| Tautan internal | Anchor deskriptif: "harga dan paket", "jasa pasang sticker sandblast", "tabel perbandingan layanan", "layanan pemasangan di Denpasar" (bukan "klik di sini") |

## 5. Aset media

| File (`mockup/assets/img/photos/`) | Ukuran | Dipakai di | Loading |
|---|---|---|---|
| `hero-artikel-single.webp` | 1920×1280 | Section 1, Image latar hero (ACF `hero_gambar`) | eager, `fetchpriority=high` |
| `g-02-glass-hallway.webp` | 900×600 | Section 2, figure "Perbandingan cepat" (16:9) | lazy |
| `g-31-tint-installer.webp` | 900×600 | Section 2, figure setelah callout (16:9) | lazy |
| `workshop-installer.webp` | 900×600 | Section 3, avatar penulis (bulat 72px, fokus 62% 50%) | lazy |
| `g-05-shower-glass.webp` · `g-28-cafe-windows.webp` · `g-04-bathroom-frost.webp` | 900×601 · 900×1349 · 900×601 | Section 4, kartu artikel terkait 1 / 2 / 3 | lazy |
| `svc-sandblast.webp` · `svc-one-way.webp` · `svc-kaca-film.webp` | 900×600 · 900×600 · 900×602 | Section 5, kartu layanan terkait 1 / 2 / 3 | lazy |

Semua foto stok Pexels; alt menggambarkan isi foto dan tidak mengklaim itu proyek bisnis.

## 6. SEO

| Item | Nilai |
|---|---|
| `<title>` (≤ 60) | Sticker Sandblast vs One Way Vision vs Kaca Film (48 karakter) |
| Meta description (≤ 155) | Bandingkan sticker sandblast, one way vision, dan kaca film dari fungsi, privasi, cahaya, dan harga awal, lalu pilih yang sesuai kebutuhan kaca Anda. |
| H1 | Sticker Sandblast vs One Way Vision vs Kaca Film: Mana yang Cocok? |
| Target keyword | sandblast vs one way vision (informasional, per artikel) |
| Schema | `BlogPosting` (headline, `datePublished` 2026-09-18, `dateModified`, `author` Organization "Tim Sticker Sandblast Bali", `publisher` = LocalBusiness dengan logo, `image` = hero, `mainEntityOfPage`) + `BreadcrumbList`; tanpa `AggregateRating` |
| Internal link wajib | 1 anchor layanan di `/layanan/` + `/tentang-kami/#area` bila relevan (anchor deskriptif), `/layanan/#harga`, artikel terkait, layanan terkait |

## 7. QA

- [ ] Hero: teks putih terbaca di atas foto pada 1440, 768, 390; H1 tidak melebihi 26ch; meta (tanggal, penulis, waktu baca) satu baris di desktop dan wrap di mobile; gambar hero eager + `fetchpriority=high`
- [ ] TOC menyorot bagian aktif saat scroll; klik entri menggulir dengan offset header; di mobile terlipat dan bisa dibuka dengan keyboard
- [ ] Desktop: TOC sticky di kanan tanpa menimpa header; tablet/mobile: TOC di atas isi
- [ ] Tabel perbandingan menjadi kartu di 390 px dengan label; tidak overflow horizontal
- [ ] Baris isi tidak melebihi ±68 karakter; H2 26–32px; H3 24/22/20px
- [ ] Kotak CTA tengah menampilkan dua tombol yang berfungsi; kontras putih di atas Ink 900
- [ ] Kotak penulis: avatar `workshop-installer.webp` bulat 72px tidak mengecil di 320 px; nama, peran, dan bio sama dengan bagian 2 section 3
- [ ] Schema `BlogPosting` valid; tanggal `dateModified` diperbarui saat revisi
- [ ] Artikel terkait menampilkan tepat tiga kartu sesuai ACF `artikel_terkait` dan tidak memuat artikel yang sedang dibuka; layanan terkait sesuai ACF `layanan_dibahas`
