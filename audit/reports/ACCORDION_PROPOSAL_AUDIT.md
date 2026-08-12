# ACCORDION PROPOSAL AUDIT

Date: 2026-08-11T20:45:47.482064
Current HEAD: 17ec7b1ef1a (emergency recovery state)
Last known good: 62d5c65574b2

## Current State

All 19 content pages are live. The emergency recovery forced every `details.content-tile` open, so content is visible but the accordion markup remains. The repository and live site match exactly. No files were modified during this audit.

## Previous Failure Analysis

The explicit `<details class="content-tile">` conversion in commit `3247d221cf76` collapsed too much content by default. Sections that should have remained immediately visible — including entire page bodies such as `CLAIMS BATTLE ROOM`, `APPEALS NAVIGATION`, `EMPLOYMENT AND MONEY`, `SUBSTANCE USE AND RECOVERY`, `WIDOWS AND SURVIVING SPOUSES`, and the state directory — were wrapped into collapsed `<details>` elements. The result was that users landed on pages and saw only headings or summaries, with the actual legal guidance hidden inside dropdowns.

Content was not deleted; it was merely hidden. The emergency recovery forced every `details.content-tile` open by adding the `open` attribute, restoring visibility. This audit now reclassifies each section so that only genuinely secondary or advanced content is collapsed, while P0 and P1 information remains visible.

Key mistakes to avoid in the next implementation:
1. Do not collapse the page purpose, primary action, deadlines, or orientation sections.
2. Do not collapse entire dense pages in a single wrapper.
3. Do not use JavaScript to decide the hierarchy; encode the hierarchy in HTML.
4. Preserve existing IDs and anchors.
5. Use only one level of disclosure; no nested accordions.


## Proposal Table

