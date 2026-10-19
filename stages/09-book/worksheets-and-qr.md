# Worksheets & QR Codes

The book is a funnel the reader carries around for years. Worksheets make it useful; QR codes make it **measurable** and connect it to the advisor's calendar.

## 1. Worksheets

### Rules
- **One per chapter** (the Integration movement), 1–2 pages, mapped to the chapter's One Thing
- **Print-first:** black and white, no fill colors (they band on cream paper), 11-point minimum, generous write-in lines (at least 0.35" apart, for older hands), checkboxes ☐, at most 10 items per page
- **Mirrors the funnel:** worksheet items echo the assessment questions (Stage 05) and the webinar workbook (Stage 06), so a reader who brings the book to Meeting 1 has already done the discovery
- **Every worksheet has a downloadable, fillable version** in the reader bonus hub (Stage 10), reached by QR. People prefer to write in a printout rather than the book.
- **No individualized advice:** they're self-assessments and checklists, not recommendations

### Worksheet file format (`worksheets/<id>.md`)
```markdown
## Worksheet: Who Is Actually Named?

List each account and the beneficiary named on it today.

| Account | Where it is | Who is named | Last checked |
|---|---|---|---|
| | | | |
| | | | |

☐ I found at least one beneficiary I need to update
☐ I know where my most recent will or trust is

**Download a printable copy:** see the QR code below.
```

### Worksheet library by track (adapt per advisor)
| Track | Worksheets |
|---|---|
| Retirement Paycheck | Monthly Needs (essential vs. lifestyle) · Dependable Income · My Paycheck Gap · Three Risks Check · Social Security Questions to Ask |
| Tax | My Three Buckets · Income Sources Timeline · Tax Time Bomb Check · Questions for My CPA |
| Estate | What I Own & How It's Titled · Who Is Actually Named? · Who Decides If I Can't · Family Readiness Checklist · Letter of Wishes Starter |
| Asset Protection | Five Threats Score · My Protection Layers · Protecting My Heirs · Fraud-Proof Family Plan |
| Long-Term Care | My Care Wishes · Care Costs Where I Live · Care Readiness Check · Four Options Compared · The Family Conversation Guide |
| Every book | [Mechanism] Readiness Check (all steps; mirrors the assessment) · Questions for My [Named Appointment] |

## 2. QR codes

### Rules
1. **Never print a QR code that points straight at a third-party URL.** Point every code at a **short redirect link on the advisor's own domain** (e.g., `ellisretirement.com/go/ch3`). The destination can then change (a new calendar tool, a new webinar date) **without reprinting the book.**
2. **One code per chapter, plus the bonus hub, the appointment, and the review page.** Each has its own tracking (`utm_source=book&utm_medium=qr&utm_campaign=<book-slug>&utm_content=<qr-id>`), so the advisor learns which chapters drive bookings.
3. **Print spec:** at least 0.8" (2 cm) square, ideally 1"; black on white; a quiet zone around it; error correction level M or higher; 300+ DPI or vector (SVG); **always print the short URL under it** for people who don't scan.
4. **Caption it with the benefit**, not the mechanics: "Scan to download this worksheet" / "Scan to book your Blueprint Session."
5. **Test every code** with iPhone and Android cameras, from the printed proof copy, before release.

### `qr-map.json`
```json
{
  "domain": "ellisretirement.com",
  "book_slug": "paycheck-gap",
  "codes": [
    {"id": "hub", "path": "go/book", "destination": "https://ellisretirement.com/book-bonus", "caption": "Scan for all the worksheets and bonus videos"},
    {"id": "ch03-beneficiary-checklist", "path": "go/ch3", "destination": "https://ellisretirement.com/book-bonus#ch3", "caption": "Scan to download this worksheet"},
    {"id": "appointment", "path": "go/session", "destination": "https://calendly.com/ellis/blueprint", "caption": "Scan to book your Blueprint Session"}
  ]
}
```

### The tool
```
python3 tools/make_qr.py --map clients/<slug>/09-book/qr-map.json --out clients/<slug>/09-book/build/qr
```
It produces, for each code, a print-ready **SVG and 1200px PNG** of the short URL, plus **redirect files** ready to publish on the advisor's site:
- `redirects/_redirects` (Netlify / Cloudflare Pages format, with tracking appended)
- `redirects/go/<path>/index.html` (a meta-refresh page that works on any static host)
- `qr-index.md` (a table of every code, its short URL, and its destination, for the launch test)

Publish the redirects with the website (Stage 07) **before the book is printed**, then test them from the proof copy.
