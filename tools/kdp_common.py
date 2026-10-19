"""Shared helpers for the KDP tools: KDP math, font download, and turning the
book's source files (Stage 09) into HTML for print or ebook.

KDP figures below follow Terrance McMahon's Quill KB-5/KB-6 and KDP's published
guidance at the time of writing. KDP changes specs; verify on kdp.amazon.com
before every upload.
"""
import json
import os
import re
import shutil
import subprocess
import urllib.request

TRIM_W, TRIM_H = 6.0, 9.0
BLEED = 0.125
PAPER = {"white": 0.002252, "cream": 0.0025, "color": 0.002347}   # inches per page (KB-6)
MIN_PAGES, MAX_PAGES = 24, 828
SPINE_TEXT_MIN = 80       # KDP allows spine text above 79 pages
SPINE_TEXT_COMFORT = 100  # KB-6: practical minimum for readable spine text
BARCODE_W, BARCODE_H = 2.0, 1.2


def kdp_min_gutter(pages):
    """KDP minimum inside margin by page count (no bleed)."""
    for limit, g in ((150, 0.375), (300, 0.5), (500, 0.625), (700, 0.75), (828, 0.875)):
        if pages <= limit:
            return g
    return 0.875


def gutter(pages, house=0.75):
    return max(kdp_min_gutter(pages), house)


def spine_width(pages, paper="white"):
    return round(pages * PAPER[paper], 4)


def cover_size(pages, paper="white"):
    sp = spine_width(pages, paper)
    return round(BLEED + TRIM_W + sp + TRIM_W + BLEED, 4), TRIM_H + 2 * BLEED, sp


def fetch_fonts(families, cache_dir):
    """Download Google Fonts (regular, bold, italic) as TTF and return @font-face CSS.
    Fonts are cached in cache_dir. Returns '' for any family that can't be fetched."""
    os.makedirs(cache_dir, exist_ok=True)
    css_out = []
    for fam in families:
        q = fam.replace(" ", "+")
        url = f"https://fonts.googleapis.com/css2?family={q}:ital,wght@0,400;0,700;1,400"
        manifest = os.path.join(cache_dir, re.sub(r"\W+", "_", fam) + ".css")
        if not os.path.exists(manifest):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/4.0"})  # old UA → TTF urls
                css = urllib.request.urlopen(req, timeout=30).read().decode()
            except Exception as e:
                print(f"⚠️  couldn't fetch font '{fam}': {e}")
                continue
            local = []
            for block in re.findall(r"@font-face\s*{[^}]+}", css):
                src = re.search(r"url\((https://[^)]+)\)", block)
                style = re.search(r"font-style:\s*(\w+)", block).group(1)
                weight = re.search(r"font-weight:\s*(\d+)", block).group(1)
                fname = re.sub(r"\W+", "_", fam) + f"-{weight}-{style}.ttf"
                path = os.path.join(cache_dir, fname)
                if src and not os.path.exists(path):
                    urllib.request.urlretrieve(src.group(1), path)
                local.append(f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{weight};src:url('file://{path}') format('truetype');}}")
            with open(manifest, "w") as f:
                f.write("\n".join(local))
        css_out.append(open(manifest).read())
    return "\n".join(css_out)


def md_to_html(text):
    r = subprocess.run(["pandoc", "-f", "markdown", "-t", "html"], input=text, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr)
    return r.stdout


def load_book(book_dir):
    with open(os.path.join(book_dir, "book.json")) as f:
        b = json.load(f)
    codes, domain = {}, ""
    qp = os.path.join(book_dir, "qr-map.json")
    if os.path.exists(qp):
        with open(qp) as f:
            m = json.load(f)
        domain = m.get("domain", "")
        codes = {c["id"]: {**c, "short": f"{domain.rstrip('/')}/{c['path'].strip('/')}"} for c in m.get("codes", [])}
    return b, codes


def render_parts(book_dir, target, qr_dir=None):
    """Return a list of (kind, html) for front matter, each chapter, and back matter.
    target='print' → QR images (SVG); target='ebook' → tappable links instead of QR codes."""
    b, codes = load_book(book_dir)
    if not shutil.which("pandoc"):
        raise SystemExit("pandoc is required")

    def qr(mo):
        c = codes.get(mo.group(1).strip())
        if not c:
            raise SystemExit(f"QR '{mo.group(1)}' not in qr-map.json")
        if target == "ebook":
            cap = re.sub(r"^Scan\b", "Tap", c.get("caption", "Open the link"))  # ebook readers tap, they don't scan
            return f'\n\n<p class="qr-link"><a href="https://{c["short"]}">{cap}: {c["short"]}</a></p>\n\n'
        img = os.path.join(qr_dir, c["id"] + ".svg")
        return (f'\n\n<figure class="qr"><img src="file://{img}" alt="QR code"><figcaption><strong>{c.get("caption", "")}</strong>'
                f'<br>{c["short"]}</figcaption></figure>\n\n')

    def ws(mo):
        p = os.path.join(book_dir, "worksheets", mo.group(1).strip() + ".md")
        text = re.sub(r"\n(☐|☑)", r"\n\n\1", open(p).read())
        return f'\n\n<section class="worksheet">\n\n{text}\n\n</section>\n\n'

    def prep(text):
        text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
        text = re.sub(r"\{\{worksheet:([^}]+)\}\}", ws, text)
        text = re.sub(r"\{\{qr:([^}]+)\}\}", qr, text)
        text = text.replace("{{pagebreak}}", '\n\n<div class="pagebreak"></div>\n\n')
        return re.sub(r"\n(☐|☑)", r"\n\n\1", text)

    parts = []
    if b.get("front_matter"):
        parts.append(("front", md_to_html(prep(open(os.path.join(book_dir, b["front_matter"])).read()))))
    for ch in b["chapters"]:
        parts.append(("chapter", md_to_html(prep(open(os.path.join(book_dir, "chapters", ch)).read()))))
    if b.get("back_matter"):
        parts.append(("back", md_to_html(prep(open(os.path.join(book_dir, b["back_matter"])).read()))))
    return b, parts
