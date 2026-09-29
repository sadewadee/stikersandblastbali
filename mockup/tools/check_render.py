#!/usr/bin/env python3
"""Regresi render + keyboard untuk semua halaman hasil build (mockup/*.html).

Butuh Playwright untuk Python dan satu Chromium (headless shell). Dijalankan dari mana pun:

    python3 mockup/tools/check_render.py                 # semua halaman x 1440/768/390 + keyboard
    python3 mockup/tools/check_render.py --fast          # hanya 1440+390 pada 4 halaman
    python3 mockup/tools/check_render.py --pages index,harga --widths 390
    python3 mockup/tools/check_render.py --no-keyboard   # lewati tes keyboard
    python3 mockup/tools/check_render.py --online        # izinkan Google Fonts (default: dijawab kosong, lebih cepat)

Path Chromium: env CHROME_PATH, atau otomatis dari ~/Library/Caches/ms-playwright
(chromium_headless_shell-*), atau bawaan Playwright.

Per halaman x lebar (390 = emulasi mobile) yang dicek:
  overflow  documentElement.scrollWidth <= innerWidth
  errors    tanpa console error / page error / request lokal gagal (file://)
  reveal    setiap .reveal yang tampil (bukan display:none/[hidden], mis. item "muat lebih banyak") menjadi .is-visible
            setelah halaman di-scroll penuh
  tap44     (hanya <=767px) tidak ada a/button/input/select/textarea setinggi < 44px
            (kecuali tautan inline di dalam teks dan skip-link; tautan yang diperluas ke seluruh kartu lewat ::after
            diukur dari kartunya)
  h1        tepat satu <h1>
Tambahan: index.html dijalankan ulang dengan prefers-reduced-motion=reduce (reveal harus langsung terlihat).
Keyboard (index.html): 1440 = tautan header, pemicu dropdown, "Chat WhatsApp" header, tombol WhatsApp
mengambang; 390 = hamburger, 6 pemicu FAQ, tombol bar bawah. Semuanya harus terjangkau lewat Tab
dan punya indikator fokus (outline terlihat atau box-shadow yang berubah). Tab dibatasi --max-tabs
(default 250, karena tombol mengambang ada di akhir DOM setelah puluhan tautan).

Exit code 0 hanya bila semua pemeriksaan lolos.
"""
import argparse
import glob
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
FAST_PAGES = ["index", "layanan", "layanan-sticker-sandblast", "harga"]
WIDTHS = [1440, 768, 390]

JS_METRICS = """() => ({
  sw: document.documentElement.scrollWidth, iw: window.innerWidth,
  h1: document.querySelectorAll('h1').length,
  hidden: [...document.querySelectorAll('.reveal:not(.is-visible)')].filter(e => e.getClientRects().length > 0).length
})"""

JS_SMALL_TARGETS = """() => {
  const out = [];
  document.querySelectorAll('a, button, input:not([type=hidden]), select, textarea').forEach(el => {
    if (el.closest('.skip-link') || el.classList.contains('skip-link')) return;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    let rect = el.getBoundingClientRect();
    if (rect.width <= 1 || rect.height <= 1) return;
    if (el.tagName === 'A' && cs.display === 'inline' && el.closest('p, li, dd, td, th, figcaption, blockquote, small, span')) return;
    const after = getComputedStyle(el, '::after');
    if (after.position === 'absolute' && after.content !== 'none' && el.offsetParent) rect = el.offsetParent.getBoundingClientRect(); /* tautan yang diperluas ke seluruh kartu (::after) */
    if (el.matches('input[type=checkbox], input[type=radio]')) { const l = el.closest('label'); if (l) rect = l.getBoundingClientRect(); }
    if (rect.height < 43.5) {
      out.push(el.tagName.toLowerCase() + '.' + (el.className || '').toString().split(' ')[0] + ' "' + (el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 28) + '" h=' + Math.round(rect.height));
    }
  });
  return out;
}"""

JS_TAG_TARGETS = """(mobile) => {
  const tag = (sel, key) => document.querySelectorAll(sel).forEach((e, i) => { e.dataset.qa = key; });
  if (!mobile) {
    tag('.site-header .brand', 'brand');
    tag('.site-header .nav__list > .nav__item > a.nav__link', 'hdr-link');
    tag('.site-header .nav__toggle', 'dropdown-toggle');
    tag('.site-header .site-header__cta', 'hdr-cta');
    tag('.wa-float', 'wa-float');
  } else {
    tag('.site-header .menu-btn', 'hamburger');
    tag('.accordion__trigger', 'faq');
    tag('.mobile-bar a', 'mobile-bar');
  }
  const rest = {};
  document.querySelectorAll('[data-qa]').forEach((e, i) => { e.dataset.qaId = i; rest[i] = getComputedStyle(e).boxShadow; });
  window.__rest = rest;
  const count = {};
  document.querySelectorAll('[data-qa]').forEach(e => { count[e.dataset.qa] = (count[e.dataset.qa] || 0) + 1; });
  return count;
}"""

