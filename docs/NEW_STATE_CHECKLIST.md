# New State Checklist

A new state is an adversarial test of the architecture, not a clone of a previous state.

Before substantive work, confirm the contract branch/PR has merged and branch from current `main`.

## Research and encoding gate

Mark each item PASS or FAIL. Do not publish on an unresolved FAIL.

- [ ] **Primary authorities — PASS / FAIL:** Current primary authority identified for every consequential published proposition.
- [ ] **Applicability — PASS / FAIL:** Coverage, exclusions, conditions, and unknown facts are qualified separately from verification.
- [ ] **Procedural events — PASS / FAIL:** Distinct notices, filings, judgments, appeals, stays, writs, executions, terminations, and remedies are not collapsed.
- [ ] **Deadline triggers — PASS / FAIL:** Every numeric clock identifies the exact triggering event.
- [ ] **Computation — PASS / FAIL:** Unit/computation model is verified; calendar/business/court/judicial/service-dependent rules are not normalized incorrectly.
- [ ] **Clock authority — PASS / FAIL:** Every numeric clock resolves to verified legal authority.
- [ ] **Display text — PASS / FAIL:** High-consequence prose matches structured trigger, unit, exceptions, and coverage.
- [ ] **Authority references — PASS / FAIL:** No unknown, deprecated, resource-only, or wrong-jurisdiction authority supports a verified route.
- [ ] **Local law — PASS / FAIL:** Local substantive law, local procedure/forms, and unknown location are handled without guessing.
- [ ] **Federal overlays — PASS / FAIL:** State and federal rules remain separately sourced and overlays are not automatically rendered as defenses.
- [ ] **Provider routing — PASS / FAIL:** Official/statewide locators are verified and do not promise representation or eligibility.
- [ ] **Null safety — PASS / FAIL:** Null never renders as no deadline/no right/no requirement.
- [ ] **Cross-dataset validation — PASS / FAIL:** All declared route/dependency references resolve.
- [ ] **Dataset registration — PASS / FAIL:** Every production legal dataset is registered and has a discoverable semantic validator.
- [ ] **CI — PASS / FAIL:** Full legal-quality workflow passes on the exact reviewed head.

## Release rule

A green test suite is necessary, not sufficient. The legal release review must independently confirm that every published high-consequence proposition is supported and applicable as displayed.
