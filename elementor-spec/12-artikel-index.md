# 12 — Index Artikel (`/artikel/`)

Sections in mockup: **5** `<section>` di dalam `<main>` (hero foto besar, artikel unggulan, grid 7 kartu "Baca juga", kategori + pagination, CTA). Sumber: `mockup/artikel.html` (kode `mockup/src/pages/artikel.html`; CSS `pages-c.css` bagian "Artikel: index"). Delapan artikel di halaman: 1 unggulan + 7 kartu. Resep di `../ELEMENTOR-SPEC.md` bagian 2.9 dan 5; struktur hero foto di subbagian "Hero foto besar" pada master; tabel foto di master, bagian media library.

## 1. Pengaturan template

| Item | Nilai |
|---|---|
| Tipe | Theme Builder **Archive**: "Archive — Artikel" (Display Conditions: Include > Archive > Posts Archive) dan salinan "Archive — Artikel (Kategori)" tanpa section unggulan (Include > Archive > Categories). WordPress: Settings > Reading > Posts page = halaman "Artikel" (slug `artikel`), Blog pages show at most **7**; Settings > Permalinks: struktur kustom `/artikel/%postname%/`, Category base `kategori` (menghasilkan `/artikel/kategori/{slug}/`) |
| URL | `/artikel/` (halaman 2+: `/artikel/page/2/`); kategori: `/artikel/kategori/panduan/`, `/artikel/kategori/harga/`, `/artikel/kategori/perawatan/`, `/artikel/kategori/bahan/` (kategori artikel, bukan halaman harga) |
| Layout | Elementor Full Width; judul halaman tidak dipakai (H1 ditulis di hero template) |
| Header / Footer | Global (menu aktif: Artikel) |
| Kelas hook | `sbb-page-artikel`; kartu `sbb-card-post`; kartu unggulan `sbb-post-featured`; kartu ke-7 lebar `sbb-card-post--wide` |
| CSS / kode | Tidak ada JS. CSS kartu, kategori chip, dan pagination di Kit CSS (master 2.8); CSS kartu lebar di bagian 3 |
| Penulis | Semua artikel diterbitkan oleh akun WP dengan Display Name "Tim Sticker Sandblast Bali" |

## 2. Tabel section

