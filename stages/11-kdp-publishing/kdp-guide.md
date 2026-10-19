# KDP Publishing Guide (Quill Steps 15–20)

From a committee-approved manuscript (Stage 09) to a paperback and Kindle ebook live on Amazon. **The order matters:** illustrations → interior → *final page count* → cover → listing → proof → launch. Specs follow Quill KB-5 and KB-6. **KDP changes its specs, printing costs, and royalty rules. Verify on kdp.amazon.com before every upload; the KDP previewer is the final authority.**

---

## Step 15: Illustrations (before formatting)
1. **Illustration map:** list every placement (chapter openers, concept diagrams, story moments) with chapter, concept, and purpose.
2. **Style lock:** one style per book, written into every prompt (e.g., "minimalist black-and-white line illustration, high contrast, print-ready"). Consistency beats beauty.
3. **Always include:** the **mechanism diagram** from Stage 04 (`mechanism_diagram.py`, stack layout) converted to grayscale for the print interior.
4. **Prompt pack (Ideogram or similar):** subject, composition, the identical style block, aspect ratio, "black and white, high contrast, print-ready." No text inside images.
5. **Print spec:** grayscale for B&W interiors, 300 DPI at placed size, no fine gray gradients (they band), no full-bleed images in a no-bleed interior.
6. **Approval:** show the set in one gallery; the advisor approves before typesetting.
Place images in chapter files as `![](../images/name.png)` (inside the book folder).

## Step 16: Interior (6×9 print PDF)
```
python3 tools/kdp_interior.py --book clients/<slug>/09-book --out clients/<slug>/11-kdp-publishing/build \
  --palette clients/<slug>/02-knowledge-base/brand-palette.json --paper white --size 11.5
```
- **Typography for 55+ readers:** Literata (a free Google font designed for long-form reading) at **11.5pt**, line height 1.45, justified with hyphenation; headings in the brand's heading font. All fonts embedded.
- **Margins:** mirror margins; the **gutter is set from the final page count** (KDP minimum: 0.375" up to 150 pages, 0.5" to 300, 0.625" to 500, 0.75" to 700, 0.875" to 828; house standard 0.75" minimum); outside 0.6".
- **Book conventions built in:** a title page, front matter in roman numerals, a generated table of contents with real page numbers, **chapters start on right-hand pages** (blank pages inserted automatically), page 1 at the introduction, running heads (book title on left pages, chapter title on right pages, none on chapter openers or blank pages), worksheets on their own pages, vector QR codes at 1".
- **Paper:** white (crisper for worksheets and QR codes) or cream (a warmer reading feel); it changes the spine width.
- `interior-report.json` records the page count, margins, and spine width for the cover.
- **Large print (optional):** run with `--size 16` to produce a large-print edition. Check KDP's large-print requirements and list it as a separate edition.

