#!/usr/bin/env python3
"""Build the book funnel: the book offer page, the reader bonus hub, and a
printable page for every worksheet.

  python3 tools/build_book_funnel.py \
      --content clients/jane/10-book-funnel/book-funnel.json \
      --book clients/jane/09-book \
      --palette clients/jane/02-knowledge-base/brand-palette.json \
      --out clients/jane/10-book-funnel/build

Writes build/book/index.html (offer page) and build/book-bonus/index.html (hub)
with build/book-bonus/worksheets/<id>.html. Publish them at the paths used in
qr-map.json (e.g. advisor.com/book and advisor.com/book-bonus). The build checks
that every QR destination pointing at the hub lands on a real chapter anchor
and that every worksheet exists.

Needs: pip install jinja2; pandoc (for worksheet pages)
"""
import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
from urllib.parse import urlparse

from jinja2 import Environment, FileSystemLoader, select_autoescape

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_site import DEFAULT_FONTS, DEFAULT_PALETTE, RISKY  # noqa: E402

OFFERS = {"mailed", "download", "amazon"}


def md_to_html(path):
    text = re.sub(r"\n(☐|☑)", r"\n\n\1", open(path).read())  # each checkbox on its own line
    if shutil.which("pandoc"):
        r = subprocess.run(["pandoc", "-f", "markdown", "-t", "html"], input=text, capture_output=True, text=True)
        if r.returncode == 0:
            return r.stdout
    return "<pre>" + text.replace("<", "&lt;") + "</pre>"


