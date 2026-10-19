#!/usr/bin/env python3
"""Build an advisor brand kit: a color palette, font pairing, contrast checks,
and an HTML preview page.

Two modes:

  From an existing logo (colors are extracted from the image):
    python3 tools/brand_kit.py --logo clients/jane/02-knowledge-base/assets/logo.png \
        --headshot clients/jane/02-knowledge-base/assets/headshot.jpg \
        --out clients/jane/02-knowledge-base

  New company with no logo (shows several preset options side by side):
    python3 tools/brand_kit.py --preset heritage --preset evergreen --preset teal \
        --name "Smith Retirement Partners" --out clients/jane/02-knowledge-base

  List the presets:
    python3 tools/brand_kit.py --list

Writes brand-kit-preview.html and brand-palette.json into --out.
"""
import argparse
import colorsys
import html
import json
import os
import sys

PRESETS = {
    "heritage": {
        "label": "Heritage Navy & Gold",
        "feel": "Established, trustworthy, classic wealth management.",
        "primary": "#1F3A5F", "accent": "#C9A227",
        "fonts": ("Playfair Display", "Source Sans 3"),
    },
    "evergreen": {
        "label": "Evergreen & Brass",
        "feel": "Growth, stability, legacy. A good fit for estate and family-wealth practices.",
        "primary": "#1E4D3A", "accent": "#B8893B",
        "fonts": ("Lora", "Inter"),
    },
    "slate": {
        "label": "Slate & Coral",
        "feel": "Modern and approachable. Stands out from traditional advisors.",
        "primary": "#2F3E4E", "accent": "#E07A5F",
        "fonts": ("DM Serif Display", "DM Sans"),
    },
    "teal": {
        "label": "Deep Teal & Sand",
        "feel": "Calm and reassuring. A good fit for retirement-income and LTC planning.",
        "primary": "#0F5257", "accent": "#D9A86C",
        "fonts": ("Merriweather", "Open Sans"),
    },
    "burgundy": {
        "label": "Burgundy & Champagne",
        "feel": "Premium and dignified. A good fit for estate, legacy, and high-net-worth work.",
        "primary": "#6B1E2E", "accent": "#C8A97E",
        "fonts": ("Cormorant Garamond", "Lato"),
    },
    "horizon": {
        "label": "Horizon Blue & Sunrise",
        "feel": "Optimistic and energetic. A good fit for pre-retirees and younger families.",
        "primary": "#1D5C9B", "accent": "#F2B134",
        "fonts": ("Montserrat", "Source Serif 4"),
    },
}
DEFAULT_FONTS = ("Playfair Display", "Source Sans 3")


# ---------- color math ----------

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#%02X%02X%02X" % tuple(max(0, min(255, round(c))) for c in rgb)


def luminance(h):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = hex_to_rgb(h)
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def hls(h):
    r, g, b = (c / 255 for c in hex_to_rgb(h))
    return colorsys.rgb_to_hls(r, g, b)


def from_hls(hh, l, s):
    return rgb_to_hex(c * 255 for c in colorsys.hls_to_rgb(hh, l, s))


def darken_until(h, against, target):
    """Darken h until it reaches the target contrast against `against`."""
    hh, l, s = hls(h)
    while contrast(from_hls(hh, l, s), against) < target and l > 0.05:
        l -= 0.02
    return from_hls(hh, l, s)


def build_palette(primary, accent=None, secondary=None):
    hh, l, s = hls(primary)
    if accent is None:
        accent = "#C9A227"  # warm gold works with most primaries
    palette = {
        "primary": primary,
        # buttons and links need white text (or text on white) at 4.5:1
        "primary-strong": darken_until(primary, "#FFFFFF", 4.5),
        "primary-tint": from_hls(hh, 0.93, min(s, 0.45)),
        "accent": accent,
        "ink": from_hls(hh, 0.13, min(s, 0.30)),
        "body-text": from_hls(hh, 0.27, min(s, 0.15)),
        "surface": from_hls(hh, 0.975, min(s, 0.25)),
        "white": "#FFFFFF",
    }
    if secondary:
        palette["secondary"] = secondary
    return palette


def checks(p):
    rows = [
        ("Body text on page background", p["body-text"], p["surface"], 4.5),
        ("Headlines on page background", p["ink"], p["surface"], 4.5),
        ("White text on buttons", "#FFFFFF", p["primary-strong"], 4.5),
        ("Accent on dark sections", p["accent"], p["ink"], 3.0),
        ("Primary on white (links, headings)", p["primary-strong"], "#FFFFFF", 4.5),
    ]
    return [
        {"use": u, "fg": fg, "bg": bg, "ratio": round(contrast(fg, bg), 2),
         "needs": need, "pass": contrast(fg, bg) >= need}
        for u, fg, bg, need in rows
    ]


