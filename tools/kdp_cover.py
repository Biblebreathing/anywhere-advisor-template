#!/usr/bin/env python3
"""Build the KDP paperback wraparound cover (back + spine + front, with bleed)
from the FINAL interior page count, following Quill KB-6.

  python3 tools/kdp_cover.py --cover clients/jane/11-kdp-publishing/cover.json \
      --interior clients/jane/11-kdp-publishing/build/interior-report.json \
      --palette clients/jane/02-knowledge-base/brand-palette.json \
      --out clients/jane/11-kdp-publishing/build

Writes:
  cover.pdf              the upload file (trim + spine + bleed, fonts embedded)
  cover-guides.png       QA view: trim, spine folds, live area, bleed, barcode zone
  front-cover.jpg        1800x2700 front panel (ebook cover, ads, website)
  thumbnail-100px.png    the front at Amazon thumbnail size: is the title readable?
  cover-report.json      the math used

Spine text is added only when the page count allows it (KDP: more than 79 pages;
KB-6: ~100 for comfortable legibility). The barcode zone (2.0" x 1.2", back
lower right) is kept clear. Needs: pip install weasyprint; pdftoppm (poppler).
"""
import argparse
import html
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kdp_common as K  # noqa: E402

LIVE = 0.375  # house live-area inset from trim (KDP minimum 0.25")


def esc(s):
    return html.escape(s or "")


