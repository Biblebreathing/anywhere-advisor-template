# Anywhere Advisor — Interview-to-Asset Template

One repeatable system that takes a financial advisor from **a single interview** to a full set of **appointment-generating assets**:

```
Intake + Interview ─► Knowledge Base ─► (Deep Research) ─► Offer + Unique Mechanism
    │
    ├─► Assessments (lead magnets / tools)
    ├─► Webinars (Estate · Tax · Retirement Paycheck · Asset Protection · LTC)
    ├─► Website ─► Funnel + Upsells ─► Calendar
    └─► Book (worksheets + QR codes ─► calendar) ─► Book website + funnel ─► Amazon KDP
```

Every asset points to one place: **a booked appointment on the advisor's calendar.**

## How it's organized

| Folder | What it holds |
|---|---|
| `stages/` | The **master template**: instructions, question banks, and frameworks for each stage. Write these once, reuse them for every advisor. |
| `clients/<advisor-slug>/` | **One folder per advisor.** Each stage writes its outputs into the matching subfolder. Copy `clients/_example/` to start a new advisor. |
| `compliance/` | Review checklist that every public-facing asset must pass. |
| `tools/` | Helper scripts. `brand_kit.py` builds color palettes from a logo (or offers preset options for new firms) and checks color contrast. `mechanism_diagram.py` draws the Unique Mechanism as a branded diagram. `build_assessment.py` turns an assessment config into a finished, branded scorecard page. `build_deck.py` turns a webinar script file into a branded PowerPoint with the speaker script in the notes. `build_site.py` generates the advisor's full website from one content file. `build_funnel.py` generates the registration, thank-you, replay, and booking-confirmation pages. |
| `.claude/skills/advisor-launch/` | The Claude skill that runs the pipeline for a client, one stage at a time. |

## Stages

| # | Stage | Status |
|---|---|---|
| 01 | Intake + Interview → Knowledge Base | ✅ Built |
| 02 | Knowledge Base Review, Gap-Fill + Brand Kit | ✅ Built |
| 03 | Deep Research (Core always; Extended optional) | ✅ Built |
| 04 | Offer, Unique Mechanism + Client Journey | ✅ Built |
| 05 | Assessments (working scorecard engine) | ✅ Built |
| 06 | Webinars: framework + 5 track templates + deck builder | ✅ Built |
| 07 | Website: guide + site generator | ✅ Built |
| 08 | Funnel, sequences, CRM map + funnel page generator | ✅ Built |
| 09 | Book (manuscript, worksheets, QR codes) | ⏳ Next |
| 10 | Book Website + Funnel | ⏳ |
| 11 | KDP Publishing (formatting, cover, listing) | ⏳ |

## Starting a new advisor

1. `cp -r clients/_example clients/jane-smith`
2. Send the advisor `stages/01-interview/intake-form.md` (5–10 min) and `stages/01-interview/interview-prompt.md` (30–45 min, run in any AI tool).
3. Save what comes back in `clients/jane-smith/01-interview/` as `intake.md`, `transcript.md`, and `knowledge-base.md`.
4. In Claude Code, say: **"Run advisor-launch for jane-smith"**. Claude checks which stages are done and builds the next one.
