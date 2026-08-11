# CHANGE CONTROL POLICY

Project: LEGAL HELP 4 VETS
Applies to: All future legal-content, source, and structural changes
Effective: 2026-08-11

## Purpose

This project is a live public-facing legal-information resource. Accuracy is more important than volume. Every change must be traceable to an authoritative source and must not mislead a veteran into taking the wrong action.

## Change Classes

### Class A — Critical Legal Content
Any change to:
- eligibility rules
- deadlines
- phone numbers or hotlines
- government URLs
- statutes, regulations, or form numbers
- legal rights or remedies
- claim/appeal procedures

Requires:
- a source registry update
- verification of the source
- citation on the affected page(s)
- update to `data/sources.json` verification date and status
- review of related pages for inconsistent information

### Class B — Action Steps / Scripts / Checklists
Changes to what users should do, say, or gather.

Requires:
- a supporting source or, when based on best practice, a clear note that it is procedural guidance rather than a legal requirement
- no guarantee of outcome
- no fabricated phone numbers or addresses

### Class C — UX / Accessibility / Technical
Changes to layout, navigation, print styles, metadata, etc.

Requires:
- no regression in existing functionality
- no removal of disclaimers or sources
- validation on the live site after deployment

### Class D — Pure Editorial
Spelling, formatting, heading clarity, plain-language improvements with no legal effect.

Requires:
- spot-check that no legal meaning was altered
- no source registry update needed

## Required Change Record

For every Class A or Class B change, record:

1. **What changed?** — exact text or section changed
2. **Why did it change?** — reason for the update (law changed, source updated, correction, user need)
3. **Which source supports the change?** — source_id from `data/sources.json`
4. **When was the source verified?** — verification date
5. **Does the change affect eligibility?** — yes/no
6. **Does the change affect a deadline?** — yes/no
7. **Does the change affect a phone number?** — yes/no
8. **Does the change affect a legal right?** — yes/no
9. **Does the change require auditing other pages?** — yes/no + list
10. **Does the change require updating the source registry?** — yes/no + source_id

Record this in the commit message or in a `CHANGELOG.md` entry.

## Prohibited Changes

- Never invent a source, URL, phone number, or legal authority.
- Never change a legal claim based only on memory, a blog, or AI-generated material.
- Never remove a source from the registry unless it has been retired or replaced.
- Never present a suggested deadline as a statutory deadline unless verified.
- Never guarantee an outcome or eligibility.
- Never change veteran/servicemember terminology in a way that affects legal meaning.

## Approval Workflow

1. Author identifies the change and supporting source.
2. Author updates `data/sources.json` and affected page(s).
3. Author runs regression tests in `tests/` or equivalent scripts.
4. Author reviews git diff for accidental changes.
5. Author commits with a clear message including the change class.
6. Author verifies the live site after deployment.

## Commit Message Format

```
[A/B/C/D] SHORT DESCRIPTION

- What: ...
- Why: ...
- Source: source_id (data/sources.json)
- Verified: YYYY-MM-DD
- Pages affected: ...
- Other pages audited: ...
```

Example:
```
[A] Update VA home-loan loss-mitigation URL

- What: Replaced broken avoid-foreclosure link with current trouble-making-payments URL
- Why: VA reorganized the housing assistance pages
- Source: va-home-loan-foreclosure
- Verified: 2026-08-11
- Pages affected: housing.html
- Other pages audited: employment-money.html, toolkit.html
```
