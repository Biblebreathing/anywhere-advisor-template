# Stage 07 — Website

**Purpose:** Build the advisor's authority website: the hub that every ad, QR code, webinar follow-up, and referral points to. It's designed to **turn visitors into booked appointments**, or into leads (assessment, webinar, book) who'll book later.

## Read first
`website-guide.md`: the conversion hierarchy, sitemap, page-by-page structure, writing rules, design for a 55+ audience, local SEO, and compliance (BrokerCheck, Form CRS, approved vendors).

## Inputs
- `02-knowledge-base/`: the knowledge base (story, voice, differentiators), brand palette, logo, headshots
- `03-deep-research/`: market brief and fact sheets (for planning pages)
- `04-offer-and-mechanism/`: positioning, mechanism and diagram, appointment offer, client journey
- `05-assessments/`: the assessment URL
- `06-webinars/`: titles, promises, Through Lines, seeded questions per track
- `01-interview/intake.md`: domain, phone, address, calendar link, **who must approve the website and whether the firm requires an approved website vendor**

## Steps
1. **Confirm the platform first.** If the firm requires an approved website vendor, the content from this stage goes into that platform; the generated site then serves as the design and copy prototype for review.
2. **Write `site.json`** (Claude): copy `examples/site.json` to `clients/<slug>/07-website/site.json` and replace every field from the client's files, following `website-guide.md`. One planning page per track the advisor runs. No placeholder text may remain at launch (search for `[`).
3. **Build it:**
   ```
   python3 tools/build_site.py --content clients/<slug>/07-website/site.json \
     --palette clients/<slug>/02-knowledge-base/brand-palette.json \
     --out clients/<slug>/07-website/build
   ```
   The build warns about missing booking links, BrokerCheck and Form CRS links, privacy text, long headlines and SEO titles, and risky compliance words.
4. **Test** (Claude): check for no broken links; check desktop and phone screenshots for no sideways scrolling; confirm every button goes to the right place (booking, assessment, webinar registration); confirm the phone number is tap-to-call.
5. **Compliance review:** submit the full site (or a PDF of every page) to the approver. Keep the approved copy, dated.
6. **Publish** (see *Hosting*), then: point the domain, submit `sitemap.xml` to Google Search Console, and set up the Google Business Profile with the same name, address, and phone.

## Outputs (in `clients/<slug>/07-website/`)
| File | What it is |
|---|---|
| `site.json` | All site copy and settings (the source of truth; edit, then rebuild) |
| `build/` | The finished static site: pages, `style.css`, `assets/`, `sitemap.xml`, `robots.txt` |
| `launch-checklist.md` | Test results, the compliance approval date, and the domain/Search Console/Google Business Profile steps completed |

## Content file reference (`site.json`)
| Key | What it holds |
|---|---|
| `site` | domain, firm, tagline, logo; `advisor` (name, title, photo, photo2, phone, email, address, hours); `mechanism` (name, diagram, steps with text/detail/deliverable); `appointment` (name, headline, text, deliverable, button, button_short, scarcity, url); `assessment`, `webinar`, `book` (cards on the home page); `legal_links` (Form CRS, BrokerCheck, ADV, disclosures); `disclosure` (footer text on every page) |
| `seo` | home_title, description, area_served |
| `home` | hero (eyebrow, headline, subhead), problem (headline, bullets, not_your_fault), mechanism_intro, proof (verified stats only), guide_text, faq |
| `about` | headline, lead, story (paragraphs), calling, different, credentials |
| `how` | headline, lead, meetings, faq |
| `planning` | one object per track: slug, title, card_title, card_text, seo_title (≤ 60 characters), h1, lead, webinar_url, belief, familiar, ideas, how, note (compliance), faq |
| `webinars` | headline, lead, events (when, title, promises, url, button), note |
| `book_page` | optional, once Stage 09/10 exist: title, subtitle, cover, bullets, url, button |
| `contact` | headline, lead, note |
| `privacy`, `disclosures` | paragraphs approved by compliance |

## Hosting
The `build/` folder is a complete static site that works on any host: Netlify, Cloudflare Pages, Vercel, or GitHub Pages (free or low cost; drag-and-drop or connected to the repo), or uploaded to existing hosting. To move it into a site builder (WordPress, GoHighLevel, Squarespace, or a compliance-approved vendor), use the generated pages as the layout and copy reference.

## Done when
- [ ] No placeholder text remains; every fact is current; every story has consent
- [ ] The build has no errors; warnings are resolved or accepted (with a note)
- [ ] There are no broken links; it works on phone and desktop; every call to action goes to the right place
- [ ] BrokerCheck, Form CRS, ADV (as applicable), the privacy policy, and the disclosures are in place
- [ ] Compliance approval received and the approved copy archived
- [ ] Live on the domain; sitemap submitted; Google Business Profile matches
