# Stage 05 — Assessments

**Purpose:** Build interactive scorecards that **capture leads, pre-qualify them, and send the right people to the booking page.** The assessment scores the prospect on each step of the advisor's Unique Mechanism, so the results page sells the mechanism and the appointment for us.

Assessments are the hardest-working lead magnet in the system. They're used:
- **On their own** (ads → assessment → booking)
- **In the webinar funnel** (a pre-webinar homework assignment, or a post-webinar "get your score")
- **In the book** (a QR code → "take the assessment for your chapter")
- **In meetings** (the advisor reviews the scores in Meeting 1)

## Inputs
- `04-offer-and-mechanism/unique-mechanism.md`: step names, IDs, and deliverables
- `04-offer-and-mechanism/offer-stack.md`: the named appointment and its deliverable, and the nurture offer
- `02-knowledge-base/brand-palette.json`, `assets/` (logo and headshot), `knowledge-base.md` (voice, ideal client)
- `01-interview/intake.md`: calendar link, CRM, minimum qualifications

## What to build
| Assessment | When |
|---|---|
| **Master assessment** ("What's Your [Mechanism] Score?"), scoring every step | Always |
| **Track assessments** (one per webinar track, e.g., "Estate Plan Gap Check," "LTC Readiness Score") | Optional; one per webinar track the advisor runs |

## Steps
1. **Write the config** (Claude): copy `examples/retirement-readiness.json` to `clients/<slug>/05-assessments/<name>.json`. Follow `assessment-guide.md` and draw on `question-bank.md`. Use the mechanism step IDs, names, and appointment wording **exactly** as approved in Stage 04.
2. **Build it:**
   ```
   python3 tools/build_assessment.py --config clients/<slug>/05-assessments/<name>.json \
     --palette clients/<slug>/02-knowledge-base/brand-palette.json \
     --out clients/<slug>/05-assessments/build/<name>
   ```
   The build checks the config and warns about missing pieces (webhook, privacy link, calendar link) and risky compliance words.
3. **Test it** (Claude): click through as a qualified and an unqualified prospect, on desktop and phone sizes. Confirm the booking link pre-fills the name and email, and that the webhook payload reaches the CRM.
4. **Connect it** to the advisor's CRM: see *Connecting the CRM* below.
5. **Compliance review:** submit the questions, the results text, and the disclosure to the advisor's compliance approver.
6. **Publish:** upload the `build/<name>/` folder to any static host, or embed it in the advisor's website or funnel builder (see *Hosting*).

## Outputs (in `clients/<slug>/05-assessments/`)
- `<name>.json`: the config (source of truth; edit this, then rebuild)
- `build/<name>/index.html`: the finished page (self-contained, plus logo and headshot files)
- `test-notes.md`: test results and the compliance submission date

## Config reference
| Key | What it holds |
|---|---|
| `advisor` | name, firm, logo and headshot (paths relative to the config file, or URLs), privacyUrl |
| `assessment` | title, subtitle, bullets, minutes, startButton, scoreName |
| `mechanism` | name, plus steps: `{id, name, deliverable}`. Must match Stage 04. |
| `questions` | `{id, step, text, help?, options:[{label, points}]}`. Each step needs 2–3 questions. |
| `qualifiers` | Unscored routing questions: `{id, text, options:[{label, qualified:true/false}]}` |
| `focusSteps` | How many weakest steps to tag "Focus area" (default 2; only steps under 80%) |
| `bands` | Score ranges covering 0–100: `{min, max, label, headline, message}` |
| `stepFeedback` | Per step: `{low, mid, high}` text (under 50% / 50–79% / 80%+) |
| `capture` | Lead form text, the phone field on/off, the SMS consent wording |
| `appointment` | The named appointment: headline, text, deliverable, button text, scarcity, the calendar `url`, and `urlParams` (which query names pre-fill name and email; e.g., Calendly uses `name` and `email`) |
| `nurture` | What unqualified prospects are offered instead (usually the webinar) |
| `webhookUrl` | Where completed results are POSTed (the CRM / Zapier / Make / GoHighLevel inbound webhook) |
| `resultsNote`, `disclosure` | Compliance text shown on the results page and in the footer |

**Routing:** if every qualifier answer is `qualified: true`, the main button books the appointment. Otherwise, the main button is the nurture offer, with a smaller link to book anyway.

## Connecting the CRM
When someone finishes, the page POSTs this JSON to `webhookUrl`:
```json
{ "event": "assessment_completed", "assessment": "...", "advisor": "...",
  "contact": {"firstName": "...", "email": "...", "phone": "...", "smsConsent": true},
  "utm": {"utm_source": "facebook", "utm_campaign": "..."}, "page": "...", "completedAt": "...",
  "overallScore": 37, "band": "Getting Started", "qualified": true, "focusSteps": ["protect", "legacy"],
  "stepScores": {"income": 44, "tax": 44}, "answers": {"q1": "I have a rough idea"} }
```
In the CRM, use the payload to: create or update the contact; tag it by band, qualification, focus steps, and source; send the "your results" email; and start the right follow-up (qualified + not booked → booking reminders; unqualified → webinar invitation). Only send text messages when `smsConsent` is true. The sequences themselves are built in Stage 08.

It works with any tool that accepts an inbound webhook: GoHighLevel, HubSpot (workflows), Zapier, Make, ActiveCampaign, Keap. The page sends it as a plain-text body to avoid browser cross-site blocking. If a receiver can't read it, route it through Zapier or Make.

The page also pushes an `assessment_completed` event to Google Tag Manager's `dataLayer` (if present) for ad conversion tracking.

## Hosting
The `build/<name>/` folder is a complete static site. You can:
- Upload it to Netlify, Vercel, Cloudflare Pages, or GitHub Pages and point a subdomain at it (e.g., `score.advisorfirm.com`)
- Embed it in the advisor's site or funnel builder with an `<iframe>`
- Paste the HTML into a custom-code page in GoHighLevel, ClickFunnels, or WordPress

## Done when
- [ ] The config uses the approved mechanism and appointment exactly
- [ ] The build has no errors, and every warning is resolved or accepted (with a note)
- [ ] Tested as qualified and unqualified, on desktop and phone sizes; the booking link pre-fills
- [ ] A test lead arrived in the CRM with tags
- [ ] The compliance approver has signed off on the questions, results text, and disclosure
