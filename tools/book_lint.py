#!/usr/bin/env python3
"""Check a book manuscript against the house rules (stages/09-book/voice-and-craft.md).

  python3 tools/book_lint.py --book clients/jane/09-book

Reads <book>/book.json and every chapter it lists. Errors (exit code 1):
em dashes, banned vocabulary, banned closers, "journey" more than once per chapter,
flags or placeholders left in prose, emoji, unresolved {{worksheet:}} / {{qr:}}
references, a missing compliance line. Warnings: word counts outside targets,
reading grade above 9, mechanism spelling variants, villain usage, risky
compliance words. Writes <book>/build/lint-report.md.
"""
import argparse
import json
import os
import re
import sys

BANNED = [r"in today'?s fast[- ]paced world", r"\bleverag(e|es|ed|ing)\b", r"\bunlock(s|ed|ing)?\b", r"\bdelv(e|es|ed|ing)\b",
          r"\bgame[- ]changer", r"\brevolutioni[sz](e|es|ed|ing)\b", r"\bnavigat(e|es|ed|ing)\b", r"\blandscape\b",
          r"\bempower(s|ed|ing|ment)?\b", r"\belevat(e|es|ed|ing)\b", r"\bunleash(es|ed|ing)?\b", r"\bdive deep\b",
          r"\bdeep dive\b", r"at the end of the day"]
CLOSERS = [r"journey begins", r"the choice is yours", r"turn the page", r"your journey starts", r"the rest is up to you"]
RISKY = r"\b(guarantee[ds]?|risk[- ]free|tax[- ]free|worry[- ]free|never run out|no risk|beat the market|safe(st)? investment|fiduciary|senior specialist)\b"
FLAGS = r"\[(VERIFY|ANONYMIZE|INFERRED|COMPLIANCE|ATTORNEY REVIEW|NEW STEP[^\]]*)\]|\[F-\d+\]|\bTODO\b|\bTK\b|\{\{(?!(worksheet|qr):|pagebreak\}\})[^}]*\}\}|\[\[.*?\]\]"
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")