def check(c, book_dir):
    errs, warns = [], []
    for k in ("site", "book", "offer", "hub", "hub_url"):
        if k not in c:
            errs.append(f"'{k}' is missing")
    if errs:
        return errs, warns
    o, h = c["offer"], c["hub"]
    if o.get("type") not in OFFERS:
        errs.append(f"offer.type must be one of {sorted(OFFERS)}")
    if o.get("type") == "download" and not o.get("download_url"):
        errs.append("offer.download_url is required for a download offer")
    if o.get("type") == "mailed" and not o.get("states"):
        warns.append("offer.states is empty: signed copies will be offered everywhere (set licensed states or service area)")
    if not c.get("sms_consent"):
        errs.append("sms_consent text is missing")
    ws_dir = os.path.join(book_dir, "worksheets")
    anchors = set()
    for ch in h.get("chapters", []):
        anchors.add(ch.get("anchor"))
        if ch.get("worksheet") and not os.path.exists(os.path.join(ws_dir, ch["worksheet"] + ".md")):
            errs.append(f"hub chapter '{ch.get('anchor')}': worksheet '{ch['worksheet']}' not found in {ws_dir}")
    qmap = os.path.join(book_dir, "qr-map.json")
    hub = urlparse(c["hub_url"])
    if os.path.exists(qmap):
        with open(qmap) as f:
            for code in json.load(f).get("codes", []):
                d = urlparse(code["destination"])
                if d.netloc == hub.netloc and d.path.rstrip("/") == hub.path.rstrip("/") and d.fragment and d.fragment not in anchors:
                    errs.append(f"QR '{code['id']}' points to #{d.fragment}, but the hub has no chapter with that anchor")
    else:
        warns.append("no qr-map.json in the book folder: couldn't cross-check QR anchors")
    if not c.get("webhookUrl"):
        warns.append("no webhookUrl: book requests and reader sign-ups will NOT reach the CRM")
    if not c["site"].get("appointment", {}).get("url", "").startswith("http"):
        warns.append("site.appointment.url is not a real booking link yet")
    text = json.dumps({k: v for k, v in c.items() if k != "site"})
    for m in sorted(set(x[0] if isinstance(x, tuple) else x for x in re.findall(RISKY, text, re.I))):
        warns.append(f"compliance: '{m}' appears in the copy; check the context")
    return errs, warns


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--content", required=True)
    ap.add_argument("--book", required=True, help="the client's 09-book folder")
    ap.add_argument("--palette")
    ap.add_argument("--option", type=int, default=0)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    with open(a.content) as f:
        c = json.load(f)
    errs, warns = check(c, a.book)
    for w in warns:
        print("⚠️ ", w)
    if errs:
        for e in errs:
            print("❌", e)
        sys.exit(1)

    palette, fonts = DEFAULT_PALETTE, DEFAULT_FONTS
    if a.palette:
        with open(a.palette) as f:
            o = json.load(f)[a.option]
        palette, fonts = {**DEFAULT_PALETTE, **o["palette"]}, o["fonts"]
    css_vars = ":root{" + "".join(f"--{k}:{palette[k]};" for k in DEFAULT_PALETTE) + \
        f"--head-font:'{fonts[0]}';--body-font:'{fonts[1]}';}}\n"
    with open(os.path.join(HERE, "site", "style.css")) as f:
        css = css_vars + f.read()

    s, bk = c["site"], c["book"]
    slug = re.sub(r"[^a-z0-9]+", "-", bk["title"].lower()).strip("-")
    base = os.path.dirname(os.path.abspath(a.content))
    offer_dir, hub_dir = os.path.join(a.out, "book"), os.path.join(a.out, "book-bonus")
    for d in (offer_dir, hub_dir, os.path.join(hub_dir, "worksheets")):
        os.makedirs(d, exist_ok=True)
    for d in (offer_dir, hub_dir):
        with open(os.path.join(d, "style.css"), "w") as f:
            f.write(css)
    for obj, key in ((s, "logo"), (s["advisor"], "photo"), (bk, "cover")):
        v = obj.get(key)
        if v and not v.startswith("http"):
            src = v if os.path.isabs(v) else os.path.join(base, v)
            if os.path.exists(src):
                for d in (offer_dir, hub_dir):
                    shutil.copy(src, os.path.join(d, os.path.basename(src)))
                obj[key] = os.path.basename(src)
            else:
                print(f"⚠️  image not found, left out: {v}")
                obj[key] = ""

    env = Environment(loader=FileSystemLoader(os.path.join(HERE, "site", "templates")), autoescape=select_autoescape(["html"]))
    q = "&".join("family=" + x.replace(" ", "+") + ":wght@400;600;700" for x in fonts)
    wjson = json.dumps({"title": bk["title"], "sessions": [], "webhookUrl": c.get("webhookUrl", "")}).replace("</", "<\\/")
    common = dict(s=s, c=c, wjson=wjson, year=datetime.date.today().year, fonts_url=f"https://fonts.googleapis.com/css2?{q}&display=swap")

    o = c["offer"]
    ojson = json.dumps({"type": o["type"], "title": bk["title"], "slug": slug, "states": [x.upper() for x in o.get("states", [])],
                        "outOfAreaMessage": o.get("out_of_area_message", "")}).replace("</", "<\\/")
    html = env.get_template("book_landing.html").render(page_title=f"{bk['title']} | {s['advisor']['name']}",
                                                        page_description=bk.get("subtitle", ""), robots="index,follow", ojson=ojson, **common)
    with open(os.path.join(offer_dir, "index.html"), "w") as f:
        f.write(html)

    h = c["hub"]
    hjson = json.dumps({"title": bk["title"], "slug": slug, "gate": bool(h.get("gate", True))}).replace("</", "<\\/")
    html = env.get_template("book_hub.html").render(page_title=f"Reader Resources | {bk['title']}", page_description="",
                                                    robots="noindex", hjson=hjson, **common)
    with open(os.path.join(hub_dir, "index.html"), "w") as f:
        f.write(html)

    n = 0
    for ch in h.get("chapters", []):
        if not ch.get("worksheet"):
            continue
        src = os.path.join(a.book, "worksheets", ch["worksheet"] + ".md")
        body = re.sub(r"<!--.*?-->", "", md_to_html(src), flags=re.S)
        title = re.search(r"<h2[^>]*>(.*?)</h2>", body)
        html = env.get_template("book_worksheet.html").render(ws_title=re.sub("<[^>]+>", "", title.group(1)) if title else ch["title"],
                                                              ws_html=body, back_anchor="#" + ch["anchor"], **common)
        with open(os.path.join(hub_dir, "worksheets", ch["worksheet"] + ".html"), "w") as f:
            f.write(html)
        n += 1
    print(f"✅ Built offer page ({o['type']}) → {offer_dir}/index.html · hub → {hub_dir}/index.html · {n} worksheet page(s)")


if __name__ == "__main__":
    main()