| Page | Section | Priority | Proposed State | Reason |
| ---- | ------- | -------- | -------------- | ------ |
| index.html | Hero / What do you need help with? | P0 | ALWAYS VISIBLE | Primary decision screen; user must immediately see major paths |
| index.html | Crisis / Help Now card | P0 | ALWAYS VISIBLE | Emergency access must not be hidden |
| index.html | Primary 8 task cards (Claims, Appeals, Housing, USERRA, VA Debt, Discharge, Family, Toolkit) | P0 | ALWAYS VISIBLE | Core navigation; hiding would defeat homepage purpose |
| index.html | More Resources expandable section | P2 | COLLAPSED by default | Secondary pages (library, state resources, faith, sources, about) can be grouped and collapsed |
| index.html | What this site is / disclaimer | P1 | VISIBLE initially | Important but not urgent; could be P2 if homepage gets too long |
| claims.html | H1 + short page purpose | P0 | ALWAYS VISIBLE | Orientation |
| claims.html | Do This First / Action Ladder | P0 | ALWAYS VISIBLE | Primary action |
| claims.html | Top 5 Claim Denial Traps | P1 | VISIBLE | Common pitfalls; helps user understand |
| claims.html | When They Say No or Stall | P1 | VISIBLE | Common next-step scenario |
| claims.html | CLAIMS BATTLE ROOM / detailed procedures (Nexus Letter) | P2 | COLLAPSED | Detailed step-by-step content; secondary to initial orientation |
| appeals.html | H1 + short page purpose | P0 | ALWAYS VISIBLE | Orientation |
| appeals.html | Do This First / Appeal options overview | P0 | ALWAYS VISIBLE | Primary choices |
| appeals.html | Deadline Warning | P0 | ALWAYS VISIBLE | Urgent |
| appeals.html | APPEALS NAVIGATION / C-File + paths | P2 | COLLAPSED | Detailed navigation of appeal types; useful after user chooses a path |
| housing.html | H1 + short page purpose | P0 | ALWAYS VISIBLE | Orientation |
| housing.html | Stop Eviction / Action Ladder | P0 | ALWAYS VISIBLE | Primary emergency action |
| housing.html | Servicemembers Civil Relief Act intro | P1 | VISIBLE | Relevant protection overview |
| housing.html | Housing Safety | P1 | VISIBLE | Practical immediate guidance |
| housing.html | Action Ladder: 24/72/30 Days | P1 | VISIBLE | Primary timeline |
| housing.html | When They Say No or Stall | P2 | COLLAPSED | Secondary troubleshooting |
| housing.html | Reasonable Accommodation | P2 | COLLAPSED | Specific scenario |
| housing.html | VA-Backed Home Loan trouble | P2 | COLLAPSED | Specific scenario |
| employment-money.html | H1 + short page purpose | P0 | ALWAYS VISIBLE | Orientation |
| employment-money.html | Do This First | P0 | ALWAYS VISIBLE | Primary action |
| employment-money.html | Military Service Affecting Your Job? | P1 | VISIBLE | Quick routing to USERRA |
| employment-money.html | VA Says You Owe Money? | P1 | VISIBLE | Quick routing to VA Debt |
| employment-money.html | EMPLOYMENT AND MONEY detailed content (Unemployment UCX) | P2 | COLLAPSED | Detailed content already covered by dedicated pages |
| employment-rights.html | H1 + short page purpose | P0 | ALWAYS VISIBLE | Orientation |
| employment-rights.html | Do This First | P0 | ALWAYS VISIBLE | Primary action |
| employment-rights.html | What Is USERRA? | P1 | VISIBLE | Core definition |
| employment-rights.html | Who USERRA May Protect | P1 | VISIBLE | Eligibility is primary |
| employment-rights.html | What Kind of Problem Do I Have? | P1 | VISIBLE | Routing to next step |
| employment-rights.html | Important Return-to-Work Deadlines | P0 | ALWAYS VISIBLE | Critical deadline; must not be hidden |
| employment-rights.html | Notice to Your Employer | P2 | COLLAPSED | Detailed procedural guidance |
| employment-rights.html | Reemployment Rights in Plain Language | P2 | COLLAPSED | Detailed explanation |
| employment-rights.html | Anti-Discrimination and Retaliation | P2 | COLLAPSED | Detailed explanation |
| employment-rights.html | Health Insurance, Pension, and Other Benefits | P2 | COLLAPSED | Detailed benefits explanation |
| employment-rights.html | Employer Defenses / Exceptions | P3 | COLLAPSED | Advanced legal nuance |
| employment-rights.html | The Five-Year Service Limit | P1 | VISIBLE | Important eligibility cap |
| employment-rights.html | Where to Get Help: DOL VETS, ESGR, and DOJ | P1 | VISIBLE | Primary contacts |
| employment-rights.html | "Do Not Confuse These" | P2 | COLLAPSED | Comparative reference |
| employment-rights.html | Action Ladder: From Problem to Help | P0 | ALWAYS VISIBLE | Primary action path |
| employment-rights.html | Sample Letters | P2 | COLLAPSED | Templates; useful after user understands problem |
| employment-rights.html | Documents to Save | P2 | COLLAPSED | Reference checklist |
| employment-rights.html | Common Terms | P3 | COLLAPSED | Glossary |
| va-debt.html | H1 + short page purpose | P0 | ALWAYS VISIBLE | Orientation |
| va-debt.html | Deadline Warning | P0 | ALWAYS VISIBLE | Urgent |
| va-debt.html | Do This First: 5 Steps | P0 | ALWAYS VISIBLE | Primary action |
| va-debt.html | What Kind of VA Debt Is This? | P1 | VISIBLE | Routing |
| va-debt.html | "I Think the Debt Is Wrong" | P1 | VISIBLE | Primary path branch |
| va-debt.html | "I Owe It, But I Cannot Afford It" | P1 | VISIBLE | Primary path branch |
| va-debt.html | "I Disagree With the Underlying VA Decision" | P1 | VISIBLE | Primary path branch |
| va-debt.html | If VA Is Already Collecting | P1 | VISIBLE | Common urgent scenario |
| va-debt.html | "Do Not Confuse These" | P2 | COLLAPSED | Reference distinction |
| va-debt.html | Action Ladder: From Notice to Escalation | P0 | ALWAYS VISIBLE | Primary action path |
| va-debt.html | Sample Letters | P2 | COLLAPSED | Templates |
| va-debt.html | Documents to Save | P2 | COLLAPSED | Reference checklist |
| va-debt.html | Common Terms | P3 | COLLAPSED | Glossary |
| va-debt.html | Where to Get Help | P1 | VISIBLE | Primary contacts |
| toolkit.html | H1 + short page purpose | P0 | ALWAYS VISIBLE | Orientation |
| toolkit.html | Step-by-Step: How to Organize a Veteran Case from Day One | P1 | VISIBLE | Core purpose of page |
| toolkit.html | USERRA Toolkit card | P1 | VISIBLE | Quick access |
| toolkit.html | VA Debt Response Toolkit card | P1 | VISIBLE | Quick access |
| toolkit.html | Common Myths That Stop Veterans from Acting | P1 | VISIBLE | Important motivator |
| toolkit.html | ADVOCATE TOOLKIT / Full Document Checklist | P2 | COLLAPSED | Extensive reference checklist |
| discharge-upgrade.html | H1 + short page purpose | P0 | ALWAYS VISIBLE | Orientation |
| discharge-upgrade.html | Do This First | P0 | ALWAYS VISIBLE | Primary action |
| discharge-upgrade.html | Who Can Apply / Eligibility | P1 | VISIBLE | Primary gating info |
| discharge-upgrade.html | DISCHARGE UPGRADES AND RECORD CORRECTIONS / Step-by-Step Application | P2 | COLLAPSED | Detailed procedure; useful after orientation |
| family-immigration.html | H1 + short page purpose | P0 | ALWAYS VISIBLE | Orientation |
| family-immigration.html | Do This First | P0 | ALWAYS VISIBLE | Primary action |
| family-immigration.html | Eligibility / Who Qualifies | P1 | VISIBLE | Primary gating info |
| family-immigration.html | FOREIGN CITIZENSHIP & MILITARY IMMIGRATION detailed sections | P2 | COLLAPSED | Detailed immigration paths (INA 328/329, parole, family petitions) |
| legal-library.html | H1 + short page purpose | P0 | ALWAYS VISIBLE | Orientation |
| legal-library.html | LEGAL LANGUAGE TRANSLATOR | P1 | VISIBLE | Core tool of page |
| legal-library.html | LEGAL REFERENCE LIBRARY / Sample Legal Demand Letters | P2 | COLLAPSED | Templates and reference; secondary to translator |
| substance-use.html | H1 + short page purpose | P0 | ALWAYS VISIBLE | Orientation |
| substance-use.html | Do This First / Crisis resources | P0 | ALWAYS VISIBLE | Urgent/safety |
| substance-use.html | How to Request Community Care Under the MISSION Act | P2 | COLLAPSED | Specific detailed procedure |
| widows.html | H1 + short page purpose | P0 | ALWAYS VISIBLE | Orientation |
| widows.html | Do This First | P0 | ALWAYS VISIBLE | Primary action |
| widows.html | DIC / Survivor Benefits overview | P1 | VISIBLE | Primary benefit info |
| widows.html | CHAMPVA and detailed survivor sections | P2 | COLLAPSED | Detailed benefit explanations |
| state-resources.html | H1 + short page purpose | P0 | ALWAYS VISIBLE | Orientation |
| state-resources.html | Local Emergency Contacts to Find Tonight | P0 | ALWAYS VISIBLE | Urgent |
| state-resources.html | What This Is and Who Qualifies | P1 | VISIBLE | Explanation |
| state-resources.html | National Contacts to Use With This Directory | P1 | VISIBLE | Primary contacts |
| state-resources.html | How to Use This Directory | P1 | VISIBLE | Instructions |
| state-resources.html | Document Checklist for State Benefits | P2 | COLLAPSED | Reference |
| state-resources.html | State-specific entries (54 states/territories) | P3 | COLLAPSED by default | Reference directory; user can expand their state |

