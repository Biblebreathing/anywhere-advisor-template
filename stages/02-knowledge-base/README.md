# Stage 02 — Knowledge Base Review, Gap-Fill & Brand Kit

**Purpose:** Turn the interview's draft into the two **approved foundations** that every later asset is built from:

1. **The approved Knowledge Base:** accurate, complete, and cleared for consent and compliance.
2. **The Brand Kit:** logo, colors, fonts, headshot, and photo direction.

The website, funnel, webinars, and book all pull from these two files. Time spent here saves rework in every later stage.

## Inputs (from `clients/<slug>/01-interview/`)
- `knowledge-base.md` (the draft written by the interview AI)
- `transcript.md`
- `intake.md`, plus the logo and headshot files the advisor sent

## Steps

### A. Audit the draft (Claude, ~10 min)
Run `review-checklist.md` against the draft and the transcript. Fix what can be fixed from the transcript: missing stories, paraphrased quotes, missing flags. Anything the transcript can't answer goes onto the follow-up list.

### B. Brand Kit (Claude)
1. Save the files the advisor sent in `clients/<slug>/02-knowledge-base/assets/` as `logo.<ext>` (plus `logo-white.<ext>` and `logo-icon.<ext>` if provided) and `headshot-1.jpg`, `headshot-2.jpg`, and so on.
2. **If the advisor has a logo**, run:
   ```
   python3 tools/brand_kit.py --logo clients/<slug>/02-knowledge-base/assets/logo.png \
     --headshot clients/<slug>/02-knowledge-base/assets/headshot-1.jpg \
     --name "<Firm Name>" --out clients/<slug>/02-knowledge-base
   ```
   If they gave official color codes, use `--primary` and `--accent` instead of extracting colors from the logo. If the logo is a vector file (`.svg`, `.ai`, `.eps`, `.pdf`), export a PNG copy for the tool and keep the original.
3. **If the advisor has no logo (new company)**, pick **3 presets** that fit how they said they want the brand to feel (`python3 tools/brand_kit.py --list`), and run:
   ```
   python3 tools/brand_kit.py --preset heritage --preset teal --preset slate \
     --headshot clients/<slug>/02-knowledge-base/assets/headshot-1.jpg \
     --name "<Firm Name>" --out clients/<slug>/02-knowledge-base
   ```
   The advisor picks one from the preview page. A logo can then be designed in their chosen colors (for example with Canva, or by a designer).
4. Write `brand-kit.md` from `brand-kit-template.md`.
5. If the headshot is missing or unusable (low resolution, dated, casual snapshot), send `headshot-guide.md`.

### C. Follow-up (advisor, ~15 min)
Send `follow-up-email.md`, filled in with: up to 10 follow-up questions, consent requests, the knowledge base summary to check, and the brand preview page (or options) to approve. A 15-minute call works too; record the answers either way.

### D. Finalize (Claude)
1. Save the advisor's answers to `follow-up-answers.md`.
2. Update the knowledge base, remove resolved flags, and set the header to **Approved**, with the date.
3. Record every consent decision in `consent-log.md`.
4. Record the chosen palette in `brand-kit.md`.

## Outputs (in `clients/<slug>/02-knowledge-base/`)
| File | What it is |
|---|---|
| `knowledge-base.md` | The approved Knowledge Base (same structure as the draft, plus an approval header) |
| `follow-up-answers.md` | The advisor's answers, verbatim |
| `consent-log.md` | Who and what may appear publicly |
| `brand-kit.md` | The brand rules every asset follows |
| `brand-kit-preview.html` | Visual preview (or options, for new companies) |
| `brand-palette.json` | Machine-readable colors and fonts for the website and funnel stages |
| `assets/` | Logo and headshot originals |

## Done when
- [ ] Every item in `review-checklist.md` passes
- [ ] The advisor has answered the follow-ups (or chosen to skip specific ones; note which)
- [ ] Every `[ANONYMIZE]` person and sensitive detail has a decision in `consent-log.md`
- [ ] The palette is chosen, and the logo and headshot are on file (or flagged as pending)
- [ ] The knowledge base header says **Approved** with a date
