# Funnel & Upsell Guide

The funnel turns attention into **kept appointments**. Every page and message has one job: move the person one step closer to sitting down with the advisor, or keep them warm until they're ready.

The two numbers that matter most: **booked appointments** and **show rate.** A booked appointment that doesn't show is worth nothing, so half of this stage is about getting people to *show up* (to the webinar, and to the meeting).

---

## 1. The funnels

### A. Webinar funnel (the main engine, run weekly)
```
Ad / email / social / partner / book QR
   → Registration page ──→ Thank-you page (add to calendar · workbook · take the assessment · "can't wait? book now")
        → Reminder sequence (email + SMS) ──→ LIVE WEBINAR (booking link pinned in chat from minute 20)
             ├─ Booked → Booking confirmation page → Show-rate sequence → MEETING 1
             ├─ Attended, not booked → Post-webinar sequence (replay + 3 emails) → Nurture
             └─ No-show → Replay sequence → Invited to the next session → Nurture
```

### B. Assessment funnel
```
Ad / website / book QR → Assessment → Results page
   ├─ Qualified → Book now (pre-filled calendar) → Show-rate sequence
   │      └─ Didn't book → "Your results" email + 4-email booking sequence → Webinar invite → Nurture
   └─ Not qualified → Webinar invitation → Nurture
```

### C. Book funnel (built in Stage 10)
Book offer → reader bonus hub (QR codes) → assessment / webinar / booking.

### D. Re-engagement loop (never let a lead die)
Monthly educational email in the advisor's voice · an invitation to the **next webinar track** · trigger-date messages (birthdays at 59½, 62, 65, 73; tax season; Medicare open enrollment; year-end) · an assessment re-take after 6 months.

---

## 2. The pages

| Page | Job | Must have |
|---|---|---|
| **Registration** | Get the registration | The headline = webinar title (Stage 06); 3 promises **word for word**; who it's for; the advisor photo and one-line credibility; the next session date in the visitor's time zone; a short form (first name, email, mobile with SMS consent); "Educational session. Includes an invitation to meet." |
| **Thank-you** | Raise the show rate; offer the shortcut | "You're registered"; **add to calendar** (Google + .ics); the workbook; **take the assessment** (a micro-commitment that raises attendance and gives the advisor data); **"Can't wait? Book your session now"** (the first upsell); a short welcome video from the advisor (optional) |
| **Replay** | Second chance to convert | The video; the booking button under it and repeated after; the replay expiration date (honest); the 3 promises |
| **Booking confirmation** | Make sure they show | "You're booked" + the date; what happens in the session; **bring your spouse/partner**; what to bring; a short questionnaire link; a welcome video; reschedule instructions (rescheduling beats a no-show) |

The generator (`tools/build_funnel.py`) builds all four from one file, in the advisor's brand, with **no site navigation** (funnel pages have one exit: the next step).

---

## 3. The sequences (copy in `sequences.md`)

| # | Sequence | Trigger | Goal | Stops when |
|---|---|---|---|---|
| S1 | **Registration confirmation + reminders** | Registers | Show up live | Webinar starts |
| S2 | **Show-rate (booked appointment)** | Books a meeting | Show up, prepared, with spouse | Meeting held, or cancelled |
| S3 | **No-show recovery (meeting)** | Missed the meeting | Reschedule | Rebooked, or 3 messages |
| S4 | **Post-webinar: attended** | Attended, not booked | Book | Books |
| S5 | **Post-webinar: no-show** | Registered, didn't attend | Watch replay → book | Books, or next session |
| S6 | **Assessment: qualified, not booked** | Assessment completed, qualified, no booking within 1 hour | Book | Books |
| S7 | **Assessment: not qualified** | Assessment completed, not qualified | Register for the webinar | Registers |
| S8 | **Long-term nurture** | End of any sequence without booking | Stay top of mind; re-invite | Books, or unsubscribes |
| S9 | **Client onboarding + referral** | Becomes a client | Confidence and referrals | — (handed to the advisor's service process) |

S4 and S5 copy is in Stage 06 (`post-webinar-emails.md`) because it's tied to each webinar; the rest is in `sequences.md`.

**Sequence rules**
- **Exit on booking:** the moment someone books, every sales sequence stops and S2 starts.
- **SMS only with consent,** and always with "Reply STOP to opt out." Send only between 9 am and 8 pm in the recipient's time zone.
- **From the advisor, by name**, in the advisor's voice. Plain text beats designed emails for personal follow-up.
- **One call to action per message.**
- Every email: physical address, unsubscribe link, the firm's disclosure (CAN-SPAM and compliance).

---

## 4. Upsells (see `upsell-menu.md`)

For an advisor, an "upsell" is the **next, bigger yes**: book now instead of waiting; bring your spouse; upgrade to a deeper session; or (optionally) buy a low-cost resource. Each is offered at the moment it's most natural, and **never at the expense of the main goal: the kept appointment.**

---

## 5. Metrics and targets

Track these weekly per funnel. Use the Stage 04 targets until the advisor has 60–90 days of their own data (no independent advisor benchmark exists; see Stage 06 research, R49).

| Step | Metric |
|---|---|
| Ad → registration page | Cost per click, landing page view rate |
| Registration page | **Registration rate** (visitors → registrants) |
| Thank-you page | Calendar adds, assessment starts, **immediate bookings** |
| Reminders | **Live attendance rate** (plan on about half; Stage 06 research) |
| Webinar | Watched to minute 20 (the booking link pinned), **booked during or within 48 hours** |
| Replay | Replay views, replay bookings |
| Booking | **Show rate** for Meeting 1 |
| Meeting | Meeting 1 → client |
| Overall | **Cost per kept appointment** (the North Star) |

---

## 6. Compliance

- Every page, email, and text is a marketing communication, so the full set (including the SMS copy) gets approved before launch.
- SMS: written consent (the unchecked checkbox on the form), STOP and HELP handling, quiet hours, and records of consent (TCPA).
- Email: unsubscribe, physical address, honest subject lines (CAN-SPAM).
- No new claims in sequences beyond what's already approved in the webinar and website.
- Scarcity and deadlines must be true (replay expiration, session capacity).
- Paid low-ticket products: educational only, no individualized advice. For RIAs, check consistency with Form ADV.
