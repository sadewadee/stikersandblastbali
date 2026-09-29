#!/usr/bin/env python3
"""Sticker Sandblast Bali - build script (Python 3, stdlib saja).

Merakit src/pages/*.html + src/partials/*.html menjadi halaman utuh di mockup/*.html.
Situs final 5 halaman (Beranda, Tentang Kami, Layanan, Portofolio, Kontak) + Artikel
(index + single) + style guide internal `_components.html`.
Setiap halaman otomatis diberi <meta name="robots" content="noindex, nofollow">
(mockup tidak boleh diindeks); direktif <!--@robots ...--> pada halaman tetap menang.
Dijalankan dari direktori mana pun:

    python3 mockup/build.py            # build, tampilkan peringatan lint
    python3 mockup/build.py --strict   # peringatan dianggap gagal (exit 1)

Petunjuk lengkap: mockup/README.md
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent  # .../mockup
PAGES_DIR = ROOT / "src" / "pages"
PARTIALS_DIR = ROOT / "src" / "partials"

# Nama file tujuan tautan internal yang diizinkan. Situs final = 5 halaman
# (Beranda, Tentang Kami, Layanan, Portofolio, Kontak) + Artikel (index + single)
# + style guide internal. Tautan antar halaman memakai anchor
# (mis. "layanan.html#harga"), jadi `#...` pada href sudah diabaikan oleh lint.
ALLOWED_LINKS = {
    "index.html",
    "tentang-kami.html",
    "layanan.html",
    "portofolio.html",
    "artikel.html",
    "artikel-single.html",
    "kontak.html",
    "_components.html",
}

# Direktif metadata di dalam halaman: <!--@nama nilai-->
META_RE = re.compile(r"<!--@(?!include\b)(\w+)[ \t]+(.*?)-->", re.S)
INCLUDE_RE = re.compile(r"<!--@include[ \t]+([\w-]+)[ \t]*-->")
KNOWN_META = {"title", "description", "active", "css", "js", "robots", "bodyclass"}
SINGLE_META = {
    "title",
    "description",
    "active",
    "robots",
    "bodyclass",
}  # css dan js boleh berulang

# Nilai meta robots bawaan: mockup tidak boleh diindeks. Direktif @robots di halaman menimpanya.
DEFAULT_ROBOTS = "noindex, nofollow"

HEAD_SCRIPT = "<script>document.documentElement.classList.add('js');</script>"

SHELL = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#111111">
{robots}<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Plus+Jakarta+Sans:wght@700;800&display=swap">
<link rel="stylesheet" href="assets/css/styles.css">
{extra_css}{head_script}
</head>
<body{body_class}>
<a class="skip-link" href="#main">Lewati ke konten utama</a>
{content}
<script src="assets/js/app.js" defer></script>
{extra_js}</body>
</html>
"""

errors = []
warnings = []
infos = []  # catatan informatif (tidak memengaruhi --strict)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"tidak bisa membaca {path}: {exc}")
        return ""


def esc(value: str) -> str:
    """Escape aman untuk atribut/title. Idempotent: '&amp;' tidak di-escape dua kali."""
    return html.escape(html.unescape(value), quote=True)


def parse_meta(source: str, name: str):
    """Ambil direktif <!--@key value--> dari halaman, kembalikan (meta, sisa_isi)."""
    meta = {}
    for key, value in META_RE.findall(source):
        value = " ".join(value.split())
        if key not in KNOWN_META:
            errors.append(f"{name}: direktif tidak dikenal <!--@{key} ...-->")
            continue
        if key in SINGLE_META:
            if key in meta:
                warnings.append(
                    f"{name}: direktif @{key} muncul lebih dari sekali; dipakai yang terakhir"
                )
            meta[key] = value
        else:
            meta.setdefault(key, []).append(value)
    return meta, META_RE.sub("", source)


def apply_includes(source: str, name: str, depth: int = 0) -> str:
    def repl(match):
        part = PARTIALS_DIR / f"{match.group(1)}.html"
        if not part.exists():
            errors.append(
                f"{name}: partial '{match.group(1)}' tidak ditemukan ({part.name})"
            )
            return ""
        text = read(part)
        return apply_includes(text, name, depth + 1) if depth < 3 else text

    return INCLUDE_RE.sub(repl, source)


def mark_active(header_html: str, tokens, name: str) -> str:
    """Tandai item menu aktif: <a data-nav="x"> -> aria-current="page"; <button data-nav="x"> -> data-current="true"."""
    for token in tokens:
        pattern = re.compile(
            r'<(a|button)\b([^>]*?)\bdata-nav="%s"([^>]*)>' % re.escape(token)
        )
        found = [0]

        def repl(m):
            found[0] += 1
            attr = (
                ' aria-current="page"' if m.group(1) == "a" else ' data-current="true"'
            )
            return f'<{m.group(1)}{m.group(2)}data-nav="{token}"{attr}{m.group(3)}>'

        header_html = pattern.sub(repl, header_html)
        if not found[0]:
            warnings.append(
                f'{name}: @active "{token}" tidak cocok dengan data-nav mana pun di header.html'
            )
    return header_html


