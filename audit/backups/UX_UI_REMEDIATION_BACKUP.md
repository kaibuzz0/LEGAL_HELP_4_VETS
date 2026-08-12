# UX/UI REMEDIATION BACKUP

Date: 2026-08-11T20:01:25.356026
GitHub main commit SHA: 62d5c65574b2

## Files to Modify

- assets/css/style.css
- assets/js/app.js
- assets/js/components.js
- index.html
- help-now.html
- claims.html
- appeals.html
- discharge-upgrade.html
- housing.html
- employment-money.html
- employment-rights.html
- va-debt.html
- family-immigration.html
- legal-library.html
- toolkit.html
- about.html
- sources.html
- substance-use.html
- widows.html
- state-resources.html
- faith-encouragement.html
- 404.html

## Current Behavior

- Mobile menu button uses `.menu-btn` and `#main-nav`, but JS implementation may conflict with prior code.
- Header is cluttered with legal banner, crisis strip, and page title competing for attention.
- Pages are very long vertically; no progressive disclosure.
- Search only filters the sidebar navigation list, not site content.
- New pages (employment-rights.html, va-debt.html) are live but need consistent discoverability.

## Planned Changes

1. Replace menu JavaScript with a single deterministic controller.
2. Replace/add mobile menu CSS using `.main-nav.is-open` and `.nav-overlay.is-visible`.
3. Add native `<details>`/`<summary>` accordion system via `.content-tile` CSS.
4. Convert secondary sections on dense pages into accordions.
5. Rebuild search as a static navigation index (`SITE_SEARCH_INDEX`) with title/description/keywords scoring.
6. Reorganize homepage mission grid into a clearer "What do you need help with?" hub.
7. Ensure all tests pass and all 19+ pages live-validate.

## Content Freeze

No new legal content, claims, deadlines, or sources will be added.
