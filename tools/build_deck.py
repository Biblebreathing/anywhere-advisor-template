#!/usr/bin/env python3
"""Build a branded webinar deck (.pptx) with the word-for-word speaker script in
the notes pane, plus a printable script and a run-of-show, from a deck JSON file.

  python3 tools/build_deck.py \
      --deck clients/jane/06-webinars/retirement-paycheck/deck.json \
      --palette clients/jane/02-knowledge-base/brand-palette.json \
      --out clients/jane/06-webinars/retirement-paycheck/build

Checks the deck against the framework rules (stages/06-webinars/webinar-framework.md):
total script words 5,500-7,500, every slide has a script, every Act 2 slide names
its Through Line angle, exactly 3 booking callouts, chat prompts, billboard limits,
and risky compliance words. Use --draft to build a partial deck without failing
the word-count check.

Needs: pip install python-pptx "qrcode[pil]"
"""
import argparse
import io
import json
import os
import re
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

W, H = 13.333, 7.5            # 16:9, inches (1920x1080 at 144 px/in, so 1 px = 0.5 pt)
LEFT_W = 6.1                  # left content column; the bottom-right quadrant stays clear for the camera
M = 0.7
SIZES = {"display": 60, "h1": 36, "h2": 22, "body": 16, "small": 12}   # 120/72/44/32/24 px
ANGLES = {"wrong belief", "consequence", "arithmetic", "story", "comparison", "true belief",
          "method", "analogy", "objection", "trigger"}
LAYOUTS = {"title", "statement", "bullets", "number", "cards", "table", "story", "process", "offer", "qr"}
RISKY = r"\b(guarantee[ds]?|risk[- ]free|tax[- ]free|worry[- ]free|never run out|no risk|beat the market|safe(st)? investment)\b"
DEFAULT_PALETTE = {"primary-strong": "#1F3A5F", "primary-tint": "#E5ECF5", "accent": "#C9A227",
                   "ink": "#17202B", "body-text": "#3B434F", "surface": "#F7F8FA"}
DEFAULT_FONTS = ["Playfair Display", "Source Sans 3"]


def rgb(h):
    h = h.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def words(s):
    """Spoken words only: text inside quotation marks."""
    spoken = re.findall(r'"([^"]*)"|“([^”]*)”', s or "")
    return sum(len((a or b).split()) for a, b in spoken)


