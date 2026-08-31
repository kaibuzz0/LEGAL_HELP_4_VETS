# State Legal Data Model

LEGAL HELP 4 VETS models state procedure as structured, auditable legal data rather than long narrative pages. The purpose is to make deadlines, triggering events, authority, exceptions, local variation, and verification status independently reviewable.

> **Unknown is not a legal conclusion.** A null or unverified field means the repository has not verified that proposition for publication. It does not mean there is no deadline, no remedy, no requirement, or no available protection.

## Schema versions

State files declare `schema_version`.

- `1.1` is the Texas-pilot compatibility contract already in production.
- `1.2` is the hardened additive contract for new states. It requires explicit supported propositions on authorities and removes new-state reliance on legacy exceptions.
- A future `1.x` change should be backward-compatible/additive.
- A future `2.0` change is reserved for a breaking structural change requiring migration.

The validator accepts supported historical versions deliberately; compatibility must not mean skipping cross-reference, deadline, URL, jurisdiction, or status validation. New states must use the newest supported version. Migration should occur in a focused PR with tests before an old version is retired.

## Authority hierarchy and provenance

Use primary authority first: statutes, regulations, statewide court rules, binding case law when necessary, government forms, and official agency guidance. Provider directories and assistance programs belong in resources or federal overlays; they cannot satisfy a state-law deadline's authority requirement.

Each 1.2 authority identifies its citation/title, authority type, jurisdiction, official HTTPS source, supported proposition(s), verification date, and status. `needs_refresh` means re-check required; `deprecated` means the repository affirmatively knows the authority should no longer support current public guidance. A verified route cannot rely only on a non-verified or deprecated authority.

## Status meanings

- `verified`: the published proposition was checked against current authority.
- `partially_verified`: useful and sourced, but important subissues remain qualified or unpublished.
- `unverified`: do not publish a substantive deadline or legal conclusion from this route.
- `needs_refresh`: previously reviewed material needs a new authority check.
- `deprecated`: known stale/replaced material retained only for migration/history where necessary.
- `pilot_partially_verified`: state-level pilot status containing mixed route statuses.

State-level status never overrides route-level status.

## Route contract

A `document_routes` entry represents a paper, event, or procedural problem. It may carry `id`, `label`, `description`, `status`, jurisdiction, court/forum, state authority references, federal-overlay references, classified actions, filings, clocks, remedies, possession consequences, exceptions, local variation, legal-help routing, and verification dates.

A verified route needs meaningful provenance. State-law authority references must resolve to legal authority with compatible jurisdiction. Federal overlays are separate references and are validated against the federal housing overlay registry.

## Legal clock contract

A numeric deadline is incomplete without all of these:

```json
{
  "value": 5,
  "unit": "days_under_rule_510_time_computation",
  "trigger": "judgment_signed",
  "computation_authority": "tx-trcp-510",
  "exceptions": [],
  "verified": true,
  "display": "Generally within 5 days after the judgment is signed."
}
```

The Texas 1.1 pilot contains compatible legacy names (`deadline_value`, `deadline_unit`, `deadline_trigger`, `time_computation_authority`). The semantic validator normalizes those names before applying the same deadline checks. New states use normalized names.

`immediate_clock: null` means **deadline not yet verified**. It must never render as “no deadline.” Numeric clocks require a trigger, a unit/computation description, an existing legal computation authority, explicit verification, and human-reviewed display text. Specialized units may represent court days, business days, statutory calendar-day computation, service extensions, or another authority-defined method without pretending those systems are interchangeable.

`display` is human-reviewed legal content. Automated semantic equivalence between arbitrary prose and structured triggers is not reliable enough to make a legal guarantee. Reviewers must reject display text that contradicts `value`, `unit`, `trigger`, or exceptions. Tests should cover known high-consequence formulations when a deterministic contradiction can be detected.

Automatic due-date calculation remains disabled until all relevant holiday/weekend, service, filing-cutoff, extension, and exception rules are safely represented.

## Action classification

Actions distinguish legal obligation from practical help. Supported classifications include `legal_requirement`, `procedural_requirement`, `practical_action`, `optional_strategy`, `referral`, `emergency_action`, plus legacy `optional_action` and `legal_help`. Legal/procedural requirements require a valid authority reference. Practical recommendations do not become statutory duties because the site recommends them.

## Federal overlays

Federal overlays are reusable and separate from state procedure. A route may reference overlay IDs from `data/housing-federal.json`.

The content and renderer must distinguish legal protection/procedure (for example SCRA, FHA, or Regulation X) from assistance programs (HUD-VASH, SSVF, LSV-H, VA loan assistance). A generic heading such as “your legal defenses” is unsafe for mixed overlays. Program availability is not a defense, entitlement, guaranteed payment, or guaranteed lawyer unless controlling authority actually creates that right.

## Local variation

Statewide law is the baseline. State/route metadata can record whether approved local rules or ordinances may matter, an official locator, county, court, local authority, and last-check date. Unknown county or court remains null. Local authority supplements or qualifies statewide provenance; it must not silently erase the statewide source.

## Resources

Provider resources are routing data, not legal authority. Useful fields include name, type, URL, coverage/service area, eligibility notes, verification flag/date, phone, and notes. Use official/statewide locators when service boundaries are not verified. Never fabricate ZIP-level coverage.

## Staleness

`scripts/validate_state_data.py` uses a 365-day review interval to **warn** about authorities whose verification date is old. A warning does not declare the law invalid. Reviewers re-check the source and update the date, mark `needs_refresh`, or mark `deprecated` only when supersession is actually known. Different refresh cadences may be added later for volatile forms/guidance if operational evidence justifies it.

Validator output distinguishes `PASS`, `WARNING`, and `ERROR`; semantic errors produce a non-zero exit status.

## Adding a state

1. Begin from `_template.json`; never clone another state's law.
2. Use the newest schema version.
3. Identify document-first routes before researching prose.
4. Add primary authorities with provenance and supported propositions.
5. Populate only verified propositions and clocks.
6. Leave unknown deadlines/remedies null or routes unverified.
7. Keep federal overlays separate.
8. Record local variation without inventing local rules.
9. Add provider routing only after scope is verified.
10. Run the semantic validator and full repository suite.
11. Public `verified` status is earned route by route.

## Updating and deprecating law

Re-check the official source, update verification dates, preserve requirement/advice distinctions, and update doctrine tests when law changes. Never weaken a test merely to preserve obsolete wording. When an authority is affirmatively superseded, mark it `deprecated`, replace affected verified references, and add a regression test if the old rule could cause a consequential deadline or eligibility error.