## P0 Sections (MUST ALWAYS BE VISIBLE)
- index.html — Hero / What do you need help with?
- index.html — Crisis / Help Now card
- index.html — Primary 8 task cards (Claims, Appeals, Housing, USERRA, VA Debt, Discharge, Family, Toolkit)
- claims.html — H1 + short page purpose
- claims.html — Do This First / Action Ladder
- appeals.html — H1 + short page purpose
- appeals.html — Do This First / Appeal options overview
- appeals.html — Deadline Warning
- housing.html — H1 + short page purpose
- housing.html — Stop Eviction / Action Ladder
- employment-money.html — H1 + short page purpose
- employment-money.html — Do This First
- employment-rights.html — H1 + short page purpose
- employment-rights.html — Do This First
- employment-rights.html — Important Return-to-Work Deadlines
- employment-rights.html — Action Ladder: From Problem to Help
- va-debt.html — H1 + short page purpose
- va-debt.html — Deadline Warning
- va-debt.html — Do This First: 5 Steps
- va-debt.html — Action Ladder: From Notice to Escalation
- toolkit.html — H1 + short page purpose
- discharge-upgrade.html — H1 + short page purpose
- discharge-upgrade.html — Do This First
- family-immigration.html — H1 + short page purpose
- family-immigration.html — Do This First
- legal-library.html — H1 + short page purpose
- substance-use.html — H1 + short page purpose
- substance-use.html — Do This First / Crisis resources
- widows.html — H1 + short page purpose
- widows.html — Do This First
- state-resources.html — H1 + short page purpose
- state-resources.html — Local Emergency Contacts to Find Tonight

