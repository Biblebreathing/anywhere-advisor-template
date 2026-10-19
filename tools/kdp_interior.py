#!/usr/bin/env python3
"""Build the KDP print interior: a 6x9 PDF with embedded fonts, mirror margins
sized to the page count, chapters starting on right-hand pages, running heads,
page numbers (roman in the front matter), a table of contents, and vector QR codes.

  python3 tools/kdp_interior.py --book clients/jane/09-book --out clients/jane/11-kdp-publishing/build \
      [--paper white|cream] [--body-font Literata] [--head-font "Playfair Display"] [--size 11.5]

Writes build/interior.pdf, build/interior.html (for proofing), and
build/interior-report.json (page count, margins, spine width) for the cover tool.
Run tools/book_lint.py on the book first.

Needs: pip install weasyprint "qrcode[pil]"; pandoc
"""
import argparse
import html
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kdp_common as K  # noqa: E402
import make_qr  # noqa: E402


def build_html(b, parts, fonts_css, body_font, head_font, size, gut, outside, toc=True):
    title = html.escape(b["title"])
    chapters, body = [], []
    n = 0
    for kind, h in parts:
        if kind == "chapter":
            n += 1
            m = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S)
            ch_title = re.sub("<[^>]+>", "", m.group(1)).strip() if m else f"Chapter {n}"
            h = re.sub(r"<h1[^>]*>", f'<h1 id="ch-{n}" class="chapter-title">', h, count=1)
            chapters.append((n, ch_title))
            body.append(f'<section class="chapter{" first-chapter" if n == 1 else ""}">{h}</section>')
        elif kind == "front":
            body.append(f'<section class="front">{h}</section>')
        else:
            body.append(f'<section class="back">{h}</section>')
    if toc and chapters:
        items = "".join(f'<li><a href="#ch-{i}">{html.escape(t)}</a></li>' for i, t in chapters)
        body.insert(1 if body and body[0].startswith('<section class="front"') else 0,
                    f'<section class="front toc"><h1>Contents</h1><ul>{items}</ul></section>')
    css = f"""
{fonts_css}
@page {{ size: {K.TRIM_W}in {K.TRIM_H}in; margin-top: 0.8in; margin-bottom: 0.85in;
  @top-center {{ font-family: '{body_font}'; font-size: 8.5pt; letter-spacing: .08em; text-transform: uppercase; color: #444; }}
  @bottom-center {{ font-family: '{body_font}'; font-size: 9.5pt; }} }}
@page :left {{ margin-left: {outside}in; margin-right: {gut}in;
  @top-center {{ content: "{title}"; }} @bottom-center {{ content: counter(page); }} }}
@page :right {{ margin-left: {gut}in; margin-right: {outside}in;
  @top-center {{ content: string(chaptitle, first-except); }} @bottom-center {{ content: counter(page); }} }}
@page front {{ @top-center {{ content: none; }} @bottom-center {{ content: counter(page, lower-roman); }} }}
@page back {{ @top-center {{ content: none; }} }}
@page :nth(1 of firstchap) {{ counter-reset: page 1; }}
@page :blank {{ @top-center {{ content: none; }} @bottom-center {{ content: none; }} }}
html {{ font-family: '{body_font}', 'DejaVu Serif', serif; font-size: {size}pt; line-height: 1.45; color: #000; }}
body {{ margin: 0; }}
p {{ margin: 0 0 0.6em; text-align: justify; hyphens: auto; orphans: 2; widows: 2; }}
h1, h2, h3 {{ font-family: '{head_font}', '{body_font}', serif; line-height: 1.2; page-break-after: avoid; break-after: avoid; hyphens: manual; }}
h1 {{ font-size: 22pt; margin: 0 0 0.5in; }}
h2 {{ font-size: 14pt; margin: 1.2em 0 0.5em; }}
h3 {{ font-size: 12pt; margin: 1em 0 0.4em; }}
.front {{ page: front; }}
.back {{ page: back; break-before: right; }}
.chapter {{ page: chapter; break-before: right; }}
.first-chapter {{ page: firstchap; }}
.front > h1:first-child {{ font-size: 26pt; text-align: center; margin: 2.2in 0 0.25in; }}
.front > h1:first-child + h2 {{ font-size: 13pt; font-weight: normal; font-style: italic; text-align: center; margin: 0 0.3in 1.6in; }}
.front > h1:first-child + h2 + p {{ text-align: center; font-size: 13pt; letter-spacing: .06em; text-transform: uppercase; }}
.chapter-title {{ string-set: chaptitle content(); margin-top: 1.4in; }}
.pagebreak {{ break-after: page; }}
.toc {{ break-before: right; }}
.toc ul {{ list-style: none; padding: 0; }}
.toc li {{ margin: 0.45em 0; }}
.toc a {{ color: #000; text-decoration: none; }}
.toc a::after {{ content: leader('.') target-counter(attr(href), page); }}
.worksheet {{ break-before: page; break-after: page; }}
.worksheet table {{ width: 100%; border-collapse: collapse; margin: 0.8em 0; }}
.worksheet th, .worksheet td {{ border: 0.6pt solid #000; padding: 0.12in 0.08in; text-align: left; vertical-align: top; height: 0.36in; font-size: {size - 1}pt; }}
.worksheet p {{ text-align: left; }}
figure.qr {{ margin: 1em 0; break-inside: avoid; display: flex; align-items: center; gap: 0.18in; }}
figure.qr img {{ width: 1in; height: 1in; }}
figure.qr figcaption {{ font-size: {size - 1.5}pt; line-height: 1.35; }}
img {{ max-width: 100%; }}
blockquote {{ margin: 1em 0.3in; font-style: italic; }}
hr {{ border: 0; text-align: center; margin: 1em 0; }}
"""
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title><style>{css}</style></head><body>{"".join(body)}</body></html>'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--book", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--paper", default="white", choices=["white", "cream"])
    ap.add_argument("--body-font", default="Literata")
    ap.add_argument("--head-font", default="")
    ap.add_argument("--palette", help="brand-palette.json; its heading font is used if --head-font isn't given")
    ap.add_argument("--size", type=float, default=11.5, help="body size in points (11-12 recommended for 55+ readers)")
    ap.add_argument("--outside", type=float, default=0.6)
    ap.add_argument("--no-toc", action="store_true")
    a = ap.parse_args()
    from weasyprint import HTML

    head = a.head_font
    if not head and a.palette:
        with open(a.palette) as f:
            head = json.load(f)[0]["fonts"][0]
    head = head or a.body_font
    os.makedirs(a.out, exist_ok=True)
    qr_dir = os.path.join(a.out, "qr")
    qmap = os.path.join(a.book, "qr-map.json")
    if os.path.exists(qmap):
        m, errs = make_qr.load_map(qmap)
        if errs:
            sys.exit("qr-map.json: " + "; ".join(errs))
        os.makedirs(qr_dir, exist_ok=True)
        make_qr.build(m, qr_dir)
    fonts_css = K.fetch_fonts(sorted({a.body_font, head}), os.path.join(a.out, ".fonts"))
    b, parts = K.render_parts(a.book, "print", qr_dir)

    gut = K.gutter(150)
    for _ in range(3):  # page count decides the gutter; re-render until stable
        doc = HTML(string=build_html(b, parts, fonts_css, a.body_font, head, a.size, gut, a.outside, not a.no_toc)).render()
        pages = len(doc.pages)
        need = K.gutter(pages)
        if need == gut:
            break
        gut = need
    cover_pages = pages + (pages % 2)  # printed books have an even page count; use it for the spine
    pages_note = f"{pages} (odd: KDP will add a blank last page; cover math uses {cover_pages})" if pages % 2 else str(pages)
    html_src = build_html(b, parts, fonts_css, a.body_font, head, a.size, gut, a.outside, not a.no_toc)
    with open(os.path.join(a.out, "interior.html"), "w") as f:
        f.write(html_src)
    pdf = os.path.join(a.out, "interior.pdf")
    doc.write_pdf(pdf)

    warns = []
    if pages < K.MIN_PAGES:
        warns.append(f"only {pages} pages: KDP paperbacks need at least {K.MIN_PAGES}")
    if pages > K.MAX_PAGES:
        warns.append(f"{pages} pages exceeds KDP's {K.MAX_PAGES}-page maximum")
    try:
        fonts = subprocess.run(["pdffonts", pdf], capture_output=True, text=True).stdout.splitlines()[2:]
        not_emb = [l.split()[0] for l in fonts if len(l.split()) > 4 and l.split()[-5] == "no"]
        if not_emb:
            warns.append("fonts not embedded: " + ", ".join(not_emb))
    except FileNotFoundError:
        warns.append("pdffonts not available: verify font embedding in the KDP previewer")
    report = {"pages": pages, "cover_pages": cover_pages, "paper": a.paper, "trim": f"{K.TRIM_W}x{K.TRIM_H} in", "gutter_in": gut,
              "kdp_min_gutter_in": K.kdp_min_gutter(pages), "outside_in": a.outside,
              "spine_in": K.spine_width(cover_pages, a.paper), "body_font": a.body_font, "head_font": head, "body_size_pt": a.size}
    with open(os.path.join(a.out, "interior-report.json"), "w") as f:
        json.dump(report, f, indent=2)
    for w in warns:
        print("⚠️ ", w)
    print(f"✅ interior.pdf · {pages_note} pages · gutter {gut}\" (KDP min {K.kdp_min_gutter(pages)}\") · spine {report['spine_in']}\" on {a.paper} paper → {a.out}")


if __name__ == "__main__":
    main()
