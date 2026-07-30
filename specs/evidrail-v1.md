---
spec: SPEC-EVIDRAIL-0001
title: "Evidrail v1"
status: verified
profile: standard
mode: deliver
owner: dimidotdev
created: 2026-07-29
updated: 2026-07-29
---

# Evidrail v1

## Context and Evidence

- EVD-001 | source: skill-creator guidance | A reusable skill needs concise instructions, progressive disclosure, deterministic validation, and forward testing.
- EVD-002 | source: current AI-assisted development workflow | Requests often mix intended outcomes, implementation guesses, and unstated constraints.
- EVD-003 | source: Python standard library | Argument parsing, Markdown scanning, JSON emission, and unit testing are available without third-party packages.
- EVD-004 | source: GitHub Actions run 30546819003 | The full unit suite, dogfood gate, and trace command passed on Ubuntu, Windows, and macOS with Python 3.11.
- ASM-001 | Python 3.11 or newer is available where the validator runs. | validation: exercise the CI matrix on supported operating systems.

## Problem

AI-assisted implementation can converge on valid code that solves the wrong problem when intent, evidence, risk, and verification are implicit. Prose-only guidance cannot reliably detect missing coverage or unsupported claims.

## Outcomes

- Provide a reusable Codex skill that leads work from grounded intent through verified delivery.
- Provide a deterministic command-line tool for initializing, checking, and tracing specifications.
- Scale the artifact and its gates across light, standard, and critical risk profiles.
- Publish the project under an open-source license with reproducible tests.

## Non-goals

- Replace product judgment, threat modeling, code review, or user approval.
- Generate implementation code from a specification.
- Require a hosted service, account, database, or network connection.
- Enforce a programming language, architecture, or project-management system.

## Users and Scenarios

- A developer converts an ambiguous feature request into behavior and acceptance criteria before editing code.
- A reviewer audits whether a proposed change accounts for design quality, misuse, failure, and rollback.
- A team checks specification structure and requirement coverage in continuous integration.
- An agent updates decisions and verification evidence as implementation reveals new facts.

## Current Behavior

The repository contains a drafted skill contract and reference material. Before v1, it has no published repository, automated release gate, portability matrix, or independent forward-test evidence.

## Proposed Behavior

The repository distributes the `spec-driven-development` skill and its dependency-free `evidrail.py` companion. The skill guides evidence-first reasoning; the command-line tool enforces the stable artifact grammar and exposes traceability gaps to people and automation.

## Requirements

- REQ-001 | must | When a user initializes a specification, Evidrail shall create the canonical Markdown artifact with the selected title, profile, mode, owner, identifier, and current date.
- REQ-002 | must-not | Evidrail shall not overwrite an existing specification unless the user supplies the explicit force option.
- REQ-003 | must | When the check command reads a specification, Evidrail shall validate metadata, profile-required sections, identifiers, requirement grammar, acceptance references, placeholders, questions, and trace rows.
- REQ-004 | must | When the ready gate runs, Evidrail shall reject blocking questions, unexplained non-applicable claims, placeholders, uncovered normative requirements, and an incompatible lifecycle status.
- REQ-005 | must | When the verified gate runs, Evidrail shall require verified lifecycle status and passed evidence for every must and must-not requirement.
- REQ-006 | must | When traceability is requested, Evidrail shall report each requirement with its acceptance criteria, verification identifiers, statuses, and missing coverage.
- REQ-007 | must | When automation requests structured results, the check command shall emit deterministic JSON or SARIF 2.1.0 without diagnostic prose on standard output.
- REQ-008 | must | The validator shall run with the Python 3.11 standard library on Linux, Windows, and macOS.
- REQ-009 | must | The skill shall define specify, deliver, and audit modes plus light, standard, and critical profiles.
- REQ-010 | must | The skill shall integrate product design, accessibility, security, privacy, reliability, rollout, rollback, and verification into requirements proportional to risk.
- REQ-011 | must | Critical work shall require explicit trust boundaries, abuse cases, authorization and data decisions, recovery evidence, and independent review.
- REQ-012 | must-not | The skill shall not present assumptions, skipped checks, or generated claims as observed evidence.