JS_ACTIVE = """() => {
  const el = document.activeElement;
  if (!el || el === document.body) return null;
  const ok = cs => (cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0);
  let outline = ok(getComputedStyle(el)) || ok(getComputedStyle(el, '::after')) || ok(getComputedStyle(el, '::before'));
  const k = el.querySelector('.ba-slider__knob');
  if (!outline && k) outline = ok(getComputedStyle(k));
  const shadow = getComputedStyle(el).boxShadow;
  const changed = el.dataset.qaId !== undefined && shadow !== 'none' && shadow !== window.__rest[el.dataset.qaId];
  return { tag: el.tagName.toLowerCase(), label: (el.getAttribute('aria-label') || el.innerText || '').trim().replace(/\\s+/g, ' ').slice(0, 34),
           qa: el.dataset.qa || '', id: el.dataset.qaId || '', indicator: !!(outline || changed) };
}"""


def find_chrome():
    if os.environ.get("CHROME_PATH"):
        return os.environ["CHROME_PATH"]
    home = str(Path.home())
    for pattern in (
        home
        + "/Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-mac-arm64/chrome-headless-shell",
        home
        + "/Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-mac-x64/chrome-headless-shell",
        home
        + "/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux*/chrome-headless-shell",
    ):
        found = sorted(glob.glob(pattern))
        if found:
            return found[-1]
    return None


def new_context(browser, width, reduce, online):
    kw = dict(reduced_motion="reduce" if reduce else "no-preference")
    if width <= 767:
        kw.update(
            viewport={"width": width, "height": 844},
            is_mobile=True,
            has_touch=True,
            device_scale_factor=1,
        )
    else:
        kw.update(viewport={"width": width, "height": 900})
    ctx = browser.new_context(**kw)
    if not online:

        def handler(route):
            url = route.request.url
            if url.startswith(("file:", "data:", "blob:")):
                route.continue_()
            else:
                route.fulfill(status=200, body="", content_type="text/css")

        ctx.route("**/*", handler)
    return ctx


def check_page(browser, name, width, reduce, online):
    ctx = new_context(browser, width, reduce, online)
    page = ctx.new_page()
    errors = []
    page.on(
        "console",
        lambda m: (
            errors.append("console: " + m.text[:120])
            if m.type == "error" and not (m.location.get("url", "").startswith("http"))
            else None
        ),
    )
    page.on("pageerror", lambda e: errors.append("pageerror: " + str(e)[:120]))
    page.on(
        "requestfailed",
        lambda r: (
            errors.append("requestfailed: " + r.url[-80:])
            if r.url.startswith("file:")
            else None
        ),
    )
    page.on(
        "response",
        lambda r: (
            errors.append(f"http {r.status}: {r.url[-80:]}")
            if r.url.startswith("file:") and r.status >= 400
            else None
        ),
    )
    page.goto(f"file://{ROOT}/{name}.html", wait_until="load", timeout=45000)
    page.wait_for_timeout(250)
    if not reduce:
        h = page.evaluate("document.documentElement.scrollHeight")
        y = 0
        while y < h:
            page.evaluate(f"window.scrollTo(0,{y})")
            page.wait_for_timeout(30)
            y += 800
        page.wait_for_timeout(450)
        page.evaluate("window.scrollTo(0,0)")
    m = page.evaluate(JS_METRICS)
    small = page.evaluate(JS_SMALL_TARGETS) if width <= 767 else None
    ctx.close()
    return {
        "overflow": (m["sw"] <= m["iw"], f"sw={m['sw']} iw={m['iw']}"),
        "errors": (not errors, "; ".join(errors[:3])),
        "reveal": (m["hidden"] == 0, f"{m['hidden']} belum terlihat"),
        "tap44": (
            (True, "-")
            if small is None
            else (not small, f"{len(small)}: " + " | ".join(small[:4]))
        ),
        "h1": (m["h1"] == 1, f"h1={m['h1']}"),
    }


