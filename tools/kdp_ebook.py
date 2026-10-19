#!/usr/bin/env python3
"""Build the Kindle ebook (EPUB) from the book's source files.

  python3 tools/kdp_ebook.py --book clients/jane/09-book \
      --cover clients/jane/11-kdp-publishing/build/front-cover.jpg \
      --out clients/jane/11-kdp-publishing/build

In the ebook, every QR code becomes a tappable link (QR codes are useless on the
device you're reading on), worksheets stay as reflowable tables, and the table of
contents is generated. KDP accepts EPUB uploads directly. Needs: pandoc.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kdp_common as K  # noqa: E402

CSS = """
body { font-family: serif; line-height: 1.5; }
h1 { font-size: 1.6em; margin: 1.5em 0 1em; page-break-before: always; }
h2 { font-size: 1.2em; margin: 1.2em 0 .5em; }
p { margin: 0 0 .7em; text-indent: 0; }
.worksheet { border: 1px solid #888; padding: .8em; margin: 1.2em 0; }
.worksheet table { width: 100%; border-collapse: collapse; }
.worksheet th, .worksheet td { border: 1px solid #888; padding: .4em; text-align: left; }
.qr-link { margin: 1em 0; font-weight: bold; }
.pagebreak { page-break-after: always; }
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--book", required=True)
    ap.add_argument("--cover", help="front cover image (front-cover.jpg from kdp_cover.py)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    b, parts = K.render_parts(a.book, "ebook")
    chunks = []
    for kind, h in parts:
        if kind == "front":
            # the ebook gets its title page from metadata: drop the printed title page
            pb = h.find('<div class="pagebreak">')
            h = h[pb:] if pb >= 0 else h
        chunks.append(h)
    html = "<html><body>" + "\n".join(chunks) + "</body></html>"
    os.makedirs(a.out, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", b["title"].lower()).strip("-")
    out = os.path.join(a.out, f"{slug}.epub")
    with tempfile.TemporaryDirectory() as td:
        src, css = os.path.join(td, "book.html"), os.path.join(td, "epub.css")
        open(src, "w").write(html)
        open(css, "w").write(CSS)
        cmd = ["pandoc", src, "-f", "html", "-o", out, "--toc", "--split-level=1", "--css", css,
               "--metadata", f"title={b['title']}", "--metadata", f"subtitle={b.get('subtitle', '')}",
               "--metadata", f"author={b.get('author', '')}", "--metadata", "lang=en-US"]
        if a.cover and os.path.exists(a.cover):
            cmd += ["--epub-cover-image", a.cover]
        else:
            print("⚠️  no cover image: build the cover first (kdp_cover.py makes front-cover.jpg)")
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit("pandoc failed: " + r.stderr[:400])
    with zipfile.ZipFile(out) as z:
        names = z.namelist()
        bad = z.testzip()
    xhtml = [n for n in names if n.endswith(".xhtml")]
    if bad:
        sys.exit(f"❌ EPUB is corrupt ({bad})")
    print(f"✅ {out} · {len(xhtml)} sections · cover {'yes' if any('cover' in n for n in names) else 'no'} · QR codes converted to links")
    print("   Check it in Kindle Previewer (free from Amazon) before upload.")


if __name__ == "__main__":
    main()
