# Advisor Website Guide

The website has **one job: turn a visitor into a booked appointment**, or, if they're not ready, into a lead (assessment, webinar, or book) who'll book later. It's the hub every other asset points to: ads, the book's QR codes, webinar follow-ups, referrals, and Google searches.

It isn't a brochure. Every page answers three questions within five seconds: **Who is this for? What do I get? What do I do next?**

---

## 1. The conversion hierarchy (on every page)
1. **Primary call to action: book the named appointment** (Stage 04), e.g., "Reserve My Blueprint Session." It's in the header button, the hero, and the end of every page.
2. **Secondary: take the assessment** (Stage 05), for visitors who aren't ready to talk.
3. **Tertiary: join the webinar or get the book**, for visitors who want to learn first.

Never more than one primary button per screen. The phone number is always visible and tap-to-call. Many 55+ prospects still prefer to call.

## 2. Sitemap
| Page | Purpose | Main source |
|---|---|---|
| **Home** | The whole story in one scroll; drive the appointment | Positioning, mechanism, offer |
| **About** | Trust through story (story before credentials, like the webinar) | Knowledge Base §2, §7, §10 |
| **How We Work** | The mechanism step by step; the meeting process; the appointment offer | Stage 04 |
| **Planning pages** (one per track: Retirement Paycheck, Tax, Estate, Asset Protection, LTC) | Rank in search; teach the Through Line in brief; route to the webinar and appointment | Stage 06 track foundation, Stage 03 fact sheet |
| **Webinars / Events** | Upcoming classes and registration | Stage 06 |
| **Assessment** | Link or embed of the scorecard | Stage 05 |
| **Book** | The advisor's book and offer (once Stage 09/10 exist) | Stage 09–10 |
| **Contact / Book** | Calendar embed, phone, office, map | Intake |
| **Legal** | Privacy policy, disclosures, Form CRS / ADV, BrokerCheck, accessibility statement | Advisor's compliance department |

## 3. Home page, section by section
It follows a story arc (the same one as the webinar, in miniature). It's similar to the widely used **StoryBrand** website pattern: the prospect is the hero, the advisor is the guide, and there's a plan and a call to action.

1. **Hero:** the headline names **who + outcome** (≤ 10 words); the subhead names **how (the mechanism) + the fear avoided**; primary button; secondary text link to the assessment; advisor headshot (a real photo of the advisor, never stock). Formula: *"[Outcome] for [who]"* + *"Using the [Mechanism], we help you [result], so you don't [fear]."*
2. **The problem:** "Does this sound familiar?" 3–4 lines in the prospect's words (Knowledge Base §3), then the problem mechanism in one sentence ("It's not your fault…").
3. **The mechanism:** the diagram (Stage 04 SVG) and 1–2 lines per step with its deliverable. Button: "See how we work."
4. **Planning areas:** a card per track, each linking to its planning page.
5. **Proof:** credentials, years in practice, families served (verified only), media, the book. A client story only with consent and firm approval. **No performance claims.**
6. **The guide:** a short "Meet [Advisor]" with photo and two sentences of the origin story. Link to About.
7. **Learn first:** assessment band ("What's your [score]?"), next webinar, the book.
8. **FAQ:** 4–6 objections answered (Knowledge Base §3, Stage 06 objections): cost, "is this a sales pitch?", what happens in the first meeting, who it's for.
9. **Final call to action:** the appointment, its deliverable, honest capacity, phone number.

## 4. About page
Story first: the origin and turning point (Knowledge Base §2), then **why they do this work** (the "This Is My Calling" slide from the webinar), then credentials, then how they're different (Knowledge Base §11 differentiators with evidence), then a photo with family, team, or community (with consent). End with the appointment call to action.

## 5. Planning pages (one per track)
Each is a short, searchable version of the webinar:
- An H1 with the search phrase and location ("Retirement Income Planning in [City]")
- The wrong belief → true belief, in 2–3 short paragraphs
- "Does this sound familiar?" bullets
- The three Big Ideas, a sentence each (the teaching, not the full webinar)
- How the mechanism step works here, plus its deliverable
- 3–5 FAQs (from the track's seeded questions)
- Calls to action: the webinar for this track, the assessment, the appointment
- Track compliance notes (e.g., "not legal advice" on Estate)

## 6. Writing rules
- **Write like the advisor talks** (Knowledge Base §10), at an 8th-grade reading level. Short paragraphs.
- **Specific beats clever.** "Retirement income planning for Ohio educators" beats "Your Financial Future, Reimagined."
- **Benefits in the prospect's words; features (credentials, process) as proof.**
- **Every number cites a fact ID** in the content file, and appears only if it's current.
- **Banned:** guarantees, "safe," "risk-free," "tax-free" without qualifiers, performance claims, unaccredited titles ("Senior Specialist"), stock-photo handshakes.

## 7. Design for a 55+ audience
- Base font **at least 18px** (the generator uses 19px), line height 1.6, high contrast (the Stage 02 palette passes WCAG).
- Large, obvious buttons with plain-language labels ("Reserve My Session," not "Submit").
- A visible phone number and office address. Real photos of the advisor.
- Simple navigation (6 items or fewer), no carousels, no auto-playing video.
- Mobile first: most people will open it from an email or text on their phone.
- Accessibility: alt text, keyboard navigation, focus outlines, a skip link, and form labels.

## 8. Local search (SEO)
- One target phrase per page (e.g., "estate planning [city]"); title tag ≤ 60 characters; meta description ≤ 155.
- `FinancialService` and `Person` structured data (the generator adds them).
- **Google Business Profile:** claim it, use the same name, address, and phone as the site, and add categories and photos. Reviews only within the firm's testimonial rules.
- The same name, address, and phone everywhere (site, Google, directories).
- A `sitemap.xml` and `robots.txt` (generated). Submit them in Google Search Console.
- Later: one helpful article per month per track (see the Stage 06 seeded questions for topics).

## 9. Compliance (non-negotiable)
- **The whole site is a marketing communication.** It needs the advisor's compliance approval before launch, and again whenever content changes. Keep a dated copy of each approved version.
- **Many broker-dealers and some RIAs require approved website vendors** (with built-in archiving and review). If so, the copy, structure, and design from this stage go into the approved platform rather than being hosted independently. Check this at the start (Stage 01 intake: marketing approver).
- **Required links and disclosures** (confirm with compliance; requirements depend on registration):
  - **BrokerCheck:** FINRA member firms' websites need a readily apparent reference and hyperlink to BrokerCheck (FINRA Rule 2210(d)(8)) on the initial retail page and on pages with a rep's profile.
  - **Form CRS:** broker-dealers and RIAs serving retail investors must post their current Form CRS prominently on their public website.
  - **RIAs:** a link to Form ADV Part 2 / IAPD, as directed by compliance.
  - **Insurance:** licensing states and the insurance disclosure required by the advisor's IMO or carriers.
  - The firm's full registration and affiliation disclosure in the footer of every page.
- **Testimonials and reviews:** only if permitted (SEC Marketing Rule for RIAs; FINRA rules; carrier/IMO rules), with the required disclosures.
- **Privacy policy** and, if forms collect data, a statement on how it's used; SMS consent language where texts are sent.
- **Accessibility:** follow WCAG 2.1 AA. The generator's defaults are built for it.