## Step 17: Cover (wraparound, from the final page count)
```
python3 tools/kdp_cover.py --cover clients/<slug>/11-kdp-publishing/cover.json \
  --interior clients/<slug>/11-kdp-publishing/build/interior-report.json \
  --palette clients/<slug>/02-knowledge-base/brand-palette.json \
  --qr clients/<slug>/11-kdp-publishing/build/qr/hub.svg --out clients/<slug>/11-kdp-publishing/build
```
- **The math (KB-6):** spine = pages × 0.002252" (white) or × 0.0025" (cream); width = 0.125 + 6 + spine + 6 + 0.125; height 9.25". **Re-run whenever the page count changes.** A misaligned spine is the most common rejection.
- **Zones:** artwork through the bleed; all text inside the live area (0.375" house inset); spine text only above 79 pages (comfortable from ~100); **the barcode zone (2.0" × 1.2", lower right of the back) stays clear.**
- **Default design:** a typographic, two-tone cover in the brand palette (title, accent rule, subtitle, author). It's professional enough to publish and doubles as a proof.
- **Illustrated cover:** generate front art **at 2:3 with no text** (KB-6 prompt template: "Book cover design, [central image concept], [style], [mood], [palette], strong focal point, clean composition with space reserved at top for title text and bottom for author name, no text, no words, no letters, professional trade paperback aesthetic, 2:3 aspect ratio"), set `front_art`, and rebuild. One dominant image; 2–3 colors.
- **Check `cover-guides.png`** (trim, spine folds, live area, bleed, barcode zone) and **`thumbnail-100px.png`** (Amazon shows covers at ~100 px wide first: the title must read).
- `front-cover.jpg` (1800×2700) is the ebook cover, and is used on the book offer page and in ads.
- **Color:** the PDF is RGB with fonts embedded. KDP prints in CMYK, so colors can shift slightly: approve them on a printed proof. (KB-6's house rule is CMYK export; if KDP rejects the file, convert it in a design tool.)

## Step 18: Front and back matter (final pass)
Confirm against `09-book/chapter-template.md` §5–6: the copyright page with the **approved disclaimer and exact compliance line**, the ISBN (after KDP assigns it, or the advisor's own), How to Use This Book, Your Next Step (QR to the appointment), About the Author, Resources, A Small Request (the review page), and the glossary. Re-run the interior after any change, then the cover.

## Step 19: Amazon listing
```
python3 tools/kdp_listing.py --listing clients/<slug>/11-kdp-publishing/listing.json --book clients/<slug>/09-book \
  --interior clients/<slug>/11-kdp-publishing/build/interior-report.json --out clients/<slug>/11-kdp-publishing/build
```
- **Title and subtitle match the cover and the interior exactly.** The subtitle carries the searchable promise.
- **Description (≤ 4,000 characters, basic HTML only):** hook line → problem → promise → "Inside, you'll discover" (5–7 bullets) → author credibility → the educational disclaimer line → call to action.
- **7 keyword slots (≤ 50 characters each):** distinct phrase clusters built from reader-problem phrases, solution phrases, audience phrases, and adjacent topics. Don't repeat title words, and don't use quotes, subjective claims ("best seller"), "free," competitor names, or Amazon program names. Research them by typing seed phrases into Amazon search and noting the autocomplete suggestions; check that competing books exist but don't dominate.
- **3 categories:** one broad and credible, two narrow and winnable (check the sales rank of the #1 book in each candidate category; a modest #1 rank means a winnable category at launch).
- **Pricing:** authority paperbacks typically $14.99–$19.99; strategy titles lower. The tool estimates printing cost and royalty. The ebook is often $2.99–$9.99 (the 70% royalty band; verify). **KDP Select** (ebook exclusivity) only if it fits the funnel.
- **ISBN / imprint:** KDP's free ISBN lists the publisher as "Independently published." The advisor's own ISBN (Bowker in the US) lets the firm's imprint appear as publisher. Decide before upload; it can't change later for that edition.
- **Compliance:** the description and subtitle go to the approver with the manuscript.

## Ebook
```
python3 tools/kdp_ebook.py --book clients/<slug>/09-book --cover clients/<slug>/11-kdp-publishing/build/front-cover.jpg \
  --out clients/<slug>/11-kdp-publishing/build
```
QR codes become **tappable links** ("Tap to download this worksheet"); worksheets reflow as tables; the table of contents is generated. **Open it in Kindle Previewer** (free from Amazon) on phone and tablet views before upload.

## Step 20: Upload, proof, and launch
**Upload (paperback):** Book details (from `listing.md`) → Content: upload `interior.pdf`, choose B&W + paper color, 6×9, **no bleed**, matte or glossy cover, upload `cover.pdf` → **launch the previewer and fix every flagged issue** → Pricing → **order an author proof copy before publishing.**
**Upload (ebook):** a separate Kindle eBook title linked to the paperback: upload the `.epub` and `front-cover.jpg`, run the previewer, set pricing.

### Launch checklist (KB-5 Step 20 + pipeline)
- [ ] `verify-list.md` fully resolved or accepted; attorney and **firm compliance** approvals logged
- [ ] Interior: fonts embedded, page count recorded, previewer clean
- [ ] Cover: spine matches the final page count, barcode zone clear, previewer clean, readable at thumbnail size
- [ ] Metadata locked: the title matches everywhere; description, 7 keywords, 3 categories, pricing
- [ ] **Printed proof reviewed by the advisor**: typos, images, margins, colors, and **every QR code scanned from the paper copy** (iPhone + Android) to the right hub section
- [ ] The book funnel (Stage 10) is live: offer page, bonus hub, redirects, reader sequence (S10)
- [ ] Review plan: advance readers lined up (they disclose the free copy; no incentives)
- [ ] Author Central profile (photo, bio, links) and the book page claimed after publication; A+ Content (optional)
- [ ] Author copies ordered for the playbook (pre-meeting mailing, referral partners, client kits)
- [ ] Handoff package archived: source files, `interior.pdf`, `cover.pdf`, `.epub`, `listing.md`, prompt packs, Book Bible