# ---------- logo extraction ----------

def extract_colors(path, n=6):
    from PIL import Image
    img = Image.open(path).convert("RGBA")
    img.thumbnail((300, 300))
    data = img.get_flattened_data() if hasattr(img, "get_flattened_data") else img.getdata()
    pixels = [p[:3] for p in data if p[3] > 200]  # skip transparent pixels
    # skip the near-white and near-black background/outline pixels
    useful = [p for p in pixels if 25 < sum(p) / 3 < 235]
    if not useful:
        useful = pixels
    sample = Image.new("RGB", (len(useful), 1))
    sample.putdata(useful)
    q = sample.quantize(colors=n, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[: n * 3]
    counts = sorted(q.getcolors(), reverse=True)
    total = sum(c for c, _ in counts)
    out = []
    for count, idx in counts:
        rgb = pal[idx * 3: idx * 3 + 3]
        out.append({"hex": rgb_to_hex(rgb), "share": round(count / total, 3)})
    return out


def pick_roles(colors):
    """Most prominent saturated color = primary; most different saturated color = accent."""
    def sat(h):
        return hls(h)[2]
    saturated = [c["hex"] for c in colors if sat(c["hex"]) > 0.15]
    if not saturated:
        return colors[0]["hex"], None, "Logo is monochrome. The accent is a suggested gold [INFERRED]."
    primary = saturated[0]
    others = [h for h in saturated[1:] if abs(hls(h)[0] - hls(primary)[0]) > 0.06]
    accent = others[0] if others else None
    note = "" if accent else "Logo has one main color. The accent is a suggested gold [INFERRED]."
    return primary, accent, note


# ---------- HTML preview ----------

def option_html(o, logo_rel, headshot_rel):
    p, (hf, bf) = o["palette"], o["fonts"]
    swatches = "".join(
        f'<div class="sw"><div class="chip" style="background:{v}"></div>'
        f'<b>{html.escape(k)}</b><code>{v}</code></div>'
        for k, v in p.items()
    )
    rows = "".join(
        f'<tr><td>{html.escape(c["use"])}</td><td>{c["ratio"]}:1</td>'
        f'<td>{"✅" if c["pass"] else "⚠️ needs " + str(c["needs"]) + ":1"}</td></tr>'
        for c in o["checks"]
    )
    logo = f'<img class="logo" src="{logo_rel}" alt="logo">' if logo_rel else \
        f'<span class="wordmark" style="font-family:\'{hf}\';color:{p["ink"]}">{html.escape(o["name"])}</span>'
    head = f'<img class="headshot" src="{headshot_rel}" alt="headshot" style="border-color:{p["accent"]}">' if headshot_rel else ""
    return f"""
<section class="opt">
  <h2>{html.escape(o["label"])}</h2>
  <p class="feel">{html.escape(o["feel"])}</p>
  <div class="hero" style="background:{p["surface"]};font-family:'{bf}'">
    <div class="bar">{logo}</div>
    <div class="herobody">
      <div>
        <h3 style="font-family:'{hf}';color:{p["ink"]}">Will your retirement paycheck last as long as you do?</h3>
        <p style="color:{p["body-text"]}">Join a free 45-minute class on turning your savings into dependable income.</p>
        <span class="btn" style="background:{p["primary-strong"]}">Save My Seat</span>
        <span class="link" style="color:{p["primary-strong"]};border-color:{p["accent"]}">Take the Retirement Readiness Score →</span>
      </div>{head}
    </div>
    <div class="band" style="background:{p["ink"]}"><span style="color:{p["accent"]};font-family:'{hf}'">The 5-Step Retirement Paycheck Blueprint</span></div>
  </div>
  <div class="sws">{swatches}</div>
  <p class="fonts">Fonts: <b>{hf}</b> (headlines) · <b>{bf}</b> (body)</p>
  <table><tr><th>Contrast check (WCAG)</th><th>Ratio</th><th></th></tr>{rows}</table>
</section>"""


def write_preview(options, out, logo, headshot, title):
    fams = sorted({f for o in options for f in o["fonts"]})
    q = "&".join("family=" + f.replace(" ", "+") + ":wght@400;700" for f in fams)
    rel = lambda pth: os.path.relpath(pth, out) if pth else None
    body = "".join(option_html(o, rel(logo), rel(headshot)) for o in options)
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} — Brand Options</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{q}&display=swap">
<style>
body{{margin:0;padding:24px 16px;background:#F4F4F2;color:#1A1A1A;font-family:system-ui,sans-serif}}
main{{max-width:980px;margin:auto}} h1{{margin:0 0 4px}} .sub{{color:#555;margin:0 0 24px}}
.opt{{background:#fff;border-radius:14px;padding:20px;margin-bottom:28px;box-shadow:0 1px 3px #0002}}
.opt h2{{margin:0}} .feel{{color:#555;margin:4px 0 14px}}
.hero{{border-radius:10px;overflow:hidden;border:1px solid #0001}}
.bar{{padding:14px 20px;border-bottom:1px solid #0001}} .logo{{max-height:44px}} .wordmark{{font-size:22px;font-weight:700}}
.herobody{{display:flex;gap:20px;align-items:center;justify-content:space-between;padding:28px 20px}}
.herobody h3{{font-size:28px;line-height:1.2;margin:0 0 10px}}
.headshot{{width:140px;height:140px;object-fit:cover;border-radius:50%;border:4px solid;flex:none}}
.btn{{display:inline-block;color:#fff;padding:12px 22px;border-radius:8px;font-weight:700;margin:8px 12px 8px 0}}
.link{{display:inline-block;border-bottom:2px solid;font-weight:600}}
.band{{padding:14px 20px;font-size:18px}}
.sws{{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}}
.sw{{font-size:12px;width:104px;display:flex;flex-direction:column}} .chip{{height:44px;border-radius:6px;border:1px solid #0002;margin-bottom:4px}}
.fonts{{margin:14px 0 6px}} table{{border-collapse:collapse;font-size:14px;width:100%}} td,th{{text-align:left;padding:4px 8px;border-bottom:1px solid #eee}}
@media (max-width:600px){{.herobody{{flex-direction:column-reverse;align-items:flex-start}}}}
</style></head><body><main>
<h1>{html.escape(title)}</h1><p class="sub">Brand {"options" if len(options) > 1 else "kit"} preview. Sample copy only.</p>
{body}
</main></body></html>"""
    with open(os.path.join(out, "brand-kit-preview.html"), "w") as f:
        f.write(page)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--logo")
    ap.add_argument("--headshot")
    ap.add_argument("--preset", action="append", choices=PRESETS.keys())
    ap.add_argument("--primary", help="hex, if the advisor already has brand colors")
    ap.add_argument("--accent", help="hex")
    ap.add_argument("--name", default="Your Firm Name")
    ap.add_argument("--out", default=".")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()

    if a.list:
        for k, v in PRESETS.items():
            print(f"{k:10} {v['label']:28} {v['primary']} / {v['accent']}  {v['feel']}")
        return
    os.makedirs(a.out, exist_ok=True)
    options = []

    if a.logo or a.primary:
        extracted, note = None, ""
        if a.primary:
            primary, accent = a.primary, a.accent
        else:
            extracted = extract_colors(a.logo)
            primary, accent, note = pick_roles(extracted)
            accent = a.accent or accent
        pal = build_palette(primary, accent)
        options.append({"label": "Brand Kit (from your logo)" if a.logo else "Brand Kit",
                        "feel": note or "Built from the advisor's existing brand colors.",
                        "name": a.name, "palette": pal, "fonts": DEFAULT_FONTS,
                        "checks": checks(pal), "extracted": extracted})
    for key in a.preset or []:
        pr = PRESETS[key]
        pal = build_palette(pr["primary"], pr["accent"])
        options.append({"label": pr["label"], "feel": pr["feel"], "preset": key, "name": a.name,
                        "palette": pal, "fonts": pr["fonts"], "checks": checks(pal)})
    if not options:
        sys.exit("Give --logo, --primary, or at least one --preset (see --list).")

    write_preview(options, a.out, a.logo, a.headshot, a.name)
    with open(os.path.join(a.out, "brand-palette.json"), "w") as f:
        json.dump(options, f, indent=2)
    for o in options:
        fails = [c["use"] for c in o["checks"] if not c["pass"]]
        print(f"{o['label']}: primary {o['palette']['primary']}, accent {o['palette']['accent']}"
              + (f"  ⚠️ contrast issues: {', '.join(fails)}" if fails else "  ✅ all contrast checks pass"))
    print(f"Wrote {a.out}/brand-kit-preview.html and brand-palette.json")


if __name__ == "__main__":
    main()
