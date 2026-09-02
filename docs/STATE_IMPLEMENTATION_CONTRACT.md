# State Implementation Contract v2

This contract governs every new state legal-data implementation after the Texas pilot and California release review.

## Core invariants

1. **Verification is not applicability.** Verification asks whether a proposition is supported by current authority. Applicability asks whether that proposition governs this person, property, loan, tenancy, document, procedural posture, or event. A renderer must never convert `verified` into “you have this right.”
2. **Null is a legal-safety state.** `null` never means none, no deadline, not required, or unavailable. It means the proposition is not established, not verified, fact-dependent, or cannot safely be expressed generically.
3. **Legal events remain distinct.** Notice, complaint, default, judgment, appeal, stay, writ, and physical execution are separate events. The same rule applies to NOD versus notice of sale, subsidy termination versus lease termination versus eviction, and benefit proposal versus final reduction.
4. **Every production legal dataset must receive semantic validation.** A JSON file outside the state directory cannot silently escape validation.
5. **A new state is an adversarial architecture test, not a clone of the previous state.** Do not copy another state and change statutes or numbers.

## Seven separate dimensions

Every route must keep these dimensions conceptually separate:

- legal verification
- applicability
- procedural timing
- local variation
- federal overlays
- resource routing
- publication status

## Applicability model

Schema 1.2 remains the current state schema. No schema bump is required merely to document the rule. Until a later schema change is justified, applicability is represented through route description, exceptions, authority-supported coverage statements, and null-safe clocks. Agents should reason in the following canonical states:

- `covered`
- `excluded`
- `conditional`
- `unknown`

If a route cannot establish coverage from known facts, it must not speak as if coverage is established. California §1946.2, SCRA, HBOR, PTFA, and similar regimes are canonical examples.

## Null contract

A null field must render as uncertainty or a prompt to identify the missing fact/authority. It must never render as “no deadline,” “no notice required,” “no remedy,” or an equivalent negative conclusion.

California examples intentionally held null include computation rules that could not safely be generalized across statutory subsections, generic foreclosure postponement timing, former-owner notice computation, and program-specific subsidized-housing deadlines.

## Legal clock contract v2

Every actionable numeric clock requires:

- value
- unit or rule-specific computation description
- triggering event
- computation authority
- applicability/coverage qualification where relevant
- exceptions where relevant
- explicit `verified: true`
- human-reviewed display text
- current authority verification provenance

A number without a trigger is not a legal deadline. Do not normalize calendar, business, court, judicial, service-dependent, mailing-extension, posting-plus-mailing, or event-specific clocks into one convenient unit.

Structured clock fields are machine-enforced. Display text remains human-reviewed legal content and must be checked against the trigger, unit, exceptions, and coverage. Add targeted regression tests for known dangerous contradictions.

## Authority contract v2

Substantive legal propositions should resolve to authority with:

- id
- citation/title
- authority type
- jurisdiction
- HTTPS official source
- supported proposition(s)
- status
- last verification date

Verified routes cannot rely solely on `needs_refresh`, `unverified`, `deprecated`, provider/resource, or program entries.

Preferred authority hierarchy is statute, regulation, binding case law, court rule, official agency guidance, government form, then government program, adjusted where jurisdiction-specific law requires. A government program is not legal authority establishing a deadline.

### Case law

Where case law is necessary, preserve the court, year, binding jurisdiction, exact proposition supported, and current status when useful. Never broaden a holding beyond the issue actually decided.

## Action classification

Use the existing action classes deliberately:

- `legal_requirement`
- `procedural_requirement`
- `practical_action`
- `optional_strategy`
- `emergency_action`
- `referral`

Legal and procedural requirements require legal authority. Practical advice does not become a legal right merely because it is useful. “File an Answer by the governing deadline” and “keep a stamped copy” are different classes of statement.

## Federal overlay contract

Keep federal law and programs separate from state law. Reusable layers include SCRA, FHA, Regulation X, PTFA, HUD-VASH, SSVF, LSV-H, project-based federal housing, public housing, HCV, and VA home-loan assistance.

Classify an overlay conceptually as a substantive protection, procedural protection, assistance program, referral program, or benefit/program eligibility layer. Do not render all overlays as legal defenses.

