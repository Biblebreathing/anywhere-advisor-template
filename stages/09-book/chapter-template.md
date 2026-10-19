# Chapter Template, Front & Back Matter

## 1. The Transformational Chapter Formula, scaled (Quill Step 10)
Quill's original formula adds up to about 3,500 words a chapter, which makes a 42,000–52,000-word book. Advisor books are **25,000–35,000 words**, so the same five movements are scaled to **about 2,200 words** (range 1,800–2,400):

| Movement | Words | What it does |
|---|---|---|
| **1. Opening Hook** | ~300 | An emotional scene (author, client, or parable); the chapter's core problem; curiosity; connection to the reader's life |
| **2. Explanation** | ~600 | The one idea: what it is, why it matters, key components, the common obstacle. Plain language, one analogy. |
| **3. Illustration** | ~550 | The author's experience and/or a client case (with consent), or the parable family. Concrete detail. |
| **4. Implementation** | ~450 | Steps the reader can take, pitfalls, what "done" looks like. Tie to the mechanism step. |
| **5. Integration** | ~300 | The worksheet or reflection, **The One Thing**, the QR code, a one-line bridge to the next chapter |

### Model-specific rhythms (they wrap the formula)
- **A. Parable + Field Guide:** Narrative Beat (movements 1 + 3) → **What [Advisor] Wants You to Know** (2 + 4) → **The One Thing** (5). Never merge or skip the three labeled sections.
- **B. Psychology + Myth-Buster:** the chapter title is the excuse itself; it ends with a one-page **Finish This Thought** reflection.
- **C. Mechanism Field Guide:** each step chapter ends with that step's **deliverable preview** ("In a [Named Appointment], this becomes your [Deliverable]") plus the QR code to the matching assessment section.

## 2. Source format for chapter files
Write each chapter in `chapters/NN-slug.md`:
```markdown
# Chapter 3: A Will Doesn't Keep You Out of Court

Prose in the advisor's voice. Fact citations go in HTML comments so they never print. <!-- F-014 -->

{{worksheet:who-is-named}}

**The One Thing:** List every account you own and write down who is named on it.

{{qr:ch03-beneficiary-checklist}}
```
- `{{worksheet:id}}` inserts `worksheets/id.md` (a page break before and after it in print)
- `{{qr:id}}` inserts the QR code image + caption + short URL from `qr-map.json`
- `{{pagebreak}}` starts a new page (title page, copyright page, dedication)
- `<!-- ... -->` comments hold fact IDs and notes; the assembler removes them

## 3. The introduction (Quill Step 9)
- **Opening scene (~750 words):** a vivid moment (the anchor story, or the parable's stasis) with a relatable struggle and a hint of transformation
- **The promise (~500 words):** name the problem (and the villain), show what's possible, introduce the mechanism, establish authority naturally
- **The invitation (~250 words):** acknowledge the reader's pain, show understanding, explain how to use the book (worksheets, QR codes)
- **QR:** the reader bonus hub (all worksheets in one place)

## 4. The closing (Quill Step 11)
- **Celebration (~400):** honor the reader for finishing (most people don't)
- **Transformation review (~500):** the shifts, the mechanism in one page
- **Future vision (~300):** the reader's life with it done
- **The one action (~400):** what to do this week, **including how to do it without the author** (how to choose a professional, what to ask, what it should cost); the author's named appointment is one clear option
- **Author's closing message (~400):** personal and memorable. No banned closers.
- **QR:** the named appointment

## 5. Front matter (Quill Step 18; finalized in Stage 11)
1. **Title page:** title, subtitle, author
2. **Copyright page:** © year and author; All rights reserved; edition; ISBN; publisher line; **disclaimer block** (below); credits
3. Dedication (optional)
4. Table of contents
5. Endorsements (optional, real and permitted only)
6. **How to Use This Book:** worksheets, QR codes, the bonus hub

**Disclaimer block (adapt with compliance; the approved wording goes in `style-sheet.md`):**
> This book provides general educational information only. It is not individualized legal, tax, investment, insurance, or financial advice. Consult qualified professionals about your situation. [For parables: The characters in this book are fictional composites; any resemblance to actual persons is coincidental.] Client stories are shared with permission, and names and identifying details have been changed. Examples are illustrations, not guarantees of results. [Advisor's registration and firm disclosure, as approved.] [Anywhere Advisor estate titles: the exact approved program compliance line.]

## 6. Back matter (Quill Step 18)
1. **Your Next Step:** the named appointment, its deliverable, QR + short URL, phone
2. **About the Author:** credibility, the human story, photo, contact
3. **Resources:** the bonus hub (QR), the worksheet list, the assessment, the next webinar
4. **A Small Request:** one short paragraph inviting an honest Amazon review (QR to the review page). No incentives for reviews.
5. **Glossary** in plain language (for regulated topics)
6. Also by the author (if any)
