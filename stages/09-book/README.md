# Stage 09 — The Book

**Purpose:** Write the advisor's book: the authority asset that pre-sells the mechanism, gets passed between friends and family, and brings readers back to the calendar through a tracked QR code in every chapter. Built on **Quill**, Terrence McMahon's One Hour Book / 24-Hour Publishing method, in a **pipeline edition** that reuses everything Stages 01–08 already produced.

- **`quill-custom-instructions-pipeline-edition.md`**: paste-ready Quill Project instructions (v2), for running the book in Claude chat instead of the repo.

## Read first
| File | What it is |
|---|---|
| `quill-method.md` | The 20 Quill steps mapped to this pipeline: what's drafted from earlier stages, what's interviewed, the gates, and the Book Bible as files |
| `book-models.md` | Three proven book architectures: **A. Parable + Field Guide**, **B. Psychology + Myth-Buster**, **C. Mechanism Field Guide**, plus title architecture |
| `book-interview-prompt.md` | The **gap-targeted book interview** (20–30 min, run in any AI), with the gap checklist |
| `voice-and-craft.md` | KB-1 house style plus advisor-book rules (the [LINT] items are enforced by `book_lint.py`) |
| `chapter-template.md` | The Transformational Chapter Formula **scaled to ~2,200 words**, model rhythms, source-file directives, intro/closing, front and back matter, disclaimer block |
| `worksheets-and-qr.md` | Worksheet rules and library by track; QR rules (redirect links, tracking, print spec) |
| `committee-review.md` | Steps 12–14: five-lens critique, editor review, the Committee of Experts (+ target reader panel + compliance reviewer), the 8.0 gate |
| `book-bible-template.md`, `blueprint-template.md` | Templates for Steps 1–5 and Step 8 |
| `examples/sample-book/` | A small, fictional sample in the exact file format (passes the linter; assembles to .md and .docx) |

**Taste reference:** Quill's KB-3 gold standard ("CALM Money"): one idea, one mechanism, one promise; story carries the teaching; every chapter ends with a takeaway and an action; regulated-topic restraint; short on purpose.

## Inputs
Everything from Stages 01–08, especially: the approved knowledge base and consent log (02), the fact registry and fact sheets (03), the mechanism, positioning, and appointment offer (04), the assessment (05), the webinar Big Ideas and objections (06), the domain (07), and the bonus hub and booking links (08/10).

## Steps
1. **Pipeline Intake** (Claude): draft `book-bible.md` (Steps 1–5) from earlier stages. Lock the mechanism, villain, CTA, and compliance line. Recommend a book model with a one-line reason.
2. **Gap interview** (advisor, 20–30 min): fill in `book-interview-prompt.md` with what we know and the gaps; the advisor runs it; save the addendum as `book-interview.md`. Log new consent items in the Stage 02 consent log.
3. **Refine the arc** (Step 7) → `refined-arc.md`.
4. **Blueprint** (Step 8) → `blueprint.md` from the template. **GATE: advisor sign-off.**
5. **Write** (Steps 9–11): introduction, then **one chapter per session** (confirmed before the next), then the closing, in `chapters/`. Worksheets in `worksheets/`; codes in `qr-map.json`; facts as `<!-- F-### -->` comments.
6. **Check:** `python3 tools/book_lint.py --book clients/<slug>/09-book` after every chapter. Keep errors at zero.
7. **Polish** (Steps 12–13): critique → editor review → linter clean.
8. **Committee** (Step 14): scores in `critique.md`. **GATE: composite 8.0+, compliance 8+.** All flags into `verify-list.md`; send to the attorney and the firm's compliance approver.
9. **Assemble:** `python3 tools/assemble_book.py --book clients/<slug>/09-book` → `build/manuscript.md`, `build/manuscript.docx`, `build/qr/` (print-ready codes, redirect files, launch test list).
10. **Publish the QR redirects** on the advisor's site (Stage 07) so every printed code works before printing.
11. Hand off to **Stage 10** (book website and funnel) and **Stage 11** (KDP formatting, cover, metadata).

## Outputs (in `clients/<slug>/09-book/`)
`book.json` · `book-bible.md` · `book-interview.md` · `refined-arc.md` · `blueprint.md` (signed off) · `chapters/` · `worksheets/` · `front-matter.md` · `back-matter.md` · `qr-map.json` · `critique.md` · `verify-list.md` · `style-sheet.md` · `build/` (manuscript, QR codes, redirects, lint report)

## book.json
```json
{
  "title": "", "subtitle": "", "author": "", "model": "C. Mechanism Field Guide",
  "mechanism": "exact locked spelling", "villain": "the named enemy",
  "compliance_line": "exact approved sentence that must appear in the front matter",
  "front_matter": "front-matter.md", "back_matter": "back-matter.md",
  "chapters": ["00-introduction.md", "01-....md", "...", "13-closing.md"],
  "targets": {"chapter": [1800, 2400], "intro": [1500, 2500], "closing": [1500, 2500]}
}
```

## Done when
- [ ] Blueprint signed off by the advisor
- [ ] Every chapter confirmed; linter shows 0 errors
- [ ] Committee composite 8.0+, compliance 8+
- [ ] `verify-list.md` fully resolved or explicitly accepted; attorney and compliance approvals logged
- [ ] Consent confirmed for every real person
- [ ] Manuscript assembled; QR codes generated; redirects published and tested