When state and federal law both apply, encode `STATE RULE + FEDERAL OVERLAY`; do not invent a hybrid deadline or hybrid right. California HBOR and Regulation X are the canonical example.

## Local-law contract

State baseline and local law are separate. Capture, when verified:

- local substantive law
- local court rule
- local standing order
- local form requirement
- local administrative procedure
- county/city/court
- official local source/locator
- local last-checked date and status

Unknown location stays null. Never guess an ordinance. The current 1.2 `local_variation` object is accepted as the compatibility representation; richer local-law typing should be added only when a future state proves the current structure inadequate.

## Cross-dataset contract

A state may have multiple subject datasets. Cross-layer route references must resolve. No dangling IDs are permitted. Examples include eviction ↔ foreclosure and future veterans-treatment-court ↔ criminal-diversion layers.

`data/datasets.json` is the canonical production dataset registry. CI must fail when a registered path is missing, its validator is missing, a production JSON under registered legal-data roots is unregistered, or declared cross-dataset dependencies do not resolve.

## Validator minimum standard

Where applicable, semantic validation must enforce:

- authority IDs resolve
- jurisdiction is correct
- official source is HTTPS
- verification date exists
- supported proposition exists
- route authority references resolve
- numeric clock integrity
- verified clocks use verified legal authority
- statuses are valid
- null safety
- federal/state separation
- resource/program versus legal-authority separation
- cross-dataset references resolve

## Publication model

Storage, verification, and publication are different states. Schema 1.2 does not yet add a `publication_status` field. Until an actual renderer requires it, publication is governed by the release gate rather than a speculative schema field.

A route may be public only when its displayed propositions are verified, applicability is qualified, every displayed actionable clock is verified, authority references resolve, high-risk display text has been reviewed, federal overlays are correctly classified, local limitations are disclosed, and nulls render safely. A partially verified route may publish only if the unverified portion is withheld and every displayed proposition is independently supported.

## State release gate

A state need not complete every legal topic. Its release-reviewed core must have:

- no P0 legal defect
- validated core emergency routes
- verified major published deadlines
- authority provenance
- local-variation architecture
- federal-overlay separation
- provider routing
- green CI

Incomplete areas remain explicitly partial, unverified, or null.

## Mandatory research sequence

1. Identify the document/problem.
2. Identify governing jurisdiction.
3. Find primary authority.
4. Determine coverage/applicability.
5. Determine procedural event.
6. Determine clock trigger.
7. Determine computation rule.
8. Determine remedy/consequence.
9. Determine local variation.
10. Determine federal overlay.
11. Determine legal-help routing.
12. Encode data.
13. Validate.
14. Perform adversarial release review.
15. Publish only what clears the gate.

## Lessons from California converted to invariants

- Multiple notice types → document types remain distinct when legal consequences differ.
- HBOR coverage → verification and applicability are separate.
- CCP §1161 subsection differences → never inherit computation rules merely because statutory provisions are adjacent.
- UD service methods → service-dependent clocks remain separate computation models.
- Appeal/stay → procedural remedies cannot be collapsed into one stage.
- Foreclosure occupant categories → do not guess occupant status.
- HBOR + Regulation X → state and federal regimes remain separately sourced.
- Local just-cause/court procedure → local substantive law and local procedure are not one generic variation string.
- California foreclosure dataset → every production legal dataset requires discoverable semantic validation.
- Human-readable deadlines → machine-valid structured data does not replace legal review of display text.

## Texas compatibility

Texas is a valid legacy schema 1.1 implementation and compatibility debt. New states must use the current contract and schema 1.2. Texas migration, if undertaken, belongs in a dedicated migration PR and does not block state #3.

## Schema version decision

**Remain on schema 1.2.** This contract does not yet require a structural data change. Do not create schema 1.3 for documentation alone. A later state may justify additive fields such as typed applicability, publication status, or richer local-law structures; that decision must be based on demonstrated data requirements.

## State #3 gate

Do not begin substantive state #3 work until this contract PR is green and merged. Candidate selection should consider veteran population, housing/legal demand, procedural distinctiveness, local-law complexity, foreclosure and eviction architecture, official-source quality, and whether the state meaningfully stress-tests the contract without becoming unmanageably broad.