| # | Section | Container | Widget dan setelan utama (copy persis mockup) | Responsif | Interaksi / kode | Sumber konten |
|---|---|---|---|---|---|---|
| 1 | Hero foto besar `--page` | `HERO-FOTO` varian `page` (master 2.10 "Hero foto besar"): Container Full Width `sbb-hero-photo sbb-hero-photo--page` (62vh, batas 440–620; mobile 56vh, batas 400–520), Custom CSS `selector{--focus:50% 40%}` > Image latar + Container overlay `sbb-hero-photo__overlay` + Container Boxed 1200 `sbb-hero-photo__inner` | Image `sbb-hero-photo__img` `hero-artikel.webp` (1920×1278), Object Position 50% 40% (`--focus`), Loading **eager** tanpa lazy + Custom Attributes `fetchpriority\|high`, `decoding\|async`; alt "Dua teknisi merentangkan lembar film bening di ruang pemasangan sebelum menempelkannya pada mobil". Overlay `sbb-hero-photo__overlay` Ink 900 `#111111` (gradasi per breakpoint di kolom Responsif). Inner: `TPL-BC` "Beranda > Artikel" (varian terang `sbb-bc--light`, teks White) · Eyebrow terang "Artikel dan panduan" (pil Ink 900 alfa .72, teks Red 300) · **H1** White "Artikel & Panduan Sticker Kaca di Bali" · Lead White "Panduan singkat memilih bahan, menghitung biaya, mengukur kaca, dan merawat sticker. Ditulis untuk pemilik villa, kantor, dan toko di Bali." · Button Row: `BTN-WA` "Tanya lewat WhatsApp" (`https://wa.me/6282226920230`, tab baru, `rel="noopener"`) + `BTN-SEC-L` "Baca artikel unggulan" (`/artikel/sticker-sandblast-vs-one-way-vision-vs-kaca-film/`) · **Badge chips** (Icon List horizontal Wrap, `aria-label` "Tentang artikel"; pil frosted gelap Ink 900 alfa .45, blur 10, border White alfa .32, teks White 15px 600, ikon Red 300 20px): ikon kunci pas "Ditulis oleh Tim Sticker Sandblast Bali" · ikon jam "Diperbarui September 2026" | Overlay (master 2.10): ≥ 1025 gradasi 90° Ink 900 alfa .88 → .72 (66%) → .30, teks maks 640px / 62% lebar; 768–1024 seragam .72; ≤ 767 overlay .12 + gradasi 0 → .72 dalam 72px di container inner, teks menempel di bawah, tombol penuh lebar, chip wrap | Tanpa Reveal di hero | Statis di template |
| 2 | Artikel unggulan | `SEC(putih)`: Eyebrow lalu kartu unggulan | Eyebrow "Artikel unggulan". **Loop Grid** 1 kolom (`LI-ARTIKEL-UNGGULAN`): Source Posts, Query ID `sbb_artikel_unggulan` (artikel yang ditandai sticky, bagian 3), Posts Per Page 1. Item = container Grid 2 kolom (bg White, border 1px Border, radius 14, Overflow Hidden, hover border Red 600, klik penuh): Image 16:9 (featured `g-02-glass-hallway.webp` 900×600, Loading **lazy**, alt "Lorong kantor dengan sekat kaca bermotif titik dan lantai kayu") · kolom teks (padding 44/24, gap 12, Justify Center): kategori "Panduan" (14px 700 uppercase Red 600) · **H2** "Sticker sandblast vs one way vision vs kaca film: mana yang cocok?" (24–32px, Ink 900) · excerpt 17px Text "Tiga bahan yang sering dibandingkan punya tugas berbeda: menyamarkan pandangan, menampilkan gambar tanpa menutup pandangan keluar, atau mengurangi panas. Pahami perbedaannya sebelum memilih." · meta 14px Text Muted (ikon 18px Red 600): tanggal "18 September 2026" · penulis "Tim Sticker Sandblast Bali" · ikon jam "6 menit baca" | ≥ 1025: dua kolom (1,1fr / 0,9fr, gambar min-height 380). ≤ 1024: gambar di atas teks | Kartu klik penuh. Judul memakai H2 (satu-satunya judul di section ini; `aria-labelledby` = judul) | Post Info (Date "j F Y", Author, Terms) + ACF `waktu_baca` (Number; After " menit baca"). Artikel unggulan: satu post sticky (pilihan editor) |
| 3 | Grid "Baca juga" (7 kartu) | `SEC(alt)`: `HEAD` + Loop Grid 3 kolom | Eyebrow "Artikel lainnya" · H2 "Baca juga". **Loop Grid** `LI-ARTIKEL`: Source **Current Query** (agar pagination dan kategori bekerja), Posts Per Page 7, unggulan dikeluarkan (bagian 3), Columns 3 / 2 / 1, Gap 24. Kartu: Image 16:9 (hover zoom 1,03, Loading **lazy**) · kategori · H3 judul (19px) · excerpt 15px Text Muted · meta (tanggal, waktu baca). Tujuh kartu, urutan tampil (tabel di bawah) | 3 → 2 → 1. Kartu ke-7 melebar penuh satu baris di ≥ 768 (foto 5fr / teks 7fr) | Kartu klik penuh (container Link = Post URL). Ring fokus 2px Red 600 offset 2 | **Post** WordPress (kategori bawaan) |
| 4 | Kategori + pagination | `SEC(putih)`: `HEAD` + chip + pagination | Eyebrow "Kategori" · H2 "Telusuri berdasarkan topik" · **Nav Menu** (Pro, Layout Horizontal, menu WP "Kategori Artikel", `aria-label` "Kategori artikel", class `sbb-chip-menu`): Semua (`/artikel/`) · Panduan · Harga · Perawatan · Bahan. Item aktif: latar Ink 900 teks putih (otomatis dari state "current"). **Pagination** (opsi Loop Grid section 3: Pagination = Numbers + Previous/Next, Prev Label "Sebelumnya", Next Label "Berikutnya", `aria-label` "Halaman artikel"): urutan "Sebelumnya" (nonaktif di halaman 1) · 1 (aktif) · 2 · 3 · "Berikutnya"; tombol 44x44, border 1px Border, radius 10; halaman aktif Ink 900 teks putih | Chip wrap; pagination rata tengah (margin-top 48), wrap di mobile | Pagination hanya muncul bila artikel di luar unggulan lebih dari 7 | Menu WP "Kategori Artikel" (kategori post) |
| 5 | Bar CTA akhir | `TPL-CTA` | H2 "Kirim foto kaca Anda, kami hitungkan estimasinya." + Text "Sebutkan jenis layanan dan ukuran kira-kira. Balasan awal lewat WhatsApp, dan harga final dipastikan setelah kaca diukur langsung." + `BTN-WA` "Chat WhatsApp" + `BTN-SEC-L` "Minta penawaran" (`/kontak/#penawaran`) | Tumpuk di ≤ 1024 | Reveal | Template global |