def build(c, pal, fonts, pages, paper, base, qr_svg=None, guides=False):
    W, H, sp = K.cover_size(pages, paper)
    b = K.BLEED
    back_l, back_r = b, b + K.TRIM_W
    spine_l, spine_r = back_r, back_r + sp
    front_l, front_r = spine_r, spine_r + K.TRIM_W
    hf, bf = fonts
    p = pal
    t_words = len(c["title"].split())
    t_size = 46 if t_words <= 3 else (40 if t_words <= 5 else 32)
    art = c.get("front_art")
    art_css = ""
    if art:
        path = art if os.path.isabs(art) else os.path.join(base, art)
        art_css = f"background-image:url('file://{path}');background-size:cover;background-position:center;"
    back = c.get("back", {})
    photo = back.get("author_photo")
    photo_path = (photo if os.path.isabs(photo) else os.path.join(base, photo)) if photo else None
    spine_text = pages >= K.SPINE_TEXT_MIN and sp >= 0.2 and c.get("spine_text", True)
    sp_font = min(11, max(6, sp * 72 * 0.42))
    bc_x, bc_y = back_r - LIVE - K.BARCODE_W, b + K.TRIM_H - LIVE - K.BARCODE_H

    el = []
    # backgrounds (extend through the bleed)
    el.append(f'<div style="left:0;top:0;width:{spine_l}in;height:{H}in;background:{p["primary-tint"]}"></div>')
    el.append(f'<div style="left:{spine_l}in;top:0;width:{sp}in;height:{H}in;background:{p["primary-strong"]}"></div>')
    el.append(f'<div style="left:{front_l}in;top:0;width:{W - front_l}in;height:{H}in;background:{p["ink"]};{art_css}"></div>')
    if art:
        el.append(f'<div style="left:{front_l}in;top:0;width:{W - front_l}in;height:{H * 0.55}in;background:linear-gradient(rgba(0,0,0,.65),rgba(0,0,0,0))"></div>')
    # front: two-tone typographic design (or art + gradient); title block flows so nothing can overlap
    fx, fw = front_l + 0.55, K.TRIM_W - 1.1
    if not art:
        el.append(f'<div style="left:{front_l}in;top:{b + K.TRIM_H * 0.68}in;width:{W - front_l}in;height:{H}in;background:{p["primary-strong"]}"></div>')
        el.append(f'<div style="left:{front_l}in;top:{b + K.TRIM_H * 0.68}in;width:{W - front_l}in;height:0.06in;background:{p["accent"]}"></div>')
    el.append(f'<div style="left:{fx}in;top:{b + 1.0}in;width:{fw}in;color:#fff">'
              f'<div style="font-family:\'{hf}\';font-weight:700;font-size:{t_size}pt;line-height:1.05">{esc(c["title"])}</div>'
              f'<div style="width:1.2in;height:0.07in;background:{p["accent"]};margin:0.3in 0 0.25in"></div>'
              f'<div style="font-family:\'{bf}\';font-size:15pt;line-height:1.3">{esc(c.get("subtitle"))}</div></div>')
    el.append(f'<div style="left:{fx}in;top:{b + K.TRIM_H - LIVE - 0.85}in;width:{fw}in;font-family:\'{bf}\';font-size:17pt;letter-spacing:.12em;text-transform:uppercase;color:#fff;font-weight:700">{esc(c["author"])}</div>')
    if c.get("author_credential"):
        el.append(f'<div style="left:{fx}in;top:{b + K.TRIM_H - LIVE - 0.45}in;width:{fw}in;font-family:\'{bf}\';font-size:10pt;color:#fff;opacity:.85">{esc(c["author_credential"])}</div>')
    # spine (reads top to bottom)
    if spine_text:
        el.append(f'<div style="left:{spine_l + sp / 2}in;top:{b + 0.5}in;width:{K.TRIM_H - 1.0}in;height:{sp - 0.125}in;'
                  f'transform-origin:0 0;transform:rotate(90deg) translateY(-50%);display:flex;justify-content:space-between;align-items:center;'
                  f'font-family:\'{bf}\';font-size:{sp_font}pt;color:#fff;font-weight:700;white-space:nowrap">'
                  f'<span>{esc(c["title"])}</span><span style="font-weight:400">{esc(c["author"])}</span></div>')
    # back
    bx, bw = back_l + 0.6, K.TRIM_W - 1.2
    blocks = []
    if back.get("headline"):
        blocks.append(f'<div style="font-family:\'{hf}\';font-weight:700;font-size:19pt;line-height:1.15;color:{p["ink"]};margin-bottom:12pt">{esc(back["headline"])}</div>')
    for para in back.get("blurb", []):
        blocks.append(f'<p style="margin:0 0 8pt">{esc(para)}</p>')
    if back.get("bullets"):
        blocks.append('<ul style="margin:4pt 0 10pt;padding-left:14pt">' + "".join(f'<li style="margin:0 0 4pt">{esc(x)}</li>' for x in back["bullets"]) + "</ul>")
    if back.get("bio"):
        img = f'<img src="file://{photo_path}" style="width:0.9in;height:0.9in;border-radius:50%;object-fit:cover;float:left;margin:0 10pt 4pt 0;border:2pt solid {p["accent"]}">' if photo_path and os.path.exists(photo_path) else ""
        blocks.append(f'<div style="margin-top:10pt;font-size:9pt;line-height:1.35">{img}<strong>About the author.</strong> {esc(back["bio"])}</div>')
    el.append(f'<div style="left:{bx}in;top:{b + 0.75}in;width:{bw}in;font-family:\'{bf}\';font-size:10.5pt;line-height:1.4;color:{p["body-text"]}">{"".join(blocks)}</div>')
    if qr_svg:
        el.append(f'<div style="left:{bx}in;top:{bc_y}in;width:{bc_x - bx - 0.2}in;display:flex;gap:8pt;align-items:center;font-family:\'{bf}\';font-size:8.5pt;color:{p["ink"]}">'
                  f'<img src="file://{qr_svg}" style="width:0.85in;height:0.85in;background:#fff;padding:3pt"><span>{esc(back.get("qr_caption", ""))}</span></div>')
    if back.get("price_line") or back.get("category_line"):
        el.append(f'<div style="left:{bx}in;top:{b + K.TRIM_H - LIVE - 0.2}in;width:2.5in;font-family:\'{bf}\';font-size:8pt;color:{p["body-text"]}">{esc(back.get("category_line", ""))}</div>')
    if guides:
        g = []
        g.append(f'<div style="left:0;top:0;width:{W}in;height:{H}in;border:{b}in solid rgba(255,80,140,.45);box-sizing:border-box"></div>')
        for x in (spine_l, spine_r):
            g.append(f'<div style="left:{x}in;top:0;width:0;height:{H}in;border-left:1.2pt dashed #1e6bff"></div>')
        for (l, r) in ((back_l, back_r), (front_l, front_r)):
            g.append(f'<div style="left:{l + LIVE}in;top:{b + LIVE}in;width:{r - l - 2 * LIVE}in;height:{K.TRIM_H - 2 * LIVE}in;border:1pt dashed #18a558"></div>')
        g.append(f'<div style="left:{b}in;top:{b}in;width:{W - 2 * b}in;height:{K.TRIM_H}in;border:1pt solid #000"></div>')
        g.append(f'<div style="left:{bc_x}in;top:{bc_y}in;width:{K.BARCODE_W}in;height:{K.BARCODE_H}in;background:rgba(255,0,0,.25);border:1pt solid red;'
                 f'font:9pt sans-serif;color:#900;display:flex;align-items:center;justify-content:center">BARCODE ZONE</div>')
        el += g
    body = "".join(f'<div class="a" {e[5:]}' if e.startswith("<div ") else e for e in el)
    css = f"@page{{size:{W}in {H}in;margin:0}} body{{margin:0}} .a{{position:absolute;box-sizing:border-box}}"
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body><div style="position:relative;width:{W}in;height:{H}in;overflow:hidden">{body}</div></body></html>', (W, H, sp, spine_text, front_l)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cover", required=True)
    ap.add_argument("--interior", required=True, help="interior-report.json from kdp_interior.py")
    ap.add_argument("--palette")
    ap.add_argument("--option", type=int, default=0)
    ap.add_argument("--qr", help="QR SVG for the back cover (e.g. build/qr/appointment.svg)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    from weasyprint import HTML

    with open(a.cover) as f:
        c = json.load(f)
    with open(a.interior) as f:
        rep = json.load(f)
    pages, paper = rep.get("cover_pages", rep["pages"]), rep.get("paper", "white")
    pal = {"primary-strong": "#1F3A5F", "primary-tint": "#E5ECF5", "accent": "#C9A227", "ink": "#17202B", "body-text": "#3B434F"}
    fonts = ["Playfair Display", "Source Sans 3"]
    if a.palette:
        with open(a.palette) as f:
            o = json.load(f)[a.option]
        pal.update(o["palette"])
        fonts = o["fonts"]
    os.makedirs(a.out, exist_ok=True)
    fonts_css = K.fetch_fonts(fonts, os.path.join(a.out, ".fonts"))
    base = os.path.dirname(os.path.abspath(a.cover))
    qr = os.path.abspath(a.qr) if a.qr else None
    warns = []
    if pages < K.MIN_PAGES:
        warns.append(f"{pages} pages: below KDP's {K.MIN_PAGES}-page paperback minimum (cover built anyway for review)")

    for guides, name in ((False, "cover.pdf"), (True, "cover-guides.pdf")):
        src, (W, H, sp, spine_text, front_l) = build(c, pal, fonts, pages, paper, base, qr, guides)
        src = src.replace("<style>", f"<style>{fonts_css}", 1)
        HTML(string=src).write_pdf(os.path.join(a.out, name))
    if not spine_text:
        warns.append(f"no spine text: {pages} pages gives a {sp}\" spine (spine text needs more than {K.SPINE_TEXT_MIN - 1} pages; about {K.SPINE_TEXT_COMFORT}+ for comfort)")
    elif pages < K.SPINE_TEXT_COMFORT:
        warns.append(f"spine text on a {sp}\" spine: check legibility in the KDP previewer")

    # previews: guides PNG, front panel JPG (300 dpi = 1800x2700), thumbnail
    subprocess.run(["pdftoppm", "-r", "60", "-png", "-singlefile", os.path.join(a.out, "cover-guides.pdf"), os.path.join(a.out, "cover-guides")], check=True)
    os.remove(os.path.join(a.out, "cover-guides.pdf"))
    subprocess.run(["pdftoppm", "-r", "300", "-png", "-singlefile", os.path.join(a.out, "cover.pdf"), os.path.join(a.out, ".full")], check=True)
    from PIL import Image
    full = Image.open(os.path.join(a.out, ".full.png")).convert("RGB")
    x0, y0 = round(front_l * 300), round(K.BLEED * 300)
    front = full.crop((x0, y0, x0 + 1800, y0 + 2700))
    front.save(os.path.join(a.out, "front-cover.jpg"), quality=92)
    front.resize((100, 150), Image.LANCZOS).save(os.path.join(a.out, "thumbnail-100px.png"))
    os.remove(os.path.join(a.out, ".full.png"))
    rep_out = {"pages": pages, "paper": paper, "spine_in": sp, "cover_w_in": W, "cover_h_in": H, "spine_text": spine_text,
               "barcode_zone_in": [K.BARCODE_W, K.BARCODE_H], "live_inset_in": LIVE, "bleed_in": K.BLEED}
    with open(os.path.join(a.out, "cover-report.json"), "w") as f:
        json.dump(rep_out, f, indent=2)
    for w in warns:
        print("⚠️ ", w)
    print(f"✅ cover.pdf {W}\" x {H}\" (spine {sp}\" for {pages} pages, {paper}) · cover-guides.png · front-cover.jpg · thumbnail-100px.png → {a.out}")


if __name__ == "__main__":
    main()
