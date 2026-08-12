# LEGAL HELP 4 VETS — PHASE 8 FINAL REPORT

Date: 2026-08-11T19:28:58.811244
Repository: https://github.com/kaibuzz0/LEGAL_HELP_4_VETS
Live site: https://kaibuzz0.github.io/LEGAL_HELP_4_VETS/
Live page: https://kaibuzz0.github.io/LEGAL_HELP_4_VETS/employment-rights.html
Commit: 23c72925169b

## Mission

Build a deeply researched, source-verified guide explaining USERRA and veteran employment rights, including reemployment, anti-discrimination, retaliation, deadlines, and enforcement through DOL VETS, ESGR, and DOJ.

## Research

- Verified 38 U.S.C. §§ 4301, 4311, 4312, 4313, 4316, 4317, 4318, 4321, 4322, 4323 (Cornell LII)
- Verified eCFR 29 C.F.R. Part 100 (USERRA implementing regulations)
- Verified DOL elaws USERRA Advisor
- Verified DOL VETS USERRA canonical URL (automated access restricted, user-access verified)
- Verified DOJ Civil Rights Division Employment Litigation Section
- Verified ESGR USERRA page (SSL verification issue automated, user-access verified)
- Verified USERRA poster location

## Legal Authorities Used

- 38 U.S.C. Chapter 43 (USERRA)
- 29 C.F.R. Part 100
- DOL VETS / elaws
- DOJ Civil Rights Division
- ESGR

## New Page

- `employment-rights.html`
- Title: "USERRA & Veteran Employment Rights | LEGAL HELP 4 VETS"
- Sections: Do This First, What Is USERRA?, Who USERRA May Protect, What Kind of Problem Do I Have?, Return-to-Work Deadlines, Notice, Reemployment Rights, Anti-Discrimination, Benefits, Employer Defenses, DOL VETS / ESGR / DOJ, Do Not Confuse These, Action Ladder, Sample Letters, Documents to Save, Common Terms

## Sources Added

- 16 new sources added
- Total source registry entries: 156
- All sources have lifecycle metadata

## Claims Added

- 46 new claim-source mappings on `employment-rights.html`
- All claims supported by primary authority

## Claim Mappings

- `audit/CLAIM_SOURCE_MAP.json` regenerated
- Total mappings: 492

## Deadlines Verified

- Return-to-work deadlines presented by service length (1-30 days, 31-180 days, more than 180 days)
- No universal deadline invented
- Hospitalization/convalescence extension mentioned
- Users directed to verify dates with DOL VETS/ESGR if unsure

## Sample Letters

- Request for reemployment
- USERRA rights concern
- Request for written explanation

All templates use placeholders and avoid unsupported conclusions.

## Action Ladder

- 7-level ladder from documentation to qualified legal assistance

## DOL / ESGR / DOJ Pathways

- DOL VETS: primary assistance and complaint investigation
- ESGR: informal mediation and ombudsman support
- DOJ: enforcement litigation after DOL VETS referral; private right of action also available

## User Journeys

| User | Scenario | Result |
| ---- | -------- | ------ |
| A | Employer refuses reemployment | PASS |
| B | Fired due to military obligations | PASS |
| C | Employer claims missed deadline | PASS |
| D | Retaliation after asserting rights | PASS |
| E | Benefits/seniority questions | PASS |
| F | USERRA vs ADA vs general employment law | PASS |

## Accessibility

- Single H1
- Semantic headings
- Skip link
- 988 crisis line
- Print button
- Disclaimer
- Accessible tables
- Site-standard footer

## Tests

- `tests.test_html`: 9/9 OK
- `tests.test_sources`: 5/5 OK
- Tag balance: all 19 pages OK
- Legal language scan: no "veterans cannot be fired" or equivalent unsafe simplification

## Live Validation

- All 19 pages HTTP 200
- `employment-rights.html` renders correctly
- Sources load (156 entries)
- Sitemap updated
- Navigation and internal links work

## Files Changed

- `employment-rights.html` (new)
- `data/sources.json`
- `sources.html`
- `employment-money.html`
- `toolkit.html`
- `sitemap.xml`
- `tests/test_html.py`
- `tests/test_sources.py`
- `tests/test_legal_language.py`
- `audit/CLAIM_SOURCE_MAP.json`

## Commit

23c72925169b

## Remaining Limitations

- DOL VETS and USERRA poster URLs return 403 to automated requests but are canonical; marked with access-restriction notes.
- ESGR site has an SSL certificate issue in this environment but is user-accessible; marked accordingly.
- The guide does not cover state employment-law variations, union grievances, or non-USERRA workplace disputes.

## Risk Assessment

- Legal accuracy risk: LOW
- Deadline misstatement risk: LOW
- Source integrity risk: LOW
- Technical regression risk: LOW
- Accessibility risk: LOW

## Production Status

PRODUCTION READY

The USERRA / Veteran Employment Rights Guide is live, source-verified, tested, and integrated without breaking the existing system.
