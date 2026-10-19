#!/usr/bin/env python3
"""Draw an advisor's Unique Mechanism as a branded SVG diagram.

  python3 tools/mechanism_diagram.py \
      --name "The Retirement Paycheck Blueprint" \
      --step "Income Map" --step "Tax Plan" --step "Protection Plan" --step "Legacy Plan" --step "Annual Review" \
      --detail "Know your paycheck" --detail "Keep more of it" --detail "Shield it" --detail "Pass it on" --detail "Stay on track" \
      --palette clients/jane/02-knowledge-base/brand-palette.json \
      --out clients/jane/04-offer-and-mechanism

Writes mechanism-row.svg (website, slides) and mechanism-stack.svg (mobile, book, worksheets).
--detail is optional (one per step: a short deliverable or benefit line).
"""
import argparse
import html
import json
import os

DEFAULT = {"primary-strong": "#1F3A5F", "accent": "#C9A227", "ink": "#17202B",
           "body-text": "#3B434F", "surface": "#F7F8FA", "primary-tint": "#E5ECF5"}
DEFAULT_FONTS = ("Playfair Display", "Source Sans 3")


def load_palette(path, option):
    if not path:
        return DEFAULT, DEFAULT_FONTS
    with open(path) as f:
        opts = json.load(f)
    o = opts[option]
    return o["palette"], tuple(o["fonts"])


def wrap(text, max_chars):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > max_chars:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


def font_css(fonts):
    q = "&amp;".join("family=" + f.replace(" ", "+") + ":wght@400;700" for f in fonts)
    return f"@import url('https://fonts.googleapis.com/css2?{q}&amp;display=swap');"


def text_lines(lines, x, y, size, lh, cls, anchor="middle"):
    return "".join(
        f'<text x="{x}" y="{y + i * lh}" class="{cls}" font-size="{size}" text-anchor="{anchor}">{html.escape(l)}</text>'
        for i, l in enumerate(lines)
    )


def svg_open(w, h, p, fonts, title):
    hf, bf = fonts
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{html.escape(title)}">'
            f'<style>{font_css(fonts)}'
            f".t{{font-family:'{hf}',Georgia,serif;font-weight:700;fill:{p['ink']}}}"
            f".s{{font-family:'{bf}',Arial,sans-serif;font-weight:700;fill:{p['ink']}}}"
            f".d{{font-family:'{bf}',Arial,sans-serif;fill:{p['body-text']}}}"
            f".n{{font-family:'{hf}',Georgia,serif;font-weight:700;fill:#FFFFFF}}"
            f"</style><rect width='{w}' height='{h}' rx='18' fill='{p['surface']}'/>")


def row(name, steps, details, p, fonts):
    n = len(steps)
    col = 230
    w = max(900, col * n + 80)
    col = (w - 80) / n
    title = wrap(name, 52)
    top = 70 + (len(title) - 1) * 40
    cy = top + 80
    h = cy + 125 + (45 if details else 0)
    out = [svg_open(w, h, p, fonts, name), text_lines(title, w / 2, 62, 36, 40, "t")]
    out.append(f'<rect x="{w/2-40}" y="{top+6}" width="80" height="4" rx="2" fill="{p["accent"]}"/>')
    x0, x1 = 40 + col / 2, 40 + col * (n - 0.5)
    out.append(f'<line x1="{x0}" y1="{cy}" x2="{x1}" y2="{cy}" stroke="{p["primary-strong"]}" stroke-opacity="0.3" stroke-width="6" stroke-linecap="round"/>')
    for i, s in enumerate(steps):
        cx = 40 + col * (i + 0.5)
        out.append(f'<circle cx="{cx}" cy="{cy}" r="38" fill="{p["primary-strong"]}" stroke="{p["accent"]}" stroke-width="4"/>')
        out.append(f'<text x="{cx}" y="{cy+12}" class="n" font-size="34" text-anchor="middle">{i+1}</text>')
        sl = wrap(s, max(10, int(col / 12)))
        out.append(text_lines(sl, cx, cy + 78, 21, 25, "s"))
        if details:
            out.append(text_lines(wrap(details[i], max(12, int(col / 9))), cx, cy + 86 + 25 * len(sl), 16, 20, "d"))
    out.append("</svg>")
    return "".join(out)


def stack(name, steps, details, p, fonts):
    w = 720
    title = wrap(name, 34)
    y = 60 + len(title) * 40
    rows = []
    for i, s in enumerate(steps):
        sl, dl = wrap(s, 30), wrap(details[i], 46) if details else []
        hgt = max(90, 30 + 28 * len(sl) + 22 * len(dl))
        rows.append((s, sl, dl, hgt))
    h = y + sum(r[3] for r in rows) + 30
    out = [svg_open(w, h, p, fonts, name), text_lines(title, w / 2, 58, 34, 40, "t")]
    out.append(f'<rect x="{w/2-40}" y="{y-24}" width="80" height="4" rx="2" fill="{p["accent"]}"/>')
    cx = 90
    first_cy, last_cy = y + 45, None
    cur = y
    for i, (s, sl, dl, hgt) in enumerate(rows):
        cy = cur + 45
        last_cy = cy
        cur += hgt
    out.append(f'<line x1="{cx}" y1="{first_cy}" x2="{cx}" y2="{last_cy}" stroke="{p["primary-strong"]}" stroke-opacity="0.3" stroke-width="6" stroke-linecap="round"/>')
    cur = y
    for i, (s, sl, dl, hgt) in enumerate(rows):
        cy = cur + 45
        out.append(f'<circle cx="{cx}" cy="{cy}" r="32" fill="{p["primary-strong"]}" stroke="{p["accent"]}" stroke-width="4"/>')
        out.append(f'<text x="{cx}" y="{cy+11}" class="n" font-size="30" text-anchor="middle">{i+1}</text>')
        ty = cy - (8 if dl else -8)
        out.append(text_lines(sl, 145, ty, 24, 28, "s", "start"))
        if dl:
            out.append(text_lines(dl, 145, ty + 28 * len(sl) + 2, 17, 22, "d", "start"))
        cur += hgt
    out.append("</svg>")
    return "".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--step", action="append", required=True)
    ap.add_argument("--detail", action="append")
    ap.add_argument("--palette", help="brand-palette.json from Stage 02")
    ap.add_argument("--option", type=int, default=0, help="which option in brand-palette.json (default: first)")
    ap.add_argument("--out", default=".")
    a = ap.parse_args()
    if not 2 <= len(a.step) <= 7:
        ap.error("use 2–7 steps (4–5 is ideal)")
    if a.detail and len(a.detail) != len(a.step):
        ap.error("give one --detail per --step, or none")
    p, fonts = load_palette(a.palette, a.option)
    os.makedirs(a.out, exist_ok=True)
    for fname, fn in (("mechanism-row.svg", row), ("mechanism-stack.svg", stack)):
        with open(os.path.join(a.out, fname), "w") as f:
            f.write(fn(a.name, a.step, a.detail, p, fonts))
    print(f"Wrote {a.out}/mechanism-row.svg and mechanism-stack.svg")


if __name__ == "__main__":
    main()
