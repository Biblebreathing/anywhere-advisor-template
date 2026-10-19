#!/usr/bin/env python3
"""Build a branded, self-contained assessment page from a JSON config.

  python3 tools/build_assessment.py \
      --config clients/jane/05-assessments/retirement-readiness.json \
      --palette clients/jane/02-knowledge-base/brand-palette.json \
      --out clients/jane/05-assessments/build/retirement-readiness

Writes <out>/index.html (plus copies of the logo and headshot). Upload that folder
to any web host, or embed the page in the advisor's site or funnel builder.
The config format is documented in stages/05-assessments/README.md, and a full
example is in stages/05-assessments/examples/.
"""
import argparse
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PALETTE = {"primary-strong": "#1F3A5F", "primary-tint": "#E5ECF5", "accent": "#C9A227",
                   "ink": "#17202B", "body-text": "#3B434F", "surface": "#F7F8FA"}
DEFAULT_FONTS = ["Playfair Display", "Source Sans 3"]
RISKY = r"\b(guarantee[ds]?|risk[- ]free|tax[- ]free|worry[- ]free|safe|never run out|no risk|beat the market|senior specialist)\b"


def validate(c):
    errors, warnings = [], []
    for key in ("advisor", "assessment", "mechanism", "questions", "bands", "capture", "appointment", "disclosure"):
        if key not in c:
            errors.append(f"missing top-level '{key}'")
    if errors:
        return errors, warnings
    step_ids = [s["id"] for s in c["mechanism"]["steps"]]
    ids = set()
    for q in c["questions"] + c.get("qualifiers", []):
        if q["id"] in ids:
            errors.append(f"duplicate question id '{q['id']}'")
        ids.add(q["id"])
        if len(q.get("options", [])) < 2:
            errors.append(f"question '{q['id']}' needs at least 2 options")
    for q in c["questions"]:
        if q.get("step") not in step_ids:
            errors.append(f"question '{q['id']}' has unknown step '{q.get('step')}'")
        if not any(o.get("points", 0) > 0 for o in q["options"]):
            errors.append(f"question '{q['id']}' has no option worth points")
    for s in step_ids:
        n = sum(1 for q in c["questions"] if q["step"] == s)
        if n == 0:
            warnings.append(f"step '{s}' has no questions; it won't appear in results")
        elif n == 1:
            warnings.append(f"step '{s}' has only 1 question; 2-3 give a fairer score")
        if s not in c.get("stepFeedback", {}):
            warnings.append(f"step '{s}' has no stepFeedback")
    covered = set()
    for b in c["bands"]:
        covered.update(range(b["min"], b["max"] + 1))
    if not set(range(0, 101)) <= covered:
        errors.append("bands must cover every score from 0 to 100")
    total = len(c["questions"]) + len(c.get("qualifiers", []))
    if total > 18:
        warnings.append(f"{total} questions; completion drops above ~15")
    if not c["appointment"].get("url", "").startswith("http"):
        warnings.append("appointment.url is not a real link yet")
    if not c.get("webhookUrl"):
        warnings.append("no webhookUrl: leads will NOT be sent to the CRM")
    if not c["advisor"].get("privacyUrl"):
        warnings.append("no advisor.privacyUrl (needed before going live)")
    text = json.dumps({k: v for k, v in c.items() if k != "disclosure"})
    for m in sorted(set(re.findall(RISKY, text, re.I))):
        warnings.append(f"compliance: the word '{m}' appears in the copy; check the context")
    return errors, warnings


def css_vars(p, fonts):
    v = {**DEFAULT_PALETTE, **p}
    out = "".join(f"--{k}:{v[k]};" for k in ("primary-strong", "primary-tint", "accent", "ink", "body-text", "surface"))
    return out + f"--head-font:'{fonts[0]}';--body-font:'{fonts[1]}';"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True)
    ap.add_argument("--palette")
    ap.add_argument("--option", type=int, default=0)
    ap.add_argument("--out", required=True, help="output folder")
    a = ap.parse_args()

    with open(a.config) as f:
        c = json.load(f)
    errors, warnings = validate(c)
    for w in warnings:
        print("⚠️ ", w)
    if errors:
        for e in errors:
            print("❌", e)
        sys.exit(1)

    palette, fonts = DEFAULT_PALETTE, DEFAULT_FONTS
    if a.palette:
        with open(a.palette) as f:
            o = json.load(f)[a.option]
        palette, fonts = o["palette"], o["fonts"]

    os.makedirs(a.out, exist_ok=True)
    cfg_dir = os.path.dirname(os.path.abspath(a.config))
    for key in ("logo", "headshot"):
        src = c["advisor"].get(key)
        if src and not src.startswith("http"):
            path = src if os.path.isabs(src) else os.path.join(cfg_dir, src)
            if os.path.exists(path):
                name = key + os.path.splitext(path)[1]
                shutil.copy(path, os.path.join(a.out, name))
                c["advisor"][key] = name
            else:
                print(f"⚠️  {key} file not found: {path} (left out)")
                c["advisor"][key] = ""

    with open(os.path.join(HERE, "assessment", "engine.html")) as f:
        page = f.read()
    q = "&".join("family=" + x.replace(" ", "+") + ":wght@400;700" for x in fonts)
    cfg = json.dumps(c, ensure_ascii=False).replace("</", "<\\/")
    page = (page.replace("__TITLE__", c["assessment"]["title"].replace("<", "&lt;"))
                .replace("__DESCRIPTION__", c["assessment"].get("subtitle", "").replace('"', "&quot;").replace("<", "&lt;"))
                .replace("__FONTS_URL__", f"https://fonts.googleapis.com/css2?{q}&display=swap")
                .replace("__CSS_VARS__", css_vars(palette, fonts))
                .replace("/*__CONFIG__*/null", cfg))
    with open(os.path.join(a.out, "index.html"), "w") as f:
        f.write(page)
    n = len(c["questions"]) + len(c.get("qualifiers", []))
    print(f"✅ Built {a.out}/index.html ({n} questions, {len(c['mechanism']['steps'])} steps)")


if __name__ == "__main__":
    main()
