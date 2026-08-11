# AI_PROJECT_RULES.md

Project: LEGAL HELP 4 VETS
Purpose: Rules for any AI system editing this project
Effective: 2026-08-11

## Core rule

This is a live public-facing legal-information resource for veterans.
Accuracy is more important than volume.

## Before editing

1. Read the current `audit/CHANGE_CONTROL.md`.
2. Read the current `audit/PRODUCTION_QA.md`.
3. Read `audit/reports/PRODUCTION_BASELINE.md`.
4. Inspect the file(s) you plan to change.
5. Inspect related files that might be affected.
6. Run the regression tests (`python -m unittest tests.test_html tests.test_sources`).

## Source rules

- Never invent a source, URL, phone number, form number, or legal authority.
- Every new factual claim must have a source registry entry before it appears in page copy.
- Prefer primary government sources: U.S. Code, eCFR, VA.gov, benefits.va.gov, SSA.gov, USCIS.gov, HUD.gov, DOL.gov, DOJ.gov, FTC.gov, CFPB.gov, Cornell LII.
- Verify the source URL resolves and the claim matches the source.
- Update `data/sources.json` with `verified_date`, `next_review`, `authority_level`, and `status`.
- Resolve or remove every `[?]` citation marker before committing.

## Legal language rules

- Do not use "must," "always," "guaranteed," or "automatically" unless a verified legal requirement supports it.
- Distinguish "veteran" from "servicemember" and "active duty" from "discharged."
- Do not present suggested response deadlines as statutory deadlines.
- Do not guarantee eligibility or outcomes.
- Do not provide individualized legal representation or attorney-client advice.

## Content rules

- Do not overwrite good content just to restate it.
- Preserve the plain-language field-manual style.
- Keep legal authority followed by action steps.
- Maintain the source-before-claim order.
- Do not remove information without justification.
- Do not add large amounts of content without change-control records.

## Technical rules

- Maintain exactly one H1 per page.
- Keep title and meta description on every page.
- Keep the disclaimer and 988 crisis line on every page.
- Keep print buttons on content pages.
- Keep the last-updated footer on every page.
- Preserve semantic HTML and heading hierarchy.
- Do not add unnecessary frameworks or dependencies.
- Do not change navigation without a reason.

## Verification rules

- Run regression tests after changes.
- Review git diff for accidental modifications.
- Check that no secrets were added.
- Verify the live site after deployment.
- Update the source registry if needed.
- Record changes in `CHANGELOG.md` or commit messages.

## Prohibited

- Inventing sources, URLs, phone numbers, organizations, or legal citations.
- Removing disclaimers or safety warnings.
- Changing legal meaning during editorial rewrites.
- Committing API keys, tokens, or personal information.
- Adding unverified state/local resources as verified.
- Over-designing or replacing working systems without measurable improvement.

## Commit format

```
[A/B/C/D] SHORT DESCRIPTION

- What: ...
- Why: ...
- Source: source_id (data/sources.json)
- Verified: YYYY-MM-DD
- Pages affected: ...
- Tests: ...
```

## Failure response

If a regression test fails, stop. Fix the regression before adding new content.

## Contact

If you are unsure about a legal change, mark the section as PENDING and ask the maintainer before publishing.
