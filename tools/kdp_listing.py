#!/usr/bin/env python3
"""Check the Amazon KDP listing (Quill Step 19) and write the upload sheet.

  python3 tools/kdp_listing.py --listing clients/jane/11-kdp-publishing/listing.json \
      --book clients/jane/09-book \
      --interior clients/jane/11-kdp-publishing/build/interior-report.json \
      --out clients/jane/11-kdp-publishing/build

Checks: title and subtitle match the book (and the cover); description length
and allowed HTML; 7 keyword slots of 50 characters or fewer; no quotes,
subjective claims, "free", competitor or Amazon program terms in keywords; keywords
that repeat title words; 3 categories; risky compliance words; and estimates
paperback printing cost and royalty at the chosen price.

Writes build/listing.md (copy-paste upload sheet) and build/description.html.
KDP rules, printing costs, and royalty rates change: confirm on kdp.amazon.com.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_site import RISKY  # noqa: E402

ALLOWED_TAGS = {"b", "strong", "i", "em", "u", "br", "p", "ul", "ol", "li", "h4", "h5", "h6"}
KEYWORD_BANNED = r"\b(best ?sell(er|ing)|#1|number one|free|new|sale|kindle unlimited|kdp|amazon|bestseller)\b"
STOP = {"a", "an", "the", "to", "of", "and", "for", "you", "your", "in", "on", "how", "with", "can", "on"}


def print_cost_estimate(pages, ink="bw"):
    """US paperback printing cost estimate (KDP published rates at the time of writing; verify)."""
    if ink != "bw":
        return None
    return 2.30 if pages <= 108 else round(1.00 + 0.012 * pages, 2)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--listing", required=True)
    ap.add_argument("--book", required=True)
    ap.add_argument("--interior")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    with open(a.listing) as f:
        L = json.load(f)
    with open(os.path.join(a.book, "book.json")) as f:
        B = json.load(f)
    errs, warns = [], []

    if L.get("title") != B.get("title"):
        errs.append(f"title '{L.get('title')}' doesn't match book.json '{B.get('title')}' (cover, interior, and listing must match exactly)")
    if L.get("subtitle", "") != B.get("subtitle", ""):
        errs.append("subtitle doesn't match book.json exactly")
    if len(L.get("title", "") + L.get("subtitle", "")) > 200:
        errs.append("title + subtitle over 200 characters")

    desc = L.get("description_html", "")
    text_len = len(re.sub(r"<[^>]+>", "", desc))
    if len(desc) > 4000:
        errs.append(f"description is {len(desc)} characters including HTML (max 4,000)")
    tags = {t.lower() for t in re.findall(r"</?\s*([a-zA-Z0-9]+)", desc)}
    if tags - ALLOWED_TAGS:
        errs.append(f"description uses HTML tags KDP doesn't support: {sorted(tags - ALLOWED_TAGS)}")
    if text_len < 600:
        warns.append(f"description is short ({text_len} characters of text); aim for 1,500-3,000")

    kws = L.get("keywords", [])
    if len(kws) != 7:
        errs.append(f"{len(kws)} keyword slots (fill all 7)")
    title_words = {w.lower() for w in re.findall(r"[A-Za-z']+", L.get("title", "") + " " + L.get("subtitle", ""))} - STOP
    for i, k in enumerate(kws, 1):
        if len(k) > 50:
            errs.append(f"keyword {i} is {len(k)} characters (max 50): '{k}'")
        if re.search(r"[\"']", k):
            errs.append(f"keyword {i} contains quotes")
        m = re.search(KEYWORD_BANNED, k, re.I)
        if m:
            errs.append(f"keyword {i} contains a prohibited/subjective term '{m.group(0)}'")
        rep = {w.lower() for w in re.findall(r"[A-Za-z']+", k)} & title_words
        if rep:
            warns.append(f"keyword {i} repeats title/subtitle words {sorted(rep)}; use the slot for new phrases")
    if len(set(k.lower() for k in kws)) < len(kws):
        errs.append("duplicate keyword slots")

    cats = L.get("categories", [])
    if len(cats) != 3:
        warns.append(f"{len(cats)} categories (choose 3: one broad and credible, two narrow and winnable)")

    for m in sorted(set(x[0] if isinstance(x, tuple) else x for x in re.findall(RISKY, desc + " " + L.get("subtitle", ""), re.I))):
        warns.append(f"compliance: '{m}' in the description/subtitle; check with the approver")

    pages = None
    if a.interior and os.path.exists(a.interior):
        with open(a.interior) as f:
            pages = json.load(f).get("cover_pages")
    royalty = ""
    price = L.get("pricing", {}).get("paperback_usd")
    if pages and price:
        cost = print_cost_estimate(pages)
        r = round(0.60 * price - cost, 2)
        royalty = f"Paperback ${price:.2f}: est. printing ${cost:.2f} → est. royalty ${r:.2f}/copy (60% − printing). Author copies cost about printing + shipping."
        if r <= 0:
            errs.append(f"paperback price ${price} doesn't cover the estimated printing cost ${cost} at 60%")
    eb = L.get("pricing", {}).get("ebook_usd")
    if eb and not 2.99 <= eb <= 9.99:
        warns.append(f"ebook ${eb}: the 70% royalty option generally requires $2.99-$9.99 (verify)")

    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "description.html"), "w") as f:
        f.write(desc)
    sheet = [f"# KDP Upload Sheet: {L.get('title')}", "",
             "Copy these into KDP exactly. Verify current KDP rules at upload.", "",
             "## Book details", f"- **Language:** {L.get('language', 'English')}", f"- **Title:** {L.get('title')}",
             f"- **Subtitle:** {L.get('subtitle', '')}", f"- **Series:** {L.get('series', '(none)')}",
             f"- **Author:** {L.get('author', B.get('author', ''))}", f"- **Contributors:** {', '.join(L.get('contributors', [])) or '(none)'}",
             f"- **Publisher / imprint:** {L.get('imprint', '(KDP default)')}", f"- **ISBN:** {L.get('isbn', 'KDP free ISBN')}",
             "", "## Description", "Paste `description.html` (or the text below) into the description field.", "", desc, "",
             "## Keywords (7 slots)"] + [f"{i}. {k}  ({len(k)} chars)" for i, k in enumerate(kws, 1)] + \
            ["", "## Categories"] + [f"- {c}" for c in cats] + \
            ["", "## Content settings", f"- **Adult content:** No", f"- **Low-content book:** No", f"- **Large-print:** {L.get('large_print', 'No')}",
             f"- **Primary audience / reading age:** {L.get('reading_age', 'Adult')}",
             "", "## Print settings", f"- **Ink and paper:** Black & white interior with {L.get('paper', 'white')} paper",
             "- **Trim size:** 6 x 9 in · **Bleed:** No bleed (interior) · **Cover finish:** " + L.get("finish", "Matte"),
             f"- **Pages:** {pages or '(run kdp_interior.py)'}", "", "## Pricing",
             f"- **Paperback:** ${price}" if price else "- **Paperback:** (set)", f"- **Ebook:** ${eb}" if eb else "- **Ebook:** (set)",
             f"- {royalty}" if royalty else "", f"- **KDP Select (ebook exclusivity):** {L.get('kdp_select', 'Decide: only if exclusivity fits the funnel')}"]
    with open(os.path.join(a.out, "listing.md"), "w") as f:
        f.write("\n".join(sheet) + "\n")
    for w in warns:
        print("⚠️ ", w)
    for e in errs:
        print("❌", e)
    print(f"{'✅' if not errs else '❌'} listing: {len(errs)} errors, {len(warns)} warnings → {a.out}/listing.md, description.html" + (f" · {royalty}" if royalty else ""))
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
