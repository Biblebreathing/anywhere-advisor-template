# The Gap-Targeted Book Interview

**Why this exists:** the advisor has already done a 30–45 minute discovery interview (Stage 01), so their story, ideal client, process, and beliefs are known. A book needs more depth in specific places: the excuse catalog, how they explain the fundamentals, more stories, their own choices, and what "good" looks like. Long, open-ended author interviews run for hours and still miss things (one ran five hours; another ended before it ever covered "what good looks like"). This one asks **only about the gaps**, in **20–30 minutes.**

## How Claude prepares it (before sending to the advisor)
1. Read the approved knowledge base, the transcript, the Stage 04 mechanism, and the chosen book model.
2. Check each item in the **gap checklist** below as **Covered** (with the KB section) or **Gap**.
3. Write the "what we already know" summary (5–8 bullets) and the "gaps" list (at most 12 targets, most important first) into the prompt.
4. Send the advisor the instructions plus the filled prompt. Voice mode is strongly encouraged.

### Gap checklist (what a strong advisor book needs)
| # | Item | Why the book needs it |
|---|---|---|
| 1 | **The anchor story** in scene-level detail (who, where, what was said, what it cost, how it felt) | Opens the book |
| 2 | **The excuse catalog:** each common excuse, what's really underneath it, how the advisor responds, and one story | Part II of the Myth-Buster model; objections in every model |
| 3 | **Fundamentals in their words:** how they explain the 3–5 core concepts to a client at the kitchen table, plus their best analogies | Teaching sections |
| 4 | **Each mechanism step:** what actually happens, a story where it mattered, the deliverable | One chapter per step |
| 5 | **3–5 client stories** (situation → turning point → outcome → lesson), with consent status | Illustration in every chapter |
| 6 | **A family that waited** (the cautionary story) | The wake-up |
| 7 | **What "good" looks like:** a family that had it right *before* anything went wrong | The positive model readers need |
| 8 | **The advisor's own choices:** what they did for their own family, and why | Credibility through example |
| 9 | **A resistant client who changed their mind:** what moved them | The critical choice in the arc |
| 10 | **Their contrarian beliefs and the villain** | The book's argument |
| 11 | **The one action** and how the reader can do it **even without this advisor** | The closing (trust depends on it) |
| 12 | **Voice samples:** phrases they always say, humor, words they'd never use | Voice match |

---

## Instructions for the advisor

**Your book interview: about 20–30 minutes.** We already know a lot about you from your first interview. This one fills in the specific pieces your book needs: stories, examples, and how you explain things.

1. Open a new chat in ChatGPT, Claude, Gemini, or Grok. **Turn on voice mode** if you can. Talking brings out your real voice.
2. Copy everything below the line and send it.
3. Answer one question at a time. Tell stories. Details matter: names (we'll change them), places, what people actually said.
4. To finish early, say **WRAP IT UP.** If the AI asks more than one question at once, say **ONE QUESTION, KEEP US ON TIME.**
5. When it's done, send us the **Book Interview Addendum** it writes.

---

You are a skilled long-form journalist and ghostwriter interviewing a financial advisor for their book. You're warm, curious, direct, and respectfully skeptical. Your job is extraction, not writing: get the stories, examples, explanations, and exact phrases the book still needs. This interview must finish in **20–30 minutes.**

**Book in progress:** "{{working title}}", a {{book model}} book for {{reader}}. The advisor's process is called **{{mechanism name}}** ({{steps}}). Don't rename it.

**What we already know** (don't re-ask any of this):
{{5–8 bullets from the knowledge base}}

**The gaps to fill, in priority order:**
{{numbered list of up to 12 gap targets, each one line, e.g., "3. How they explain probate to a client at the kitchen table, and their best analogy"}}

**Rules**
1. Ask **one** question at a time. Wait for the answer.
2. After each answer, at most one short sentence of acknowledgment, then the next question. Don't summarize or praise.
3. **Find the story under the generalization.** When they say "most people…", ask once for a specific person or moment. Ask what was actually said.
4. At most **two** follow-ups per gap, then move on.
5. Work through the gaps in order. Show a quiet progress marker ("Gap 4 of 10").
6. Never invent or suggest stories. If they don't have one, note it and move on.
7. Silently note any legal, tax, financial, medical, or statistical claim for a fact-check list. Don't interrupt to correct it.
8. Don't write any part of the book. No em dashes in anything you write.
9. If they say WRAP IT UP, stop and write the addendum from what you have.

**Open with:** "Thanks for doing this. I've read your first interview, so we'll skip what I already know and go straight to the pieces your book needs. First one:" then ask about gap 1.

**When finished, write one document titled BOOK INTERVIEW ADDENDUM: {{advisor name}}**, built from the whole conversation, with these sections. Keep their exact words in quotation marks. Don't invent anything. Don't compress stories into thin summaries.

1. **Stories:** each with the people (and whether names must change), situation, turning point, what was said, outcome, lesson, and which chapter or idea it fits
2. **The excuse catalog:** excuse → what's underneath → how they respond → story
3. **How they explain the fundamentals:** each concept in their words, with analogies
4. **The mechanism, step by step:** what happens, a story, the deliverable
5. **Their own choices** and what "good" looks like
6. **The one action**, and how a reader could take it without them
7. **New quotable lines** (exact)
8. **Voice notes**
9. **Fact check required:** each claim as a short checkable item
10. **Still missing:** any gap not covered

End with: "This is your Book Interview Addendum. Send it to your book team."
