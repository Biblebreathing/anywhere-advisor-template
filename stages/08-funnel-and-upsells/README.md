# Stage 08 — Funnel, Sequences & Upsells

**Purpose:** Connect everything into a working appointment machine: pages that capture registrations, sequences that get people to **show up** (to the webinar and the meeting), upsells offered at the natural moment, and CRM automation that tags, routes, and reports. The North Star metric is the **cost per kept appointment.**

## Read first
- `funnel-guide.md`: the funnel maps (webinar, assessment, book, re-engagement), the four pages, the sequence list and rules, metrics, compliance
- `sequences.md`: template copy for every email and text (registration reminders, show-rate, no-show recovery, assessment follow-up, long-term nurture, client onboarding)
- `automation-map.md`: CRM fields, tags, pipeline stages, triggers → actions, advisor notifications, weekly reporting (works with any CRM)
- `upsell-menu.md`: free and paid "next yes" offers, with timing rules

## Inputs
- `04-offer-and-mechanism/`: the appointment offer, client journey, goal math
- `05-assessments/`: the assessment URL and webhook payload
- `06-webinars/<track>/`: title, promises, call-out, post-webinar emails, workbook
- `07-website/`: the domain and privacy policy
- `02-knowledge-base/`: voice, brand palette, headshot
- `01-interview/intake.md`: CRM, email platform, calendar tool, webinar platform

## Steps
1. **Funnel pages** (per webinar track): copy `examples/funnel.json` to `clients/<slug>/08-funnel-and-upsells/<track>/funnel.json`, fill it from Stages 04–07 (the title and promises **word for word** from Stage 06), and build:
   ```
   python3 tools/build_funnel.py --content clients/<slug>/08-funnel-and-upsells/<track>/funnel.json \
     --palette clients/<slug>/02-knowledge-base/brand-palette.json \
     --out clients/<slug>/08-funnel-and-upsells/<track>/build
   ```
   This produces the registration page (`index.html`), `thank-you.html` (add to calendar, workbook, assessment, "book now"), `replay.html`, and `booked.html` (the show-rate page). Add new session dates to `sessions` and rebuild weekly, or keep 6–8 weeks of dates listed.
2. **Sequences:** write the advisor's versions of S1–S3 and S6–S9 from `sequences.md` (plus S4–S5 from Stage 06) into `clients/<slug>/08-funnel-and-upsells/sequences.md`, in the advisor's voice.
3. **CRM setup:** build the fields, tags, pipeline, and triggers from `automation-map.md` in the advisor's CRM. Point the registration form and assessment webhooks at it. Connect the calendar (booking → stop sales sequences → start S2) and the webinar platform (attendance → S4/S5).
4. **Test end to end with a real phone and email:** register → confirmation email and text → reminders → mark attended / no-show → the right follow-up → book → show-rate sequence → advisor notification. Do the same for the assessment (qualified and not qualified).
5. **Compliance:** submit the pages, every email, and every text message. Log approval.
6. **Launch and measure weekly** (funnel-guide §5). After 60–90 days, replace the Stage 04 assumptions with the advisor's real numbers.

## Outputs (in `clients/<slug>/08-funnel-and-upsells/`)
| File | What it is |
|---|---|
| `<track>/funnel.json` + `<track>/build/` | Funnel pages for each webinar track |
| `sequences.md` | All sequence copy, final, in the advisor's voice |
| `crm-setup.md` | What was built in the CRM (fields, tags, triggers), with test results |
| `launch-checklist.md` | End-to-end test log, compliance approval date, launch date |

## funnel.json reference
| Key | What it holds |
|---|---|
| `site` | firm, logo, advisor (name, title, photo, phone), appointment (name, headline, text, deliverable, deliverable_short, button, url), disclosure, privacy_url |
| `webinar` | track, eyebrow, title, subtitle, promises (3), who, credibility, question (optional form question), `sessions` (ISO dates **with time zone offset**), duration_minutes, join_link, dial_in, workbook_url, assessment_url, button, note, replay (video_embed_url, expires_text) |
| `booked` | what_happens, bring, questionnaire_url, video_embed_url, reschedule_text |
| `sms_consent` | Consent text next to the unchecked SMS checkbox |
| `thanks` | video_embed_url (optional welcome video) |
| `webhookUrl` | Where registrations are POSTed (the same CRM inbound webhook pattern as Stage 05) |

**Registration webhook payload:** `{event: "webinar_registered", track, webinar, session, contact: {firstName, email, phone, smsConsent}, question, utm, page, registeredAt}`

## Done when
- [ ] Funnel pages built for each live track; the title and promises match the webinar word for word
- [ ] All sequences written in the advisor's voice and loaded in the CRM
- [ ] Triggers tested end to end with a real phone and email (registration, reminders, attended/no-show, booking, no-show recovery, assessment routes)
- [ ] The advisor receives booking notifications with assessment results
- [ ] Compliance approval received for pages, emails, and texts
- [ ] Weekly reporting set up
