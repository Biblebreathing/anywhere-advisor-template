# Voice and Craft Standards

Quill's KB-1 house style, adopted in full and extended for advisor books read by 55–75-year-olds. **`tools/book_lint.py` checks the bracketed [LINT] rules automatically.** The rest need a human or committee eye.

## Prose voice: Pressfield Plain (KB-1)
- Short declarative sentences. Muscular verbs. Concrete nouns.
- Say the hard thing directly, then support it. No hedging, no wind-up.
- **Name the enemy.** The villain gets a name in chapter 1 and keeps it (e.g., Drift, the Paycheck Gap, the Empty Binder). [LINT: the villain term appears in the introduction and at least half of the chapters]
- Write like a professional talking to one reader, not a brand addressing a market. "You" appears early and often.

## Structure: the Atomic Habits influence (KB-1)
- One idea per chapter, stated plainly in the first two pages.
- Story opens, principle follows, application closes. Every chapter gives the reader something to do.
- Frameworks are named, numbered, and repeated. **The mechanism name appears in every chapter that uses it, spelled exactly as locked** (including ™ if approved). [LINT: mechanism spelling]
- Small promises kept beat big promises implied.

## Hard rules (never violate)
1. **No em dashes of any kind.** Use colons, semicolons, or commas. [LINT: catches — and – and "--"]
2. **No AI-sounding chapter-ending flourishes.** Banned closers include any variation of "the journey begins now," "the choice is yours," and rhetorical triple questions. [LINT: closing-phrase list]
3. **Never "turn the page" as a closing pattern.** [LINT]
4. **Traditional punctuation only.** No emoji, no hashtags, no exclamation-point runs. [LINT: emoji, "!!"]
5. **Banned vocabulary:** "in today's fast-paced world," "leverage" (except for debt), "unlock," "delve," "game-changer," "revolutionize," "navigate" (metaphorical), "landscape" (metaphorical), "journey" (more than once per chapter), "empower," "elevate," "unleash," "dive deep," "at the end of the day." [LINT; "journey" counted per chapter]
6. **Never fabricate** stories, statistics, quotes, client results, or credentials.
7. **Never state legal, tax, medical, or financial claims as settled fact** without a fact ID, or a flag in `verify-list.md`.
8. **Preserve the author's voice.** The edit makes them sound like themselves on their best day.
9. **Faith content,** where the author brings it, is woven in authentically; never bolted on, never scrubbed out.
10. **Compliance language is exact** (from `style-sheet.md`); no paraphrase drift. [LINT: if a `compliance_line` is set, it must appear verbatim in the front matter]

## Additions for advisor books
11. **Readability for 55–75:** aim for a grade level of 8 or below in teaching sections; paragraphs of 4 sentences or fewer; define every term the first time. [LINT: Flesch-Kincaid grade per chapter; warns above 9]
12. **No flags left in prose:** no `[VERIFY]`, `[ANONYMIZE]`, `[INFERRED]`, `[F-###]`, `TODO`, or `{{placeholders}}` in the final manuscript. Fact IDs stay in the source chapters as HTML comments `<!-- F-012 -->`, which the assembler strips. [LINT]
13. **Compliance words:** guarantees, "safe," "risk-free," "tax-free" without qualifiers, performance claims, product names. [LINT: flags them for review]
14. **Composite characters** are never described as real clients ("a client of mine" ❌ for a parable character).
15. **The reader can act without you.** The closing shows how to take the one action independently, with the advisor's appointment as one clear option. It's the book's most important trust signal.
16. **Chapter length:** 1,800–2,400 words (intro and closing 1,500–2,500). [LINT: word counts against targets]

## Quality bar (KB-1)
- **The read-aloud test:** if a sentence sounds like a press release, cut or rewrite it.
- **The "who says" test:** author experience, a fact ID, or a flag.
- **The consent test:** real people appear only with permission (Stage 02 consent log) or anonymization.
- **Committee composite 8.0+** before production.
