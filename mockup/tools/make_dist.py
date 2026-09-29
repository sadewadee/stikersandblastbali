#!/usr/bin/env python3
"""Paket folder deploy mockup (Cloudflare Pages) - Python 3, stdlib saja.

Menjalankan build (--strict), menghapus dan membuat ulang mockup/dist/, lalu mengisinya
hanya dengan yang boleh tayang: 15 halaman *.html, assets/, deploy/_headers, dan
deploy/robots.txt. Sesudahnya dicetak ringkasan dan divalidasi (noindex, isi folder,
batas Cloudflare Pages). Exit 1 bila ada validasi yang gagal.

    python3 mockup/tools/make_dist.py     # dari direktori mana pun

Deploy (dijalankan manual, bukan oleh skrip ini):

    wrangler pages deploy mockup/dist --project-name stikersandblastbali
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # .../mockup
DIST = ROOT / "dist"
PAGES_DIR = ROOT / "src" / "pages"
ASSETS_DIR = ROOT / "assets"
DEPLOY_DIR = ROOT / "deploy"
DEPLOY_FILES = ("_headers", "robots.txt")

# Tidak boleh ikut ke dist (internal). Dicek di level teratas dan, untuk sampah, di seluruh pohon.
FORBIDDEN_TOP = (
    "src",
    "tools",
    "_screens",
    "demo-content",
    "deploy",
    "dist",
    "build.py",
    "README.md",
    "DEMO-DATA.md",
)
JUNK = (".DS_Store", "__pycache__")

MAX_FILE_BYTES = 25 * 1024 * 1024  # batas Cloudflare Pages: 25 MiB per file
MAX_FILES = 20000  # batas Cloudflare Pages: 20.000 file per deployment (free plan)

ROBOTS_META = '<meta name="robots" content="noindex, nofollow">'
ROBOTS_ANY_RE = re.compile(r"<meta\s+name=[\"']robots[\"']", re.I)


def run_build() -> None:
    """Jalankan build.py --strict; hentikan seluruh proses bila gagal."""
    print("== Build (--strict)", flush=True)
    result = subprocess.run(
        [sys.executable, str(ROOT / "build.py"), "--strict"], cwd=ROOT.parent
    )
    if result.returncode != 0:
        sys.exit(
            f"GAGAL: build.py --strict exit {result.returncode}; dist tidak dibuat."
        )


def copy_tree(src: Path, dst: Path) -> None:
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*JUNK, "*.pyc"))


def make_dist() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    # Halaman = tepat yang dibangun dari src/pages (nama file datar di root mockup).
    for page in sorted(PAGES_DIR.glob("*.html")):
        built = ROOT / page.name
        if not built.is_file():
            sys.exit(f"GAGAL: {built.name} belum ada; build tidak menghasilkannya.")
        shutil.copy2(built, DIST / built.name)

    copy_tree(ASSETS_DIR, DIST / "assets")

    for name in DEPLOY_FILES:
        src = DEPLOY_DIR / name
        if not src.is_file():
            sys.exit(f"GAGAL: deploy/{name} tidak ditemukan.")
        shutil.copy2(src, DIST / name)


def validate() -> list:
    """Kembalikan daftar pesan kegagalan (kosong = semua OK)."""
    problems = []
    files = [p for p in DIST.rglob("*") if p.is_file()]

    htmls = sorted(DIST.glob("*.html"))
    if not htmls:
        problems.append("tidak ada file .html di dist")
    for page in htmls:
        text = page.read_text(encoding="utf-8")
        exact = text.count(ROBOTS_META)
        anyrobots = len(ROBOTS_ANY_RE.findall(text))
        if exact != 1 or anyrobots != 1:
            problems.append(
                f"{page.name}: meta robots noindex harus tepat 1 "
                f"(ditemukan {exact} persis, {anyrobots} total)"
            )

    for name in DEPLOY_FILES:
        if not (DIST / name).is_file():
            problems.append(f"dist/{name} tidak ada")
    headers = DIST / "_headers"
    if headers.is_file() and "X-Robots-Tag: noindex" not in headers.read_text(
        encoding="utf-8"
    ):
        problems.append("dist/_headers tidak memuat X-Robots-Tag: noindex")
    robots = DIST / "robots.txt"
    if robots.is_file():
        lines = [ln.strip() for ln in robots.read_text(encoding="utf-8").splitlines()]
        if "Disallow: /" not in lines:
            problems.append("dist/robots.txt tidak memuat 'Disallow: /'")

    for name in FORBIDDEN_TOP:
        if (DIST / name).exists():
            problems.append(f"dist/{name} tidak boleh ada (internal)")
    for path in DIST.rglob("*"):
        if path.name in JUNK:
            problems.append(f"sampah ikut ter-copy: {path.relative_to(DIST)}")

    for path in files:
        size = path.stat().st_size
        if size > MAX_FILE_BYTES:
            problems.append(
                f"{path.relative_to(DIST)}: {size / 1048576:.1f} MiB melebihi batas 25 MiB"
            )
    if len(files) >= MAX_FILES:
        problems.append(f"jumlah file {len(files)} melebihi batas {MAX_FILES}")
    return problems


def main() -> int:
    run_build()
    print("== Paket dist")
    make_dist()

    files = [p for p in DIST.rglob("*") if p.is_file()]
    total = sum(p.stat().st_size for p in files)
    n_html = len(list(DIST.glob("*.html")))
    print(f"dist   : {DIST}")
    print(f"isi    : {n_html} halaman .html, assets/, _headers, robots.txt")
    print(f"ringkas: {len(files)} file, {total / 1048576:.2f} MB")

    print("== Validasi")
    problems = validate()
    if problems:
        for msg in problems:
            print(f"GAGAL  {msg}", file=sys.stderr)
        print(f"Validasi gagal: {len(problems)} masalah.", file=sys.stderr)
        return 1
    print(f"OK  {n_html} halaman: tepat satu {ROBOTS_META}")
    print("OK  dist/_headers dan dist/robots.txt ada dan berisi aturan noindex")
    print(
        "OK  tidak ada src/, tools/, _screens/, demo-content/, build.py, README.md, DEMO-DATA.md"
    )
    print(f"OK  tidak ada file > 25 MiB; jumlah file {len(files)} < {MAX_FILES}")
    print(
        "Siap deploy: wrangler pages deploy mockup/dist --project-name stikersandblastbali"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
