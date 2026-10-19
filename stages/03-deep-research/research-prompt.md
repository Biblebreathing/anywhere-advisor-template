# Deep Research Prompt (for ChatGPT, Gemini, or Perplexity Deep Research)

*Fill in the {{ }} fields from the Knowledge Base, then paste. Run one prompt for the Core research, and separate prompts per Extended module if the output gets too long.*

---

You are a research analyst supporting a financial advisor's educational marketing. Produce **sourced, current, factual research**. This is not advice and not marketing copy.

**Advisor context**
- Service area: {{city/county, state}}
- Ideal client: {{e.g., married couples 58–72, $500K–$3M saved, pre-retirees and new retirees}}
- Niche (if any): {{e.g., retired teachers in the state pension system}}
- Webinar topics: {{Estate Planning / Tax / Retirement Paycheck / Asset Protection / Long-Term Care}}
- Current year: {{year}}

**Research these:**
1. **Federal figures for {{year}}** relevant to the webinar topics (e.g., estate and gift exemption, annual gift exclusion, RMD age, IRA/401(k) limits, Social Security full retirement age and COLA, Medicare Part B premium and IRMAA thresholds, standard deduction and brackets for retirees).
2. **{{State}} rules:** state tax on Social Security, pensions, and IRA withdrawals; state estate or inheritance tax and its exemption; probate process, typical timeline, costs, and the small-estate limit; homestead and creditor-protection basics; Medicaid long-term care asset limits, look-back period, and estate recovery.
3. **Local market data for {{service area}}:** population 55+ and 65+ (count, share, 10-year growth), median household income for householders 65+, median home value, homeownership rate 65+, major employers and their pension or retirement plans, and long-term care costs (home care, assisted living, nursing home) for the area or state.
4. **For each webinar topic:** 5 common consumer myths with the facts that correct them, and 5–10 surprising, well-sourced statistics suitable for a presentation headline.
5. **Verify these claims** from the advisor's interview: {{paste every [VERIFY] item}}
6. **Recent or upcoming law changes** (the last 2 years and the next 3) affecting these topics.

**Rules**
- Cite **every** number: organization, URL, publication date. Prefer primary sources: IRS, SSA, CMS/Medicare, Census ACS, BLS, state revenue and Medicaid agencies, state statutes, CareScout Cost of Care, EBRI.
- If the {{year}} figure isn't published yet, give the most recent one and state its year.
- Mark any state legal rule "[ATTORNEY REVIEW]".
- If a claim from step 5 is wrong or can't be verified, say so plainly and give the correct figure if there is one.
- Don't recommend products or strategies.

**Output format**
- A table of all facts: Fact · Value · Year/State · Source · URL · Published
- Then sections 1–6, each citing the table
- End with "Top 10 findings for this advisor's marketing"
