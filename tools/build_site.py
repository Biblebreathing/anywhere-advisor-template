#!/usr/bin/env python3
"""Build an advisor's website (static HTML) from a content file.

  python3 tools/build_site.py \
      --content clients/jane/07-website/site.json \
      --palette clients/jane/02-knowledge-base/brand-palette.json \
      --out clients/jane/07-website/build

Writes a complete static site: home, about, how-we-work, one page per planning
track, webinars, book (if provided), contact, privacy, disclosures, plus
style.css, sitemap.xml, and robots.txt. Images referenced in the content file
(paths relative to it) are copied into build/assets/.

The content format is documented in stages/07-website/README.md, with a full
example in stages/07-website/examples/site.json.
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
DEFAULT_PALETTE = {"primary-strong": "#1F3A5F", "primary-tint": "#E5ECF5", "accent": "#C9A227",
                   "ink": "#17202B", "body-text": "#3B434F", "surface": "#F7F8FA"}
DEFAULT_FONTS = ["Playfair Display", "Source Sans 3"]
RISKY = r"\b(guarantee[ds]?|risk[- ]free|tax[- ]free|worry[- ]free|never run out|no risk|beat the market|senior specialist|safe(st)? investment)\b"


def check(c):
    errs, warns = [], []
    s = c.get("site", {})
    for k in ("firm", "advisor", "appointment", "disclosure", "mechanism"):
        if k not in s:
            errs.append(f"site.{k} is missing")
    for k in ("home", "about", "how", "contact"):
        if k not in c:
            errs.append(f"'{k}' section is missing")
    if errs:
        return errs, warns
    if not s["appointment"].get("url", "").startswith("http"):
        warns.append("site.appointment.url is not a real booking link yet")
    if not s.get("domain"):
        warns.append("site.domain not set (canonical links and sitemap will be relative)")
    links = " ".join(l.get("label", "") for l in s.get("legal_links", []))
    if "BrokerCheck" not in links:
        warns.append("no BrokerCheck link in legal_links (required on FINRA member firm sites; confirm with compliance)")
    if "CRS" not in links:
        warns.append("no Form CRS link in legal_links (required for BD/RIA retail firms; confirm with compliance)")
    if not c.get("privacy"):
        warns.append("no privacy policy text: a placeholder page will be generated")
    hl = c["home"].get("hero", {}).get("headline", "")
    if len(hl.split()) > 12:
        warns.append(f"home hero headline is {len(hl.split())} words (aim for 10 or fewer)")
    for p in c.get("planning", []):
        if len(p.get("seo_title", "")) > 60:
            warns.append(f"planning/{p.get('slug')}: seo_title over 60 characters")
    text = json.dumps({k: v for k, v in c.items() if k not in ("disclosures", "privacy")}) + s.get("tagline", "")
    for m in sorted(set(x[0] if isinstance(x, tuple) else x for x in re.findall(RISKY, text, re.I))):
        warns.append(f"compliance: '{m}' appears in the copy; check the context")
    return errs, warns


def copy_assets(c, base, out):
    """Copy local images into build/assets and rewrite the paths."""
    os.makedirs(os.path.join(out, "assets"), exist_ok=True)

    def fix(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, str) and k in ("photo", "photo2", "logo", "cover", "diagram", "image") and v and not v.startswith("http"):
                    src = v if os.path.isabs(v) else os.path.join(base, v)
                    if os.path.exists(src):
                        name = os.path.basename(src)
                        shutil.copy(src, os.path.join(out, "assets", name))
                        obj[k] = "assets/" + name
                    else:
                        print(f"⚠️  image not found, left out: {v}")
                        obj[k] = ""
                else:
                    fix(v)
        elif isinstance(obj, list):
            for v in obj:
                fix(v)
    fix(c)


def schema(s, c):
    a = s["advisor"]
    url = f"https://{s['domain']}/" if s.get("domain") else ""
    org = {"@context": "https://schema.org", "@type": "FinancialService", "name": s["firm"],
           "description": c.get("seo", {}).get("description", ""), "url": url, "telephone": a.get("phone", "")}
    if a.get("address"):
        ad = a["address"]
        org["address"] = {"@type": "PostalAddress", "streetAddress": ad.get("street", ""), "addressLocality": ad.get("city", ""),
                          "addressRegion": ad.get("state", ""), "postalCode": ad.get("zip", ""), "addressCountry": "US"}
    if c.get("seo", {}).get("area_served"):
        org["areaServed"] = c["seo"]["area_served"]
    org["employee"] = {"@type": "Person", "name": a.get("name", ""), "jobTitle": a.get("title", "")}
    return json.dumps(org).replace("</", "<\\/")


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
    copy_assets(c, os.path.dirname(os.path.abspath(a.content)), a.out)
    s = c["site"]
    s.setdefault("advisor", {}).setdefault("first_name", s["advisor"].get("name", "").split(" ")[0])

    css_vars = ":root{" + "".join(f"--{k}:{palette[k]};" for k in DEFAULT_PALETTE) + \
        f"--head-font:'{fonts[0]}';--body-font:'{fonts[1]}';}}\n"
    with open(os.path.join(HERE, "site", "style.css")) as f:
        css = f.read()
    with open(os.path.join(a.out, "style.css"), "w") as f:
        f.write(css_vars + css)

    env = Environment(loader=FileSystemLoader(os.path.join(HERE, "site", "templates")),
                      autoescape=select_autoescape(["html"]))
    q = "&".join("family=" + x.replace(" ", "+") + ":wght@400;600;700" for x in fonts)
    nav = [{"label": "How We Work", "href": "how-we-work.html"}, {"label": "About", "href": "about.html"}]
    if c.get("planning"):
        nav.insert(1, {"label": "Planning", "href": f"planning/{c['planning'][0]['slug']}.html"})
    if c.get("webinars"):
        nav.append({"label": "Free Classes", "href": "webinars.html"})
    if c.get("book_page"):
        nav.append({"label": "The Book", "href": "book.html"})
    nav.append({"label": "Contact", "href": "contact.html"})
    seo = c.get("seo", {})
    common = dict(s=s, c=c, nav=nav, fonts_url=f"https://fonts.googleapis.com/css2?{q}&display=swap",
                  schema=schema(s, c), year=datetime.date.today().year)
    pages = []

    def render(tpl, path, title, desc, **extra):
        depth = path.count("/")
        html = env.get_template(tpl).render(root="../" * depth, path=path, page_title=title,
                                            page_description=desc, **common, **extra)
        full = os.path.join(a.out, path)
        os.makedirs(os.path.dirname(full) or a.out, exist_ok=True)
        with open(full, "w") as f:
            f.write(html)
        pages.append(path)

    firm = s["firm"]
    render("index.html", "index.html", seo.get("home_title") or f"{firm} | {s.get('tagline', '')}".strip(" |"),
           seo.get("description", ""))
    render("about.html", "about.html", f"About {s['advisor'].get('name', '')} | {firm}", c["about"].get("lead", ""))
    render("how.html", "how-we-work.html", f"{s['mechanism']['name']} | {firm}", c["how"].get("lead", ""))
    for p in c.get("planning", []):
        render("planning.html", f"planning/{p['slug']}.html", p.get("seo_title") or f"{p['title']} | {firm}",
               p.get("seo_description") or p.get("lead", ""), p=p)
    if c.get("webinars"):
        render("webinars.html", "webinars.html", f"Free Classes | {firm}", c["webinars"].get("lead", ""))
    if c.get("book_page"):
        render("book.html", "book.html", f"{c['book_page']['title']} | {firm}", c["book_page"].get("subtitle", ""))
    render("contact.html", "contact.html", f"Contact | {firm}", c["contact"].get("lead", ""))
    render("legal.html", "privacy.html", f"Privacy Policy | {firm}", "Privacy policy", legal_title="Privacy Policy",
           legal_body=c.get("privacy") or ["[PLACEHOLDER: insert the privacy policy provided or approved by the advisor's compliance department.]"])
    render("legal.html", "disclosures.html", f"Important Disclosures | {firm}", "Disclosures", legal_title="Important Disclosures",
           legal_body=c.get("disclosures") or [s["disclosure"]])

    base = f"https://{s['domain']}/" if s.get("domain") else ""
    with open(os.path.join(a.out, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for pth in pages:
            f.write(f"  <url><loc>{base}{pth}</loc></url>\n")
        f.write("</urlset>\n")
    with open(os.path.join(a.out, "robots.txt"), "w") as f:
        f.write("User-agent: *\nAllow: /\n" + (f"Sitemap: {base}sitemap.xml\n" if base else ""))
    print(f"✅ Built {len(pages)} pages → {a.out}/index.html")


if __name__ == "__main__":
    main()
