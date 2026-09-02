# Florida Phase 7C — Post-Sale Possession + Local Procedure Release Review

Date: 2026-09-02

Baseline: PR #24 merge `43a756d1da8c7df510d9074ed7f004488092422b`

Branch: `phase7-florida-postsale-local-precision`

## Scope

This review covers only the Florida subjects deliberately left incomplete after the Phase 7 precision merge: post-foreclosure possession, occupant classification, foreclosure writ/sheriff execution, appeal/stay separation, and a Hillsborough / Orange / Duval local-procedure pilot. It does not expand into HOA, condominium, tax-deed, probate, family, or criminal law.

## Statewide post-sale findings

- Title passage, possession entitlement, writ issuance, sheriff execution, and completed physical possession are distinct legal events.
- Current Fla. R. Civ. P. 1.570(b) identifies writ of possession as final process for recovery of real property.
- Current Fla. R. Civ. P. 1.580 requires a judgment/order for delivery of possession, clerk issuance of the writ, and sheriff execution; subdivision (b) preserves a third-party-occupant affidavit/court-determination process when applicable.
- Current Form 1.915 commands the sheriff to remove persons and put the named party in possession but does not publish a statewide foreclosure-specific waiting/posting countdown.
- Current Form 1.996(a) treats the certificate-of-title holder's possession as subject to qualifying bona fide-tenant rights. The actual signed judgment controls the case.
- Fla. Stat. § 83.62 is not used as a generic foreclosure-possession bridge. Its verified 24-hour rule remains in the Chapter 83 landlord-tenant eviction layer unless controlling authority independently makes it applicable to a particular track.
- No universal statewide foreclosure-specific 24-hour execution clock is published.
- Former owner, bona fide tenant, other tenant, and unknown occupant are separate classifications.
- Federal PTFA remains separately sourced and is not automatically assigned to a former mortgagor.
- Not qualifying for PTFA is not treated as proof that an occupant has no protection.
- Unknown occupant status remains identification-first and null-safe.
- Redemption expiration and sale-objection expiration are not possession deadlines.
- Filing an appeal does not itself create the ordinary foreclosure stay. Rule 9.310 stay analysis remains separate and case/order dependent.

## Current authority refresh

Final review identified a source-freshness issue: the branch originally cited the July 1, 2026 appellate-rules compilation for Fla. R. App. P. 9.310. The current Florida Rules of Appellate Procedure compilation is updated September 1, 2026. Rule 9.310(a)'s lower-tribunal stay framework remains substantively applicable. The authority record is now pinned to:

`https://www-media.floridabar.org/uploads/2026/09/Appellate-Court-Rules-09-01-26.pdf`

A regression test rejects reversion to the July source.

## Local pilot

Pilot counties: Hillsborough, Orange, Duval.

### Hillsborough

- Clerk foreclosure-sale / e-filing material remains local operational procedure.
- HCSO's Chapter 83 / § 83.62 writ guidance is treated as eviction-specific and is not used as a foreclosure clock.
- Thirteenth Circuit material establishes a local foreclosure motion/writ workflow without converting older form language into current statewide tenant law.

### Orange

- Orange Clerk and Ninth Circuit foreclosure/case-management sources remain local procedure.
- OCSO's published 24-hour writ discussion is embedded in eviction guidance and is not generalized to foreclosure possession.

### Duval

- Duval Clerk states that an occupied foreclosed property requires a writ rather than purchaser self-help after title.
- The Clerk's 24-hour foreclosure-writ statement is retained only as Duval informational/operational guidance with `legal_deadline: false`.
- Jacksonville Sheriff's Office processing/scheduling guidance remains operational and workload-dependent rather than a statewide legal deadline.
- Fourth Circuit foreclosure-division procedure remains local court workflow.

## Local architecture findings

- Local records live in registered `data/florida-local-procedure.json`; no schema bump was required.
- `default_county`, router `county`, `court`, and `sheriff` remain null until user/case selection.
- Every pilot source carries an explicit county, source type, official-source flag, non-statewide flag, verification date, and supported proposition.
- Clerk, sheriff, and informational pages are not represented as Florida substantive authority.
- Local operational timing requires explicit county scope and `legal_deadline: false`.
- Cross-layer routes resolve foreclosure route -> occupant classification -> housing/PTFA overlay where applicable -> local section -> provider routing.

## Validator / regression gate

Release validation must reject:

- § 83.62 imported as a generic foreclosure-possession bridge;
- certificate of title rendered as immediate physical eviction;
- former owner automatically assigned PTFA;
- unknown occupant assigned tenant rights before classification;
- local guidance marked statewide;
- nonofficial local sources marked verified;
- local operational timing without county scope or with `legal_deadline: true`;
- unresolved cross-layer route IDs or federal overlays;
- unregistered Florida local-procedure production data;
- stale July 2026 Rule 9.310 source provenance.

## Intentional limitations

- Statewide sheriff execution timing after a foreclosure writ remains null.
- County practice outside Hillsborough, Orange, and Duval remains unverified/null.
- Other-tenant rights remain dependent on lease, foreclosure-party status, judgment, priority/survival, and any housing-program overlay.
- Unknown occupants remain identification-first.
- No county operational timing is promoted to statewide law.

## Release decision

P0 defects identified in final substantive review: none after the Rule 9.310 source refresh.

P1 limitations: the intentionally null/partial areas above.

Merge recommendation depends on the full Legal Content Quality workflow passing on the exact final head after this review record is committed.
