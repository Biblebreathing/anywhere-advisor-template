# Book Funnel Launch Checklist — Greg Anderson

**Status:** Built and browser-tested Oct 19, 2026, from the **blueprint** (no manuscript yet). Rebuild when chapter titles or worksheets change.

| Test | Result |
|---|---|
| Build: every QR destination lands on a real hub anchor; every worksheet exists | ✅ |
| Offer page: out-of-state address blocked with the Amazon message | ✅ |
| Offer page: Colorado request → `book_requested` webhook with state CO, UTM | ✅ |
| Hub: gated; sign-up → `book_reader_registered` with chapter ch1 and utm_content = QR id | ✅ |
| Hub stays unlocked after reload, and for someone who requested the book | ✅ |
| Worksheet page prints to PDF | ✅ |
| JavaScript errors | ✅ none |

## Before launch
- [ ] Book title (placeholder: *A Path to Run On*) and PATH Plan name final
- [ ] Cover image (Stage 11) in `book.cover`
- [ ] CRM `webhookUrl`
- [ ] Publish `build/book/` at `/book`, `build/book-bonus/` at `/book-bonus`, and `09-book/build/qr/redirects/` (`/go/...`) on balancedfinancialinc.com
- [ ] Scan every printed QR from the proof copy
- [ ] Licensed states for mailed copies
- [ ] Chapter videos (optional) recorded
- [ ] Compliance approval: offer page, hub, worksheets, S10
