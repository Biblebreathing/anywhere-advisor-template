#!/usr/bin/env python3
"""Build an advisor's webinar funnel pages from a content file.

  python3 tools/build_funnel.py \
      --content clients/jane/08-funnel-and-upsells/retirement-paycheck/funnel.json \
      --palette clients/jane/02-knowledge-base/brand-palette.json \
      --out clients/jane/08-funnel-and-upsells/retirement-paycheck/build

Writes register.html (index.html), thank-you.html, replay.html, and booked.html
in the advisor's brand, sharing the website's design system. The registration
form POSTs to the CRM webhook, then sends people to the thank-you page with
add-to-calendar links. The next session date is chosen automatically from the
"sessions" list and shown in the visitor's own time zone.

The content format is documented in stages/08-funnel-and-upsells/README.md,
with an example in stages/08-funnel-and-upsells/examples/funnel.json.
"""
import argparse
import datetime
import json
import os
import re
import shutil
import sys

from jinja2 import Environment, FileSystemLoader, select_autoescape

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_site import DEFAULT_FONTS, DEFAULT_PALETTE, RISKY  # noqa: E402


def check(c):
    errs, warns = [], []
    s, w = c.get("site", {}), c.get("webinar", {})
    for k in ("firm", "advisor", "appointment", "disclosure"):
        if k not in s:
            errs.append(f"site.{k} is missing")
    for k in ("title", "promises", "sessions"):
        if k not in w:
            errs.append(f"webinar.{k} is missing")
    if not c.get("sms_consent"):
        errs.append("sms_consent text is missing (required when collecting mobile numbers)")
    if errs:
        return errs, warns
    if len(w["promises"]) != 3:
        warns.append(f"{len(w['promises'])} promises (the framework uses exactly 3, matching the webinar word for word)")
    now = datetime.datetime.now(datetime.timezone.utc)
    future = 0
    for sess in w["sessions"]:
        try:
            dt = datetime.datetime.fromisoformat(sess)
        except ValueError:
            errs.append(f"session '{sess}' is not ISO format like 2026-10-27T11:00:00-04:00")
            continue
        if dt.tzinfo is None:
            errs.append(f"session '{sess}' needs a time zone offset (e.g., -04:00)")
        elif dt > now:
            future += 1
    if future == 0:
        warns.append("no future sessions: the registration page will say 'New dates coming soon'")
    if not c.get("webhookUrl"):
        warns.append("no webhookUrl: registrations will NOT reach the CRM")
    if not s["appointment"].get("url", "").startswith("http"):
        warns.append("site.appointment.url is not a real booking link yet")
    if not w.get("join_link"):
        warns.append("webinar.join_link missing (used in calendar invites)")
    text = json.dumps({k: v for k, v in c.items() if k != "site"}) + json.dumps(s.get("appointment", {}))
    for m in sorted(set(x[0] if isinstance(x, tuple) else x for x in re.findall(RISKY, text, re.I))):
        warns.append(f"compliance: '{m}' appears in the copy; check the context")
    return errs, warns


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--content", required=True)
    ap.add_argument("--palette")
    ap.add_argument("--option", type=int, default=0)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    with open(a.content) as f:
        c = json.load(f)
    errs, warns = check(c)
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
    os.makedirs(a.out, exist_ok=True)

    base = os.path.dirname(os.path.abspath(a.content))
    s, w = c["site"], c["webinar"]
    for obj, key in ((s, "logo"), (s["advisor"], "photo")):
        v = obj.get(key)
        if v and not v.startswith("http"):
            src = v if os.path.isabs(v) else os.path.join(base, v)
            if os.path.exists(src):
                shutil.copy(src, os.path.join(a.out, os.path.basename(src)))
                obj[key] = os.path.basename(src)
            else:
                print(f"⚠️  image not found, left out: {v}")
                obj[key] = ""

    css_vars = ":root{" + "".join(f"--{k}:{palette[k]};" for k in DEFAULT_PALETTE) + \
        f"--head-font:'{fonts[0]}';--body-font:'{fonts[1]}';}}\n"
    with open(os.path.join(HERE, "site", "style.css")) as f:
        css = f.read()
    with open(os.path.join(a.out, "style.css"), "w") as f:
        f.write(css_vars + css)

    wjson = json.dumps({"title": w["title"], "track": w.get("track", ""), "sessions": sorted(w["sessions"]),
                        "duration": w.get("duration_minutes", 60), "join": w.get("join_link", ""),
                        "dial": w.get("dial_in", ""), "webhookUrl": c.get("webhookUrl", "")}).replace("</", "<\\/")
    env = Environment(loader=FileSystemLoader(os.path.join(HERE, "site", "templates")), autoescape=select_autoescape(["html"]))
    q = "&".join("family=" + x.replace(" ", "+") + ":wght@400;600;700" for x in fonts)
    common = dict(s=s, c=c, wjson=wjson, year=datetime.date.today().year,
                  fonts_url=f"https://fonts.googleapis.com/css2?{q}&display=swap")
    pages = [("funnel_register.html", "index.html", w["title"], w.get("subtitle", ""), "index,follow"),
             ("funnel_thanks.html", "thank-you.html", "You're registered", "", "noindex"),
             ("funnel_replay.html", "replay.html", "Replay: " + w["title"], "", "noindex"),
             ("funnel_booked.html", "booked.html", "You're booked", "", "noindex")]
    for tpl, name, title, desc, robots in pages:
        if tpl == "funnel_replay.html" and not w.get("replay"):
            continue
        if tpl == "funnel_booked.html" and not c.get("booked"):
            continue
        html = env.get_template(tpl).render(page_title=f"{title} | {s['firm']}", page_description=desc, robots=robots, **common)
        with open(os.path.join(a.out, name), "w") as f:
            f.write(html)
    print(f"✅ Built funnel → {a.out}/index.html (registration), thank-you.html"
          + (", replay.html" if w.get("replay") else "") + (", booked.html" if c.get("booked") else ""))


if __name__ == "__main__":
    main()
