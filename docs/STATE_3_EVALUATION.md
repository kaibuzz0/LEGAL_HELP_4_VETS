# State #3 Evaluation Gate

Date reviewed: 2026-09-02

Candidates: Florida, New York, Virginia.

This evaluation selects the next architecture stress test. It does **not** verify or publish substantive state-law routes.

## Criteria

- veteran population / likely veteran utility
- housing and foreclosure relevance
- procedural distinctiveness from California and Texas
- local-law complexity
- quality and accessibility of official primary sources
- ability to stress-test the contract without making the first replication attempt unmanageably broad

## Florida

**Architecture value: very high.** Florida uses judicial mortgage foreclosure. The 2026 Florida Statutes, Chapter 702, state that mortgages are foreclosed in equity and provide a court-centered foreclosure framework. That directly tests whether the architecture built around Texas/California can represent complaint → service/response → judgment → judicial sale → possession rather than another nonjudicial power-of-sale timeline.

Florida also has a separate current residential landlord-tenant statutory framework in Chapter 83, Part II. The official Legislature and Senate sites provide current searchable primary text.

Veteran utility is high: VA's FY2025 Annual Benefits Report estimates roughly 1.38 million veterans in Florida, making it the largest veteran population among these three candidates.

Official starting sources:

- https://www.leg.state.fl.us/STATUTES/index.cfm?App_mode=Display_Statute&URL=0700-0799%2F0702%2F0702.html
- https://www.flsenate.gov/Laws/Statutes/2026/Chapter83/All
- https://benefits.va.gov/REPORTS/abr/docs/2025-abr.pdf

**Risk:** Florida will force the system to model judicial foreclosure without reusing California's NOD/trustee-sale assumptions. That is desirable for state #3.

## New York

**Architecture value: extremely high, but first-replication scope risk is high.** New York foreclosure is court-driven and its housing law has substantial procedural and local complexity. New York Courts maintains detailed official foreclosure and eviction self-help material, and state statutes are available through NYSenate Open Legislation.

New York would strongly stress local-law and rent-regulation architecture, especially New York City distinctions. That makes it an excellent later adversarial state, but a risky first test of the replication contract because state/local/rent-regulated/subsidized layers could obscure whether failures arise from the contract itself or simply from the state's unusually broad housing complexity.

Official starting sources:

- https://www.nycourts.gov/help/homes-evictions/foreclosure-judgments
- https://www.nycourts.gov/help/homes-evictions/tenants-foreclosure-cases
- https://www.nysenate.gov/legislation/laws/RPA/768

**Risk:** local and rent-regulation complexity could make state #3 too broad before the reusable contract has been exercised once on a more bounded judicial-foreclosure state.

## Virginia

**Architecture value: moderate-high.** Virginia provides a strong contrast in the other direction: its Code expressly regulates trustee sales under deeds of trust, including pre-sale notice and trustee duties. This would test another nonjudicial system with different notice mechanics.

VA's FY2025 Annual Benefits Report estimates roughly 671,000 veterans in Virginia, so veteran utility is high. Official Code of Virginia sources are clear and current.

Official starting sources:

- https://law.lis.virginia.gov/vacodefull/title55.1/chapter3/article2/
- https://law.lis.virginia.gov/vacode/title55.1/chapter13/section55.1-321/
- https://benefits.va.gov/REPORTS/abr/docs/2025-abr.pdf

**Risk:** because California already exercised a complex nonjudicial foreclosure layer, Virginia adds less architectural contrast than Florida.

## Selection

**STATE #3: FLORIDA.**

Reasoning:

1. It provides the strongest procedural contrast: judicial foreclosure instead of California/Texas-style nonjudicial sale architecture.
2. It has very high direct veteran utility.
3. Current official statutes are accessible and structured enough for source-first implementation.
4. It has enough state/local complexity to test the contract, but is less likely than New York to turn the first replication into a local-law/rent-regulation project.
5. It tests whether the legal-event model can cleanly represent a court-driven foreclosure from complaint through judgment and sale.

## Gate

Do **not** create `phase7-florida-housing` until the replication-contract PR is green and merged into `main`. Florida must branch from that merged main commit, not from this architecture branch.
