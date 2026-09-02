# Phase 8A Income Protection Baseline Audit

Verified: 2026-09-02

Scope:
- `employment-money.html`
- `employment-rights.html`
- `va-debt.html`

This audit is the pre-change legal baseline for Phase 8A. Existing citations were not treated as proof by themselves; high-consequence propositions were rechecked against current primary/current official authority.

## Executive result

The Income Protection cluster is useful but not release-ready without correction.

### P0 / high-risk defects

1. **VA debt waiver deadline is stale/wrong in Money content.** Existing text says to request a waiver within 30 days. Current 38 U.S.C. § 5302 and 38 C.F.R. § 1.963 use a **one-year** ordinary waiver-request period for covered non-loan-guaranty benefit debt, subject to statutory/regulatory extension rules.
   - https://uscode.house.gov/view.xhtml?edition=prelim&num=0&req=granuleid%3AUSC-prelim-title38-section5302
   - https://www.ecfr.gov/current/title-38/chapter-I/part-1/subpart-B/section-1.963
   - Current VA guidance separately says disputing an overpayment within **30 days of the first debt letter** can prevent collection actions while VA decides the dispute. These are different rules and must not be merged.
   - https://www.va.gov/resources/options-to-request-help-with-va-debt/

2. **FDCPA validation language is universalized.** Existing content can be read as applying to every creditor/debt and as requiring every item listed in the sample letter. The statutory validation right is tied to a covered **debt collector** and the validation notice/30-day period. A timely written dispute triggers the statutory pause until verification; absent such a dispute, lawful collection activity may continue during the validation period.
   - 15 U.S.C. § 1692g: https://uscode.house.gov/view.xhtml?req=%28title%3A15+section%3A1692g%28b%29+edition%3Aprelim%29
   - CFPB debt collection guidance: https://www.consumerfinance.gov/consumer-tools/debt-collection/

3. **TDIU schedular thresholds are presented as though they are the whole framework.** Current 38 C.F.R. § 4.16(b) preserves extraschedular referral when service-connected disabilities prevent substantially gainful employment but the §4.16(a) percentages are not met.
   - https://www.ecfr.gov/current/title-38/chapter-I/part-4/subpart-A/section-4.16

4. **VA pension service rule is overgeneralized.** Existing “90 days with one wartime day” language is not universal for post-1980 entrants. Current VA guidance distinguishes pre-September 8, 1980 service from later minimum-active-duty rules and exceptions.
   - https://www.va.gov/pension/eligibility/
   - 38 U.S.C. § 1521: https://uscode.house.gov/view.xhtml?edition=2023&num=0&req=granuleid%3AUSC-2023-title38-section1521

5. **GI Bill/education debt uses an unsupported generic 30-day dispute/waiver instruction.** Student debt, school debt, certification disputes, waiver, and repayment must be separated. Do not publish a single education-debt deadline unless tied to the actual notice/process.
   - https://www.benefits.va.gov/gibill/resources/education_resources/debt_info.asp
   - https://www.va.gov/manage-va-debt/

6. **SCRA source registry contains an incorrect nonmortgage duration statement.** Current 50 U.S.C. § 3937 caps qualifying pre-service nonmortgage obligations during military service; qualifying mortgage-type obligations receive the additional one-year period. The existing source entry saying “service plus six months” for other obligations must be corrected.
   - https://uscode.house.gov/view.xhtml?edition=prelim&num=0&path=%2Fprelim%40title50%2Fchapter50&req=granuleid%3AUSC-prelim-title50-section3937

## Employment & Money audit

### SCRA
Status: verified but needs qualification.

Needed corrections:
- qualifying military service, not veteran status alone;
- debt generally must predate military service for §3937;
- written notice plus orders/other appropriate indicator no later than 180 days after termination/release from military service;
- excess interest is forgiven, not deferred;
- mortgages: service + one year; other covered obligations: service period;
- creditor may seek court relief if military service does not materially affect ability to pay above 6%;
- route housing-specific SCRA issues to Housing rather than duplicate state housing law.

