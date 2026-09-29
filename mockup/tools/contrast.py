#!/usr/bin/env python3
"""Kontras WCAG 2.x untuk semua pasangan teks/latar yang dipakai dari tabel token.

Token dibaca langsung dari assets/css/styles.css (blok :root) sehingga selalu
sinkron dengan CSS. Exit code 0 hanya bila semua pasangan wajib lolos.

    python3 mockup/tools/contrast.py

Jenis pasangan:
  N   teks normal        >= 4.5:1
  L   teks besar         >= 3.0:1  (>= 24px, atau >= 18.66px tebal)
  UI  komponen/ikon/fokus >= 3.0:1 (WCAG 1.4.11)

Spesifikasi warna:  nama-token | #RRGGBB | "nama@alpha/latar" = warna ber-alpha di atas latar
  (dipakai untuk panel frosted: white@0.72/blue-600 = putih 72% di atas blue-600).
  Susunan lapisan: "dasar>warna@alpha>warna@alpha" (lapisan ditumpuk dari kiri ke kanan).
  Alpha boleh angka atau nama token numerik --hero-* dari :root (mis. hero-a-min), sehingga
  pasangan hero foto dihitung dari nilai CSS sebenarnya, bukan angka yang ditulis ulang di sini.

Hero foto (.hero-photo): kasus terburuk = piksel foto PUTIH murni di bawah overlay hitam dengan
alfa minimum (--hero-a-min) di area teks. Eyebrow dan chip badge memakai pil gelap translusen
(--hero-pill-a / --hero-chip-a) di atas overlay.
Mobile (<=767px): bagian atas hero sengaja terang (--hero-a-top, hanya foto) supaya foto terbaca. TEKS TIDAK PERNAH
berada di zona itu: gradasi dipasang di .hero-photo__inner (bukan persentase tinggi hero) dan padding-top-nya
(--hero-fade + 4px) menjaga breadcrumb/eyebrow/H1/lead/tombol/badge di bawah titik alfa = --hero-a-min. Lapisan di area
teks = overlay --hero-a-top lalu gradasi --hero-a-min (alfa gabungan >= --hero-a-min), dihitung di pasangan "mobile".
"""
import re
import sys
from pathlib import Path

CSS = Path(__file__).resolve().parent.parent / "assets" / "css" / "styles.css"

# Latar terburuk di bawah panel frosted / label placeholder (warna gradien tergelap di CSS).
WORST_BACKDROPS = {
    "ph-img (dasar abu)": "#6E6E6E",
    "ph-img--deep (paling gelap)": "#1C1C1C",
}


def load_tokens():
    text = CSS.read_text(encoding="utf-8")
    block = re.search(r":root\s*\{(.*?)\n\}", text, re.S)
    if not block:
        sys.exit("ERROR: blok :root tidak ditemukan di styles.css")
    return {
        k: v.upper()
        for k, v in re.findall(r"--([\w-]+):\s*(#[0-9A-Fa-f]{6})\b", block.group(1))
    }


def load_numbers():
    """Token numerik --hero-* (alfa overlay) dari blok :root."""
    text = CSS.read_text(encoding="utf-8")
    block = re.search(r":root\s*\{(.*?)\n\}", text, re.S)
    return {
        k: float(v)
        for k, v in re.findall(r"--(hero-[\w-]+):\s*(\d*\.?\d+)\s*;", block.group(1))
    }


TOKENS = load_tokens()
NUMS = load_numbers()


def alpha_of(text):
    text = text.strip()
    if text in NUMS:
        return NUMS[text]
    return float(text)


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def resolve(spec):
    """Kembalikan (r, g, b) untuk nama token, hex, atau 'fg@alpha/bg'."""
    spec = spec.strip()
    if ">" in spec:
        parts = [p.strip() for p in spec.split(">")]
        cur = resolve(parts[0])
        for layer in parts[1:]:
            name, alpha = layer.split("@", 1)
            lr, lg, lb = resolve(name)
            a = alpha_of(alpha)
            cur = (
                lr * a + cur[0] * (1 - a),
                lg * a + cur[1] * (1 - a),
                lb * a + cur[2] * (1 - a),
            )
        return cur
    if "@" in spec:
        fg, rest = spec.split("@", 1)
        alpha, bg = rest.split("/", 1)
        fr, fg_, fb = resolve(fg)
        br, bg_, bb = resolve(bg)
        a = alpha_of(alpha)
        return (fr * a + br * (1 - a), fg_ * a + bg_ * (1 - a), fb * a + bb * (1 - a))
    if spec.startswith("#"):
        return hex_to_rgb(spec)
    if spec not in TOKENS:
        sys.exit(f"ERROR: token tidak dikenal: {spec}")
    return hex_to_rgb(TOKENS[spec])


