# Stage 01 — Interview

**Purpose:** Capture everything needed to build every later asset, in one 60–90 minute conversation.
Everything after this is built from it, so a weak interview means weak assets.

**Inputs:** a recorded interview (Zoom transcript preferred) or a filled-out written questionnaire.

**Outputs** (in `clients/<slug>/01-interview/`):
- `transcript.md`: the raw transcript, unedited
- `advisor-profile.md`: the structured profile, filled in from the transcript using `advisor-profile-template.md`
- `gaps.md`: questions the interview didn't answer, to send back to the advisor

**Rules for Claude when filling the profile:**
- Only use what the advisor actually said. Mark anything inferred as `[INFERRED]`, and anything missing as `[MISSING]` (it also goes in `gaps.md`).
- Keep the advisor's **exact phrases** for stories, beliefs, and client language. They become copy later.
- Note any claim that will need substantiation or compliance review (returns, guarantees, "tax-free", testimonials) under *Compliance flags*.
