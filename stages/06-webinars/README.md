# Stage 06 — Webinars

**Purpose:** Build a **high-converting, genuinely useful 60-minute webinar** for each track the advisor runs: Estate Planning, Tax, Retirement Paycheck, Asset Protection, and Long-Term Care. Each one teaches a step of the advisor's mechanism and invites attendees to the named appointment.

## Read first
- `webinar-framework.md`: **the standard.** It combines Terrence's 1-Hour Webinar Book, Webinar Warrior Prompt 03, and the 400-40 system into one 3-act, ~45-slide structure, with the word-for-word script rules, PARADISE offer, compliance, and quality loop.
- `tracks/`: one template per webinar system (topic-specific hooks, Through Lines, Big Ideas, objections, chat prompts, workbook pages, seeded questions, track compliance)
- `webinar-research.md`: sourced benchmarks (attendance, timing, length, reminders, engagement)

## Inputs
- `02-knowledge-base/`: the knowledge base (stories, voice, beliefs), brand palette, headshot, consent log
- `03-deep-research/`: fact registry, fact sheet for this track, market brief
- `04-offer-and-mechanism/`: mechanism (name, steps), named appointment and deliverable, positioning

## Steps (per track)
1. **Pick the first track:** the one research and the advisor's strengths support most (see `research-summary.md`). Launch one track first and run it weekly before adding more (framework §6).
2. **Write the foundation** in `clients/<slug>/06-webinars/<track>/foundation.md`: XYZ + M, the Through Line (wrong → true belief), the three false beliefs, the PARADISE offer, a title (2–3 options), and the three promises. Use the track template as a starting point.
3. **Write the deck** as `deck.json` (format below): about 45 slides following the framework table, with a **word-for-word script** in the advisor's voice (6,000–7,000 spoken words), 3 booking callouts, chat prompts every 5–7 minutes, and workbook cues. Every number cites a fact ID; every story comes from the knowledge base, with consent.
4. **Run the quality loop** (framework §8): the five tests, then score; revise until the gate passes.
5. **Build it:**
   ```
   python3 tools/build_deck.py --deck clients/<slug>/06-webinars/<track>/deck.json \
     --palette clients/<slug>/02-knowledge-base/brand-palette.json \
     --out clients/<slug>/06-webinars/<track>/build
   ```
   This produces the branded `.pptx` (script in the notes pane), `script.md` (a printable script), and `run-of-show.md`. The build **fails** if any slide lacks a script, an Act 2 slide lacks an angle, the word count is out of range, or the booking callouts aren't exactly 3.
6. **Workbook:** fill in `workbook-template.md` with the pages the script cues.
7. **Post-webinar emails:** fill in `post-webinar-emails.md` (attended / no-show). Stage 08 loads them into the CRM.
8. **Registration copy handoff:** the title, subtitle, three promises, and call-out go to Stage 08 for the registration page, **word for word**.
9. **Compliance:** submit the deck, script, workbook, and emails to the advisor's approver. Log the date.
10. **Rehearse:** one dry run with the advisor reading the script cold. Fix any slide where they had to improvise.

## Outputs (in `clients/<slug>/06-webinars/<track>/`)
| File | What it is |
|---|---|
| `foundation.md` | XYZ+M, Through Line, false beliefs, PARADISE offer, titles, promises |
| `deck.json` | The source of truth for slides and script |
| `build/<title>.pptx` | Branded deck with the full script in the notes pane. Opens in PowerPoint, Keynote, or Google Slides. |
| `build/script.md` | Printable script, with timing and callouts marked |
| `build/run-of-show.md` | Minute-by-minute run of show |
| `workbook.md` | The attendee workbook |
| `post-webinar-emails.md` | Follow-up for attendees and no-shows |
| `quality-report.md` | Test results, scores, and the compliance submission date |

## deck.json format
```json
{
  "deck_title": "", "track": "retirement-paycheck",
  "advisor": {"name": "", "firm": "", "headshot": "../../02-knowledge-base/assets/headshot-1.jpg"},
  "disclosure_short": "Shown on the title and final slides",
  "through_line": {"wrong_belief": "", "true_belief": ""},
  "mechanism": {"name": "", "steps": [{"name": ""}]},
  "appointment": {"name": "", "deliverable": "", "url": ""},
  "slides": [{
    "number": 1, "act": 1, "layout": "title | statement | bullets | number | cards | table | story | process | offer | qr",
    "angle": "Act 2 only: wrong belief | consequence | arithmetic | story | comparison | true belief | method | analogy | objection | trigger",
    "headline": "", "subhead": "", "body": [],
    "big_numbers": [{"value": "", "label": ""}], "cards": [{"title": "", "text": ""}],
    "table": {"headers": [], "rows": [[]]}, "focus_step": 1, "url": "", "display_url": "", "image": "",
    "speaker_script": "\"Spoken words in quotes.\"\n\n[Stage directions in brackets.]\n\nTiming: about two minutes.",
    "timing_seconds": 120, "chat_prompt": "", "workbook_cue": {"page": 0, "instruction": ""},
    "claims_used": ["F-012"]
  }]
}
```
Mark booking callouts inside the script with `[BOOKING CALLOUT]`. Only text inside quotation marks counts toward the spoken word count.

**Fonts:** the deck uses the brand's Google Fonts. They display correctly in Google Slides, or in PowerPoint and Keynote once the fonts are installed (free from fonts.google.com).

## Done when
- [ ] The foundation is approved by the advisor (Through Line, title, promises)
- [ ] The deck builds with no errors; 6,000–7,000 spoken words; quality gate passed
- [ ] The advisor has done a cold read-through and their fixes are made
- [ ] The workbook and emails are written; registration copy has been handed to Stage 08
- [ ] Compliance approval received (or submitted, with the date)
