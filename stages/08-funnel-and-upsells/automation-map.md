# CRM Automation Map (works with any CRM)

The blueprint for setting up the funnel in GoHighLevel, HubSpot, ActiveCampaign, Keap, Salesforce, or Redtail/Wealthbox plus an email tool. Field and tag names are standard across the system, so every advisor's CRM looks the same and reports compare cleanly.

## 1. Contact fields
| Field | Example | Set by |
|---|---|---|
| `first_name`, `email`, `phone` | | Forms |
| `sms_consent` (yes/no) + `sms_consent_at` (timestamp + page) | yes · 2026-10-20 · /register | Forms |
| `lead_source` | facebook, google, book-qr, referral, partner-[name], website | UTM / form |
| `utm_campaign`, `utm_content` | | Forms |
| `first_track` | retirement-paycheck | Registration |
| `assessment_score`, `assessment_band`, `focus_steps` | 37 · Getting Started · protect, legacy | Assessment webhook |
| `qualified` (yes/no) | | Assessment / qualifiers |
| `retire_timeline`, `asset_range` | 5–10 years · $500K–$1M | Qualifier answers |
| `webinar_question` | "When should I take Social Security?" | Registration form |
| `next_session_at` | 2026-10-27 11:00 ET | Registration |
| `meeting_1_at` | | Calendar |
| `birth_year` (if collected) | | Meeting / CRM |

## 2. Tags
- **Source:** `src:facebook`, `src:book-qr`, `src:referral`, …
- **Track interest:** `track:retirement-paycheck`, `track:tax`, `track:estate`, `track:asset-protection`, `track:ltc`
- **Webinar behavior:** `web:registered`, `web:attended`, `web:stayed-20min`, `web:no-show`, `web:replay-watched`
- **Assessment:** `assess:completed`, `assess:qualified`, `assess:not-qualified`, `focus:<step>`
- **Book:** `book:requested`, `book:reader`, `book:qr-<chapter>`, `src:book-<channel>` (partner, mailer, webinar-gift)
- **Booking:** `booked:meeting-1`, `showed:meeting-1`, `no-show:meeting-1`, `rescheduled`
- **Status:** `client`, `do-not-contact`, `sms-opted-out`

## 3. Pipeline (opportunity stages)
`New lead` → `Registered` → `Attended / Assessed` → `Meeting 1 booked` → `Meeting 1 held` → `Meeting 2 (plan)` → `Client` · plus `Nurture` and `Not a fit`

## 4. Triggers → actions
| Trigger | Actions |
|---|---|
| Registration form submitted | Create/update contact · tags `web:registered`, `track:*`, `src:*` · set `next_session_at` · stage **Registered** · start **S1** |
| Webinar attendance report (platform integration or CSV) | Tag `web:attended` / `web:no-show` (and `web:stayed-20min` if available) · stop S1 · start **S4** or **S5** |
| Assessment webhook (Stage 05 payload) | Update the score fields · tags `assess:*`, `focus:*` · qualified + no booking in 60 minutes → **S6**; not qualified → **S7** |
| Meeting booked (calendar integration) | Tag `booked:meeting-1` · stage **Meeting 1 booked** · **stop all sales sequences** · start **S2** · notify the advisor with the assessment results and the webinar question |
| Meeting status: no-show | Tag `no-show:meeting-1` · start **S3** · task for staff: call within 2 hours |
| Meeting status: held | Tag `showed:meeting-1` · stage **Meeting 1 held** · advisor task: notes plus next meeting |
| Became a client | Tag `client` · stop all marketing sequences · start **S9** |
| `book_requested` webhook (Stage 10) | Tag `book:requested` + source · fulfillment task for mailed copies · start **S10** reader sequence |
| `book_reader_registered` webhook (Stage 10) | Tag `book:reader`, `book:qr-<chapter>` · start **S10** if not already in it |
| Any sequence ends without booking | Stage **Nurture** · start **S8** |
| SMS reply STOP | Tag `sms-opted-out` · no further SMS (email continues if allowed) |
| Unsubscribe | Tag `do-not-contact` · stop everything |

## 5. Advisor notifications
When a meeting is booked, send the advisor (email or SMS): name, phone, source, track, assessment score with focus steps, the webinar question, and the qualifier answers. The advisor walks into Meeting 1 already knowing what matters.

## 6. Reporting (weekly)
Registrants · live attendance % · bookings (during the webinar, within 48 hours, from the replay) · Meeting 1 show rate · Meeting 1 → client · cost per kept appointment, by source and by track.