def keyboard_test(browser, mobile, online, max_tabs):
    width = 390 if mobile else 1440
    ctx = new_context(browser, width, False, online)
    page = ctx.new_page()
    page.goto(f"file://{ROOT}/index.html", wait_until="load", timeout=45000)
    page.wait_for_timeout(300)
    expected = page.evaluate(JS_TAG_TARGETS, mobile)
    seen = {}  # (qa, id) -> indicator
    stops = []
    for i in range(max_tabs):
        page.keyboard.press("Tab")
        info = page.evaluate(JS_ACTIVE)
        if info is None:
            continue
        stops.append(info)
        if info["qa"]:
            seen[(info["qa"], info["id"])] = info["indicator"]
        got = {}
        for qa, _id in seen:
            got[qa] = got.get(qa, 0) + 1
        if all(got.get(k, 0) >= v for k, v in expected.items()):
            break
    ctx.close()
    return expected, seen, stops


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--fast", action="store_true", help="hanya 1440+390 pada 4 halaman")
    ap.add_argument("--pages", help="daftar halaman dipisah koma (tanpa .html)")
    ap.add_argument("--widths", help="daftar lebar dipisah koma")
    ap.add_argument("--no-keyboard", action="store_true")
    ap.add_argument("--online", action="store_true")
    ap.add_argument("--max-tabs", type=int, default=250)
    args = ap.parse_args()

    all_pages = sorted(p.stem for p in ROOT.glob("*.html"))
    pages = (
        args.pages.split(",")
        if args.pages
        else (FAST_PAGES if args.fast else all_pages)
    )
    widths = (
        [int(w) for w in args.widths.split(",")]
        if args.widths
        else ([1440, 390] if args.fast else WIDTHS)
    )
    missing = [p for p in pages if p not in all_pages]
    if missing:
        sys.exit(f"halaman tidak ditemukan (jalankan build.py dulu): {missing}")

    jobs = [(p, w, False) for p in pages for w in widths]
    if "index" in pages or not args.pages:
        jobs += [("index", w, True) for w in widths]

    passed = failed = 0
    fail_rows = []
    cols = ["overflow", "errors", "reveal", "tap44", "h1"]
    print(
        f"{'halaman':<30} {'lebar':>5} {'motion':<7} "
        + " ".join(f"{c:<8}" for c in cols)
        + " hasil"
    )
    print("-" * 100)
    with sync_playwright() as p:
        chrome = find_chrome()
        browser = (
            p.chromium.launch(executable_path=chrome) if chrome else p.chromium.launch()
        )
        for name, w, reduce in jobs:
            try:
                res = check_page(browser, name, w, reduce, args.online)
            except Exception as exc:  # noqa: BLE001
                res = {c: (False, f"EXC {exc}"[:120]) for c in cols}
            cells = []
            row_ok = True
            for c in cols:
                ok, detail = res[c]
                if c == "tap44" and w > 767:
                    cells.append(f"{'n/a':<8}")
                    continue
                passed += 1 if ok else 0
                failed += 0 if ok else 1
                row_ok &= ok
                cells.append(f"{'ok' if ok else 'FAIL':<8}")
                if not ok:
                    fail_rows.append(
                        f"{name} @{w} {'reduce' if reduce else 'normal'} [{c}] {detail}"
                    )
            print(
                f"{name:<30} {w:>5} {'reduce' if reduce else 'normal':<7} "
                + " ".join(cells)
                + f" {'PASS' if row_ok else 'FAIL'}"
            )

        if not args.no_keyboard:
            print("\nKEYBOARD (index.html)")
            for mobile in (False, True):
                label = "390 (mobile)" if mobile else "1440 (desktop)"
                expected, seen, stops = keyboard_test(
                    browser, mobile, args.online, args.max_tabs
                )
                print(
                    f"- {label}: {len(stops)} stop Tab; target: "
                    + ", ".join(f"{k} x{v}" for k, v in expected.items())
                )
                if not mobile:
                    for n, s in enumerate(stops[:60], 1):
                        print(
                            f"    {n:>2}. <{s['tag']}> {s['label'] or '-':<34} {'[' + s['qa'] + ']' if s['qa'] else '':<18} fokus={'ya' if s['indicator'] else 'TIDAK'}"
                        )
                got = {}
                for (qa, _id), ind in seen.items():
                    got.setdefault(qa, []).append(ind)
                for key, need in expected.items():
                    have = got.get(key, [])
                    reach_ok = len(have) >= need
                    ind_ok = reach_ok and all(have)
                    passed += (1 if reach_ok else 0) + (1 if ind_ok else 0)
                    failed += (0 if reach_ok else 1) + (0 if ind_ok else 1)
                    print(
                        f"    {label:<14} {key:<16} terjangkau {len(have)}/{need} {'ok' if reach_ok else 'FAIL'}; indikator fokus {'ok' if ind_ok else 'FAIL'}"
                    )
                    if not reach_ok:
                        fail_rows.append(
                            f"keyboard {label} [{key}] hanya {len(have)}/{need} terjangkau dalam {args.max_tabs} Tab"
                        )
                    elif not ind_ok:
                        fail_rows.append(
                            f"keyboard {label} [{key}] indikator fokus tidak terlihat pada {have.count(False)} elemen"
                        )
        browser.close()

    print("\nRINGKASAN: %d pemeriksaan lolos, %d gagal" % (passed, failed))
    for row in fail_rows:
        print("  FAIL", row)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
