#!/usr/bin/env python3
"""Generate print-ready QR codes for a book, plus the redirect files that make
them editable after printing.

  python3 tools/make_qr.py --map clients/jane/09-book/qr-map.json --out clients/jane/09-book/build/qr

Each code encodes a short link on the advisor's own domain (e.g. ellis.com/go/ch3),
never the final destination, so destinations can change without reprinting.

Writes, per code: <id>.svg (vector, for print) and <id>.png (1200 px).
Also writes redirects/_redirects (Netlify/Cloudflare Pages), redirects/go/<path>/index.html
(works on any static host), and qr-index.md (the launch test list).

Needs: pip install "qrcode[pil]"
"""
import argparse
import json
import os
import sys
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl

import qrcode
import qrcode.image.svg


def with_tracking(dest, book_slug, qr_id):
    u = urlparse(dest)
    q = dict(parse_qsl(u.query))
    q.update({"utm_source": "book", "utm_medium": "qr", "utm_campaign": book_slug, "utm_content": qr_id})
    return urlunparse(u._replace(query=urlencode(q)))


def load_map(path):
    with open(path) as f:
        m = json.load(f)
    errs = []
    if not m.get("domain"):
        errs.append("qr-map needs 'domain' (the advisor's own domain)")
    ids, paths = set(), set()
    for c in m.get("codes", []):
        for k in ("id", "path", "destination"):
            if not c.get(k):
                errs.append(f"code {c.get('id', '?')}: missing '{k}'")
        if c.get("id") in ids:
            errs.append(f"duplicate id {c['id']}")
        if c.get("path") in paths:
            errs.append(f"duplicate path {c['path']}")
        ids.add(c.get("id"))
        paths.add(c.get("path"))
        if c.get("destination") and not c["destination"].startswith("http"):
            errs.append(f"code {c['id']}: destination must be a full https:// URL")
    return m, errs


def short_url(m, c):
    return f"{m['domain'].rstrip('/')}/{c['path'].strip('/')}"


def build(m, out):
    os.makedirs(os.path.join(out, "redirects"), exist_ok=True)
    rules, rows = [], ["| QR id | Short URL (printed) | Destination | Tested iPhone | Tested Android |", "|---|---|---|---|---|"]
    for c in m["codes"]:
        url = "https://" + short_url(m, c)
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=4, box_size=10)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((1200, 1200))
        img.save(os.path.join(out, f"{c['id']}.png"))
        svg = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, error_correction=qrcode.constants.ERROR_CORRECT_M, border=4)
        svg.save(os.path.join(out, f"{c['id']}.svg"))
        dest = with_tracking(c["destination"], m.get("book_slug", "book"), c["id"])
        path = "/" + c["path"].strip("/")
        rules.append(f"{path}  {dest}  302")
        page_dir = os.path.join(out, "redirects", c["path"].strip("/"))
        os.makedirs(page_dir, exist_ok=True)
        with open(os.path.join(page_dir, "index.html"), "w") as f:
            f.write(f'<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex">'
                    f'<meta http-equiv="refresh" content="0; url={dest}"><link rel="canonical" href="{dest}">'
                    f'<title>Redirecting…</title><p>Redirecting… <a href="{dest}">Continue</a></p>')
        rows.append(f"| {c['id']} | {short_url(m, c)} | {c['destination']} | ☐ | ☐ |")
    with open(os.path.join(out, "redirects", "_redirects"), "w") as f:
        f.write("\n".join(rules) + "\n")
    with open(os.path.join(out, "qr-index.md"), "w") as f:
        f.write("# QR Codes: Launch Test List\n\nScan each code from the **printed proof copy** with an iPhone and an Android camera.\n\n" + "\n".join(rows) + "\n")
    return len(m["codes"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--map", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    m, errs = load_map(a.map)
    if errs:
        for e in errs:
            print("❌", e)
        sys.exit(1)
    os.makedirs(a.out, exist_ok=True)
    n = build(m, a.out)
    print(f"✅ {n} QR codes → {a.out} (SVG + PNG), redirects/_redirects, redirects/go/…, qr-index.md")


if __name__ == "__main__":
    main()
