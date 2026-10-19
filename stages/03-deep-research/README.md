# Stage 03 — Deep Research

**Purpose:** Add the knowledge the interview deliberately doesn't collect: the advisor's **local market**, **sourced, current facts** for each webinar topic, **competitors**, and **how prospects actually talk**. This lets the webinars, website, and book make specific, credible, compliant claims.

The interview tells us what the advisor **believes and has lived**. Research tells us **what's true right now, where they practice.** When the two disagree, we flag it; we never silently overwrite the advisor.

## Inputs
- `02-knowledge-base/knowledge-base.md` (approved): service area, ideal client, niche, webinar tracks, `[VERIFY]` items
- `01-interview/intake.md`: the webinar tracks they chose, location, registration type

## Two levels

| Level | When | What's included |
|---|---|---|
| **Core** (every advisor) | Always | A. Verify list · B. Topic fact sheets for the advisor's chosen webinar tracks · C. Local market snapshot |
| **Extended** | Advisor has a niche, a crowded market, or is a premium client | D. Competitor scan · E. Voice of the customer · F. Niche deep dive |

## Research modules

**A. Verify list.** Check every `[VERIFY]` item in the knowledge base. Mark each one *Confirmed*, *Corrected* (give the right figure and source), *Can't verify* (rephrase it as the advisor's experience, e.g., "In my practice I've seen…"), or *Unverifiable / remove*.

**B. Topic fact sheets**, one per chosen track: Estate · Tax · Retirement Paycheck · Asset Protection · Long-Term Care. Use `topic-fact-sheet-template.md`. Include current-year federal figures, **the advisor's state rules**, common myths with the facts, and 5–10 headline-worthy statistics for webinar hooks and book chapters. See `source-guide.md` for which sources to trust.

**C. Local market snapshot.** Use `market-brief-template.md`: the 55+ population and trends, income and home values, major employers and pensions, state taxes on retirement income, state estate/inheritance tax, probate realities, local long-term care costs, and Medicaid rules.

**D. Competitor scan.** Use `competitor-scan-template.md`: 5–10 local and online advisors targeting the same people. What they offer (seminars, webinars, books, assessments), how they position themselves, and where the gaps are that this advisor can own.

**E. Voice of the customer.** How the ideal client talks about these worries, in their own words, from public forums, reviews, and comment threads (e.g., Reddit retirement communities, AARP forums, Amazon reviews of competing books). Capture 15–30 verbatim phrases; they become headlines and email subject lines. Never collect anyone's name or identifying details.

**F. Niche deep dive.** If the advisor has a niche (teachers, a specific employer, farmers, physicians, business owners): their pension or benefit plan specifics, key dates (e.g., early-retirement windows), associations and events, and the niche's own vocabulary.

## How to run it
- **In Claude Code:** run it in this repo. Claude uses web search and runs the modules in parallel (one research agent per module), then compiles the results.
- **In another AI deep-research tool** (ChatGPT Deep Research, Gemini Deep Research, Perplexity): fill in `research-prompt.md` and paste it in. Save the output, then have Claude check it against the rules below and convert it into the output files.

## Rules (non-negotiable)
1. **Every fact has a source:** the organization, a link, the publication date, and the date accessed. Primary sources first (IRS, SSA, CMS, Census, state statutes and agencies); reputable secondary sources only when no primary exists.
2. **No numbers from memory,** not even ones that seem well known. Tax limits, exemptions, and costs change every year.
3. **Every fact goes into `fact-registry.md` with an ID** (F-001, F-002…). Later stages cite these IDs, so when a number changes, every webinar, page, and book chapter that uses it can be found.
4. **Annual figures get marked** (🔁 annual) with the year they apply to.
5. **State-specific legal facts** (probate, trusts, homestead, Medicaid, creditor protection) are marked `[ATTORNEY REVIEW]` before they're published. They're educational and need the advisor's partner attorney to confirm.
6. **Tensions with the advisor's beliefs** go in `tensions.md`: what the advisor said, what the research says, the source, and a suggested reframe. These go to the advisor; don't silently "correct" their voice.
7. Research is **educational context, not advice.** Nothing here recommends a product.

## Outputs (in `clients/<slug>/03-deep-research/`)
| File | Level |
|---|---|
| `fact-registry.md`: every fact, with ID, source, and date | Core |
| `verify-results.md` | Core |
| `fact-sheet-<track>.md` (one per chosen track) | Core |
| `market-brief.md` | Core |
| `tensions.md` | Core (may be empty) |
| `competitor-scan.md` | Extended |
| `voice-of-customer.md` | Extended |
| `niche-brief.md` | Extended |
| `research-summary.md`: one page, the 10 most useful findings for the next stages | Core |

## Done when
- [ ] Every `[VERIFY]` item from the knowledge base is resolved
- [ ] There's a fact sheet for each chosen track, with state-specific facts
- [ ] Every number in every output has a fact ID and a source in the registry
- [ ] Tensions (if any) are sent to the advisor with the Stage 02 follow-up, or in a separate short note
- [ ] `research-summary.md` is written
