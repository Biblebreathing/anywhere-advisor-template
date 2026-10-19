# The Quill Method, Pipeline Edition

Quill is Terrence McMahon's end-to-end ghostwriting and publishing method (the One Hour Book / 24-Hour Publishing method: 20 steps in 7 phases; source knowledge bases KB-1 to KB-6). This is the **Anywhere Advisor pipeline edition**. The method and its quality bar stay the same. What changes:

1. **Pipeline Intake replaces most interviewing.** By Stage 09 the advisor has already been interviewed (01), their knowledge base approved (02), research done (03), and their mechanism, positioning, and offer approved (04). Quill **drafts** Steps 1–5 from those files and confirms them. It doesn't re-ask 31 questions.
2. **One short, gap-targeted book interview** (`book-interview-prompt.md`, 20–30 minutes) replaces the long author interview. It asks only what the book still needs.
3. **The mechanism is locked.** The book uses the Stage 04 name and steps exactly. Quill never renames it.
4. **Facts come from the fact registry** (Stage 03) with IDs, so most verification happens *before* drafting, not at the end.
5. **The book is wired into the funnel:** every chapter has a tracked QR code to the right next step (assessment, worksheet download, webinar, or appointment).
6. **The house rules are enforced by a tool** (`tools/book_lint.py`): em dashes, banned words, banned closers, flags left in, mechanism spelling, reading level, word counts.
7. **The chapter formula is scaled** to the advisor-book length (25,000–35,000 words).
8. **Firm compliance review** is a gate, alongside attorney review.

---

## The Book Bible = the client's `09-book/` folder
In chat, the Book Bible lives in context and can get lost. Here it's a set of files, so nothing is ever lost between sessions:

```
clients/<slug>/09-book/
  book-bible.md            Steps 1-5 artifacts: Big Idea Brief, mechanism (locked), XYZ Bridge, avatar + journals, 8-point arc, villain, CTA
  book-interview.md        The gap interview output (Book Interview Addendum)
  refined-arc.md           Step 7
  blueprint.md             Step 8, Deliverable 1 (signed off)
  chapters/00-intro.md … chapters/NN-closing.md     Steps 9-11
  front-matter.md, back-matter.md                    Step 18 (drafted here, finalized in Stage 11)
  worksheets/*.md          One per chapter exercise
  qr-map.json              Every QR code: id, chapter, destination, tracking
  critique.md              Steps 12-14: critique, editor notes, committee scores
  verify-list.md           Every open fact/compliance/consent item, by chapter (never left in the prose)
  style-sheet.md           Spellings, capitalization, numbers, names, the locked terms
  build/                   Assembled manuscript (.md and .docx), QR images, lint report
```

---

## The 20 steps, mapped

| Phase | Quill step | In this pipeline | Source / tool |
|---|---|---|---|
| **1. Foundation** | 1. Big Idea Brief | **Draft** from the knowledge base (§7–8), positioning, research summary. Confirm with the advisor. | Stage 02, 03, 04 |
| | 2. Unique Mechanism | **Locked:** copy the Stage 04 mechanism (name, steps, deliverables). No renaming. | Stage 04 |
| **2. Client Journey** | 3. XYZ Bridge | **Draft** from Stage 04 positioning + KB §3 (X, Y, Z, M, and R = objections) | Stage 02, 04 |
| | 4. Avatar + Hell/Heaven journals | **Generate.** Base the avatar on the KB ideal client; journal language from the client words in KB §3 and Stage 03 voice-of-customer | Stage 02, 03 |
| | 5. 8-Point Story Arc | **Generate** (stasis, trigger, quest, surprise, critical choice, climax, reversal, resolution) | — |
| **3. Author's Story** | 6. Author interview | **Gap-targeted book interview** (20–30 min). Skip it only if the KB already covers every item in the gap checklist. | `book-interview-prompt.md` |
| | 7. Arc refinement | **Generate:** weave the author's journey and client stories into the arc | — |
| **4. Blueprint** | 8. Book outline | **Generate in the chosen book model** (`book-models.md`). **GATE: explicit advisor sign-off. Deliverable 1.** | `book-models.md` |
| **5. Manuscript** | 9. Hook / introduction | Generate (opening scene, promise, invitation) | `chapter-template.md` |
| | 10. Chapters | Generate **one chapter per session**, confirmed before the next | `chapter-template.md` |
| | 11. Closing | Generate (celebration, review, vision, the one action, author's message) | `chapter-template.md` |
| **6. Polish** | 12. Five-lens critique | Generate, in priority order | `committee-review.md` |
| | 13. Editor review | Line edit that preserves the voice; **run `book_lint.py`** until clean | `voice-and-craft.md`, lint |
| **7. Production** | 14. Committee of Experts | Commercial + editorial committees **+ target reader panel + compliance reviewer**. **GATE: 8.0+ composite; compliance 8+.** Pull every flag into `verify-list.md`. | `committee-review.md` |
| | 15. Illustrations | Illustration map + style lock (from the brand kit, grayscale for print) + prompt pack + approval. The mechanism diagram comes from Stage 04 (stack layout). | Stage 11 guide |
| | 16. Interior formatting | **Stage 11** (KDP 6×9) | Stage 11 |
| | 17. Cover | **Stage 11** (KB-6 cover math, using the *final* page count) | Stage 11 |
| | 18. Front and back matter | Draft here (templates in `chapter-template.md`), finalize in Stage 11 | — |
| | 19. Amazon metadata | **Stage 11** | Stage 11 |
| | 20. Launch checklist + handoff | **Stages 10–11** (the book funnel goes live before launch) | Stages 10–11 |

---

## Rules carried over from Quill (non-negotiable)
- **Never fabricate** stories, statistics, quotes, client results, or credentials. If it didn't come from the advisor (or the fact registry), ask.
- **Never put words in the advisor's mouth.** Mirror their exact words, stories, and phrases.
- **Name the villain, the mechanism, and the call to action before drafting.** Lock all three and keep them consistent.
- **Interview steps:** one question at a time. **Generation steps:** draft, then pause for confirmation.
- **Never skip the Step 8 and Step 14 gates.**
- **State which phase and step you're in, and what comes next.**
- **Absorb corrections immediately** and carry them through all later work (update `style-sheet.md`).
- **No em dashes. No AI-sounding prose** (`voice-and-craft.md`).
- **Never leave VERIFY flags in client-facing files.** They live in `verify-list.md`.
- **Legal, tax, medical, and financial claims** are never stated as settled fact without a fact ID; otherwise they're flagged.

## What's new in the pipeline edition
- **Compliance language is exact** and comes from the advisor's approver (recorded in `style-sheet.md`). For Anywhere Advisor estate titles, the program line is stated exactly as approved: *advisors are paid to fund trusts, never to sell or create them.*
- **No guarantees.** Quill's Big Idea question 13 ("what guarantee can be offered?") becomes **risk reversal for the appointment only**: no cost, no obligation, a deliverable they keep. Never an outcome guarantee.
- **Composite characters** (the parable model) are disclosed on the copyright page and never presented as real clients.
- **The whole manuscript goes to the firm's compliance approver** before printing (it's a marketing communication), in addition to attorney review of legal content.
- **The CTA is the Stage 04 named appointment**, reached through QR codes that point at redirect links the advisor controls (`worksheets-and-qr.md`).