## P1 Sections (SHOULD BE VISIBLE INITIALLY)
- index.html — What this site is / disclaimer
- claims.html — Top 5 Claim Denial Traps
- claims.html — When They Say No or Stall
- housing.html — Servicemembers Civil Relief Act intro
- housing.html — Housing Safety
- housing.html — Action Ladder: 24/72/30 Days
- employment-money.html — Military Service Affecting Your Job?
- employment-money.html — VA Says You Owe Money?
- employment-rights.html — What Is USERRA?
- employment-rights.html — Who USERRA May Protect
- employment-rights.html — What Kind of Problem Do I Have?
- employment-rights.html — The Five-Year Service Limit
- employment-rights.html — Where to Get Help: DOL VETS, ESGR, and DOJ
- va-debt.html — What Kind of VA Debt Is This?
- va-debt.html — "I Think the Debt Is Wrong"
- va-debt.html — "I Owe It, But I Cannot Afford It"
- va-debt.html — "I Disagree With the Underlying VA Decision"
- va-debt.html — If VA Is Already Collecting
- va-debt.html — Where to Get Help
- toolkit.html — Step-by-Step: How to Organize a Veteran Case from Day One
- toolkit.html — USERRA Toolkit card
- toolkit.html — VA Debt Response Toolkit card
- toolkit.html — Common Myths That Stop Veterans from Acting
- discharge-upgrade.html — Who Can Apply / Eligibility
- family-immigration.html — Eligibility / Who Qualifies
- legal-library.html — LEGAL LANGUAGE TRANSLATOR
- widows.html — DIC / Survivor Benefits overview
- state-resources.html — What This Is and Who Qualifies
- state-resources.html — National Contacts to Use With This Directory
- state-resources.html — How to Use This Directory

