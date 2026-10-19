# Stage 11 — KDP Publishing

**Purpose:** Turn the approved manuscript into a **print-ready 6×9 paperback** (interior and wraparound cover) and a **Kindle ebook**, with a validated Amazon listing, then proof and launch. This covers Quill Steps 15–20, automated with four tools.

## Read first
`kdp-guide.md`: illustrations, interior specs, cover math and design, front and back matter, listing rules (keywords, categories, pricing, ISBN), the ebook, upload, proof, and the launch checklist.

## Inputs
- `09-book/`: a committee-approved, lint-clean book (`book.json`, chapters, worksheets, `qr-map.json`, front and back matter)
- `02-knowledge-base/brand-palette.json` (cover colors and fonts), the headshot
- `10-book-funnel/`: live, so the QR codes work on the proof copy

## Steps
1. **Illustrations** (if any): map → style lock → prompt pack → approval (guide, Step 15).
2. **Interior:** `python3 tools/kdp_interior.py --book … --out … --palette …` → `interior.pdf` + `interior-report.json`
3. **Cover:** write `cover.json` (copy `examples/cover.json`), then `python3 tools/kdp_cover.py --cover … --interior …/interior-report.json --palette … --qr …/qr/hub.svg --out …` → `cover.pdf`, `cover-guides.png`, `front-cover.jpg`, `thumbnail-100px.png`. Review the guides and the thumbnail.
4. **Ebook:** `python3 tools/kdp_ebook.py --book … --cover …/front-cover.jpg --out …` → `.epub`. Check it in Kindle Previewer.
5. **Listing:** write `listing.json` (copy `examples/listing.json`, then research keywords and categories), then `python3 tools/kdp_listing.py --listing … --book … --interior … --out …` → `listing.md` + `description.html`. Fix all errors.
6. **Compliance:** the final interior, cover copy, and listing go to the approver (with the manuscript approval from Stage 09).
7. **Upload** paperback and ebook (guide, Step 20) → previewer → **order a proof** → advisor approves the printed proof (including scanning every QR code) → publish.
8. **Launch:** run the Stage 10 launch plan; claim the Author Central page; order author copies for the playbook.

> Any change to the manuscript after the interior is built means re-running the interior, then the cover (the spine width depends on the page count), then the ebook.

## Outputs (in `clients/<slug>/11-kdp-publishing/`)
| File | What it is |
|---|---|
| `cover.json`, `listing.json` | Sources for the cover and the listing |
| `build/interior.pdf` | Print interior (upload) |
| `build/cover.pdf` | Wraparound cover (upload) |
| `build/<title>.epub` | Kindle ebook (upload) |
| `build/front-cover.jpg` | Ebook cover, website, ads |
| `build/cover-guides.png`, `build/thumbnail-100px.png` | Cover QA |
| `build/listing.md`, `build/description.html` | Copy-paste upload sheet |
| `build/interior-report.json`, `build/cover-report.json` | The math (page count, margins, spine) |
| `launch-checklist.md` | Completed checklist with dates |

## Done when
- [ ] Interior and cover pass the KDP previewer with no issues; the spine matches the final page count
- [ ] Ebook checked in Kindle Previewer
- [ ] The listing tool shows 0 errors; compliance approved the listing copy
- [ ] The advisor approved a **printed proof**, and every QR code was scanned from paper
- [ ] Published; Author Central claimed; author copies ordered; handoff package archived
