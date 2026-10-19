# Test Notes — Greg Anderson Assessments (Oct 19, 2026)

| Assessment | File | Questions | Steps | Use |
|---|---|---|---|---|
| **Legacy Readiness Check** | `legacy-readiness.json` → `build/legacy-readiness/` | 10 scored + 2 qualifiers | Documents, Beneficiaries, Incapacity, Court & Probate, Family Readiness | **Estate funnel (campaign #1)**: ads → check → PATH Review (Family Legacy Edition) |
| **PATH Score** (master) | `path-score.json` → `build/path-score/` | 14 scored + 2 qualifiers | Paycheck, Assets, Taxes, Heirs | Website, Tax Trap webinar, book QR codes |

## Browser tests (Playwright, Chromium), both assessments
| Test | Result |
|---|---|
| Desktop 1100px, qualified prospect (all middle answers) | ✅ Score 36 (PATH) / 47 (Legacy); focus areas tagged; CTA books the PATH Review with name and email pre-filled |
| Phone 390px, unqualified (10+ years from retirement) | ✅ Main button routes to the class (nurture); no page errors |
| Form validation | ✅ "Please enter your first name." / "Please enter a valid email address." |
| Webhook payload | ✅ One POST per completion with scores, band, qualified, focus steps, UTMs, SMS consent |
| UTM capture | ✅ utm_source / utm_campaign carried through |

## Before going live (see `../gaps.md`)
- [ ] **Calendar link**: replace `https://balancedfinancialinc.com/path-review`
- [ ] **CRM webhook URL** (`webhookUrl` is empty: leads are NOT sent anywhere yet)
- [ ] **Privacy policy URL**: confirm `https://balancedfinancialinc.com/privacy-policy` exists
- [ ] **Class URLs**: `/tax-trap` and `/estate-class` (built in Stage 08)
- [ ] **Asset floor**: unqualified = under $500K or 10+ years out. Confirm with Greg (offer stack suggested $750K)
- [ ] **Scarcity line** says "a limited number" until Greg confirms his real monthly capacity
- [ ] **Disclosure**: the footer holds a [COMPLIANCE] placeholder; replace it with the approved text
- [ ] **Legal wording** in the Legacy Check (probate, beneficiary forms overriding a will, court-appointed decision makers) → [ATTORNEY REVIEW]
- [ ] Mechanism name is the **PATH Plan placeholder**
- [ ] Compliance submission date: ______