## Acceptance Criteria

- AC-001 | REQ-001 | Given an absent target path, when init runs with explicit metadata, then the created artifact contains that metadata and every canonical section.
- AC-002 | REQ-002 | Given an existing target path, when init runs without force, then the file remains unchanged and the command exits with an I/O error code.
- AC-003 | REQ-003 | Given a malformed requirement, duplicate definition, or unknown trace reference, when check runs, then it reports a stable finding code and source line.
- AC-004 | REQ-004 | Given a ready specification with a blocking question or uncovered must requirement, when the ready gate runs, then the command fails.
- AC-005 | REQ-005 | Given a verified specification with a planned verification row, when the verified gate runs, then the command fails until the row is passed.
- AC-006 | REQ-006 | Given requirements with complete and incomplete mappings, when trace runs, then its matrix identifies the missing acceptance or verification coverage.
- AC-007 | REQ-007 | Given the JSON or SARIF format option, when check runs, then the output parses as one document with stable paths, findings, and locations.
- AC-008 | REQ-008 | Given each supported CI operating system, when the unit suite and ready gate run, then both exit successfully without installing a runtime dependency.
- AC-009 | REQ-009 | Given a new task, when the skill is invoked, then it states one operating mode and one risk profile before delivery work.
- AC-010 | REQ-010 | Given a standard user-facing change, when the skill produces a ready specification, then applicable behavior includes design, accessibility, failure, security, privacy, observability, rollout, and recovery dispositions.
- AC-011 | REQ-011 | Given authentication, sensitive data, migration, destructive behavior, or untrusted execution, when risk is classified, then the profile is critical and its additional evidence is required.
- AC-012 | REQ-012 | Given an unverified belief or an unavailable check, when the skill records it, then it remains labeled as an assumption or verification gap rather than evidence.

## Product and Design

- Primary flow: invoke the skill, select mode and profile, initialize the artifact, fill it from evidence outward, pass the ready gate, deliver, record evidence, and pass the verified gate.
- Empty/loading/error/recovery: the local command has no loading state; empty or malformed artifacts produce line-addressable findings and preserve the input file.
- Keyboard and focus: command usage is terminal-native and does not require pointer interaction; Markdown remains editable with any accessible editor.
- Responsive and content extremes: text output remains line-oriented while JSON and SARIF provide machine-readable alternatives for large result sets.
- Motion: no motion or animation is introduced.
- Performance budget: local validation of a one-file specification shall complete within one second in the CI fixtures.

## Security and Privacy

- Assets and trust boundaries: repository content, specification text, tool output, fetched content, and generated code are untrusted data; only explicit user and repository authority can authorize effects.
- Authentication and authorization: v1 has no network service or identity layer and grants no additional authority to an agent.
- Untrusted input and output: the validator reads UTF-8 text, performs no evaluation or shell interpolation, and emits escaped JSON when structured output is selected.
- Data minimization and retention: the tool sends no telemetry, stores no personal data, and writes only the explicitly requested specification path.
- Abuse and operational controls: existing files require force to overwrite; parsing has no extension execution, dependency hooks, or network access.

## Data and Interfaces

The public interface is `python3 scripts/evidrail.py` with `init`, `check`, and `trace` subcommands. The persisted contract is one UTF-8 Markdown file with scalar frontmatter, canonical H2 sections, stable IDs, and a four-column trace table. Text, JSON, and SARIF are versioned output surfaces.

## Failure Modes and Recovery

- Missing or invalid arguments return usage code 2 without changing files.
- Unreadable, non-UTF-8, or unsafe overwrite targets return I/O code 3.
- Specification findings or trace gaps return code 1 and preserve the artifact.
- A validator regression is recovered by reverting the release or using the last tagged script; specifications remain plain Markdown.

## Observability

