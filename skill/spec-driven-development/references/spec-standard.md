# Specification Standard

## Contents

1. Artifact model
2. Requirement grammar
3. Profile gates
4. Readiness semantics
5. Traceability
6. Anti-patterns

## Artifact model

Use one Markdown file per independently deliverable change. Keep frontmatter scalar and machine-readable:

```yaml
---
spec: SPEC-0001
title: Stable route transitions
status: draft
profile: standard
mode: deliver
owner: team-or-person
created: 2026-07-29
updated: 2026-07-29
---
```

Valid statuses: `draft`, `ready`, `implemented`, `verified`, `superseded`.

Valid profiles: `light`, `standard`, `critical`.

Valid modes: `specify`, `deliver`, `audit`.

Use these section names exactly so deterministic validation remains possible:

- Context and Evidence
- Problem
- Outcomes
- Non-goals
- Users and Scenarios
- Current Behavior
- Proposed Behavior
- Requirements
- Acceptance Criteria
- Product and Design
- Security and Privacy
- Data and Interfaces
- Failure Modes and Recovery
- Observability
- Rollout and Rollback
- Verification and Traceability
- Decisions
- Open Questions

The canonical template contains every section. A lower-risk profile may use `N/A — <specific reason>` in non-required sections.

## Requirement grammar

Assign stable identifiers. Do not renumber existing IDs after review.

```text
- REQ-001 | must | When a route load exceeds 120 ms, the system shall show a progress indicator without changing content geometry.
- REQ-002 | must-not | The system shall not expose draft posts to unauthenticated requests.
- REQ-003 | should | While offline, the editor should retain the last locally saved draft.
```

Use EARS-style clauses when they fit:

- ubiquitous: `The system shall <response>.`
- event-driven: `When <trigger>, the system shall <response>.`
- state-driven: `While <state>, the system shall <response>.`
- unwanted behavior: `If <fault or abuse>, the system shall <response>.`
- optional feature: `Where <capability is enabled>, the system shall <response>.`

Normative levels:

- `must` and `must-not`: release gate;
- `should`: expected unless a `DEC-*` explains why not;
- `may`: explicitly optional and excluded from release gating.

Write acceptance scenarios as observable Given/When/Then behavior:

```text
- AC-001 | REQ-001 | Given an idle route, when loading remains pending for 150 ms, then the progress indicator is visible and the content bounding box is unchanged.
```

Record evidence, assumptions, decisions, questions, and tests as `EVD-*`, `ASM-*`, `DEC-*`, `Q-*`, and `TEST-*`.

## Profile gates

### Light

Require context/evidence, problem, outcomes, non-goals, current/proposed behavior, requirements, acceptance criteria, security/privacy disposition, verification/traceability, decisions, and open questions.

Use for reversible local bugfixes and polish, including visual fixes, when there is no new trust boundary, persisted data shape, destructive behavior, public contract, or material interaction-semantic change. Cover relevant accessibility behavior without automatically raising every UI bug to standard. Prefer a concise micro-spec; omitted canonical sections are intentional under this profile.

### Standard

Require every light section plus users/scenarios, product/design, data/interfaces, failure/recovery, observability, rollout/rollback, and decisions.

Use for normal user-facing features, APIs, shared components, dependency changes, background work, or meaningful refactors.

### Critical

Require every canonical section. Also require:

- explicit trust boundaries and assets;
- abuse and misuse cases;
- authorization decision points;
- data classification and retention;
- migration rehearsal when schemas or state change;
- tested rollback or forward-recovery procedure;
- observability tied to failure modes;
- independent security and verification review.

Select critical automatically for authentication, authorization, secrets, money, sensitive data, destructive actions, migrations, untrusted code/file execution, or infrastructure with broad blast radius.

Record completed critical review under `Verification and Traceability` using a stable entry:

```text
- REVIEW-001 | security | passed | reviewer: reviewer identity | evidence: dated review artifact or URL
```

Valid scopes are `general`, `security`, `privacy`, `design`, and `verification`; states are `planned`, `passed`, `failed`, and `blocked`. The ready gate requires at least one `passed` review for a critical spec. Prose saying review is planned or required is not review evidence. Add separate records when the risk needs multiple domain reviewers.

## Readiness semantics

### Draft gate

Allow unresolved work, but require valid metadata and recognizable structure. Report placeholders, ambiguous language, and missing links.

### Ready gate

Require no placeholders, duplicate IDs, orphaned normative requirements, unexplained `N/A`, or blocking questions. Require every `must`/`must-not` requirement to map to at least one acceptance criterion and one planned verification.

For a critical profile, also require a structured `REVIEW-*` record with `passed` status, a reviewer identity, and evidence. The author cannot self-waive failed or blocked review.

### Verified gate

Require `status: verified`, no traceability row remaining `planned`, `blocked`, or `failed`, and evidence for every normative requirement.

## Traceability

Use the canonical table:

```markdown
| Requirement | Acceptance | Verification | Status |
| --- | --- | --- | --- |
| REQ-001 | AC-001 | TEST-001 | planned |
```

Each row maps exactly one `REQ-*`, one `AC-*`, and one `TEST-*`. Repeat the requirement or test across multiple rows when it covers multiple scenarios; do not use comma-separated IDs in a cell.

Valid trace statuses: `planned`, `passed`, `failed`, `blocked`, `not-applicable`.

`not-applicable` requires a `DEC-*` explanation and is invalid for a `must` or `must-not` requirement under the verified gate.

## Anti-patterns

- solution-first specs that never establish the problem;
- requirements phrased as implementation steps without user/system behavior;
- adjectives such as fast, secure, scalable, intuitive, robust, or seamless without a measurable boundary;
- happy-path-only acceptance criteria;
- `N/A` used to bypass reasoning;
- tests listed without the requirement they prove;
- status changed to verified before production or boundary evidence exists;
- architecture diagrams or prose added only to make the document look substantial.
