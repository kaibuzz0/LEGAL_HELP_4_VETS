# State Release Review

This is an adversarial legal-safety review. Answer every question before a state or subject layer is declared release-ready.

## Coverage and applicability

- Could a correctly verified law be shown as governing someone/property/event it does not cover?
- Are exemptions, thresholds, status conditions, service method, property type, loan type, occupant type, and procedural posture separated where they change the rule?
- Could an unknown fact be silently treated as satisfied?

## Null safety

- Could any `null` become “no deadline,” “no notice,” “no remedy,” or “not required”?
- Is an unresolved computation withheld rather than approximated?

## Procedural separation

- Could notice, complaint, default, judgment, appeal, stay, writ, and physical execution be collapsed?
- Could NOD and notice of sale be collapsed?
- Could subsidy termination, lease termination, and court eviction be collapsed?
- Could an appeal be mistaken for a stay?

## Authority integrity

- Does every verified route resolve to current legal authority or an intentionally classified federal overlay?
- Could a provider, government program, referral service, or form be mistaken for authority establishing a right/deadline?
- Is case law limited to the proposition actually decided?
- Does each numeric clock resolve to verified computation authority?

## Federal overlays

- Could an assistance program be presented as a legal defense or entitlement?
- Could state and federal rules be fused into an invented hybrid deadline?
- Are SCRA, FHA, Regulation X, PTFA, HUD-VASH, SSVF, LSV-H, public housing, HCV, project-based housing, and VA loan assistance classified according to what they actually do?

## Local variation

- Could stronger local substantive law be ignored?
- Could local court rules/forms/standing orders be mistaken for substantive state law?
- Is unknown location left unknown rather than guessed?

## Occupant and party classification

- Could an occupant category be guessed?
- Could former owner, bona fide tenant, subsidized tenant, borrower, servicer, landlord, successor owner, or other legally distinct party categories be conflated?

## Validation and publication

- Could a production legal dataset bypass semantic validation because it lives outside a conventional directory?
- Are cross-dataset references resolvable?
- Are high-risk display strings reviewed against structured data?
- Are partially verified routes withholding their unresolved propositions?
- Is CI green on the exact reviewed head?
- Are there any P0 legal defects? If yes, release fails.

## Decision

Record:

- P0 defects
- P1 risks/intentional limitations
- exact reviewed head SHA
- CI run/status
- release recommendation: PASS or FAIL
