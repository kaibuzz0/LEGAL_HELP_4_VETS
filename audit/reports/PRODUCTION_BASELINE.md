# PRODUCTION BASELINE

Project: LEGAL HELP 4 VETS
Repository: https://github.com/kaibuzz0/LEGAL_HELP_4_VETS
Live site: https://kaibuzz0.github.io/LEGAL_HELP_4_VETS/

Production version: Phase 5 Hardened + Phase 6 Governance
Date: 2026-08-11T18:35:48.847067
Branch: main
GitHub Pages source: / (root)
Latest commit: 5edf6ae09a37
Latest commit message: LEGAL HARDENING: source verification, SCRA precision, housing corrections, technical audit (audit/reports/user_journey_housing.json)

## Inventory

- Total files: 37
- HTML pages: 17
- Source registry entries: 129
- CSS files: 1
- JS files: 2
- Data files: 3

## HTML Pages

- 404.html
- about.html
- appeals.html
- claims.html
- discharge-upgrade.html
- employment-money.html
- faith-encouragement.html
- family-immigration.html
- help-now.html
- housing.html
- index.html
- legal-library.html
- sources.html
- state-resources.html
- substance-use.html
- toolkit.html
- widows.html

## Source Registry

- File: data/sources.json
- Entries: 129
- Status levels used: VERIFIED, VERIFIED_PRIMARY, VERIFIED_SECONDARY, PENDING, STALE, BROKEN, RETIRED
- Last updated: 2026-08-11T18:35:48.852069

## Known Pending Items

1. BJA Veterans Treatment Courts URL (justiceforvets.org / bja.gov path) - automated verification blocked by environment; source marked PENDING
2. Some external authoritative sources return HTTP 403 to automated requests (CFPB, 988 Lifeline, Justice for Vets) but remain accessible to normal users

## External Verification Limitations

- HTTP 403 responses do not indicate a broken source when the site is known to block automated requests.
- State/local program URLs are verified when possible; some smaller court/legal-aid sites may block or time out.

## Major Completed Hardening Work

- 246 high-risk legal statements audited
- SCRA section-by-section corrections applied (50 U.S.C. 3931, 3932, 3937, 3951, 3953)
- Fair Housing reasonable-accommodation language corrected
- VA home-loan canonical URL corrected
- HUD-VASH / SSVF eligibility language updated
- Housing safety box and action ladder added
- Source registry expanded to 129 entries
- All unresolved [?] markers resolved
- Technical audit: duplicate H1 fixed, metadata present on all pages
- Last-updated dates added to every page
- 35 files committed and live site validated

## Baseline Confirmation

This file is the reference state for all future Phase 6+ changes.
