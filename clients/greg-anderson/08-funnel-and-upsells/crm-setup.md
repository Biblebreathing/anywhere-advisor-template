# CRM Setup — Greg Anderson

**Status:** Blueprint, not built yet. Greg's CRM is open: he uses **Gradient** today (fed by the Color of Money tool) and mentioned moving to Redtail "or something." The AIMO pilot needs a CRM that accepts inbound webhooks and runs email and SMS sequences (GoHighLevel, HubSpot, ActiveCampaign or Keap; Redtail alone does not run marketing sequences). **[DECISION: Terrance/Greg]**

Build exactly from `stages/08-funnel-and-upsells/automation-map.md`. Greg-specific settings:

## Fields (add to the standard set)
| Field | Values |
|---|---|
| `first_track` | `estate` (campaign #1), `tax` (campaign #2) |
| `assessment_name` | `legacy-readiness`, `path-score` |
| `focus_steps` | Legacy: documents, beneficiaries, incapacity, court, family · PATH: paycheck, assets, taxes, heirs |
| `market` | engineer, long-time employee, landlord, business owner, RSU holder |
| `tax_client` | yes/no (Fort Collins Tax Advisory Group client) |
| `tax_return_uploaded` | yes/no (for the CPA What-If) |

## Tags (Greg-specific, in addition to the standard)
`track:estate` `track:tax` · `assess:legacy-readiness` `assess:path-score` · `focus:documents` … `focus:heirs` · `market:*` · `src:tax-client` `src:color-of-money` (existing tool) · `path-review:family-legacy` `path-review:tax`

## Triggers specific to Greg
| Trigger | Actions |
|---|---|
| Legacy Readiness webhook, qualified, not booked in 60 min | S6-L |
| PATH Score webhook, qualified, not booked in 60 min | S6-P |
| Either assessment, not qualified | S7 (estate class or Tax Trap class to match) |
| PATH Review booked | Stop all sales sequences · S2 · notify **Greg and Paula** with score, focus areas, qualifier answers, class question · task: request tax return upload |
| Tax return uploaded | Task for the tax team: CPA What-If before the meeting |
| Color of Money lead (Gradient) | Until migrated: forward to the new CRM by Zapier/Make or manual import; tag `src:color-of-money`; start S6-P |

## Notifications
Booking notice to Greg (SMS) and Paula (email). Weekly report to Greg and Terrance: registrants, attendance %, assessment completions, bookings by source, show rate, meeting 1 → client, **cost per kept PATH Review**, versus the goal math (about 8 booked a month).

## Test log
| Test | Date | Result |
|---|---|---|
| Legacy Readiness, qualified → S6-L | | |
| Legacy Readiness, not qualified → S7 | | |
| PATH Score → S6-P | | |
| Class registration → S1 | | |
| Attended / no-show → S4 / S5 | | |
| Booking → S2 + notifications; sales sequences stop | | |
| Meeting no-show → S3 | | |
| SMS STOP | | |
