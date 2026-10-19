# Critique, Editing & Committee Review (Quill Steps 12–14)

## Step 12: Five-lens critique (Quill KB-2)
Review the whole draft as a senior publisher in transformational nonfiction:
1. **Narrative flow:** hook strength, arc progression, transitions, pacing, story-to-teaching balance
2. **Reader engagement:** emotional connection, teaching clarity, implementation support, participation (worksheets), transformation path
3. **Commercial viability:** positioning, unique value, differentiation, audience fit, **funnel fit** (does each chapter create a reason to scan and book?)
4. **Structure and formatting:** chapter organization, frameworks, exercise placement, visual elements
5. **Transformation effectiveness:** problem clarity, solution credibility, ease of implementation, evidence

For each issue: what it is, its impact, the fix, an example, and the expected improvement. List them in priority order.

## Step 13: Editor review (Quill KB-2 + KB-1)
A line edit across technical elements, narrative flow, clarity, language, and reading experience. **Never flatten the author's voice.** Then run the linter until it's clean:
```
python3 tools/book_lint.py --book clients/<slug>/09-book
```
Fix every error. Review every warning, then fix it or note why it stays.

## Step 14: The Committee of Experts (quality gate)
Score 1–10. Each reviewer gives a **score, two strengths, and two specific fixes.**

### Commercial committee (Quill KB-5)
- **Alex Hormozi lens:** offer strength and the value equation. Is the named appointment irresistible?
- **Russell Brunson lens:** hook, story, offer, and funnel fit
- **Jay Abraham lens:** strategic positioning and preeminence
- **Dan Kennedy lens:** direct-response salesmanship and CTA strength

### Editorial committee (Quill KB-5)
Developmental editor · line editor · narrative structure · reader experience

### Added in the pipeline edition
- **Target reader panel:** three simulated readers built from the avatar (e.g., a 62-year-old married pre-retiree; a 71-year-old widow; a 55-year-old adult child buying for a parent). Each answers: *Would I keep reading after chapter 1? Where did I get lost? Where did I feel sold to? Did I scan a QR code? Would I book?* Score = how likely they are to finish and act.
- **Compliance reviewer:** guarantees, performance claims, product names, unqualified "tax-free"/"safe," misuse of regulated titles ("fiduciary," "specialist"), testimonial rules, legal advice (unauthorized practice of law), consent for every real person, the disclosure block, the exact compliance line. **Compliance below 8 fails the manuscript outright.**

### The gate
- **Composite 8.0 or higher**, no committee below 7, compliance 8 or higher → proceed to production
- Otherwise: a ranked fix list, revise, re-score (when the target is raised mid-project, **rewrite, don't polish**)
- **Before leaving Step 14:**
  - [ ] Every VERIFY / FACT CHECK item is in `verify-list.md` (none in the prose), resolved or accepted by the advisor
  - [ ] Attorney review items listed by chapter and sent
  - [ ] Consent confirmed for every real person (Stage 02 consent log)
  - [ ] The villain, mechanism, and CTA are locked and consistent (lint passes)
  - [ ] Linter clean
  - [ ] The whole manuscript has been submitted to the firm's compliance approver (date logged)