def luminance(rgb):
    def chan(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (chan(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg, bg):
    l1, l2 = luminance(resolve(fg)), luminance(resolve(bg))
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


REQUIRED = {"N": 4.5, "L": 3.0, "UI": 3.0}

# (label, fg, bg, jenis, dipakai di)
PAIRS = [
    # --- galat formulir (token --error; dibedakan dari merah brand) ---
    ("error / white", "error", "white", "N", "pesan galat di kartu/formulir putih"),
    ("error / gray-50", "error", "gray-50", "N", "pesan galat di section alt"),
    ("error / frost", "error", "frost", "N", "pesan galat di section frost"),
    (
        "error / white (border input galat)",
        "error",
        "white",
        "UI",
        "border input aria-invalid",
    ),
    # --- pasangan wajib ---
    ("text / white", "text", "white", "N", "teks isi"),
    ("text-muted / white", "text-muted", "white", "N", "teks pendukung, kartu"),
    (
        "text-muted / frost",
        "text-muted",
        "frost",
        "N",
        "teks pendukung di section frost",
    ),
    (
        "text-muted / gray-50",
        "text-muted",
        "gray-50",
        "N",
        "teks pendukung di section alt",
    ),
    ("text / frost", "text", "frost", "N", "teks isi di section frost"),
    ("text / gray-50", "text", "gray-50", "N", "teks isi di section alt, callout"),
    ("red-600 / white", "red-600", "white", "N", "link, eyebrow, ikon"),
    ("red-600 / gray-50", "red-600", "gray-50", "N", "link, eyebrow di section alt"),
    ("red-600 / frost", "red-600", "frost", "N", "link, eyebrow di section frost"),
    (
        "white / red-600",
        "white",
        "red-600",
        "N",
        "tombol primer, promo-bar, ::selection",
    ),
    ("white / red-800", "white", "red-800", "N", "teks di ujung gelap gradasi pane"),
    ("white / wa-green", "white", "wa-green", "N", "tombol WhatsApp, bar bawah"),
    (
        "white / ink-900",
        "white",
        "ink-900",
        "N",
        "footer, section gelap, tabel head, chip aktif, hover tombol primer",
    ),
    (
        "red-300 / ink-900",
        "red-300",
        "ink-900",
        "N",
        "eyebrow, link, ikon di latar gelap",
    ),
    ("ink-900 / gray-50", "ink-900", "gray-50", "N", "judul di section alt"),
    # --- teks di berbagai latar terang ---
    ("ink-900 / white", "ink-900", "white", "N", "judul, tombol sekunder"),
    ("ink-900 / frost", "ink-900", "frost", "N", "judul di section frost"),
    ("ink-700 / white", "ink-700", "white", "N", "waktu langkah proses, aksen garis"),
    (
        "ink-700 / gray-50",
        "ink-700",
        "gray-50",
        "N",
        "aksen garis (dash-list) di section alt",
    ),
    # --- hover dan varian ---
    (
        "white / wa-green-hover",
        "white",
        "wa-green-hover",
        "N",
        "hover tombol WhatsApp",
    ),
    # --- latar gelap ---
    (
        "border / ink-900",
        "border",
        "ink-900",
        "N",
        "teks sekunder di footer, CTA, statistik",
    ),
    (
        "white / ink-900 (heading besar)",
        "white",
        "ink-900",
        "L",
        "angka statistik, H2 di latar gelap",
    ),
    (
        "white / ink-700",
        "white",
        "ink-700",
        "N",
        "judul di panel demo gelap (sg-on-pane)",
    ),
    # --- band pane merah (semua teks putih) ---
    (
        "white / red-600 (pane, teks isi)",
        "white",
        "red-600",
        "N",
        "teks/lead/link/eyebrow/text-muted di .section--pane",
    ),
    # --- panel frosted (worst case backdrop) ---
    (
        "ink-900 / frost-panel di atas red-600",
        "ink-900",
        "white@0.72/red-600",
        "N",
        "judul di panel frosted (worst case)",
    ),
    (
        "text / frost-panel di atas red-600",
        "text",
        "white@0.72/red-600",
        "N",
        "teks di hero-card, estimator, kartu harga frosted di pane",
    ),
    (
        "ink-900 / frost-panel di atas red-800",
        "ink-900",
        "white@0.72/red-800",
        "N",
        "judul panel frosted di ujung gelap gradasi pane",
    ),
    (
        "text / frost-panel di atas red-800",
        "text",
        "white@0.72/red-800",
        "N",
        "teks panel frosted di ujung gelap gradasi pane",
    ),
    (
        "red-600 / frost-panel di atas red-800 (ikon)",
        "red-600",
        "white@0.72/red-800",
        "UI",
        "ikon di panel frosted di ujung gelap gradasi pane",
    ),
    (
        "text-muted / white (teks kartu nilai di pane)",
        "text-muted",
        "white",
        "N",
        ".card-value__text di kartu putih pada band pane homepage",
    ),
    (
        "ink-900 / label di atas " + list(WORST_BACKDROPS)[0],
        "ink-900",
        "white@0.72/" + WORST_BACKDROPS["ph-img (dasar abu)"],
        "N",
        "label .ph-img",
    ),
    (
        "ink-900 / label di atas " + list(WORST_BACKDROPS)[1],
        "ink-900",
        "white@0.72/" + WORST_BACKDROPS["ph-img--deep (paling gelap)"],
        "N",
        "label .ph-img--deep, tag sebelum/sesudah",
    ),
    (
        "ink-900 / fallback panel (tanpa backdrop-filter)",
        "ink-900",
        "white@0.92/red-600",
        "N",
        "@supports not backdrop-filter",
    ),
    # --- komponen UI, ikon, fokus, garis ---
    (
        "red-600 / frost-panel di atas red-600 (ikon)",
        "red-600",
        "white@0.72/red-600",
        "UI",
        "ikon di badge/label",
    ),
    ("focus red-600 / white", "red-600", "white", "UI", "ring fokus di latar terang"),
    (
        "focus red-600 / gray-50",
        "red-600",
        "gray-50",
        "UI",
        "ring fokus di section alt",
    ),
    (
        "focus red-600 / frost",
        "red-600",
        "frost",
        "UI",
        "ring fokus di section frost",
    ),
    (
        "focus red-300 / ink-900",
        "red-300",
        "ink-900",
        "UI",
        "ring fokus di latar gelap",
    ),
    (
        "focus red-300 / ink-700",
        "red-300",
        "ink-700",
        "UI",
        "ring/ikon di latar gelap turunan; tidak ada TEKS red-300 di atas ink-700 (4,5 tidak tercapai: 3,89)",
    ),
    (
        "focus white / red-600",
        "white",
        "red-600",
        "UI",
        "ring fokus di pane merah dan promo-bar",
    ),
    (
        "text-muted / white (border input)",
        "text-muted",
        "white",
        "UI",
        "border input formulir",
    ),
    (
        "red-500 / white (non-teks)",
        "red-500",
        "white",
        "UI",
        "glow hero/page-hero (hanya elemen non-teks)",
    ),
    # --- hero foto (.hero-photo): piksel foto PUTIH di bawah overlay hitam beralfa minimum ---
    (
        "white / overlay hero (alfa min) di atas foto putih",
        "white",
        "white>ink-900@hero-a-min",
        "N",
        "H1, lead, breadcrumb terang, tombol outline-light",
    ),
    (
        "white (heading besar) / overlay hero",
        "white",
        "white>ink-900@hero-a-min",
        "L",
        "H1 hero foto (>= 32px)",
    ),
    (
        "white / pil eyebrow di atas overlay hero",
        "white",
        "white>ink-900@hero-a-min>ink-900@hero-pill-a",
        "N",
        ".eyebrow--light (putih; red-300 di pil hanya 4,43:1)",
    ),
    (
        "white / overlay hero mobile (a-top lalu a-min)",
        "white",
        "white>ink-900@hero-a-top>ink-900@hero-a-min",
        "N",
        "teks di zona gelap mobile (<=767px), atas foto putih",
    ),
    (
        "white / pil eyebrow di overlay hero mobile",
        "white",
        "white>ink-900@hero-a-top>ink-900@hero-a-min>ink-900@hero-pill-a",
        "N",
        ".eyebrow--light di mobile",
    ),
    (
        "white / chip badge di overlay hero mobile",
        "white",
        "white>ink-900@hero-a-top>ink-900@hero-a-min>ink-900@hero-chip-a",
        "N",
        ".hero-photo__badges li di mobile",
    ),
    (
        "white / chip badge di atas overlay hero",
        "white",
        "white>ink-900@hero-a-min>ink-900@hero-chip-a",
        "N",
        ".hero-photo__badges li",
    ),
    (
        "red-300 / chip badge (ikon)",
        "red-300",
        "white>ink-900@hero-a-min>ink-900@hero-chip-a",
        "UI",
        "ikon di chip badge",
    ),
    (
        "focus white / overlay hero",
        "white",
        "white>ink-900@hero-a-min",
        "UI",
        "ring fokus di atas hero foto (red-300 hanya 2,09:1 di kasus terburuk)",
    ),
    (
        "ink-900 / kartu frosted hero di atas piksel hitam",
        "ink-900",
        "#000000>white@0.72",
        "N",
        ".hero-photo__card, .photo__cap (latar foto tergelap)",
    ),
    (
        "text / kartu frosted hero di atas piksel hitam",
        "text",
        "#000000>white@0.72",
        "N",
        "teks isi .hero-photo__card",
    ),
]

# Invarian overlay: alfa tidak boleh turun di bawah batas aman di mana pun teks bisa berada.
HERO_A_MIN_FLOOR = 0.68


def mobile_text_clear_of_light_zone():
    """Blok mobile styles.css: padding-top .hero-photo__inner >= titik akhir gradasi (--hero-fade)."""
    text = CSS.read_text(encoding="utf-8")
    m = re.search(
        r"@media \(max-width: 767px\) \{\s*\.hero-photo \{ justify-content: flex-end; \}.*?\n\}\n",
        text,
        re.S,
    )
    if not m:
        return False
    b = m.group(0)
    return (
        "padding-top: calc(var(--hero-fade) +" in b
        and "var(--hero-a-min)) var(--hero-fade)" in b
        and "var(--hero-a-top)" in b
    )


def main():
    print(f"Token dibaca dari {CSS}")
    print("Token: " + ", ".join(f"{k}={v}" for k, v in TOKENS.items()))
    print()
    header = f"{'Pasangan':<52} {'Rasio':>7}  {'Min':>4}  {'Hasil':<5} Dipakai di"
    print(header)
    print("-" * len(header) + "-" * 20)
    failures = 0
    for label, fg, bg, kind, where in PAIRS:
        r = ratio(fg, bg)
        need = REQUIRED[kind]
        ok = r >= need
        failures += 0 if ok else 1
        print(
            f"{label:<52} {r:>6.2f}:1  {need:>4}  {'PASS' if ok else 'FAIL':<5} [{kind}] {where}"
        )
    print()
    print(f"Token hero: " + ", ".join(f"{k}={v}" for k, v in NUMS.items()))
    checks = 0
    for label, ok in (
        (
            f"hero-a-min >= {HERO_A_MIN_FLOOR}",
            NUMS.get("hero-a-min", 0) >= HERO_A_MIN_FLOOR,
        ),
        (
            "hero-a-start >= hero-a-min",
            NUMS.get("hero-a-start", 0) >= NUMS.get("hero-a-min", 1),
        ),
        (
            "hero-pill-a dan hero-chip-a ada",
            "hero-pill-a" in NUMS and "hero-chip-a" in NUMS,
        ),
        (
            "hero-a-top ada dan < hero-a-min (zona terang tanpa teks)",
            0 < NUMS.get("hero-a-top", 1) < NUMS.get("hero-a-min", 0),
        ),
        (
            "mobile: padding-top inner >= zona pudar (teks di luar zona terang)",
            mobile_text_clear_of_light_zone(),
        ),
    ):
        checks += 1
        failures += 0 if ok else 1
        print(f"{label:<52} {'PASS' if ok else 'FAIL'}")
    print()
    print(f"{len(PAIRS)} pasangan dan {checks} invarian diperiksa, {failures} gagal.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
