# Stage 10 — Book Website & Funnel

**Purpose:** Turn readers into appointments. Build the **book offer page**, the **reader bonus hub** every chapter's QR code points to, **printable worksheet pages**, and the **reader sequence**, then put the book to work across the practice.

## Read first
`book-funnel-guide.md`: the four offer types (free signed copy mailed, free + shipping, download, Amazon), hub design, worksheets, the reader sequence (S10), **the book as an appointment engine** (7 uses), the launch plan, and compliance.

## Inputs
- `09-book/`: `book.json`, `worksheets/`, `qr-map.json` (destinations must point at this stage's hub anchors)
- `02-knowledge-base/`: brand palette, headshot; book cover (Stage 11, or a placeholder until then)
- `04-offer-and-mechanism/`: the named appointment and deliverable
- `08-funnel-and-upsells/`: the CRM webhook, automation map, sequence rules
- `01-interview/intake.md`: licensed states / service area (for the mailed offer)

## Steps
1. **Choose the offer** (with the advisor): the **free signed copy, mailed, to the licensed states** is the default for local advisors.
2. **Write `book-funnel.json`** (copy `examples/book-funnel.json`): offer copy, hub chapters (one per chapter with a QR code; anchors must match `qr-map.json`), the SMS consent text, the webhook.
3. **Build:**
   ```
   python3 tools/build_book_funnel.py --content clients/<slug>/10-book-funnel/book-funnel.json \
     --book clients/<slug>/09-book \
     --palette clients/<slug>/02-knowledge-base/brand-palette.json \
     --out clients/<slug>/10-book-funnel/build
   ```
   This produces `build/book/` (offer page) and `build/book-bonus/` (hub + `worksheets/*.html`, each with Print / Save as PDF). The build **fails** if any QR code points to a hub anchor that doesn't exist, or a worksheet is missing.
4. **Publish** both folders on the advisor's domain at the paths in `qr-map.json` (e.g., `/book` and `/book-bonus`), together with the QR redirects from Stage 09 (`09-book/build/qr/redirects/`).
5. **CRM:** add the events below to the Stage 08 automation map; load the S10 reader sequence; set up fulfillment for mailed copies (who signs and ships, and how fast).
6. **Test** with a real phone: scan every printed QR code → redirect → hub anchor → sign-up → worksheet → CRM record with the chapter tag. Request a book from inside and outside the service area.
7. **Compliance:** submit the offer page, hub, worksheet pages, and S10 emails.
8. **Roll out the playbook** (guide §5): pre-meeting mailing, webinar gifts, referral-partner boxes, client welcome kits.

## Outputs (in `clients/<slug>/10-book-funnel/`)
`book-funnel.json` · `build/book/` · `build/book-bonus/` · `reader-sequence.md` (S10, in the advisor's voice) · `fulfillment.md` (who mails signed copies, inventory, turnaround) · `launch-checklist.md`

## Webhook events
| Event | When | Payload highlights | CRM action |
|---|---|---|---|
| `book_requested` | Offer form submitted | contact, **address** (mailed), offer type, UTM | Tag `book:requested`, `src:<utm_source>`; create a fulfillment task (mailed); start **S10** |
| `book_reader_registered` | Hub sign-up | contact, **chapter** (from the URL anchor), UTM (`utm_content` = the QR id) | Tag `book:reader`, `book:qr-<chapter>`; start **S10** if not already in it |

## book-funnel.json reference
| Key | What it holds |
|---|---|
| `site` | firm, logo, advisor (name, photo, phone), appointment (name, deliverable, deliverable_short, button, url), disclosure, privacy_url |
| `book` | title, subtitle, cover |
| `hub_url` | The hub's public URL (used to cross-check QR destinations) |
| `offer` | `type` (`mailed` / `download` / `amazon`), eyebrow, headline, bullets, who, author_line, form_headline, form_text, button, `states` (2-letter codes for mailed copies), out_of_area_message, limit_note, done_headline, done_text, download_url, amazon_url, faq |
| `hub` | `gate` (true = one-time sign-up unlocks worksheets), headline, lead, `chapters` (anchor, label, title, text, worksheet, video_embed_url, next {label, url}) |
| `sms_consent`, `webhookUrl` | As in Stage 08 |

## Done when
- [ ] The offer page and hub are live at the paths the QR codes use; every printed code works from the proof copy
- [ ] Book requests and reader sign-ups reach the CRM with tags; S10 runs and stops when someone books
- [ ] Mailed-copy fulfillment is assigned, with a turnaround target
- [ ] Compliance approval received
- [ ] At least two playbook uses are running (e.g., the pre-meeting mailing + webinar gift)