class Builder:
    def __init__(self, deck, palette, fonts, base_dir):
        self.d, self.p, self.base = deck, {**DEFAULT_PALETTE, **palette}, base_dir
        self.hf, self.bf = fonts
        self.prs = Presentation()
        self.prs.slide_width, self.prs.slide_height = Inches(W), Inches(H)
        self.blank = self.prs.slide_layouts[6]

    # ---------- primitives ----------
    def bg(self, s, color):
        f = s.background.fill
        f.solid()
        f.fore_color.rgb = rgb(color)

    def text(self, s, x, y, w, h, content, size, color, font=None, bold=False, align=PP_ALIGN.LEFT,
             anchor=MSO_ANCHOR.TOP, bullets=False):
        tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = anchor
        tf.margin_left = tf.margin_right = Inches(0.05)
        lines = content if isinstance(content, list) else [content]
        for i, line in enumerate(lines):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.alignment = align
            if bullets:
                para.space_after = Pt(size * 0.6)
            r = para.add_run()
            r.text = ("•  " if bullets else "") + str(line)
            r.font.size, r.font.bold = Pt(size), bold
            r.font.color.rgb = rgb(color)
            r.font.name = font or self.bf
        return tb

    def rect(self, s, x, y, w, h, color, shape=MSO_SHAPE.RECTANGLE):
        r = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
        r.fill.solid()
        r.fill.fore_color.rgb = rgb(color)
        r.line.fill.background()
        r.shadow.inherit = False
        return r

    def headline(self, s, sl, color=None):
        self.text(s, M, 0.55, W - 2 * M, 1.2, sl.get("headline", ""), SIZES["h1"], color or self.p["ink"],
                  self.hf, True, anchor=MSO_ANCHOR.MIDDLE)
        self.rect(s, M + 0.05, 1.8, 1.1, 0.07, self.p["accent"])
        if sl.get("subhead"):
            self.text(s, M, 1.95, LEFT_W, 0.6, sl["subhead"], SIZES["body"], self.p["body-text"])

    def footer(self, s, dark=False):
        self.text(s, M, H - 0.5, LEFT_W, 0.35, self.d["advisor"].get("firm", ""), SIZES["small"],
                  "#FFFFFF" if dark else self.p["body-text"])

    def image(self, s, path, x, y, w=None, h=None):
        if not path:
            return
        full = path if os.path.isabs(path) else os.path.join(self.base, path)
        if os.path.exists(full):
            s.shapes.add_picture(full, Inches(x), Inches(y), Inches(w) if w else None, Inches(h) if h else None)

    # ---------- layouts ----------
    def L_title(self, s, sl):
        self.bg(s, self.p["ink"])
        self.rect(s, 0, 0, 0.25, H, self.p["accent"])
        hl = sl.get("headline", "")
        size = SIZES["display"] if len(hl.split()) <= 7 else 44
        self.text(s, M + 0.2, 0.9, 8.2, 3.6, hl, size, "#FFFFFF", self.hf, True, anchor=MSO_ANCHOR.MIDDLE)
        if sl.get("subhead"):
            self.text(s, M + 0.2, 4.6, 7.5, 0.9, sl["subhead"], SIZES["h2"], self.p["accent"])
        a = self.d["advisor"]
        self.text(s, M + 0.2, 5.6, 6.0, 0.9, [a.get("name", ""), a.get("firm", "")], SIZES["body"], "#FFFFFF")
        self.image(s, a.get("headshot"), 9.4, 0.9, h=3.0)
        if self.d.get("disclosure_short"):
            self.text(s, M + 0.2, H - 0.6, 6.0, 0.45, self.d["disclosure_short"], SIZES["small"], "#CCCCCC")

    def L_statement(self, s, sl):
        self.bg(s, self.p["surface"])
        self.rect(s, M, 1.0, 0.12, 2.6, self.p["accent"])
        self.text(s, M + 0.4, 0.9, W - 2 * M - 0.4, 2.8, sl.get("headline", ""), SIZES["h1"] + 8, self.p["ink"],
                  self.hf, True, anchor=MSO_ANCHOR.MIDDLE)
        if sl.get("subhead"):
            self.text(s, M + 0.4, 4.0, LEFT_W - 0.4, 1.5, sl["subhead"], SIZES["h2"], self.p["body-text"])
        self.footer(s)

    def L_bullets(self, s, sl):
        self.bg(s, self.p["surface"])
        self.headline(s, sl)
        y = 2.6 if sl.get("subhead") else 2.15
        self.text(s, M, y, LEFT_W, H - y - 0.7, sl.get("body", []), SIZES["h2"], self.p["body-text"], bullets=True)
        self.image(s, sl.get("image"), 7.4, 2.15, w=5.2)
        self.footer(s)

    def L_number(self, s, sl):
        self.bg(s, self.p["surface"])
        self.headline(s, sl)
        y = 2.3
        for n in sl.get("big_numbers", [])[:3]:
            self.text(s, M, y, LEFT_W, 0.95, n.get("value", ""), SIZES["display"] - 6, self.p["primary-strong"], self.hf, True)
            self.text(s, M, y + 0.92, LEFT_W, 0.5, n.get("label", ""), SIZES["body"], self.p["body-text"])
            y += 1.55
        self.footer(s)

    def L_cards(self, s, sl):
        self.bg(s, self.p["surface"])
        self.headline(s, sl)
        cards = sl.get("cards", [])[:4]
        y, gap = 2.25, 0.15
        ch = (H - 0.75 - y - gap * (len(cards) - 1)) / max(1, len(cards))
        for i, c in enumerate(cards):
            self.rect(s, M, y, LEFT_W, ch, "#FFFFFF")
            self.rect(s, M, y, 0.09, ch, self.p["accent"])
            self.text(s, M + 0.3, y + 0.08, LEFT_W - 0.45, 0.45, f"{i + 1}. {c.get('title', '')}", SIZES["h2"] - 2,
                      self.p["ink"], self.bf, True)
            if c.get("text"):
                self.text(s, M + 0.3, y + 0.5, LEFT_W - 0.45, ch - 0.55, c["text"], SIZES["body"], self.p["body-text"])
            y += ch + gap
        self.footer(s)

    def L_table(self, s, sl):
        self.bg(s, self.p["surface"])
        self.headline(s, sl)
        t = sl.get("table", {})
        hdr, rows = t.get("headers", []), t.get("rows", [])
        if not hdr:
            return
        shape = s.shapes.add_table(len(rows) + 1, len(hdr), Inches(M), Inches(2.25), Inches(LEFT_W + 0.3),
                                   Inches(0.8 * (len(rows) + 1)))
        tbl = shape.table
        for ci, h in enumerate(hdr):
            cell = tbl.cell(0, ci)
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(self.p["primary-strong"] if ci == len(hdr) - 1 else self.p["body-text"])
            cell.text = h
            r = cell.text_frame.paragraphs[0].runs[0]
            r.font.size, r.font.bold, r.font.name = Pt(SIZES["body"] + 2), True, self.bf
            r.font.color.rgb = rgb("#FFFFFF")
        for ri, row in enumerate(rows, start=1):
            for ci, val in enumerate(row):
                cell = tbl.cell(ri, ci)
                cell.fill.solid()
                cell.fill.fore_color.rgb = rgb("#FFFFFF" if ri % 2 else self.p["primary-tint"])
                cell.text = str(val)
                r = cell.text_frame.paragraphs[0].runs[0]
                r.font.size, r.font.name = Pt(SIZES["body"]), self.bf
                r.font.color.rgb = rgb(self.p["ink"])
        self.footer(s)

    def L_story(self, s, sl):
        self.bg(s, self.p["primary-strong"])
        self.text(s, M, 1.0, W - 2 * M, 2.6, sl.get("headline", ""), SIZES["h1"] + 4, "#FFFFFF", self.hf, True,
                  anchor=MSO_ANCHOR.MIDDLE)
        self.rect(s, M + 0.05, 3.75, 1.1, 0.07, self.p["accent"])
        if sl.get("subhead"):
            self.text(s, M, 4.0, LEFT_W, 1.6, sl["subhead"], SIZES["h2"], "#FFFFFF")
        self.image(s, sl.get("image"), 8.2, 0.9, h=2.7)
        self.footer(s, dark=True)

    def L_process(self, s, sl):
        self.bg(s, self.p["surface"])
        self.headline(s, sl)
        steps = self.d.get("mechanism", {}).get("steps", [])
        focus = sl.get("focus_step")
        n = max(1, len(steps))
        col = (W - 2 * M) / n
        cy = 2.75
        self.rect(s, M + col / 2, cy - 0.04, col * (n - 1), 0.08, self.p["primary-tint"])
        for i, st in enumerate(steps):
            cx = M + col * (i + 0.5)
            hi = focus is not None and i + 1 == focus
            c = self.rect(s, cx - 0.42, cy - 0.42, 0.84, 0.84, self.p["accent"] if hi else self.p["primary-strong"], MSO_SHAPE.OVAL)
            c.text_frame.text = str(i + 1)
            r = c.text_frame.paragraphs[0].runs[0]
            r.font.size, r.font.bold, r.font.name = Pt(SIZES["h2"]), True, self.hf
            r.font.color.rgb = rgb(self.p["ink"] if hi else "#FFFFFF")
            c.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
            self.text(s, cx - col / 2 + 0.05, cy + 0.55, col - 0.1, 0.8, st.get("name", ""), SIZES["body"] + 2,
                      self.p["ink"], self.bf, True, align=PP_ALIGN.CENTER)
        if sl.get("body"):
            self.text(s, M, 4.2, LEFT_W, 2.5, sl["body"], SIZES["body"] + 2, self.p["body-text"], bullets=True)
        self.footer(s)

    def L_offer(self, s, sl):
        self.bg(s, self.p["ink"])
        self.text(s, M, 0.55, W - 2 * M, 1.2, sl.get("headline", ""), SIZES["h1"], "#FFFFFF", self.hf, True,
                  anchor=MSO_ANCHOR.MIDDLE)
        self.rect(s, M + 0.05, 1.8, 1.1, 0.07, self.p["accent"])
        ap = self.d.get("appointment", {})
        box_y = 2.2
        self.rect(s, M, box_y, LEFT_W, 1.5, self.p["primary-strong"])
        self.text(s, M + 0.25, box_y + 0.12, LEFT_W - 0.5, 0.45, "You'll walk away with:", SIZES["body"], self.p["accent"], bold=True)
        self.text(s, M + 0.25, box_y + 0.55, LEFT_W - 0.5, 0.9, ap.get("deliverable", ""), SIZES["body"] + 2, "#FFFFFF")
        self.text(s, M, box_y + 1.75, LEFT_W, 2.6, sl.get("body", []), SIZES["h2"] - 2, "#FFFFFF", bullets=True)
        self.footer(s, dark=True)

    def L_qr(self, s, sl):
        self.bg(s, self.p["surface"])
        self.headline(s, sl)
        url = sl.get("url") or self.d.get("appointment", {}).get("url", "")
        try:
            import qrcode
            img = qrcode.make(url, border=1)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            s.shapes.add_picture(buf, Inches(M), Inches(2.3), Inches(3.0), Inches(3.0))
        except Exception:
            pass
        self.text(s, M + 3.3, 2.3, 3.3, 0.6, "Scan, or go to:", SIZES["body"], self.p["body-text"])
        self.text(s, M + 3.3, 2.8, 5.5, 0.8, sl.get("display_url") or url, SIZES["h2"], self.p["primary-strong"], bold=True)
        if sl.get("body"):
            self.text(s, M + 3.3, 3.6, 2.9, 2.6, sl["body"], SIZES["body"], self.p["body-text"], bullets=True)
        if self.d.get("disclosure_short"):
            self.text(s, M, H - 0.9, LEFT_W, 0.5, self.d["disclosure_short"], SIZES["small"], self.p["body-text"])

    def build(self):
        for sl in self.d["slides"]:
            s = self.prs.slides.add_slide(self.blank)
            getattr(self, "L_" + sl.get("layout", "bullets"), self.L_bullets)(s, sl)
            s.notes_slide.notes_text_frame.text = sl.get("speaker_script", "")
        return self.prs