### FDCPA
Status: dangerous/universalized.

Needed corrections:
- distinguish original creditor from covered debt collector;
- use receipt of the validation notice / notice's validation-period end date rather than “first contact” as a universal trigger;
- state what §1692g actually requires;
- sample request may ask for additional useful information but must not claim every requested document is legally required;
- timely written dispute affects collection until verification; it does not erase the debt or permanently stop collection.

### Pension
Status: verified but materially overgeneralized.

Needed corrections:
- pre-1980 90-day rule vs later minimum-active-duty framework;
- discharge, income/net worth, age/disability/nursing-home/SSDI/SSI conditions;
- VA Form 21P-527EZ;
- VA Form 21-2680 for Aid & Attendance/Housebound where applicable;
- no blanket promise that Aid & Attendance creates eligibility despite excessive income; increased pension rate can change the income calculation but eligibility remains fact-specific.

### TDIU
Status: incomplete.

Needed corrections:
- §4.16(a) schedular thresholds;
- §4.16(b) extraschedular referral;
- marginal employment and protected-environment concepts;
- VA Form 21-8940 and VA Form 21-4192;
- evidence of inability to secure/follow substantially gainful employment due to service-connected disability.

## USERRA audit

Status: strong foundation, needs precision hardening.

Needed corrections:
- maintain separate return/application categories: <31 days, 31–180 days, >180 days, fitness exams, service-related injury/illness;
- clarify that missing a return/application period does not automatically forfeit every USERRA right; employer rules for unexcused absence can apply;
- five-year cumulative limit has numerous statutory exceptions and must not be reduced to “five years”;
- escalator position is not a universal promise of the exact former job;
- distinguish seniority rights, non-seniority benefits, health coverage, pensions, training/requalification, and service-connected disability reemployment duties;
- discrimination and retaliation are separate from reemployment eligibility;
- private/state employer enforcement differs from federal executive agency enforcement;
- DOL-VETS complaint/referral, DOJ, OSC/MSPB, and private action routes must not be universalized;
- USERRA enforcement claims are not governed by a general federal statute-of-limitations period under 38 U.S.C. §4327(b), while reemployment eligibility still has reporting/application timing rules.

Primary/current anchors:
- 38 U.S.C. §§ 4311–4318, 4321–4327
- https://uscode.house.gov/view.xhtml?edition=prelim&path=%2Fprelim%40title38%2Fpart3%2Fchapter43
- https://www.dol.gov/agencies/vets/programs/userra/aboutuserra
- https://www.osc.gov/services/userra/enforcement/
- https://www.justice.gov/crt/laws-we-enforce

## VA Debt audit

Status: needs decision-tree rewrite.

The page must preserve four separate concepts:
1. debt validity/creation;
2. underlying VA benefit decision;
3. waiver;
4. repayment/compromise.

High-risk timing:
- ordinary covered benefit-overpayment waiver: one year from notice under current §5302 / §1.963, subject to exceptions;
- VA current guidance: dispute within 30 days of first overpayment debt letter can avoid collection actions while dispute is decided;
- underlying benefit decision review uses its own AMA deadline(s);
- health-care copay, home-loan, education, school-liability, and other debt processes can differ;
- do not turn the above into one universal “30 days” or “1 year.”

Collection:
- 38 C.F.R. §1.911 recognizes separate dispute, waiver, hearing, and underlying-decision appeal rights and states they may be exercised separately or simultaneously;
- Treasury referral/offset and VA benefit withholding are different mechanisms;
- not every collection mechanism automatically occurs in every case.

Financial status:
- VA Form 5655 is current for specified waiver, compromise, and longer repayment-plan requests.
- https://www.va.gov/forms/5655/
- https://www.va.gov/resources/submitting-a-financial-status-report-va-form-5655/

## Publication rule for Phase 8A

No actionable deadline remains on these pages unless the trigger, applicability, authority, and display language have been manually reviewed. Practical evidence/document advice remains labeled as practical rather than legally mandatory.
