# State Legal Data Model

LEGAL HELP 4 VETS models state procedure as structured, auditable legal data rather than long narrative pages. The purpose is to make deadlines, triggering events, authority, exceptions, local variation, and verification status independently reviewable.

> **Unknown is not a legal conclusion.** A null or unverified field means the repository has not verified that proposition for publication. It does not mean there is no deadline, no remedy, or no requirement.

## Authority hierarchy

Use primary authority first: statutes, regulations, statewide court rules, binding case law when necessary, government forms, and official agency guidance/program material. Legal-aid organizations, bar programs, and provider directories belong in `resources`; they are not primary legal authority.

Each authority should identify its citation/title, authority type, jurisdiction, official HTTPS source, what it supports where useful, verification date, and status. `needs_refresh` means the authority has not been checked recently; `deprecated` means the repository affirmatively knows it should no longer support current public guidance.

## Status meanings

- `verified`: the published proposition was checked against current authority.
- `partially_verified`: the route is useful and sourced, but important subissues remain intentionally unpublished or qualified.
- `unverified`: do not publish a substantive deadline or legal conclusion from this route.
- `needs_refresh`: previously reviewed material has crossed the repository refresh interval or otherwise needs a new authority check.
- `deprecated`: known stale/replaced material retained only for migration/history where necessary.
- `pilot_partially_verified`: state-level status used while a pilot contains a mixture of route statuses.

State-level status never overrides route-level status.

## Route contract

A `document_routes` entry represents a paper, event, or procedural problem the user can identify. It may carry:

- `id`, `label`, `description`, `status`
- `jurisdiction` (or inherit the state jurisdiction)
- `court_or_forum` / legacy `court`
- authority references
- classified `required_actions` and `optional_actions`
- `required_filing` and `optional_filing`
- one `immediate_clock` and optional `other_clocks`
- remedies and possession consequences
- exceptions and local-variation metadata
- legal-help routing
- route verification date

Do not mark a route verified solely because some background information is known.

## Legal clock contract

A deadline is incomplete without its triggering event. A clock may contain:

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

The Texas pilot still contains compatible legacy names (`deadline_value`, `deadline_trigger`, `time_computation_authority`). New states should prefer the normalized names above.

`immediate_clock: null` means **deadline not yet verified**. The renderer or downstream consumer must never translate null into “no deadline.” Automatic date calculation should remain disabled until every relevant computation rule, holiday/weekend rule, service rule, extension rule, and exception can be represented safely.

## Required vs optional actions

Legal requirements must not be mixed with practical recommendations. New structured actions use a classification:

```json
{"type": "legal_requirement", "text": "File the required appeal instrument.", "authority": "authority-id"}
{"type": "practical_action", "text": "Keep a copy and proof of submission.", "authority": null}
```

A practical step does not become mandatory merely because the site recommends it.

## Federal overlays

Federal overlays are reusable and separate from state procedure. They must distinguish legal protections from assistance programs.

Examples of federal legal protections include SCRA eviction/foreclosure provisions, Fair Housing Act reasonable accommodation, and covered Regulation X mortgage-servicing procedures. Examples of assistance programs include HUD-VASH, SSVF, and LSV-H.

Never transform program availability into a legal defense or guaranteed service: HUD-VASH is not itself an eviction defense, SSVF is not a statutory entitlement to a particular payment, and LSV-H does not guarantee representation.

## Local variation

Statewide law is the baseline. A state or route can separately record whether approved local rules/standing orders may matter, an official locator, county, court, local authority, and last-check date. Unknown county or court remains null until identified.

Do not infer one county's Justice Court, sheriff, clerk, or local-form practice statewide.

## Resources

Provider resources are routing data, not legal authority. Useful fields include name, type, URL, coverage/service area, eligibility notes, verification flag/date, phone, and notes. Use statewide or official locators when service boundaries are not verified. Never fabricate ZIP-level coverage.

## Staleness

`scripts/validate_state_data.py` uses a 365-day review interval to **flag** authorities whose verification date is old. A staleness flag does not declare the law wrong. Reviewers should re-check the authority and either update `last_verified`, mark it `needs_refresh`, or mark it `deprecated` if it has actually been superseded.

## Adding a state

1. Begin from `data/states/_template.json`; never clone another state's legal content.
2. Identify document-first routes before researching prose.
3. Add primary authorities with provenance.
4. Populate only verified propositions and clocks.
5. Leave unknown deadlines/remedies null or routes unverified.
6. Keep federal overlays separate.
7. Add official local-rule/court locators where local variation exists.
8. Add provider routing only after service scope is verified or use a statewide locator.
9. Run `python scripts/validate_state_data.py` and `python -m unittest tests.test_state_schema` plus the full repository suite.
10. Public `verified` status is earned route by route.

## Updating existing law

Re-check the official source, update the verification date, preserve distinctions between legal requirements and practical advice, and update tests when doctrine changes. Never change a test merely to preserve old wording when controlling law changed.

## Deprecating stale authority

When an authority is affirmatively superseded, mark it `deprecated`, replace affected references with current authority, and add a regression test if the old rule could create a consequential deadline or eligibility error.