def validate(d, draft):
    errs, warns = [], []
    slides = d.get("slides", [])
    total = 0
    callouts = chats = 0
    for sl in slides:
        n = sl.get("number", "?")
        sc = sl.get("speaker_script", "")
        if not sc.strip():
            errs.append(f"slide {n}: no speaker script (a deck without notes is incomplete)")
        if sl.get("layout") not in LAYOUTS:
            errs.append(f"slide {n}: unknown layout '{sl.get('layout')}'")
        w = words(sc)
        total += w
        callouts += sc.count("[BOOKING CALLOUT")
        chats += 1 if (sl.get("chat_prompt") or re.search(r"in the chat", sc, re.I)) else 0
        if sl.get("act") == 2:
            ang = (sl.get("angle") or "").lower()
            if ang not in ANGLES:
                errs.append(f"slide {n}: Act 2 slide must name a Through Line angle (got '{ang or 'none'}')")
        hl = sl.get("headline", "")
        if len(hl.split()) > 12 and sl.get("layout") not in ("title", "statement", "story"):
            warns.append(f"slide {n}: headline is {len(hl.split())} words (billboard rule: 8 or fewer)")
        body_words = sum(len(str(b).split()) for b in sl.get("body", []))
        if len(sl.get("body", [])) > 5 or body_words > 40:
            warns.append(f"slide {n}: too much on-slide text ({len(sl.get('body', []))} bullets, {body_words} words)")
        if sc and "Timing:" not in sc:
            warns.append(f"slide {n}: script has no 'Timing:' line")
    if callouts != 3:
        (warns if draft else errs).append(f"{callouts} booking callouts (framework requires exactly 3)")
    if not (5500 <= total <= 7500):
        (warns if draft else errs).append(f"total spoken script is {total} words (needs 5,500-7,500 for a 60-minute webinar)")
    if chats < 4:
        warns.append(f"only {chats} chat prompts (aim for one every 5-7 minutes)")
    text = json.dumps(d)
    for m in sorted(set(x[0] if isinstance(x, tuple) else x for x in re.findall(RISKY, text, re.I))):
        warns.append(f"compliance: '{m}' appears; check the context and qualifiers")
    return errs, warns, total