def lint(name: str, out: str):
    """Pemeriksaan ringan pada hasil build (peringatan, bukan error)."""
    body = re.sub(r"<script\b.*?</script>", "", out, flags=re.S)
    h1 = re.findall(r"<h1\b", body)
    if len(h1) != 1:
        warnings.append(f"{name}: harus tepat satu <h1>, ditemukan {len(h1)}")
    levels = [int(x) for x in re.findall(r"<h([1-6])\b", body)]
    for prev, cur in zip(levels, levels[1:]):
        if cur > prev + 1:
            warnings.append(f"{name}: loncatan heading h{prev} -> h{cur}")
            break
    if '<main id="main"' not in body:
        warnings.append(f'{name}: tidak ada <main id="main"> (dibutuhkan skip link)')
    ids = re.findall(r'\sid="([^"]+)"', body)
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        warnings.append(f"{name}: id ganda: {', '.join(dup)}")
    for href in re.findall(r'<a\b[^>]*?\bhref="([^"]*)"', body):
        if href.startswith(("#", "tel:", "mailto:", "http://", "https://")):
            continue
        target = href.split("#", 1)[0].split("?", 1)[0]
        if target not in ALLOWED_LINKS:
            warnings.append(
                f"{name}: tautan internal di luar daftar yang diizinkan: {href}"
            )
    for m in re.finditer(r"(?:src|href)=\"(assets/[^\"#?]+)", body):
        if not (ROOT / m.group(1)).exists():
            warnings.append(f"{name}: aset tidak ditemukan: {m.group(1)}")
    # <img>: wajib alt (boleh kosong untuk dekoratif), width, dan height agar tidak ada layout shift
    for tag in re.findall(r"<img\b[^>]*>", body):
        src = re.search(r'\bsrc="([^"]*)"', tag)
        label = src.group(1) if src else tag[:50]
        missing = [
            attr
            for attr in ("alt", "width", "height")
            if not re.search(r"\s%s=" % attr, tag)
        ]
        if missing:
            warnings.append(f"{name}: <img> tanpa {'/'.join(missing)}: {label}")
    ph = len(re.findall(r'<mark\b[^>]*\bclass="[^"]*\bph\b', body))
    if ph:
        infos.append(f'{name}: {ph} <mark class="ph"> tersisa (akan diganti teks demo)')


def build_page(page: Path, header: str, footer: str) -> str:
    name = page.name
    meta, source = parse_meta(read(page), name)

    title = meta.get("title", "")
    description = meta.get("description", "")
    if not title:
        errors.append(f"{name}: <!--@title ...--> wajib ada")
    if not description:
        errors.append(f"{name}: <!--@description ...--> wajib ada")
    if len(html.unescape(title)) > 60:
        warnings.append(f"{name}: title {len(html.unescape(title))} karakter (maks 60)")
    if len(html.unescape(description)) > 155:
        warnings.append(
            f"{name}: description {len(html.unescape(description))} karakter (maks 155)"
        )

    tokens = meta.get("active", "").split()
    header_html = mark_active(header, tokens, name)

    content = source.replace("<!--@header-->", header_html).replace(
        "<!--@footer-->", footer
    )
    content = apply_includes(content, name)
    left = re.findall(r"<!--@[^>]*-->", content)
    if left:
        errors.append(f"{name}: direktif belum terproses: {left[0]}")

    robots = (
        f'<meta name="robots" content="{esc(meta.get("robots", DEFAULT_ROBOTS))}">\n'
    )
    extra_css = "".join(
        f'<link rel="stylesheet" href="assets/css/{esc(c)}">\n'
        for c in meta.get("css", [])
    )
    extra_js = "".join(
        f'<script src="assets/js/{esc(j)}" defer></script>\n'
        for j in meta.get("js", [])
    )
    body_class = f' class="{esc(meta["bodyclass"])}"' if "bodyclass" in meta else ""

    out = SHELL.format(
        title=esc(title),
        description=esc(description),
        robots=robots,
        extra_css=extra_css,
        head_script=HEAD_SCRIPT,
        body_class=body_class,
        content=content.strip("\n"),
        extra_js=extra_js,
    )
    lint(name, out)
    return out


def main() -> int:
    strict = "--strict" in sys.argv[1:]
    header = read(PARTIALS_DIR / "header.html")
    footer = read(PARTIALS_DIR / "footer.html")
    pages = sorted(PAGES_DIR.glob("*.html"))
    if not pages:
        errors.append(f"tidak ada halaman di {PAGES_DIR}")

    built = []
    for page in pages:
        out = build_page(page, header, footer)
        if errors:
            continue
        target = ROOT / page.name
        target.write_text(out, encoding="utf-8", newline="\n")
        built.append(target.name)

    for w in warnings:
        print(f"WARN  {w}", file=sys.stderr)
    for e in errors:
        print(f"ERROR {e}", file=sys.stderr)

    for i in infos:
        print(f"INFO  {i}")
    total_ph = sum(int(i.split(": ", 1)[1].split(" ", 1)[0]) for i in infos)
    print(f'INFO  total <mark class="ph"> tersisa di semua halaman: {total_ph}')
    print(f"Built {len(built)} halaman: {', '.join(built) if built else '-'}")
    if errors:
        return 1
    if strict and warnings:
        print(f"--strict: {len(warnings)} peringatan dianggap gagal", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
