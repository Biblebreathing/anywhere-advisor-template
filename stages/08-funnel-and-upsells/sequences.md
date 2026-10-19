# Sequence Library

Template copy for every automated message. **Rewrite each one in the advisor's voice** (Knowledge Base §10) and fill the `{{variables}}` from Stages 04–06. Emails are short and plain, signed by the advisor. SMS stays under 160 characters, includes the advisor's name, and goes only to contacts with `sms_consent = yes`.

Variables: `{{first_name}}` `{{advisor}}` `{{advisor_first}}` `{{firm}}` `{{webinar_title}}` `{{session_time}}` (in the contact's time zone) `{{join_link}}` `{{replay_link}}` `{{replay_expires}}` `{{workbook_link}}` `{{assessment_link}}` `{{booking_link}}` `{{appointment}}` (named session) `{{deliverable}}` `{{meeting_time}}` `{{questionnaire_link}}` `{{reschedule_link}}` `{{phone}}` `{{promise_1-3}}`

Every email footer: the firm's disclosure, physical address, and unsubscribe link. Every SMS: "Reply STOP to opt out" (on the first message, and periodically after).

---

## S1 · Registration confirmation + reminders
*Goal: show up live. Webinar research: reminders within 24 hours outperform 1-hour-only; SMS raises attendance (Stage 06, R29–R30).*

| When | Channel | Message |
|---|---|---|
| Immediately | Email | **Subject:** You're in: {{webinar_title}}<br>Hi {{first_name}}, you're registered for {{session_time}}. **Save this link:** {{join_link}}. Before the class: (1) add it to your calendar, (2) print your workbook: {{workbook_link}}, (3) if you have 3 minutes, take my free assessment ({{assessment_link}}) so you'll know which part of the class matters most for you. See you there. {{advisor_first}} |
| Immediately | SMS | {{advisor_first}} here from {{firm}}. You're registered for {{session_time}}. Join link: {{join_link}}. Reply STOP to opt out. |
| 1 day after registering (if the session is 3+ days away) | Email | **Subject:** The question I'll answer on {{day}}<br>One question I hear constantly: "{{common_question}}". I'll answer it in the class, along with {{promise_2}}. Your link: {{join_link}} |
| 24 hours before | Email | **Subject:** Tomorrow: {{webinar_title}}<br>Quick reminder: tomorrow at {{time}}. In 60 minutes you'll learn: • {{promise_1}} • {{promise_2}} • {{promise_3}}. Bring your spouse or partner; these decisions are easier together. Link: {{join_link}} |
| 24 hours before | SMS | Tomorrow at {{time}}: {{short_title}} with {{advisor_first}}. Link: {{join_link}} |
| 1 hour before | Email | **Subject:** Starting in 1 hour<br>We start at {{time}}. Grab your workbook ({{workbook_link}}) and a pen. Link: {{join_link}}. Joining by phone? {{dial_in}} |
| 1 hour before | SMS | Starting in 1 hour! {{join_link}} (Workbook: {{workbook_link}}) |
| At start | SMS + email | We're live now. Join here: {{join_link}} |
| 10 minutes in (not joined) | SMS | We just started and it's not too late. Jump in: {{join_link}} |

---

## S2 · Show-rate sequence (booked appointment)
*Goal: show up, prepared, ideally with their spouse. This is the most valuable sequence in the system.*

| When | Channel | Message |
|---|---|---|
| Immediately | Email | **Subject:** You're booked: your {{appointment}} on {{meeting_time}}<br>Hi {{first_name}}, I'm looking forward to it. **What happens:** we'll walk through {{steps_summary}}, and you'll leave with {{deliverable}}, whether or not we ever work together. **Two quick things:** (1) if you're married or planning with someone, please have them join; (2) fill out this 5-minute questionnaire so we can use our time well: {{questionnaire_link}}. **What to bring:** {{bring_list}}. Need to change the time? {{reschedule_link}}. {{advisor_first}} |
| Immediately | SMS | {{advisor_first}} here. You're booked for {{meeting_time}}. Details in your email. Need to change it? {{reschedule_link}} |
| Day after booking (if the meeting is 3+ days away) | Email | **Subject:** A quick hello before we meet<br>A short video (or note) from {{advisor_first}}: who they are, what to expect, and that there's no pressure. Link the video if there is one. |
| 2 days before | Email | **Subject:** Have you had a chance to fill this out?<br>If you haven't yet, here's the questionnaire: {{questionnaire_link}}. It helps me prepare your {{deliverable}}. *(send only if not completed)* |
| 24 hours before | SMS | Looking forward to tomorrow at {{time}}, {{first_name}}. {{location_or_zoom}}. Reply C to confirm or use {{reschedule_link}} to change. |
| 2 hours before | SMS | See you at {{time}}! {{zoom_link_or_address}}. {{advisor_first}} |
| If no confirmation by 4 hours before | Staff task | A personal call: "Just making sure the time still works." |

---

## S3 · No-show recovery (meeting)
| When | Channel | Message |
|---|---|---|
| 15 minutes after the missed start | SMS | Hi {{first_name}}, we missed you today. No problem, life happens. Want to pick a new time? {{reschedule_link}} |
| Same day | Staff call | Friendly, no guilt. Offer two specific times. |
| Next day | Email | **Subject:** Let's find a better time<br>Your {{deliverable}} is still waiting for you. Pick a time that works: {{reschedule_link}} |
| 3 days later | Email | **Subject:** Should I keep your spot open?<br>Short and gracious. After this → S8 nurture. |

---

## S6 · Assessment: qualified, not booked
| When | Channel | Message |
|---|---|---|
| Immediately | Email | **Subject:** Your {{score_name}}: {{score}}<br>Hi {{first_name}}, your score is {{score}} ({{band}}). Your two focus areas: **{{focus_1}}** and **{{focus_2}}**. {{focus_1_feedback}} The fastest way to turn this into a plan is a free {{appointment}}. You'll leave with {{deliverable}}. {{booking_link}} |
| Day 1 | Email | **Subject:** About your {{focus_1}} score<br>Teach one useful idea about focus step 1 (from the webinar's Big Ideas). Booking link. |
| Day 3 | Email | **Subject:** What happens in a {{appointment}}<br>Three bullets, the deliverable, no cost/no obligation, honest capacity. Booking link. |
| Day 3 | SMS | Hi {{first_name}}, {{advisor_first}} here. Want help with your {{focus_1}} score? Grab a time: {{booking_link}} |
| Day 6 | Email | **Subject:** A free class on {{focus_1}}<br>Invitation to the next webinar for the matching track. → S1 if they register; S8 if not. |

## S7 · Assessment: not qualified
| When | Channel | Message |
|---|---|---|
| Immediately | Email | **Subject:** Your {{score_name}} results<br>The score and focus areas, plus one useful tip per focus area. Invitation to the free class: {{webinar_link}}. |
| Day 3 | Email | **Subject:** Join me for a free class<br>The webinar's 3 promises. Register link. |
| Day 10 | Email | The book, or a helpful article on their focus step. → S8 |

---

## S8 · Long-term nurture
*Goal: stay helpful and top of mind until the timing is right. Most appointments from nurture come months later.*
- **Monthly email** (1st Tuesday): one useful idea in the advisor's voice, rotating through the tracks; one story; one soft call to action (book, or the next class). Topics come from the Stage 06 seeded questions and Stage 03 facts.
- **Next-track invitations:** when a new track webinar is scheduled, invite everyone who hasn't attended that track.
- **Trigger dates:** birthday milestones (59½, 62, 65, 73), January (tax), October (Medicare open enrollment), November (year-end), after big market moves (calm, educational, with no predictions).
- **6-month assessment re-take:** "Has anything changed? Retake your score."
- **Re-engagement after 12 months of no opens:** "Should I keep sending these?" Remove anyone who doesn't respond (keeps the list healthy and deliverability strong).

## S9 · New client onboarding + referral
| When | Message |
|---|---|
| Day 0 | Welcome: what happens next, who to contact, and the timeline. A signed copy of the advisor's book in the mail. |
| Day 7 | "Here's what we've done so far" progress note |
| Day 30 | Check-in: "How are you feeling about the plan?" (feedback) |
| Day 60 | Referral moment, if appropriate and permitted: "Is there someone you care about who's facing the same decisions? I'd be glad to send them a copy of my book, or invite them to my next class." Never incentivized in ways the firm's rules prohibit. |
| Annual | The review invitation, built around the mechanism steps |
