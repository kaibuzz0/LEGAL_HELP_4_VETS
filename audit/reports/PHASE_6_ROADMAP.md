# PHASE 6 ROADMAP

Project: LEGAL HELP 4 VETS
Date: 2026-08-11
Status: Governance baseline established; content additions frozen pending approval

## Evaluation criteria

Rank future work by:
1. Urgency for a veteran in crisis
2. Number of users potentially affected
3. Legal risk of wrong/missing information
4. Availability of authoritative sources
5. Ease of implementation under change-control system
6. Usefulness during a crisis

## Top 5 proposed priorities (not yet approved for implementation)

### Priority 1 — Expand state/local emergency contacts
**Why:** A veteran facing eviction tonight needs a local number, not a federal 1-800 line.
**Affected users:** High — every veteran searching by state.
**Legal risk:** Medium if contacts are wrong.
**Sources:** State bar associations, court websites, VA medical centers, legal aid directories.
**Implementation:** Extend `data/state-resources.json` and `state-resources.html`; verify each URL.
**Crisis usefulness:** Very high.

### Priority 2 — VA overpayment / debt collection deep guide
**Why:** VA overpayment demands and debt collection are high-stress, deadline-driven, and commonly misunderstood.
**Affected users:** High — many veterans receive VA overpayment notices.
**Legal risk:** High if deadlines or appeal rights are wrong.
**Sources:** VA debt management center, 38 U.S.C. § 5302, VA Form 1100.
**Implementation:** New dedicated section or page; integrate with employment-money.html.
**Crisis usefulness:** High.

### Priority 3 — Eviction/foreclosure crisis companion page
**Why:** housing.html is strong, but a veteran in a parking lot may need a single, ultra-simple page.
**Affected users:** High during crisis.
**Legal risk:** High if legal deadlines are wrong.
**Sources:** State court eviction timelines, SCRA, VA SSVF, legal aid.
**Implementation:** One-page triage, possibly linked from help-now.html as the primary emergency path.
**Crisis usefulness:** Very high.

### Priority 4 — Disability claims denial-trap expansion
**Why:** claims.html already has traps; more veterans lose claims due to bad C&P exams and missing Intent to File than any other reason.
**Affected users:** Very high.
**Legal risk:** Medium-High.
**Sources:** VA.gov claims process, 38 C.F.R. Part 3, VA Form 21-0966, M21-1.
**Implementation:** Expand existing traps table; add sample nexus letter and disability diary.
**Crisis usefulness:** Medium (not immediate, but high impact over time).

### Priority 5 — Spanish-language core pages
**Why:** Many veterans and family members are more comfortable in Spanish; this expands reach without changing legal accuracy.
**Affected users:** High in Spanish-speaking communities.
**Legal risk:** Medium if translation drifts from source meaning.
**Sources:** Same as English pages; consider USCIS/SSA Spanish materials where available.
**Implementation:** Create `es/` directory with translated versions of help-now, claims, housing, widows.
**Crisis usefulness:** High for affected users.

## Lower-priority ideas (do not start without explicit approval)

- PDF/large-print versions of core guides
- Schema.org structured data
- Interactive state-resource map
- More Psalms/faith content
- Veteran heritage/warrior-history page (non-legal, separated)
- Chatbot-style guided interview (high risk if not carefully scoped)

## Approval gate

None of the above should be implemented until the maintainer explicitly approves the priority order.