## P2 Candidates (GOOD TO COLLAPSE)
- index.html — More Resources expandable section
- claims.html — CLAIMS BATTLE ROOM / detailed procedures (Nexus Letter)
- appeals.html — APPEALS NAVIGATION / C-File + paths
- housing.html — When They Say No or Stall
- housing.html — Reasonable Accommodation
- housing.html — VA-Backed Home Loan trouble
- employment-money.html — EMPLOYMENT AND MONEY detailed content (Unemployment UCX)
- employment-rights.html — Notice to Your Employer
- employment-rights.html — Reemployment Rights in Plain Language
- employment-rights.html — Anti-Discrimination and Retaliation
- employment-rights.html — Health Insurance, Pension, and Other Benefits
- employment-rights.html — "Do Not Confuse These"
- employment-rights.html — Sample Letters
- employment-rights.html — Documents to Save
- va-debt.html — "Do Not Confuse These"
- va-debt.html — Sample Letters
- va-debt.html — Documents to Save
- toolkit.html — ADVOCATE TOOLKIT / Full Document Checklist
- discharge-upgrade.html — DISCHARGE UPGRADES AND RECORD CORRECTIONS / Step-by-Step Application
- family-immigration.html — FOREIGN CITIZENSHIP & MILITARY IMMIGRATION detailed sections
- legal-library.html — LEGAL REFERENCE LIBRARY / Sample Legal Demand Letters
- substance-use.html — How to Request Community Care Under the MISSION Act
- widows.html — CHAMPVA and detailed survivor sections
- state-resources.html — Document Checklist for State Benefits

## P3 Candidates (ADVANCED / REFERENCE)
- employment-rights.html — Employer Defenses / Exceptions
- employment-rights.html — Common Terms
- va-debt.html — Common Terms
- state-resources.html — State-specific entries (54 states/territories)

## Sections That MUST NOT Be Collapsed
- index.html — Hero / What do you need help with?
- index.html — Crisis / Help Now card
- index.html — Primary 8 task cards (Claims, Appeals, Housing, USERRA, VA Debt, Discharge, Family, Toolkit)
- claims.html — H1 + short page purpose
- claims.html — Do This First / Action Ladder
- appeals.html — H1 + short page purpose
- appeals.html — Do This First / Appeal options overview
- appeals.html — Deadline Warning
- housing.html — H1 + short page purpose
- housing.html — Stop Eviction / Action Ladder
- employment-money.html — H1 + short page purpose
- employment-money.html — Do This First
- employment-rights.html — H1 + short page purpose
- employment-rights.html — Do This First
- employment-rights.html — Important Return-to-Work Deadlines
- employment-rights.html — Action Ladder: From Problem to Help
- va-debt.html — H1 + short page purpose
- va-debt.html — Deadline Warning
- va-debt.html — Do This First: 5 Steps
- va-debt.html — Action Ladder: From Notice to Escalation
- toolkit.html — H1 + short page purpose
- discharge-upgrade.html — H1 + short page purpose
- discharge-upgrade.html — Do This First
- family-immigration.html — H1 + short page purpose
- family-immigration.html — Do This First
- legal-library.html — H1 + short page purpose
- substance-use.html — H1 + short page purpose
- substance-use.html — Do This First / Crisis resources
- widows.html — H1 + short page purpose
- widows.html — Do This First
- state-resources.html — H1 + short page purpose
- state-resources.html — Local Emergency Contacts to Find Tonight

## Unchanged Pages (No Accordions Currently)
- help-now.html
- about.html
- sources.html
- faith-encouragement.html
- 404.html

## Mobile Concerns
- State resources directory contains 54 entries; collapsing them is essential to avoid a 3000+ word vertical scroll on phones.
- Toolkit full checklist is dense; collapse keeps the page focused.
- Housing, claims, and appeals pages have large action ladders that must remain visible for emergency users.

## Navigation Concerns
- Global header exposes USERRA and VA Debt directly; good.
- Homepage More Resources section should remain collapsed so primary 8 tasks dominate.

## Search Concerns
- Search index is section-level and sort bug is fixed. No search changes proposed in this pass.
- Search destination quality: PASS — results link to `page.html#sectionId`.

## Recommended Implementation Order
1. Revert the emergency `open` attribute on sections classified as P2/P3 in this audit.
2. Leave P0 and P1 sections visible (remove any surrounding `<details>` or keep them as visible containers).
3. Ensure P2/P3 `<details>` have no `open` attribute.
4. Preserve all IDs, links, and wording.
5. Verify repository and live site match after deployment.

---

## NO FILES MODIFIED
## NO COMMIT CREATED
## NO DEPLOYMENT PERFORMED

AWAITING MAINTAINER APPROVAL