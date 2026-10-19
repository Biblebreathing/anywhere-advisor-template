# Stage 01 — Intake + Interview

**Purpose:** In 30–45 minutes of the advisor's time, capture everything the later stages need: positioning, offer, webinars, website, funnel, and book.

## Why there are two parts
Facts like licenses, firm, tools, and budget take up interview time but produce no stories. They go on a **written intake form** filled out beforehand. The interview is then spent only on what can't be captured on a form: **stories, beliefs, process, and voice.**

| Step | File | Time | Who |
|---|---|---|---|
| 1. Intake form | `intake-form.md` | 5–10 min | Advisor fills it out before the interview |
| 2. Interview | `interview-prompt.md` | 30–45 min | Advisor pastes it into an AI tool (or a person runs it live using the same questions) |
| 3. Knowledge Base | produced by the AI at the end of the interview, using the structure in `interview-prompt.md` | — | AI |

## Outputs (in `clients/<slug>/01-interview/`)
- `intake.md`: the completed intake form
- `transcript.md`: the full interview conversation (copy/paste or export from the AI tool)
- `knowledge-base.md`: the Advisor Knowledge Base (target 2,500–3,500 words)

## Design rules (what changed from the previous interview)
- **15 questions, not 18 areas + 2 closers.** Overlapping questions were merged (ideal client + best-client patterns + future client; vision + ideal growth outcome; unfair advantage + differentiators; natural markets + access + untapped opportunities).
- **The author interview and the discovery interview are combined into one.** The book questions are asked in the same session.
- **Must-have questions are marked ★.** If time runs short, the interviewer skips to them, so a short session still produces enough for the book and the funnel.
- **Specifics beat categories.** The best material comes from narrow follow-ups ("Tell me about one time that happened"), not from broad questions. The prompt tells the AI to push for one concrete example per answer.
- **The output is about a quarter of the old length.** Technical subject-matter knowledge (how trusts work, tax rules, LTC options) is **not** collected in the interview. It comes from Deep Research (Stage 03) and gets checked against the advisor's opinions.
- **The flag system is kept:** `[VERIFY]`, `[INFERRED]`, `[ANONYMIZE]`, `[COMPLIANCE]`.
