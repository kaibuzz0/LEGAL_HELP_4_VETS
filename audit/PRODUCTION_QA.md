# PRODUCTION QA CHECKLIST

Project: LEGAL HELP 4 VETS
Version: Phase 5 Hardened + Phase 6 Governance
Use before every release.

## SITE

- [ ] All pages load with HTTP 200
- [ ] Navigation works on desktop
- [ ] Navigation works on mobile
- [ ] Internal links work
- [ ] Page anchors work
- [ ] No console errors
- [ ] No missing assets (CSS, JS, data files)
- [ ] Print button present on every content page
- [ ] Last-updated date present on every page

## LEGAL

- [ ] New legal claims are sourced
- [ ] Existing claims were not unintentionally altered
- [ ] Eligibility language is verified
- [ ] Deadlines are verified
- [ ] Phone numbers are verified
- [ ] Government URLs are verified
- [ ] No guarantee of outcome
- [ ] No fabricated contact information

## SOURCES

- [ ] `data/sources.json` updated if needed
- [ ] No unresolved `[?]` markers
- [ ] No orphan source IDs
- [ ] No duplicate source IDs
- [ ] Verification dates present
- [ ] Next-review dates present
- [ ] Pending sources clearly identified
- [ ] Authority level set

## ACCESSIBILITY

- [ ] Exactly one H1 per page
- [ ] Heading hierarchy preserved (h1 → h2 → h3)
- [ ] Keyboard navigation works
- [ ] Focus states visible
- [ ] Alt text on any images
- [ ] Link labels are descriptive
- [ ] Mobile layout readable

## SEO / METADATA

- [ ] Title tag unique on each page
- [ ] Meta description present on each page
- [ ] Open Graph tags present
- [ ] Canonical URL where required
- [ ] Sitemap.xml is current
- [ ] robots.txt is present

## REGRESSION TESTS

- [ ] `python -m unittest tests.test_html` passes
- [ ] `python -m unittest tests.test_sources` passes
- [ ] `python tests/test_legal_language.py` reviewed for new high-risk words

## DEPLOYMENT

- [ ] Git diff reviewed for accidental changes
- [ ] No secrets, API keys, or tokens committed
- [ ] No personal information accidentally added
- [ ] Commit message follows change-control format
- [ ] GitHub Pages deployment successful
- [ ] Live site rechecked after deployment
- [ ] `data/sources.json` loads correctly on live site

## POST-DEPLOYMENT SPOT CHECKS

- [ ] https://kaibuzz0.github.io/LEGAL_HELP_4_VETS/ loads
- [ ] housing.html loads and action ladder visible
- [ ] sources.html loads and shows all entries
- [ ] tel:988 link present on crisis pages
- [ ] Disclaimer visible

## SIGN-OFF

QA completed by: ___________________  Date: ___________________

Remaining risks noted: ___________________