def strip(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return text


def prose(text):
    t = strip(text)
    t = re.sub(r"\{\{(worksheet|qr):[^}]+\}\}|\{\{pagebreak\}\}", "", t)
    t = re.sub(r"^#+\s.*$", "", t, flags=re.M)
    t = re.sub(r"[*_`>|]", " ", t)
    return t


def syllables(word):
    w = word.lower().strip(".,;:!?\"'()")
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


def fk_grade(text):
    sents = [s for s in re.split(r"[.!?]+\s", text) if s.strip()]
    words = re.findall(r"[A-Za-z']+", text)
    if len(words) < 50 or not sents:
        return None
    syl = sum(syllables(w) for w in words)
    return round(0.39 * len(words) / len(sents) + 11.8 * syl / len(words) - 15.59, 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--book", required=True)
    a = ap.parse_args()
    with open(os.path.join(a.book, "book.json")) as f:
        b = json.load(f)
    errs, warns = [], []
    ws_dir = os.path.join(a.book, "worksheets")
    worksheets = {os.path.splitext(x)[0] for x in os.listdir(ws_dir)} if os.path.isdir(ws_dir) else set()
    qr_ids = set()
    qmap = os.path.join(a.book, "qr-map.json")
    if os.path.exists(qmap):
        with open(qmap) as f:
            qr_ids = {c["id"] for c in json.load(f).get("codes", [])}
    mech = b.get("mechanism", "")
    mech_core = re.sub(r"[™®]", "", mech).strip()
    villain = b.get("villain", "")
    tgt = b.get("targets", {"chapter": [1800, 2400], "intro": [1500, 2500], "closing": [1500, 2500]})
    files = [("front", b.get("front_matter"))] + [("ch", c) for c in b["chapters"]] + [("back", b.get("back_matter"))]
    rows = ["| File | Words | Target | Grade | Issues |", "|---|---|---|---|---|"]
    total = villain_hits = chapters = 0
    front_text = ""
    for kind, name in files:
        if not name:
            continue
        path = os.path.join(a.book, "chapters" if kind == "ch" else "", name)
        if not os.path.exists(path):
            errs.append(f"{name}: file not found")
            continue
        raw = open(path).read()
        if kind == "front":
            front_text = raw
        visible = strip(raw)
        p = prose(raw)
        n = len(re.findall(r"[A-Za-z0-9']+", p))
        issues = []

        def err(msg):
            errs.append(f"{name}: {msg}")
            issues.append("❌ " + msg)

        def warn(msg):
            warns.append(f"{name}: {msg}")
            issues.append("⚠️ " + msg)

        for i, line in enumerate(visible.splitlines(), 1):
            if re.search(r"[—–]|(?<!-)--(?!-)", line):
                err(f"line {i}: em/en dash or '--'")
            for pat in BANNED:
                m = re.search(pat, line, re.I)
                if m:
                    err(f"line {i}: banned word '{m.group(0)}'")
            m = re.search(FLAGS, line)
            if m:
                err(f"line {i}: flag/placeholder left in prose '{m.group(0)}'")
            if EMOJI.search(line):
                err(f"line {i}: emoji")
            if "!!" in line:
                warn(f"line {i}: '!!'")
            for m in re.finditer(r"\{\{worksheet:([^}]+)\}\}", line):
                if m.group(1).strip() not in worksheets:
                    err(f"line {i}: worksheet '{m.group(1)}' not found in worksheets/")
            for m in re.finditer(r"\{\{qr:([^}]+)\}\}", line):
                if m.group(1).strip() not in qr_ids:
                    err(f"line {i}: QR '{m.group(1)}' not in qr-map.json")
        jc = len(re.findall(r"\bjourney\b", p, re.I))
        if jc > 1:
            err(f"'journey' used {jc} times (max 1 per chapter)")
        tail = " ".join(p.strip().split("\n")[-6:])
        for pat in CLOSERS:
            if re.search(pat, tail, re.I):
                err(f"banned closer '{pat}' near the end")
        if len(re.findall(r"\?", " ".join(re.split(r"(?<=[.!?])\s+", p.strip())[-3:]))) >= 3:
            err("ends with a rhetorical triple question")
        negated = re.sub(r"\b(not|no|never|nor)\s+(an?\s+)?(guarantee[ds]?)\b", " ", p, flags=re.I)
        for m in sorted(set(x[0] if isinstance(x, tuple) else x for x in re.findall(RISKY, negated, re.I))):
            warn(f"compliance word '{m}': check the context and qualifiers")
        if mech_core:
            exact = p.count(mech_core)
            loose = len(re.findall(re.escape(mech_core), p, re.I))
            if loose > exact:
                warn(f"mechanism spelled differently from '{mech}' {loose - exact} time(s)")
        grade = fk_grade(p) if kind == "ch" else None
        if kind == "ch":
            chapters += 1
            total += n
            key = "intro" if re.match(r"0+[-_]", name) or "intro" in name else ("closing" if "clos" in name or "conclu" in name else "chapter")
            lo, hi = tgt.get(key, tgt["chapter"])
            if not lo <= n <= hi:
                warn(f"{n} words (target {lo}-{hi})")
            if grade and grade > 9:
                warn(f"reading grade {grade} (aim for 8 or lower)")
            if villain and re.search(re.escape(villain), p, re.I):
                villain_hits += 1
        rows.append(f"| {name} | {n:,} | {'-' if kind != 'ch' else f'{lo}-{hi}'} | {grade if grade else '-'} | {'<br>'.join(issues) or '✅'} |")
    if villain and chapters and villain_hits < max(1, chapters // 2):
        warns.append(f"villain '{villain}' appears in only {villain_hits} of {chapters} chapters (aim for at least half)")
    if b.get("compliance_line") and b["compliance_line"] not in front_text:
        errs.append("front matter: the exact compliance_line from book.json is missing")
    if not 25000 <= total <= 35000:
        warns.append(f"total chapter words {total:,} (advisor book target 25,000-35,000)")
    out = os.path.join(a.book, "build")
    os.makedirs(out, exist_ok=True)
    report = [f"# Lint Report: {b.get('title', '')}", "", f"**{len(errs)} errors · {len(warns)} warnings · {total:,} words in {chapters} chapters (about {round(total / 275)} pages at 6×9)**", ""] + rows
    if warns:
        report += ["", "## Warnings"] + [f"- {w}" for w in warns]
    if errs:
        report += ["", "## Errors"] + [f"- {e}" for e in errs]
    with open(os.path.join(out, "lint-report.md"), "w") as f:
        f.write("\n".join(report) + "\n")
    for w in warns:
        print("⚠️ ", w)
    for e in errs:
        print("❌", e)
    print(f"{'✅' if not errs else '❌'} {len(errs)} errors, {len(warns)} warnings · {total:,} words · report: {out}/lint-report.md")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