- Every finding includes severity, stable code, path, one-based line, one-based column, and message.
- Command exit codes distinguish success, content findings, usage errors, and I/O failures.
- CI records the unit suite, dogfood ready gate, and operating-system matrix result.
- Forward-test notes record where independent agents followed, misunderstood, or bypassed the skill.

## Rollout and Rollback

- Rollout: validate the dogfood artifact, run isolated forward tests, publish an initial tagged repository, then use the skill on a bounded change before broader adoption.
- Stop conditions: stop rollout on false passes, destructive init behavior, invalid structured output, a platform test failure, or a critical workflow that proceeds without its required evidence.
- Rollback or forward recovery: revert to the preceding tag or disable the skill; all artifacts remain readable Markdown and require no data migration.

## Verification and Traceability

| Requirement | Acceptance | Verification | Status |
| --- | --- | --- | --- |
| REQ-001 | AC-001 | TEST-001 | passed |
| REQ-002 | AC-002 | TEST-002 | passed |
| REQ-003 | AC-003 | TEST-003 | passed |
| REQ-004 | AC-004 | TEST-004 | passed |
| REQ-005 | AC-005 | TEST-005 | passed |
| REQ-006 | AC-006 | TEST-006 | passed |
| REQ-007 | AC-007 | TEST-007 | passed |
| REQ-008 | AC-008 | TEST-008 | passed |
| REQ-009 | AC-009 | TEST-009 | passed |
| REQ-010 | AC-010 | TEST-010 | passed |
| REQ-011 | AC-011 | TEST-011 | passed |
| REQ-012 | AC-012 | TEST-012 | passed |

- TEST-001 | `test_init_creates_template_and_refuses_implicit_overwrite` and `test_light_init_uses_micro_spec_and_normalizes_prefixed_filename` passed locally and in CI.
- TEST-002 | The overwrite test preserved original bytes and returned I/O code 3; invalid identity also left no target file.
- TEST-003 | The invalid fixture produced stable metadata, structure, duplicate-ID, reference, placeholder, question, and trace finding codes.
- TEST-004 | Ready-gate tests rejected blocking content and accepted both the standard dogfood spec and compact light fixture.
- TEST-005 | `test_verified_gate_requires_passed_evidence` failed planned rows and passed only after every normative row was recorded as passed.
- TEST-006 | Trace tests reported complete mappings and failed a deliberately removed normative row plus structural defects.
- TEST-007 | JSON parsed as one stable document and repeated SARIF output was byte-identical with source locations.
- TEST-008 | GitHub Actions run 30546819003 passed the unit suite, dogfood gate, and trace command on Ubuntu, Windows, and macOS using Python 3.11.
- TEST-009 | Independent light and critical forward tests selected and stated `specify/light` and `specify/critical`; the audit test selected `audit/light`.
- TEST-010 | Forward-test artifacts converted visual continuity, accessibility, authorization, privacy, failure, observability, rollout, and recovery concerns into requirements proportional to risk.
- TEST-011 | Critical forward testing exposed the prose-review loophole; the revised gate rejected it, and `test_structured_passed_review_satisfies_critical_readiness` passed only with a structured record.
- TEST-012 | The independent audit labeled assumptions and explicitly declined to claim implementation defects without implementation evidence; skipped checks remain non-passing states in the validator.

## Decisions

- DEC-001 | Distribute one self-contained Python script beside the skill. | rationale: preserve portability, auditability, and offline use without a package installation step. | affects: REQ-001, REQ-003, REQ-008
- DEC-002 | Use one canonical Markdown artifact for v1 instead of a multi-file graph. | rationale: keep adoption cost proportional while retaining stable trace IDs. | affects: REQ-003, REQ-006
- DEC-003 | Treat warnings as failures for ready and verified critical specifications. | rationale: critical risk requires explicit disposition rather than silent acceptance. | affects: REQ-004, REQ-011
- DEC-004 | Keep judgment in the skill and structural invariants in the validator. | rationale: deterministic rules cannot decide product value or credible threats, while prose cannot guarantee referential coverage. | affects: REQ-003, REQ-010

## Open Questions

- None — the v1 interface, artifact contract, risk posture, and release gate are resolved.
