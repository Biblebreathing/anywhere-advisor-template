#!/usr/bin/env python3
"""Assemble a book manuscript: front matter + chapters + back matter, with
worksheets and QR codes inserted, into build/manuscript.md and build/manuscript.docx.

  python3 tools/assemble_book.py --book clients/jane/09-book

Resolves {{worksheet:id}} (from worksheets/id.md), {{pagebreak}}, and {{qr:id}} (image + caption +
short URL, from qr-map.json; QR images are generated if missing). Strips <!-- -->
comments (fact IDs and notes). Each chapter and worksheet starts on a new page.
Run tools/book_lint.py first; the .docx is the editing/Kindle file, and Stage 11
turns it into the KDP print PDF.

Needs: pandoc (for .docx), pip install "qrcode[pil]"
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_qr  # noqa: E402

PAGE_BREAK = '\n\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n\n'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--book", required=True)
    a = ap.parse_args()
    bk = a.book
    with open(os.path.join(bk, "book.json")) as f:
        b = json.load(f)
    out = os.path.join(bk, "build")
    os.makedirs(out, exist_ok=True)

    codes = {}
    qmap_path = os.path.join(bk, "qr-map.json")
    if os.path.exists(qmap_path):
        m, errs = make_qr.load_map(qmap_path)
        if errs:
            sys.exit("qr-map.json: " + "; ".join(errs))
        qr_dir = os.path.join(out, "qr")
        if not os.path.isdir(qr_dir) or any(not os.path.exists(os.path.join(qr_dir, c["id"] + ".png")) for c in m["codes"]):
            os.makedirs(qr_dir, exist_ok=True)
            make_qr.build(m, qr_dir)
        codes = {c["id"]: {**c, "short": make_qr.short_url(m, c)} for c in m["codes"]}

    def qr_block(mo):
        c = codes.get(mo.group(1).strip())
        if not c:
            sys.exit(f"QR '{mo.group(1)}' not in qr-map.json")
        return (f'\n\n::: {{custom-style="QR"}}\n![](qr/{c["id"]}.png){{width=1in height=1in}}\n:::\n\n'
                f'**{c.get("caption", "")}**  \n{c["short"]}\n\n')

    def ws_block(mo):
        p = os.path.join(bk, "worksheets", mo.group(1).strip() + ".md")
        if not os.path.exists(p):
            sys.exit(f"worksheet '{mo.group(1)}' not found")
        return PAGE_BREAK + re.sub(r"<!--.*?-->", "", open(p).read(), flags=re.S).strip() + PAGE_BREAK

    parts = []
    order = ([b["front_matter"]] if b.get("front_matter") else []) + [os.path.join("chapters", c) for c in b["chapters"]] + \
        ([b["back_matter"]] if b.get("back_matter") else [])
    for i, rel in enumerate(order):
        text = open(os.path.join(bk, rel)).read()
        text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
        text = re.sub(r"\{\{worksheet:([^}]+)\}\}", ws_block, text)
        text = re.sub(r"\{\{qr:([^}]+)\}\}", qr_block, text)
        text = text.replace("{{pagebreak}}", PAGE_BREAK)
        text = re.sub(r"\n(☐|☑)", r"\n\n\1", text)  # each checkbox on its own line
        parts.append(text.strip())
    md = PAGE_BREAK.join(parts) + "\n"
    meta = ""  # the title page lives in front-matter.md; title/author are set as document properties below
    md_path = os.path.join(out, "manuscript.md")
    with open(md_path, "w") as f:
        f.write(meta + md)
    words = len(re.findall(r"[A-Za-z0-9']+", re.sub(r"```.*?```", "", md, flags=re.S)))

    docx = os.path.join(out, "manuscript.docx")
    if shutil.which("pandoc"):
        r = subprocess.run(["pandoc", "manuscript.md", "-o", "manuscript.docx", "--resource-path=."], cwd=out, capture_output=True, text=True)
        if r.returncode != 0:
            print("⚠️  pandoc failed:", r.stderr.strip()[:300])
            docx = None
        else:
            try:
                import docx as pydocx
                d = pydocx.Document(docx)
                d.core_properties.title, d.core_properties.author = b["title"], b.get("author", "")
                d.save(docx)
            except Exception:
                pass
    else:
        print("⚠️  pandoc not installed: skipped .docx")
        docx = None
    print(f"✅ Assembled {len(order)} files · {words:,} words (~{round(words / 275)} pages at 6×9) → {md_path}" + (f", {docx}" if docx else ""))


if __name__ == "__main__":
    main()