def write_script(d, total, out):
    lines = [f"# {d.get('deck_title', 'Webinar')}: Speaker Script", "",
             f"Total spoken words: {total:,} (about {round(total / 140)} minutes at 140 words per minute)", ""]
    for sl in d["slides"]:
        tag = " · BOOKING CALLOUT" if "[BOOKING CALLOUT" in sl.get("speaker_script", "") else ""
        lines += [f"## Slide {sl.get('number')}: {sl.get('headline', '')}",
                  f"*Act {sl.get('act', '?')} · {sl.get('layout')} · angle: {sl.get('angle', '-')}{tag}*", "",
                  sl.get("speaker_script", ""), ""]
    with open(os.path.join(out, "script.md"), "w") as f:
        f.write("\n".join(lines))


def write_run_of_show(d, out):
    t = 0
    rows = ["# Run of Show", "", "| Clock | Slide | Act | What happens | Notes |", "|---|---|---|---|---|"]
    rows.append("| -0:10 | (pre-show) | | Doors open; music; welcome slide up; greet people by name in chat | Start 2 minutes after the hour |")
    for sl in d["slides"]:
        secs = sl.get("timing_seconds") or round(words(sl.get("speaker_script", "")) / 140 * 60)
        notes = []
        if "[BOOKING CALLOUT" in sl.get("speaker_script", ""):
            notes.append("booking callout")
        if sl.get("chat_prompt"):
            notes.append("chat: " + sl["chat_prompt"])
        if sl.get("workbook_cue", {}).get("instruction"):
            notes.append(f"workbook p{sl['workbook_cue'].get('page')}")
        rows.append(f"| {t // 60}:{t % 60:02d} | {sl.get('number')} | {sl.get('act')} | {sl.get('headline', '')} | {'; '.join(notes)} |")
        t += secs
    rows.append(f"| {t // 60}:{t % 60:02d} | (close) | | End; booking link pinned in chat; replay notice | |")
    with open(os.path.join(out, "run-of-show.md"), "w") as f:
        f.write("\n".join(rows) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--deck", required=True)
    ap.add_argument("--palette")
    ap.add_argument("--option", type=int, default=0)
    ap.add_argument("--out", required=True)
    ap.add_argument("--draft", action="store_true", help="don't fail on word count / callout count")
    a = ap.parse_args()
    with open(a.deck) as f:
        d = json.load(f)
    errs, warns, total = validate(d, a.draft)
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
        palette, fonts = o["palette"], o["fonts"]
    os.makedirs(a.out, exist_ok=True)
    prs = Builder(d, palette, fonts, os.path.dirname(os.path.abspath(a.deck))).build()
    name = re.sub(r"[^a-z0-9]+", "-", d.get("deck_title", "webinar").lower()).strip("-") or "webinar"
    prs.save(os.path.join(a.out, f"{name}.pptx"))
    write_script(d, total, a.out)
    write_run_of_show(d, a.out)
    print(f"✅ {len(d['slides'])} slides · {total:,} spoken words (~{round(total / 140)} min) → {a.out}/{name}.pptx, script.md, run-of-show.md")


if __name__ == "__main__":
    main()
