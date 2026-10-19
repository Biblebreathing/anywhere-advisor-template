# Stage 04 — Offer, Unique Mechanism & Client Journey

**Purpose:** Decide **what the advisor is known for, what their process is called, what they offer, and the path every prospect takes to become a client.** This is the strategy that the webinars, assessments, website, funnel, and book all carry out. Get this stage right and the later stages are mostly execution.

## Inputs
- `02-knowledge-base/knowledge-base.md` (approved), especially §3 Ideal Client, §5 Process, §6 Stories, §7 Beliefs, §9 Vision, §10 Voice
- `02-knowledge-base/brand-palette.json`
- `03-deep-research/research-summary.md`, `fact-registry.md`, `competitor-scan.md` (if done)
- `01-interview/intake.md`: chosen tracks, appointment goal, capacity, compensation model

## Guides (read before building)
- `mechanism-guide.md`: the problem mechanism, master architecture, step design, naming formulas, scoring, compliance-safe naming, ownability checks
- `client-journey-guide.md`: the 12-stage journey, re-engagement loop, meeting sequence, starting targets

## Steps

### A. Positioning (Claude)
Fill in `positioning-template.md`: who, category, enemy, promise, proof, differentiators, one-liner, messaging pillars. Every claim cites a KB section or fact ID.

### B. Problem mechanism (Claude)
Draft 2–3 options using the formula in the guide. Each must be backed by a fact ID or the advisor's own story. Recommend one.

### C. Steps (Claude)
Build the steps from KB §5 in the advisor's real order. Decide master vs. single-track architecture. Map each step to a webinar track, an assessment section, and a named deliverable. Mark any step the advisor doesn't do yet `[NEW STEP — ADVISOR MUST ADOPT]`.

### D. Name (Claude)
1. Generate 10–15 candidates across at least 4 naming formulas.
2. Score them all, and drop any that fail compliance.
3. Run the ownability checks on the top 3 (web search, USPTO, Amazon, domain availability).
4. Draw a diagram for each of the top 3:
   ```
   python3 tools/mechanism_diagram.py --name "<Name>" --step "..." --step "..." \
     --detail "..." --palette clients/<slug>/02-knowledge-base/brand-palette.json \
     --out clients/<slug>/04-offer-and-mechanism/options/<n>
   ```

### E. Offer stack (Claude)
Fill in `offer-stack-template.md`. Spend the most care on the **named appointment offer** and its take-home deliverable.

### F. Client journey (Claude)
Fill in `client-journey-template.md`, including the **goal math** (from the appointment goal back to the registrants needed), the meeting agendas built from the mechanism, the re-engagement loop, and the CRM tags.

### G. Mechanism review with the advisor (20-minute call or email)
Send `mechanism-review-email.md` with the three diagrams. The advisor:
- Picks a name (or asks for a mix)
- Confirms each step with **"Yes, that's what I do"**, and agrees to adopt any new step
- Approves the problem mechanism, the appointment name, and the deliverable

Then submit the name and the positioning statement to the advisor's **compliance approver.**

### H. Finalize (Claude)
Write the chosen version into `unique-mechanism.md`, generate the final `mechanism-row.svg` and `mechanism-stack.svg` in the client folder, and mark the status **Compliance approved** with the date.

## Outputs (in `clients/<slug>/04-offer-and-mechanism/`)
| File | What it is |
|---|---|
| `positioning.md` | Who, category, enemy, promise, one-liner, pillars |
| `unique-mechanism.md` | Problem mechanism, scored names, ownability results, steps, one-liner, how it runs through every asset |
| `offer-stack.md` | Value ladder + the named appointment offer |
| `client-journey.md` | Goal math, the 12-stage map, meetings, re-engagement, CRM tags |
| `mechanism-row.svg`, `mechanism-stack.svg` | Final diagrams |
| `options/` | The shortlisted diagrams shown to the advisor |

## Done when
- [ ] The advisor has confirmed every step as real (or agreed to adopt it)
- [ ] The name passed the compliance check (pass/fail) and the ownability checks, and the advisor chose it
- [ ] Every chosen webinar track and the assessment map to a step
- [ ] The appointment offer has a name, qualifiers, and a tangible deliverable
- [ ] The goal math shows the registrants and leads needed per month, within the advisor's capacity
- [ ] The compliance approver has signed off on the name and positioning (or it's submitted, with the date noted)