**Tujuh kartu section 3** (semua penulis "Tim Sticker Sandblast Bali"; tanggal = Post Date; menit = ACF `waktu_baca`; Loading lazy):

| # | Kategori | Judul (H3) | Excerpt | Tanggal | Menit | Foto (ukuran, fokus) dan alt |
|---|---|---|---|---|---|---|
| 1 | Harga | Berapa harga pasang sticker sandblast di Bali? Faktor yang menentukan | Harga dihitung per meter persegi, tetapi total biaya juga dipengaruhi kerumitan motif, ketinggian kaca, jumlah panel, dan lokasi. Artikel ini menjelaskan tiap faktor. | 13 September 2026 | 7 | `g-05-shower-glass.webp` (900×601), "Kamar mandi modern dengan pintu kaca shower dan jendela kecil" |
| 2 | Bahan | Kaca film untuk rumah dan kantor: cara memilih tingkat kegelapan | Film yang lebih gelap menahan lebih banyak panas dan silau, tetapi juga mengurangi cahaya yang masuk. Kenali pertimbangan memilih dan jenis kaca yang perlu dicek lebih dulu. | 11 September 2026 | 6 | `g-31-tint-installer.webp` (900×600), "Teknisi meratakan film pada kaca jendela" |
| 3 | Panduan | Cara mengukur kaca sebelum memesan sticker sandblast | Ukur lebar dan tinggi bagian kaca yang terlihat, catat tiap panel secara terpisah, dan foto bingkainya. Begini caranya agar estimasi awal lebih akurat. | 9 September 2026 | 4 | `g-28-cafe-windows.webp` (900×1349, fokus 50% 35%), "Jendela kaca berbingkai lengkung pada kafe dengan meja di sisi dalam" |
| 4 | Panduan | Persiapan sebelum pemasangan sticker kaca: apa yang perlu dilakukan pemilik | Kaca yang bersih, akses yang lapang, dan keputusan motif yang jelas membantu pekerjaan berjalan lancar. Ini daftar persiapan yang bisa Anda lakukan lebih dulu. | 3 September 2026 | 4 | `g-04-bathroom-frost.webp` (900×601), "Kamar mandi berdinding abu-abu dengan pintu kaca shower dan wastafel" |
| 5 | Perawatan | Cara membersihkan sticker sandblast tanpa merusak | Kain mikrofiber lembap dan sabun ringan cukup untuk sebagian besar kotoran. Kenali bahan pembersih dan alat yang sebaiknya dihindari. | 27 Agustus 2026 | 5 | `svc-riben.webp` (900×675), "Kamar mandi dengan panel kaca frosted, handuk putih, dan wastafel ganda" |
| 6 | Perawatan | Berapa lama sticker sandblast bertahan di iklim Bali? | Panas, sinar UV, dan kelembapan memengaruhi umur film. Simak faktor yang menentukan dan tanda film mulai perlu diganti. | 20 Agustus 2026 | 5 | `area-nusa-dua.webp` (900×675, fokus 50% 60%), "Resor di atas tebing dengan kolam renang di bawah sinar matahari terik" |
| 7 (lebar) | Panduan | Sticker kaca untuk kafe dan restoran: logo, jam buka, dan privasi meja | Kaca depan kafe berfungsi sebagai papan nama sekaligus pembatas ruang. Panduan ini membahas penempatan logo, jam buka, dan strip privasi setinggi mata tanpa menghalangi pandangan ke dalam. | 12 Agustus 2026 | 5 | `g-22-glass-lettering.webp` (900×623), "Kaca etalase restoran dengan tulisan logo dan pantulan bangunan bata" |

Slug tiap artikel (`/artikel/{slug}/`): unggulan `sticker-sandblast-vs-one-way-vision-vs-kaca-film`; kartu 1–7 berurutan `harga-pasang-sticker-sandblast-bali`, `memilih-kaca-film-rumah-kantor`, `cara-mengukur-kaca-sticker-sandblast`, `persiapan-sebelum-pemasangan-sticker-kaca`, `cara-membersihkan-sticker-sandblast`, `umur-sticker-sandblast-iklim-bali`, `sticker-kaca-kafe-restoran`.

## 3. Pengaturan pagination, unggulan, dan kartu lebar

- Section 2 dan 3 sama-sama memakai Loop Grid; **hanya section 3** memakai Source Current Query dan pagination. Section 2 memakai Source Posts dengan Query ID `sbb_artikel_unggulan`; salinan template kategori tidak memuat section 2.
- Posts Per Page di Settings > Reading (7) harus sama dengan Loop Grid (7) agar jumlah halaman konsisten. Artikel unggulan = satu artikel yang ditandai "Stick this post to the front page"; snippet (Code Snippets, PHP):

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

