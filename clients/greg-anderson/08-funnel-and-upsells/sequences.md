# Sequences — Greg Anderson

**Status:** Draft for compliance (Oct 19, 2026). Greg's voice: short, direct, numbers-first, no hype, no faith language. Signed "Greg." SMS only when `sms_consent = yes`. **PATH Plan is a placeholder name.** Every email footer: the approved disclosure, 3711 John F Kennedy Parkway, Suite 230, Fort Collins, CO 80525, and an unsubscribe link.

Variables follow `stages/08-funnel-and-upsells/sequences.md`. Fixed values for Greg: `{{appointment}}` = PATH Review · `{{deliverable}}` = your one-page PATH Map · `{{phone}}` = (970) 204-1500 · `{{bring_list}}` = last year's tax return, your latest account statements, and your Social Security estimates (ssa.gov/myaccount) if you have them.

---

## E0 · Estate funnel ads (campaign #1) → Legacy Readiness Check
*Default ads use no client story. The "one year and one day" version runs only after the widow's written consent and compliance approval (consent log #2).*

| # | Primary text | Headline | Button |
|---|---|---|---|
| A | If one of you died tomorrow, would the other know what to do first? Who to call, where the documents are, which accounts go where? Most families don't. Take Greg Anderson's free 3-minute Legacy Readiness Check and see what's missing. | Is Your Family Ready? | Take the Check |
| B | A will doesn't keep your family out of court, and it does nothing if you can't make decisions for yourself. Ten questions show where your plan has gaps. Free, from a Fort Collins planner who handles tax, estate and investments in one office. | 10 Questions. 3 Minutes. | Get My Score |
| C | Your beneficiary forms can override your will. When did you last check yours? Take the free Legacy Readiness Check. | Check Your Beneficiaries | Start Now |
| D (consent required) | A couple came to our office and finished their trust and powers of attorney. One year and one day later, he died suddenly. Because the paperwork was done, she could carry on. Is your family ready? | One Year and One Day | Take the Check |

Audience: ages 55–72, Larimer and Weld counties (then national), homeowners. **[COMPLIANCE: Meta special ad category rules for financial services; no age targeting if the category requires it. Ad D needs consent. "Fort Collins planner" wording approved?]**

---

## S1 · Class registration + reminders
| When | Channel | Message |
|---|---|---|
| Immediately | Email | **Subject:** You're in: {{webinar_title}}<br>Hi {{first_name}}, you're registered for {{session_time}}. Save this link: {{join_link}}.<br>Three things before class: (1) put it on your calendar, (2) print the workbook: {{workbook_link}}, (3) if you have four minutes, take your PATH Score ({{assessment_link}}). You'll know which part of the class matters most for you.<br>See you there. Greg |
| Immediately | SMS | Greg Anderson here. You're registered for {{session_time}}. Join link: {{join_link}}. Reply STOP to opt out. |
| Day after registering (if 3+ days out) | Email | **Subject:** The question I get every week<br>"{{common_question}}" I'll answer it in class, along with {{promise_2}}. Link: {{join_link}}. Greg |
| 24 hours before | Email | **Subject:** Tomorrow: {{webinar_title}}<br>Tomorrow at {{time}}. In about an hour you'll get: • {{promise_1}} • {{promise_2}} • {{promise_3}}. Bring your spouse. Two plus two equals four, but it's easier to agree on it together. Link: {{join_link}}. Greg |
| 24 hours before | SMS | Tomorrow at {{time}}: {{short_title}} with Greg Anderson. Link: {{join_link}} |
| 1 hour before | Email | **Subject:** One hour<br>We start at {{time}}. Grab the workbook ({{workbook_link}}) and a pen. Link: {{join_link}}. By phone: {{dial_in}} |
| 1 hour before | SMS | Starting in 1 hour. {{join_link}} Workbook: {{workbook_link}} |
| At start | SMS + email | We're live. Join here: {{join_link}} |
| 10 minutes in (not joined) | SMS | We just started. Not too late: {{join_link}} |

**Common questions** by track: Tax → "Should I convert to a Roth before I retire?" · Estate → "Does a will keep us out of probate?"

## S4 / S5 · Post-class (attended / no-show)
Written in Stage 06: `06-webinars/<track>/post-webinar-emails.md`. Load them as written.

---

## S2 · Show-rate (PATH Review booked)
| When | Channel | Message |
|---|---|---|
| Immediately | Email | **Subject:** You're booked: your PATH Review on {{meeting_time}}<br>Hi {{first_name}}, I'm looking forward to it.<br>**What happens:** we'll go through your Paycheck, Assets, Taxes and Heirs, and you'll leave with your one-page PATH Map whether or not we ever work together.<br>**Two things:** (1) if you're married, please have your spouse join. These decisions belong to both of you. (2) Fill out this 5-minute questionnaire: {{questionnaire_link}}<br>**Bring:** last year's tax return, your latest statements, and your Social Security estimates. Our tax team will run a CPA What-If review on the return.<br>Need a different time? {{reschedule_link}}<br>Greg |
| Immediately | SMS | Greg Anderson here. You're booked for {{meeting_time}}. Details in your email. Change it: {{reschedule_link}} |
| Day after booking (if 3+ days out) | Email | **Subject:** Before we meet<br>A 2-minute video from me: who I am, what the hour looks like, and why there's no pressure. {{video_link}} **[PLACEHOLDER: record]** |
| 2 days before (if questionnaire not done) | Email | **Subject:** Quick favor<br>If you haven't yet: {{questionnaire_link}}. And if you can upload last year's return ({{upload_link}}), we'll have your CPA What-If ready. Greg |
| 24 hours before | SMS | Looking forward to tomorrow at {{time}}, {{first_name}}. {{location_or_zoom}}. Reply C to confirm or change it: {{reschedule_link}} |
| 2 hours before | SMS | See you at {{time}}. {{zoom_link_or_address}}. Greg |
| No confirmation by 4 hours before | Staff task (Paula) | Personal call: "Just making sure the time still works for you both." |

