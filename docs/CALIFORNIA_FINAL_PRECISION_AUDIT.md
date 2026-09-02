# California Final Legal-Precision Audit

Baseline: PR #19 merge `b80b6ee3aa41f7a607d94ba071c5bfe00daeeeb0`

Verification date: 2026-09-02

This document records legal-release findings for the final California housing pass. Merge status is not legal authority. Unknown or incompletely reconciled deadlines stay null.

## 1. Civil Code § 2924g — trustee-sale postponement

Current operative text was reviewed against the current California-code version. The earlier 10-business-day / 5-business-day written-notice concept must not be restored as the general postponement rule.

Verified propositions:

- A sale ordinarily commences at the time and location stated in the notice of sale.
- A postponement is generally announced at the time and location appointed for sale.
- Section 2924g(c) permits postponement before completion of sale for specified grounds, including court order, operation-of-law stay, mutual agreement, trustee discretion, and qualifying force majeure.
- The ordinary postponement regime permits postponements totaling no more than 365 days from the date stated in the notice of sale; further scheduling after that threshold requires a new notice of sale under § 2924f.
- Section 2924g(d) uses public declaration for notice of postponement and requires the declaration to identify the new date, time, and place; the statute states that no other postponement notice is ordinarily required under that subdivision.
- A separate seven-day timing rule applies after dismissal or expiration/termination of specified injunctions, restraining orders, or stays, subject to the statute's exceptions.
- Bankruptcy stays are treated separately under subdivision (e).

Release result: keep the actionable postponement clock null unless a narrower event-specific clock is modeled with its own trigger and current subsection authority.

## 2. Civil Code § 2923.6 — complete application and denial/appeal

Verified propositions:

- Section 2923.6(c) applies to a complete first-lien loan-modification application submitted at least five business days before a scheduled foreclosure sale, subject to statutory coverage and entity exceptions.
- While a qualifying application is pending, covered actors may be restricted from recording a notice of default or notice of sale or conducting a trustee sale.
- Section 2923.6(d) provides at least 30 days from the date of the written denial to appeal and provide evidence that the determination was in error.
- Section 2923.6(e) separately controls when foreclosure activity may resume after denial or appeal.
- Section 2923.6(i) excludes entities described in § 2924.18(b), and § 2923.6(j) limits the section to mortgages/deeds of trust described in § 2924.15.

Release result: the 30-day value is not a generic HBOR deadline. Coverage and the written-denial trigger must travel with the clock.

## 3. Civil Code § 2924.12 — HBOR remedies

Current remedy structure was reviewed.

Verified propositions:

- Before a trustee's deed upon sale has been recorded, a borrower may seek injunctive relief for a material violation of the listed HBOR sections.
- The injunction remains until the court determines that the covered violation has been corrected and remedied; an enjoined entity may seek dissolution after correction.
- After a trustee's deed upon sale has been recorded, the statute provides actual-economic-damages relief for an uncorrected material violation of the listed sections.
- If the material violation was intentional or reckless or resulted from willful misconduct, the statute authorizes enhanced damages under the statutory standard.
- A violation corrected and remedied before recordation of the trustee's deed does not create liability under the section.
- The statute expressly states that a violation of the article does not affect the validity of a sale in favor of a bona fide purchaser for value without notice.
- A prevailing borrower may receive reasonable attorney fees and costs under the statutory standard.
- The section does not apply to entities described in § 2924.18(b).

Release wording rule: do not publish `HBOR violation = foreclosure void`. Use qualified language such as `may support specified statutory relief if coverage, material-violation, timing, and remedy requirements are met`.

## 4. CCP § 1161(4) — noncurable breach / nuisance notice

The current operative statute expressly adds the Saturday/Sunday/judicial-holiday exclusion to § 1161(2) pay-rent notices and § 1161(3) curable covenant notices. Section 1161(4), covering specified assignment/subletting, waste, nuisance, and unlawful-use grounds, states that the landlord is entitled to restitution upon service of three days' notice to quit but does not repeat those exclusions.

Release result: do not inherit the curable-notice computation by analogy. Until the complete computation rule, including service and any generally applicable deadline-extension provisions, is separately verified, the state-data route should remain partially verified and its actionable immediate clock should be null.

## 5. Civil Code § 1946.2 — Tenant Protection Act

Current text confirms that verification and applicability must remain separate.

Release-review anchors:

- Just-cause protection depends on the statutory occupancy thresholds, including the rules for later-added adult tenants.
- At-fault grounds are enumerated and include separate rent, material-breach, nuisance/waste, unlawful-use, refusal-to-renew, criminal-activity, assignment/subletting, access, employee/agent/licensee, and surrender-related concepts subject to the statute.
- No-fault grounds include qualifying owner/family occupancy, withdrawal from the rental market, specified government/court/local orders, and qualifying demolition/substantial-remodel situations.
- Owner-move-in rules contain relationship, primary-residence, minimum-occupancy, and lease-language/timing conditions.
- Statutory exemptions are category-specific. `Single-family home` is not by itself a complete exemption statement; ownership and required notice conditions matter.
- No-fault relocation obligations and the direct-payment alternative are conditional, and local law may provide greater protections.
- Qualifying more-protective local just-cause ordinances remain relevant.

Release wording rule: never reduce the statute to `one year = just cause` or `all California rentals are covered`.

## 6. Cross-layer rules

- California HBOR and federal Regulation X remain separate authorities even where the same borrower facts implicate both.
- Former owner, bona fide tenant, other tenant, and unknown occupant are distinct post-sale classifications.
- Federal PTFA rights apply only if the tenancy satisfies the federal bona-fide-tenancy conditions; do not publish `all tenants get 90 days`.
- VA guaranty does not mean VA owns or services the loan.
- HOA and tax foreclosure clocks remain null until independently verified.

## 7. Validator release gate

The dedicated California foreclosure validator must reject at minimum:

- unknown authority references;
- wrong jurisdiction for a verified California route;
- HTTP/non-HTTPS legal sources;
- missing verification dates;
- missing supported propositions;
- numeric clocks without a trigger, authority, explicit verification, or display text;
- numeric clocks using nonverified authority;
- null clocks described as `no deadline`.

A partially verified route may contain a verified proposition and a verified event-specific clock, but unknown clocks remain null. Partial status is not permission to publish guessed numbers.

## Remaining P1 before merge

1. Patch `data/states/california.json` so the §1161(4) route no longer publishes a borrowed/underspecified actionable clock.
2. Complete the line-by-line §1946.2 public-prose audit against the current 2026 text.
3. Add HBOR §2924.12 remedy data with the applicability/correction/material-violation limits above.
4. Complete statewide provider routing and veteran-specific routing from verified official locators.
5. Add project-based Section 8 as a distinct federal overlay with deadlines null until verified.
6. Validate cross-dataset route references between eviction and foreclosure data.

No expansion to another state until these P1 items are resolved or explicitly quarantined.