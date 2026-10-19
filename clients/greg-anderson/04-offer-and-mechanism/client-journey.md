# Client Journey — Greg W. Anderson

**Status:** Draft (Oct 19, 2026). Rates are `[ASSUMPTION]`, taken from the Stage 04 guide's benchmarks, until the AIMO pilot gives real data (pilot: 90 days from Sept 24, 2026; Greg pays the ad spend).

## Goal math (work backward)
| | Value | Basis |
|---|---|---|
| New clients wanted | 30+ a year → **2.5 a month** | KB §9 |
| Meeting 1 → client rate | 40% | `[ASSUMPTION]` guide range 30–50%; his three-company offer and referrals likely push higher |
| → Kept PATH Reviews needed / month | **6.3** | |
| Show rate | 80% | `[ASSUMPTION]` with the full reminder sequence (guide 75–85%) |
| → Booked PATH Reviews needed / month | **7.8 (call it 8)** | |
| **Estate funnel:** assessment completion → booked | 10% | `[ASSUMPTION]` guide 5–15% |
| → Legacy Readiness completions needed / month (if the estate funnel carries it all) | **~80** | |
| Assessment start → completion | 60% | `[ASSUMPTION]` |
| → Assessment starts needed / month | **~130** | |
| **Tax Trap webinar:** attendee → booked | 15% | `[ASSUMPTION]` guide 10–20% |
| → Attendees needed / month (if the webinar carries it all) | **~52** | |
| Attendance rate | 35% | `[ASSUMPTION]` guide 30–40% |
| → Registrants needed / month | **~150** | |
| Greg's monthly first-meeting capacity | **8** (2 a week on a three-day week) | `[ASSUMPTION; confirm]` |

**Reading it:** about 8 booked PATH Reviews a month hits the 30-client goal and fills his capacity. Months 1–3 (estate funnel only): about 80 assessment completions a month. From month 4, the Tax Trap webinar carries about half, so each channel needs roughly half its number. Average new money of about $870K per client × 30 ≈ $26M, which matches today; the upmarket campaigns lift the average, not the count. **The constraint is Greg's time, not leads:** above 8 a month, a second advisor or a service planner runs meeting 2.

## Entry points used
1. **Estate appointment funnel** (first): ads → Legacy Readiness Check → results page → PATH Review (Family Legacy Edition)
2. **Tax Trap webinar** (second): ads, email to the database, tax-practice clients → webinar → PATH Review
3. **The tax practice** (always): every return prepared is a planning signal (RMDs, Roth room, rentals, K-1s, RSUs). A "your return raised three planning questions" letter after tax season. **[INFERRED: a large, free lead source]**
4. **Reviews and the website** (existing): Google reviews, the risk score tool, the video library
5. **Book** (later): QR codes into the PATH Score and the PATH Review
6. **Upmarket doors** (months 4–9): Landlord Exit and Business Sale Readiness campaigns, plus CPA, attorney, broker and realtor partners **[MISSING: current partners]**

## Journey map
| # | Stage | Prospect experience | Assets | Automation | Owner | Metric | Target |
|---|---|---|---|---|---|---|---|
| 1 | Attract | Sees an ad or post: "If one of you died tomorrow, would the other know what to do?" | Ads (Story 2 angle, consented), short videos of Greg | Ad platform → UTM | AI drafts, Terrance's team runs | CTR, cost per lead | CPL tracked from week 1 |
| 2 | Capture | Takes the Legacy Readiness Check; gets a score and a gap list | Stage 05 assessment | Webhook → CRM, tag `estate-funnel` | AI | Start → complete | 60% |
| 3 | Show up | (Webinar) Gets reminders by email and SMS | Stage 08 sequences | 7-touch reminder sequence | AI | Attendance | 35% |
| 4 | Learn | Results page or webinar explains PATH; sees the diagram with their weak letter | Results page, webinar, workbook | Personalized results | AI | Results-page CTA clicks | 20% |
| 5 | Book | Reserves a PATH Review; uploads last year's tax return | Booking page, intake form | Calendar → CRM, tag `path-review-booked` | AI | Completion → booked | 10% |
| 6 | Keep | Confirmation, a 2-minute "what to expect" video from Greg, reminders, a text the morning of | Show-up sequence | Reminder sequence; no-show rebook flow | AI + Paula | Show rate | 80% |
| 7 | Meeting 1 | **PATH Review**: P, A, T, H; leaves with the PATH Map | PATH Map template | Notes → CRM | Greg | Meeting 1 → meeting 2 | 70% |
| 8 | Meeting 2 | Deliverables presented: Retirement Paycheck Map, Risk & Reserve Report, CPA What-If Tax Timeline, Legacy checklist; recommendation | Deliverable templates | Pre-meeting prep pulled from CRM | Greg + tax team | Meeting 2 → client | 55% |
| 9 | Meeting 3 | Implementation: accounts, applications, documents signed | Checklists | E-sign, task list | Paula + service | Time to funded | < 30 days |
| 10 | Onboard | Welcome kit, vault access, "your first 90 days" emails | Welcome sequence | Onboarding sequence | AI + Paula | Onboarding NPS | — |
| 11 | Review | Annual "Walk the PATH" review; tax return each spring | Review agenda = PATH | Review scheduler; prep pulled from CRM | Service planner (frees Greg) | Retention | 97%+ |
| 12 | Advocate | Asked for a review and a referral at the right moments; invited to bring friends to a client event | Referral scripts, events | Review request after meeting 2 and annual review | AI + Paula | Referrals per client per year | 0.5 |

## Re-engagement loop
- Completed the assessment but didn't book → 21-day nurture: a short video from Greg on their weakest letter, Story 2, the PATH diagram, then an invitation to the next webinar.
- Webinar no-show → replay for 72 hours, then the next track's invitation.
- Booked but didn't show → same-day text from Paula, a rebook link, one call.
- Meeting 1 but not yet a client → quarterly "tax and market notes" email; a personal invite to the next webinar on their weak letter.
- Every quarter: a new webinar track is a fresh reason to come back. Same mechanism, same appointment.

## Meeting agendas
**Meeting 1: The PATH Review (60 minutes)**
1. (5) What made you reach out now? What would make this hour worthwhile?
2. (15) **Paycheck:** what you need per year and where it comes from; Social Security timing
3. (10) **Assets:** what's at risk if the market drops the year you retire (their risk score)
4. (10) **Taxes:** first look at last year's return; what the CPA will check
5. (10) **Heirs:** documents, beneficiaries, who's protected
6. (10) Their PATH Map: the top three gaps; what meeting 2 delivers; book it before they leave

**Meeting 2: Your PATH Plan (60–75 minutes)**: the four deliverables, the recommendation, the fees and the next steps.
**Meeting 3: Put it in place.** Accounts, applications, documents, and the tax calendar.

## Tags and segments (CRM)
`src-estate-funnel` `src-tax-trap` `src-website` `src-referral` `src-tax-client` `src-book` · `path-weak-P|A|T|H` · `assessment-complete` `webinar-registered` `webinar-attended` `path-review-booked` `path-review-kept` `meeting2-done` `client` · `market-engineer` `market-landlord` `market-business-owner` `market-rsu` · `assets-750k-2m` `assets-2m-5m` `assets-5m-plus`