## S3 · No-show recovery
| When | Channel | Message |
|---|---|---|
| 15 minutes after | SMS | Hi {{first_name}}, we missed you today. No problem, life happens. Pick a new time? {{reschedule_link}} Greg |
| Same day | Call (Paula) | Friendly, no guilt. Offer two specific times. |
| Next day | Email | **Subject:** Let's find a better time<br>Your PATH Map is still waiting. Pick a time: {{reschedule_link}}. Greg |
| 3 days later | Email | **Subject:** Should I hold your spot?<br>I keep a limited number of PATH Reviews each month. If now isn't the time, no problem; I'll keep sending the occasional useful note. If it is, here's the link: {{reschedule_link}}. Greg → S8 |

---

## S6-L · Legacy Readiness Check: qualified, not booked (estate funnel)
| When | Channel | Message |
|---|---|---|
| Immediately | Email | **Subject:** Your Legacy Readiness Score: {{score}}<br>Hi {{first_name}}, your score is {{score}} ({{band}}). Your two focus areas: **{{focus_1}}** and **{{focus_2}}**. {{focus_1_feedback}}<br>The fastest way to close those gaps is a free PATH Review. You'll leave with your Legacy Document Checklist and a one-page PATH Map. {{booking_link}}<br>Greg |
| Day 1 | Email | **Subject:** The form that beats your will<br>Most people don't know this: the beneficiary form on your IRA or 401(k) usually decides who gets that account, not your will. An old form from before a divorce, a death or a new grandchild can send money to the wrong person. Pull your forms this week. Or bring them to your PATH Review and we'll check every one. {{booking_link}} **[ATTORNEY REVIEW]** |
| Day 3 | Email | **Subject:** What happens in a PATH Review<br>60 minutes, here or by Zoom. • Your documents and beneficiaries, checked • What happens to your spouse if one of you dies or can't decide • How it fits with your income and taxes. You keep the checklist and the PATH Map. No cost, no obligation. I hold a limited number each month. {{booking_link}} |
| Day 3 | SMS | Hi {{first_name}}, Greg Anderson here. Want help with your {{focus_1}} score? Grab a time: {{booking_link}} |
| Day 6 | Email | **Subject:** Free class: if something happened to you tomorrow<br>Invitation to the estate class → S1 if they register; S8 if not. |

## S6-P · PATH Score: qualified, not booked
Same structure as S6-L. Day 1 teaches the focus step: Paycheck → "plan for two people" · Assets → "the first years matter most" · Taxes → "RMDs start at 73, or 75 if you were born in 1960 or later (F-013, F-014); Medicare looks back two years (F-024)" · Heirs → the beneficiary-form email above. Day 6 invites to The Tax Trap class.

## S7 · Not qualified (either assessment)
| When | Channel | Message |
|---|---|---|
| Immediately | Email | **Subject:** Your results<br>Your score, focus areas, and one practical tip for each. Invitation to the matching free class: {{webinar_link}}. Greg |
| Day 3 | Email | **Subject:** Join me for a free class<br>The class's three promises. Register: {{webinar_link}} |
| Day 10 | Email | A useful article on their focus step (later: Greg's book). → S8 |

---

## S8 · Long-term nurture ("Greg's Notes")
- **Monthly, first Tuesday:** one idea in Greg's voice, rotating P → A → T → H; one short story (consented or composite, labeled); one soft CTA.
- **Tax-season letter (February):** "Three things your tax return can tell you about retirement." Also sent to every Fort Collins Tax Advisory Group client. **[COMPLIANCE: confirm cross-marketing to tax clients is permitted and disclosed]**
- **Trigger dates:** turning 59½, 62, 65, 73 (or 75 for those born 1960+); January (new tax figures); October (Medicare open enrollment, IRMAA reminder); November (year-end Roth conversion window); after big market moves (calm, educational, no predictions).
- **6-month retake:** "Has anything changed? Retake your PATH Score."
- **12 months of no opens:** "Should I keep sending these?" Remove non-responders.

## S9 · New client onboarding + referral
| When | Message |
|---|---|
| Day 0 | Welcome from Greg and Paula: what happens next, who to call, timeline, vault (generationalvault.com) login. |
| Day 7 | "Here's what we've done so far." |
| Day 30 | "How are you feeling about the plan?" |
| Day 60 | Referral moment (only as the firm's rules allow): "Is there someone you care about facing the same decisions? I'd be glad to invite them to my next class." No incentives. |
| Annual | "Time to walk your PATH," with a reminder to bring the tax return. |