- Kartu ke-7 lebar: Loop Grid section 3 > Advanced > Custom CSS:

```css
@media (min-width:768px){
 selector .e-loop-item:nth-child(7){grid-column:1/-1}
 selector .e-loop-item:nth-child(7) .sbb-card-post{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr)}
 selector .e-loop-item:nth-child(7) .sbb-card-post__media img{height:100%;aspect-ratio:auto;min-height:240px}
 selector .e-loop-item:nth-child(7) .sbb-card-post__body{justify-content:center;padding:clamp(24px,3vw,40px)}
}
```

- Slug artikel awal sesuai bagian 2 (sumber: `data-real-url` mockup dan `CONTENT-CALENDAR.md`).

## 4. Aset media

| File (`mockup/assets/img/photos/`) | Ukuran | Dipakai di | Loading |
|---|---|---|---|
| `hero-artikel.webp` | 1920×1278 | Section 1, Image latar hero | eager, `fetchpriority=high` |
| `g-02-glass-hallway.webp` | 900×600 | Section 2, foto artikel unggulan | lazy |
| `g-05-shower-glass.webp` | 900×601 | Section 3, kartu 1 (Harga) | lazy |
| `g-31-tint-installer.webp` | 900×600 | Section 3, kartu 2 (Bahan) | lazy |
| `g-28-cafe-windows.webp` | 900×1349 | Section 3, kartu 3 (Panduan, fokus 50% 35%) | lazy |
| `g-04-bathroom-frost.webp` | 900×601 | Section 3, kartu 4 (Panduan) | lazy |
| `svc-riben.webp` | 900×675 | Section 3, kartu 5 (Perawatan) | lazy |
| `area-nusa-dua.webp` | 900×675 | Section 3, kartu 6 (Perawatan, fokus 50% 60%) | lazy |
| `g-22-glass-lettering.webp` | 900×623 | Section 3, kartu 7 lebar (Panduan) | lazy |

Foto tiap artikel adalah featured image post. Semua foto stok Pexels; alt menggambarkan isi foto dan tidak mengklaim itu proyek bisnis.

## 5. SEO

| Item | Nilai |
|---|---|
| `<title>` (≤ 60) | Artikel & Panduan Sticker Kaca, Sandblast di Bali (49 karakter) |
| Meta description (≤ 155) | Panduan memilih bahan, menghitung biaya, mengukur kaca, dan merawat sticker sandblast, one way vision, dan kaca film untuk pemilik bangunan di Bali. |
| H1 | Artikel & Panduan Sticker Kaca di Bali |
| Target keyword | panduan sticker kaca bali (informasional, prioritas P2) |
| Schema | `CollectionPage` (opsional) dan `BreadcrumbList`; tiap artikel memakai `BlogPosting` di template single |
| Canonical dan pagination | Halaman 2+ self-canonical, `rel=prev/next` tidak wajib; halaman kategori self-canonical; tidak `noindex` |
| Internal link wajib | Tiap artikel di grid ke halaman single; kategori chip; `/layanan/` dan `/layanan/#harga` lewat CTA dan teks |

## 6. QA

- [ ] Hero: teks putih terbaca di atas foto pada 1440, 768, 390; dua chip badge tidak menutupi tombol; gambar hero eager + `fetchpriority=high`
- [ ] `/artikel/`, `/artikel/kategori/panduan/`, dan `/artikel/page/2/` berfungsi tanpa 404 (Settings > Permalinks disimpan ulang)
- [ ] Artikel unggulan tidak muncul lagi di grid; halaman kategori tidak memuat unggulan; grid memuat tepat 7 kartu di halaman 1
- [ ] Kartu ke-7 melebar penuh satu baris di 768 dan 1440 (foto kiri, teks kanan) dan menumpuk normal di 390
- [ ] Setiap kartu memakai foto, alt, tanggal, dan waktu baca sesuai tabel bagian 2; penulis "Tim Sticker Sandblast Bali"
- [ ] Pagination: "Sebelumnya" nonaktif di halaman 1; halaman aktif ditandai `aria-current="page"`
- [ ] Chip kategori (Semua, Panduan, Harga, Perawatan, Bahan): item aktif tampil Ink 900; tap target ≥ 44 px
- [ ] Kartu klik penuh, ring fokus 2px Red 600 terlihat; satu H1, H2 unggulan dan H2 "Baca juga" berurutan
