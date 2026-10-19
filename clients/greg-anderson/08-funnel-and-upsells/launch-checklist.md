# Funnel Launch Checklist — Greg Anderson

| Funnel | Pages | Browser test (Oct 19, 2026) |
|---|---|---|
| Estate class: "Who Decides When You Can't?" | `estate-planning/build/` | ✅ local-time display, validation, webhook, Google/ICS calendar, phone layout, no errors |
| Tax class: "The Tax Trap" | `tax/build/` | ✅ same tests |
| Legacy Readiness Check (estate ads) | `05-assessments/build/legacy-readiness/` | ✅ |
| PATH Score | `05-assessments/build/path-score/` | ✅ |

## Before launch
- [ ] CRM chosen and built from `crm-setup.md`; `webhookUrl` set in every funnel.json and assessment config; rebuild
- [ ] Real booking link (also rebuild both decks: the QR codes encode it)
- [ ] Zoom (or webinar platform) links, dial-in, real session dates (placeholders: Tue Tax Trap / Thu estate, 11am MT)
- [ ] Workbook PDFs published at `/tax-trap-workbook.pdf`, `/estate-workbook.pdf` (from each `workbook.md`)
- [ ] PATH Review questionnaire form at `/path-questionnaire`; tax-return upload link
- [ ] Sequences loaded (`sequences.md` + each track's `post-webinar-emails.md`)
- [ ] End-to-end test with a real phone and email (see `crm-setup.md` test log)
- [ ] Compliance approval: pages, ads, emails, texts. Date: ______
- [ ] Launch date: ______ · weekly report to Greg and Terrance running
